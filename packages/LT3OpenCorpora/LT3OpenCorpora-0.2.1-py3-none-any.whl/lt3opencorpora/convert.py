import re
import sys
import gzip
import os.path
from typing import List, Optional, Set, Union
import bz2
import codecs
import logging
import xml.etree.cElementTree as ET
from csv import DictReader

# To add stats collection in inobstrusive way (that can be simply disabled)
from blinker import signal

sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
doubleform_signal = signal('doubleform-found')


def open_any(filename: str):
    """
    Helper to open also compressed files
    """
    if filename.endswith(".gz"):
        return gzip.open

    if filename.endswith(".bz2"):
        return bz2.BZ2File

    return open


class TagSet:
    """
    Class that represents LanguageTool tagset
    Can export it to OpenCorpora XML
    Provides some shorthands to simplify checks/conversions
    """

    def __init__(self, fname: str) -> None:
        self.all = []
        self.full = {}
        self.groups = []
        self.lt2opencorpora = {}
        self.post = []

        with open(fname, 'r') as fp:
            r = DictReader(fp)

            for tag in r:
                # lemma form column represents set of tags that wordform should
                # have to be threatened as lemma.
                tag["lemma form"] = filter(None, map(str.strip, tag["lemma form"].split(",")))

                tag["divide by"] = filter(None, map(str.strip, tag["divide by"].split(",")))

                # opencopropra tags column maps LT tags to OpenCorpora tags
                # when possible
                tag["opencorpora tags"] = (
                        tag["opencorpora tags"] or tag["name"])

                # Helper mapping
                self.lt2opencorpora[tag["name"]] = tag["opencorpora tags"]

                # Parent column links tag to it's group tag.
                # For example parent tag for noun is POST tag
                # Parent for m (masculine) is gndr (gender group)
                if not hasattr(self, tag["parent"]):
                    setattr(self, tag["parent"], [])

                attr = getattr(self, tag["parent"])
                attr.append(tag["name"])

                # aux is our auxiliary tag to connect our group tags
                if tag["parent"] != "aux":
                    self.all.append(tag["name"])

                # We are storing order of groups that appears here to later
                # sort tags by their groups during export
                if tag["parent"] not in self.groups:
                    self.groups.append(tag["parent"])

                self.full[tag["name"]] = tag

    def _get_group_no(self, tag_name: str) -> int:
        """
        Takes tag name and returns the number of the group to which tag belongs
        """

        if tag_name in self.full:
            return self.groups.index(self.full[tag_name]["parent"])
        else:
            return len(self.groups)

    def sort_tags(self, tags: List[str]) -> List[str]:
        return sorted(tags, key=lambda x: (self._get_group_no(x), x))

    def export_to_xml(self) -> ET.Element:
        grammemes = ET.Element("grammemes")
        for tag in self.full.values():
            grammeme = ET.SubElement(grammemes, "grammeme")
            if tag["parent"] != "aux":
                grammeme.attrib["parent"] = tag["parent"]
            name = ET.SubElement(grammeme, "name")
            name.text = tag["opencorpora tags"]

            alias = ET.SubElement(grammeme, "alias")
            alias.text = tag["name"]

            description = ET.SubElement(grammeme, "description")
            description.text = tag["description"]

        return grammemes


class WordForm:
    """
    Class that represents single word form.
    Initialized out of form and tags strings from LT dictionary.
    """

    def __init__(self, form: str, tags: str, tag_set: TagSet, is_lemma=False) -> None:
        if ":&pron" in tags:
            tags = re.sub(
                "([a-z][^:]+)(.*):&pron((:pers|:refl|:pos|:dem|:def|:int" +
                "|:rel|:neg|:ind|:gen)+)(.*)", "pron\\3\\2\\4", tags)
        self.form, self.tags = form, tags

        self.tags = list(map(str.strip, self.tags.split(":")))
        self.is_lemma = is_lemma

        # tags signature is string made out of sorted list of wordform tags
        # This is a workout for rare cases when some wordform has
        # noun:m:v_naz and another has noun:v_naz:m
        self.tags_signature = ":".join(sorted(self.tags))

        # Here we are trying to determine exact part of speech for this
        # wordform
        pos_tags = list(filter(lambda x: x in tag_set.post, self.tags))
        self.pos = ""

        # And report cases when it's missing or wordform has more than two
        # pos tags assigned
        if len(pos_tags) == 0:
            logging.debug(
                "word form %s has no POS tag assigned" % self.form)
        elif len(pos_tags) == 1:
            self.pos = pos_tags[0]

            if pos_tags[0] != self.tags[0]:
                logging.debug(
                    "word form %s has strange POS tag %s instead of %s"
                    % (self.form, pos_tags[0], self.tags[0]))
        else:
            logging.debug(
                "word form %s has more than one POS tag assigned: %s"
                % (self.form, pos_tags))

    def __str__(self) -> str:
        return "<%s: %s>" % (self.form, self.tags_signature)

    def __unicode__(self) -> str:
        return self.__str__()


class Lemma:
    def __init__(self, word: str, lemma_form_tags: str, tag_set: TagSet) -> None:
        self.word = word

        self.lemma_form = WordForm(word, lemma_form_tags, tag_set, True)
        self.pos = self.lemma_form.pos
        self.tag_set = tag_set
        self.forms = {}
        self.common_tags = None

        self.add_form(self.lemma_form)

    def __str__(self) -> str:
        return str(self.lemma_form)

    @property
    def lemma_signature(self):
        return (self.word,) + tuple(self.common_tags)

    def add_form(self, form: WordForm) -> None:
        if self.common_tags is not None:
            self.common_tags = self.common_tags.intersection(form.tags)
        else:
            self.common_tags = set(form.tags)

        if (form.tags_signature in self.forms and
                form.form != self.forms[form.tags_signature][0].form):
            doubleform_signal.send(self, tags_signature=form.tags_signature)

            self.forms[form.tags_signature].append(form)

            logging.debug(
                "lemma %s got %s forms with same tagset %s: %s" %
                (self, len(self.forms[form.tags_signature]),
                 form.tags_signature,
                 ", ".join(map(lambda x: x.form,
                               self.forms[form.tags_signature]))))
        else:
            self.forms[form.tags_signature] = [form]

    def _add_tags_to_element(self, el: ET.Element, tags: Union[List[str], Set[str]]) -> None:
        if self.pos in tags:
            ET.SubElement(el, "g", v=self.tag_set.lt2opencorpora[self.pos])
            tags = set(tags) - {self.pos}

        tags = self.tag_set.sort_tags(tags)

        for tag in tags:
            # For rare cases when tag in the dict is not from tagset
            if tag in self.tag_set.lt2opencorpora:
                ET.SubElement(el, "g", v=self.tag_set.lt2opencorpora[tag])

    def export_to_xml(self, i: int, rev=1) -> Optional[ET.Element]:
        lemma = ET.Element("lemma", id=str(i), rev=str(rev))
        common_tags = list(self.common_tags or set())

        if not common_tags:
            logging.debug(
                "Lemma %s has no tags at all" % self.lemma_form)

            return None

        l_form = ET.SubElement(lemma, "l", t=self.lemma_form.form.lower())
        self._add_tags_to_element(l_form, common_tags)

        for forms in self.forms.values():
            for form in forms:
                el = ET.Element("f", t=form.form.lower())
                if form.is_lemma:
                    lemma.insert(1, el)
                else:
                    lemma.append(el)

                self._add_tags_to_element(el,
                                          set(form.tags) - set(common_tags))

        return lemma


class Dictionary:
    def __init__(self, input_file: str, mapping: str) -> None:
        if not mapping:
            mapping = os.path.join(os.path.dirname(__file__), "mapping.csv")

        self.tag_set = TagSet(mapping)

        self.counter = 1
        self.lemmata = ET.Element("lemmata")

        with open_any(input_file)(input_file, "r") as fp:
            current_lemma = None

            for i, line in enumerate(fp):
                # Here we've found a new lemma, let's add old one to the list
                # and continue
                if not line.startswith("  "):
                    if self.counter % 100_000 == 0:
                        # we should write text to file to prevent RAM hit
                        self.write_tree()

                    self.add_lemma(current_lemma)

                    current_lemma = Lemma(
                        *line.strip().split(" ", 1),
                        tag_set=self.tag_set)
                else:
                    # It's a form of current lemma
                    current_lemma.add_form(WordForm(
                        *line.strip().split(" ", 1),
                        tag_set=self.tag_set
                    ))

            self.add_lemma(current_lemma)
        self.write_tree()

    def add_lemma(self, lemma: Lemma):
        if lemma is not None:
            lemma_xml = lemma.export_to_xml(self.counter)
            if lemma_xml is not None:
                self.counter += 1
                self.lemmata.append(lemma_xml)

    def write_tree(self):
        total_xml = ET.tostring(self.lemmata, encoding='unicode')
        # Remove to release memory
        self.lemmata.clear()
        # Need to remove <lemata> and </lemata>
        total_xml = total_xml[len('<lemata>') + 1:-len('</lemata>') - 1]
        with open('temp.xml', 'a') as f:
            f.write('\n{}'.format(total_xml))

    @staticmethod
    def export_to_xml(out_file: str):
        with open(out_file, 'w') as of:
            with open('template_start.xml') as tf:
                of.write(tf.read())
            with open('temp.xml') as rf:
                for result_line in rf:
                    of.write(result_line)
            of.write('\n</lemmata></dictionary>')
        os.remove('{}/temp.xml'.format(os.path.abspath(os.getcwd())))
