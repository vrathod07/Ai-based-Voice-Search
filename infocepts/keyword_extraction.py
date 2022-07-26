from typing import List, Tuple
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import nltk
import string
from nltk.corpus import stopwords
from matplotlib.axes import Axes
from textacy import extract, make_spacy_doc
import regex
import sys
import os

def decompose_keyterms(keyterm_list: List[str]) -> Tuple:
    terms = [el[0].replace(" ", "\n") for el in keyterm_list]
    scores = np.asarray([el[1] for el in keyterm_list])
    return terms, scores

# Open data from .txt file
with open("data/queries.txt", "r") as file:
    data = file.read().replace("\n", "")
article = data.replace(u"\xa0", u" ")

def preprocess(text):
  text = text.lower()
  text = nltk.word_tokenize(text)

  y = []
  for i in text:
    if i.isalnum():
      y.append(i)

  text = y[:]
  y.clear()

  for i in text:
    if i not in stopwords.words('english') and i not in string.punctuation:
      y.append(i)
  return " ".join(y)

# Create doc object
def create_doc(article):
    texts = article.split(',')
    article_1 = ""
    for text in texts:
        article_1 += preprocess(text)+","

    doc = make_spacy_doc(article_1, lang="en_core_web_sm")
    return doc

def textrank_algo(doc):
    textrank = extract.keyterms.textrank(doc, normalize="lemma")
    terms_textrank, scores_textrank = decompose_keyterms(textrank)

    return terms_textrank, scores_textrank

def yake_algo(doc):
    yake = extract.keyterms.yake(doc, normalize="lemma")
    terms_yake, scores_yake = decompose_keyterms(yake)

    return terms_yake, scores_yake

def scake_algo(doc):
    scake = extract.keyterms.scake(doc, normalize="lemma")
    terms_scake, scores_scake = decompose_keyterms(scake)

    return terms_scake, scores_scake

def sgrank_algo(doc):
    sgrank = extract.keyterms.sgrank(doc, normalize="lemma")
    terms_sgrank, scores_sgrank = decompose_keyterms(sgrank)

    return terms_sgrank, scores_sgrank


def main(article):
    text = preprocess(article)
    doc = create_doc(text)
    terms_sgrank, scores_sgrank = sgrank_algo(doc)
    print('\n')
    print(terms_sgrank)

main(article)