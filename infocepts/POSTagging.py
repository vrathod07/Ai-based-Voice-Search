import spacy
from spacy.matcher import Matcher 
from spacy.tokens import Span 
from spacy import displacy 

nlp = spacy.load("en_core_web_sm")

import regex

def list_sentences(filename):
    f = open(filename, 'r')
    sentences = f.read()
    list_sent = []
    list_sent = sentences.split(".")
    return list_sent

def remove_numbering(text):
    # return regex.sub(r'^\d+\s+', '', text)
    return regex.sub(r'[0-9]+\.', '', text)

list_sent = list_sentences("data/queries.txt")
#enumerate in questions
for i, q in enumerate(list_sent):
    list_sent[i] = remove_numbering(list_sent[i])

sentences = []
for sent in  list_sent:
    sentences.append(sent)
    print(sent)

def print_parts(query):
  doc = nlp(query)

  print("Noun phrases:", [chunk.text for chunk in doc.noun_chunks])
  print("Verbs:", [token.lemma_ for token in doc if token.pos_ == "VERB"])

  for entity in doc.ents:
      print(entity.text, entity.label_)

for i,q in enumerate(sentences):
  print(f"Sentences{i} : {q}")
  print_parts(q)
  print("=========")
  print()