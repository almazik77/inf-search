import re
import pymorphy2
import nltk
from bs4 import BeautifulSoup
from os import listdir, path


class IndexEntry:
    def __init__(self):
        self.files = []
        self.count = 0

    def update(self, file_name, count):
        self.files.append(file_name)
        self.count += count


def compare_index_entry(x, y):
    return int(x.count) - int(y.count)


class BoolSearch:
    def __init__(self):
        self.words_index_mapping = None
        self.files_path = path.dirname(__file__) + '/pages'
        self.path_lemmas = path.dirname(__file__) + "/lemmas.txt"
        self.morph = pymorphy2.MorphAnalyzer()
        self.inverted_index_file_name = path.dirname(__file__) + "/index.txt"

    def get_normal_form(self, word):
        parsed_word = self.morph.parse(word)[0]
        if parsed_word.normalized.is_known:
            word_normal_form = parsed_word.normal_form
        else:
            word_normal_form = word.lower()
        return word_normal_form

    def populate_indexes_and_return(self, words_index_mapping):
        index = dict()
        for file_name in listdir(self.files_path):
            file = open(self.files_path + '/' + file_name, "r", encoding="utf-8")
            content = BeautifulSoup(file, features="html.parser").get_text()
            list_word = list(nltk.wordpunct_tokenize(content))
            words = set()
            for word in list_word:
                lemma = self.get_normal_form(word)
                if lemma in words_index_mapping.keys() and lemma not in words:
                    words.add(lemma)
                    word_special = words_index_mapping[lemma]
                    count = 0
                    for similar_word in word_special:
                        count += list_word.count(similar_word)
                    if lemma not in index.keys():
                        index[lemma] = IndexEntry()
                    index[lemma].update(re.search("\\d+", file_name)[0], count)

        for _, value in index.items():
            value.files.sort()
        return index

    def create_indexes_file(self):
        file = open(self.path_lemmas, "r")
        lines = file.readlines()
        words_index_mapping = dict()
        for line in lines:
            k = None
            words = re.split('\\s+', line)
            for i in range(len(words) - 1):
                if i == 0:
                    k = words[i]
                    words_index_mapping[k] = []
                words_index_mapping[k].append(words[i])
        index = self.populate_indexes_and_return(words_index_mapping)
        file = open(self.inverted_index_file_name, "w")
        for word, inf in index.items():
            file_field = word + " " + str(inf.count) + " "
            for file_name in inf.files:
                file_field += " " + str(file_name)
            file_field += "\n"
            file.write(file_field)
        file.close()

    def inverted_index_open(self):
        file = open(self.inverted_index_file_name, "r")
        lines = file.readlines()
        words_index_mapping = dict()
        for line in lines:
            words = re.split('\s+', line)
            k = words[0]
            if not k in words_index_mapping.keys():
                words_index_mapping[k] = set()
            for i in range(1, len(words) - 1):
                words_index_mapping[k].add(words[i])
        self.words_index_mapping = words_index_mapping

    def search(self, search_words):
        words = re.split('\s+', search_words)
        content_page = set()
        lemma_token = set(map(lambda x: self.get_normal_form(x), words))
        for word in lemma_token:
            if len(content_page) == 0:
                content_page = self.words_index_mapping[word]
            else:
                content_page = content_page.intersection(self.words_index_mapping[word])
        print(content_page)


if __name__ == '__main__':
    s = BoolSearch()
    s.create_indexes_file()
    s.inverted_index_open()
    s.search('программирование стать лучшим')
