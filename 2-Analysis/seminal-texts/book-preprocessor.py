import sys
import os
import pypdf
import textract
import string
import collections
import numpy as np
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
# import nltk
# import ssl
# try:
#     _create_unverified_https_context = ssl._create_unverified_context
# except AttributeError:
#     pass
# else:
#     ssl._create_default_https_context = _create_unverified_https_context
# nltk.download()
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer, PorterStemmer
import pandas as pd
from tqdm import tqdm
from sklearn.feature_extraction.text import CountVectorizer

################################################################################
"""                        TODO MOVE TO DIF FILE                             """
################################################################################

def stemming(words_vec):
    stemmer = PorterStemmer()
    return [stemmer.stem(word) for word in words_vec]

def lemmatize(words_vec):
    lemmatizer = WordNetLemmatizer()
    return [lemmatizer.lemmatize(word) for word in words_vec]

def baggify(words_vec):
    lemmas_vec = lemmatize(words_vec)
    lemmas_vec = stemming(lemmas_vec)
    dirty_dict = {}
    for l in lemmas_vec:
        if l in dirty_dict:
            dirty_dict[l] += 1
        else:
            dirty_dict[l] = 1
    sorted_bag = sorted(dirty_dict.items(), key=lambda x:x[1])
    print(sorted_bag)
    # TODO: FIgure this df BoW method
    # print(dirty_dict)
    # df = pd.DataFrame([lemmas_vec])
    # df.columns = ['script']
    # df.index = ['Itula']
    # df
    # corpus = df.Itula
    # vect = CountVectorizer(stop_words='english')
    # baggy = vect.fit_transform(corpus)

################################################################################
"""                             ACTUAL SCRAPING                              """
################################################################################

def clean_txt(text):
    # Declare filter for punctuation
    punctuation_chars = string.punctuation + '…' + '—'
    filter_punctuation = str.maketrans('','',punctuation_chars)
    # list of stop words to remove
    stop_words = set(stopwords.words('english'))
    # TODO: filter out all alphanum?

    # split words by whitespace
    processed = ''
    tokens = text.split()
    # save one str of whole book in lower-case
    for i in range(len(tokens)):
        processed += tokens[i].lower() + ' '

    # Tokenize by sentence
    sentence_tokens = sent_tokenize(processed)
    # remove punctuation from sentences
    for i in range(len(sentence_tokens)):
        sentence_tokens[i] = sentence_tokens[i].translate(filter_punctuation)

    # Tokenize by word
    word_tokens = processed.split()
    word_tokens = [t.translate(filter_punctuation) for t in word_tokens] # remove punct
    word_tokens = [t for t in word_tokens if t not in stop_words] # remove stop words
    return sentence_tokens, word_tokens

def pdf_to_clean(file):
    # open pdf and convert to pypdf object
    pdf = open(file, 'rb')
    pdfObj = pypdf.PdfReader(pdf)
    # loop through pages, try pypdf method
    txt = ''
    for i in tqdm(range(len(pdfObj.pages))):
        txt += pdfObj.pages[i].extract_text() + ' '
    # if pyPDF txt extract worked
    if txt != '':
        # clean data, receive sentence and word vec
        sentences, words = clean_txt(txt)
        # preprocess word vector via BoW
        bag_of_words = baggify(words)
    # else extract text data via OCR
    else:
        print("HEYA BUNCHA, TODO: USE TESSERACT OCR")
        # textract.process(file, method='tesseract', encoding='utf-8', language='eng')

def chapter_to_str(chapter):
    soup = BeautifulSoup(chapter.get_body_content(), 'html.parser')
    text = [para.get_text() for para in soup.find_all('p')]
    return ' '.join(text)

def epub_to_clean(file):
    # open epub
    book = epub.read_epub(file)
    items = list(book.get_items_of_type(ebooklib.ITEM_DOCUMENT))
    # list chapters with content
    chapters = []
    for item in items:
        if 'chapter' in item.get_name().lower():
            chapters.append(item)
    # create dict of chapter_name : str(content)
    text_to_chap = {}
    for c in chapters:
        text_to_chap[c.get_name().lower()] = chapter_to_str(c)
    # save book body as one big string
    megalostring = ''
    for c in text_to_chap:
        megalostring += text_to_chap[c] + ' '
    sentences, words = clean_txt(megalostring)
    baggify(words)

def main(path):
    file_dir = os.path.dirname(os.path.realpath('__file__'))
    file = os.path.join(file_dir, path)
    file = os.path.abspath(os.path.realpath(file))
    if file[len(file)-3:len(file)] == 'pdf':
        pdf_to_clean(file)
    if file[len(file)-4:len(file)] == 'epub':
        epub_to_clean(file)

if __name__ == "__main__":
    args = sys.argv[1:]
    main(args[0])