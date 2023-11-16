import spacy
from functions.utils import*


danish_nlp = spacy.load("da_core_news_sm")
english_ner = spacy.load("en_core_web_sm")

text = "De sjællandske bilpendlere er vågnet op til en morgen med masser af vand på vejene, og flere viadukter er spærret på grund af store vandmasser, der har samlet sig."

text = translateWord(text)

#doc = danish_nlp(text)

doc = english_ner(text)

#spacy_labels = nlp.get_pipe("ner").labels
#for label in spacy_labels:
#    print(label)

for ent in doc.ents:
    print(ent.text, ent.label)
