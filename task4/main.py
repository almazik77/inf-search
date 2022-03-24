import os
from collections import Counter
from math import log10

from nltk import WordNetLemmatizer

import nltk
from nltk.corpus import stopwords

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')


def get_tf_idf(tf, idf, word_in):
    idf_tf = []
    for tf_count in tf:
        idf_tf_dict = {}
        for word in word_in:
            idf_tf_dict[word] = tf_count[word] * idf[word]
        idf_tf.append(idf_tf_dict)
    return idf_tf


def get_idf(count, counter, word_in):
    counters = dict.fromkeys(word_in, 0)
    for p_counter in counter:
        for word in word_in:
            if p_counter[word] != 0:
                counters[word] += 1

    idf = {}
    for word in word_in:
        if counters[word] != 0:
            idf[word] = log10(count / counters[word])
        else:
            idf[word] = 0
    return idf


def get_tf(pages, counters, word_in):
    pages_tf = []
    for page, counter in zip(pages, counters):
        count = len(page)
        tf = {}
        for word in word_in:
            tf[word] = counter[word] / count
        pages_tf.append(tf)
    return pages_tf


def lemmatize(tokens):
    lemmatizer = WordNetLemmatizer()
    dict_lemma = {}
    for token in tokens:
        lemma = lemmatizer.lemmatize(token)
        lemma_dict_map = dict_lemma.get(lemma, [])
        lemma_dict_map.append(token)
        dict_lemma[lemma] = lemma_dict_map
    return dict_lemma


def tokenize(page):
    tokens = nltk.word_tokenize(page)
    low_tokens = [token.lower() for token in tokens if token.isalpha()]
    return [token for token in low_tokens if token not in stopwords.words('english')]


if __name__ == '__main__':
    lemmatizer = WordNetLemmatizer()

    pages = []
    counters = []
    for file in sorted(os.listdir(os.path.dirname(__file__) + '/pages'), key=len):
        with open(f'{os.path.dirname(__file__)}/pages/{file}', 'r', encoding='utf-8') as page:
            tokens = tokenize(page.read())
            pages.append(tokens)
            counters.append(Counter(tokens))

    tokens = set()
    with open(os.path.dirname(__file__) + "/tokens.txt", encoding="utf-8") as file:
        for line in file.readlines():
            tokens.add(line.strip())

    tf_pages_token = get_tf(pages, counters, tokens)
    idf_token = get_idf(len(pages), counters, tokens)
    tf_idf_token = get_tf_idf(tf_pages_token, idf_token, tokens)

    i = 0
    for page_tf, page_tf_idf in zip(tf_pages_token, tf_idf_token):
        i += 1
        with open(os.path.dirname(__file__) + '/tokens'f'/page_{i}.txt', 'w', encoding='utf-8') as file:
            for word in tokens:
                file.write(f'{word} {page_tf[word]} {idf_token[word]} {page_tf_idf[word]}\n')

    lemmas = set()
    with open(os.path.dirname(__file__) + '/lemmas.txt', encoding='utf-8') as lemmas_file:
        for line in lemmas_file.readlines():
            values = line.strip().split(' ')
            lemmas.add(values[0].replace(':', ''))

    counters_lemmas = []
    for page_token in pages:
        lemma_page = list(map(lambda token: lemmatizer.lemmatize(token), page_token))
        counters_lemmas.append(Counter(lemma_page))

    tf_lemma = get_tf(pages, counters_lemmas, lemmas)
    idf_lemma = get_idf(len(pages), counters_lemmas, lemmas)
    tf_idf_lemma = get_tf_idf(tf_lemma, idf_lemma, lemmas)

    i = 0
    for page_tf, page_tf_idf in zip(tf_lemma, tf_idf_lemma):
        i += 1
        with open(os.path.dirname(__file__) + '/lemmas'f'/page_{i}.txt', 'w', encoding='utf-8') as file:
            for word in lemmas:
                file.write(f'{word} {page_tf[word]} {idf_lemma[word]} {page_tf_idf[word]}\n')
