# coding:utf8
import codecs
import json
from spoken_macedonian_annotation.homonyms import homonyms
from nltk.tokenize import word_tokenize
from spoken_macedonian_annotation.file_processing import read_file, create_out_file
from pkg_resources import resource_filename

DEFAULT_DATA_FILE = resource_filename('spoken_macedonian_annotation', 'all_data.json')



class MacAnnotator:
    """ """

    def __init__(self, mark_homonyms=False, mark_unknown_tokens=False, print_to_txt_file=False):
        self.mark_homonyms = mark_homonyms
        self.mark_unknown_tokens = mark_unknown_tokens
        self.print_to_txt_file = print_to_txt_file

    def _full_annotation(self, text):
        """

        Parameters
        ----------
        text : A string to be tokenized and annotated.


        """
        tokens = word_tokenize(text)
        f = codecs.open(DEFAULT_DATA_FILE, 'r', encoding='utf-8')
        full_dict = json.loads(f.read())
        f.close()
        result_list = []
        for token in tokens:
            token = token.lower()
            if token in homonyms:
                if self.mark_homonyms:
                    lemma = "HOMONYM"
                    pos = "HOMONYM"
                    annot = "HOMONYM"
                else:
                    lemma = ""
                    pos = ""
                    annot = ""
            elif token in full_dict.keys():
                pos = full_dict[token][0]
                lemma = full_dict[token][1]
                annot = full_dict[token][2]
            else:
                if self.mark_unknown_tokens:
                    lemma = "UNKNOWN"
                    pos = "UNKNOWN"
                    annot = "UNKNOWN"
                else:
                    lemma = ""
                    pos = ""
                    annot = ""
            result_list.append([token, pos, lemma, annot])
        return result_list

    def annotate(self, input_item, outfile='annotation_output.txt'):
        """

        Parameters
        ----------
        input_item : str :  a plain text to be tokenized and annotated.

        outfile :  Outputfile name.
            (Default value = 'annotation_output.txt')


        """

        text_list = self._full_annotation(input_item)
        result = ""
        for token in text_list:
            s = "\t".join(token)
            result += s
            result += '\n'
        if self.print_to_txt_file:
            out = create_out_file(outfile)
            out.write(result)
            out.close()
        print(result)
        return result


#g = MacAnnotator(print_to_txt_file=True)

#result = g.annotate("Тој е дојден вчера. Беше многу многу многу уморен.")

#print(result)
