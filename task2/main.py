import re
import string
import nltk
import pymorphy2
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from os import listdir, path

nltk.download('stopwords')


class Tokenizer:
    def __init__(self):
        self.files_path = path.dirname(__file__) + '/pages'
        self.stop_words = stopwords.words('russian')
        self.morph = pymorphy2.MorphAnalyzer()
        self.tokens = set()
        self.lem_dict = dict()
        self.russian_letters = re.compile(r'^[а-яА-Я]{2,}$')
        self.numbers = re.compile(r'^[0-9]+$')

    def make_tokens(self):
        for file_name in listdir(self.files_path):
            file = open(self.files_path + '/' + file_name, "r", encoding="utf-8")
            self.make_tokens_from_file(file)
        tokens = open(path.dirname(__file__) + "/tokens.txt", 'w')
        for word in self.tokens:
            tokens.write("%s\n" % word)
        tokens.close()

    def make_tokens_from_file(self, text):
        content = BeautifulSoup(text, features="html.parser").get_text()
        tokens = list(nltk.wordpunct_tokenize(content))
        tokens = [i for i in tokens if all(not j in string.punctuation for j in i)]
        tokens = set(filter(self.is_correct_token, tokens))
        self.tokens = self.tokens | tokens

    def is_correct_token(self, word):
        result = not bool(self.numbers.match(word)) \
                 and bool(self.russian_letters.match(word)) \
                 and not bool(word.lower() in self.stop_words)
        return result

    def make_lemmas(self):
        self.populate_lemmas_dict()
        lemmas_file = open(path.dirname(__file__) + "/lemmas.txt", 'w')
        for lemma, tokens in self.lem_dict.items():
            words = lemma + " "
            for token in tokens:
                words += token + " "
            words += "\n"
            lemmas_file.write(words)
        lemmas_file.close()

    def populate_lemmas_dict(self):
        for word in self.tokens:
            word_normal_form = self.get_normal_form(word)
            if word_normal_form not in self.lem_dict:
                self.lem_dict[word_normal_form] = []
            self.lem_dict[word_normal_form].append(word)

    def get_normal_form(self, word):
        parsed_word = self.morph.parse(word)[0]
        if parsed_word.normalized.is_known:
            word_normal_form = parsed_word.normal_form
        else:
            word_normal_form = word.lower()
        return word_normal_form


if __name__ == '__main__':
    t = Tokenizer()
    t.make_tokens()
    t.make_lemmas()
