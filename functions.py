#imports
from xml.etree.ElementTree import *
import xml.etree.ElementTree as ET
from collections import Counter
import os
import pprint
import gensim
from gensim import corpora
from gensim import models
from gensim import similarities
from gensim.corpora import Dictionary
from gensim.models import LdaModel
from gensim.models import LdaMulticore
import nltk
from nltk.corpus import stopwords
from smart_open import open 
import spacy
import de_core_news_md


# load the language model from spacy
spacy_data = de_core_news_md.load()


# Function preprocess_text(text) transforms text to preprocessed tokens
def preprocess_text(text):
    # load and tokenize text with the spacy language model
    prep_text = spacy_data(text)
    # list for tokens
    prep_tokens = []
    # for every token in text
    for token in prep_text:
        # remove stopwords and punctuatiuon
        if token.pos_ != 'PUNCT' and token.is_stop == False:
            # lemmatize and transform to lowercase
            lemma_token = token.lemma_.lower()
            # remove non-alphabetic tokens
            if lemma_token.isalpha() or lemma_token == '-PRON-':
                prep_tokens.append(lemma_token)
    # return preprocessed text 
    return prep_tokens

# Get all texts from XML-File (not memory friendly)
def get_texts(xml_file):
    texts = []
    index = 0
    for event, elem in ET.iterparse(xml_file, events = ("start", "end")):        
        if index < 20:
            if event == 'end' and "text" in elem.tag:
                index += 1  
                texts.append(str(elem.text))
                elem.clear()
        else:
            break
    return texts

def get_titles(xml_file):
    title_ids = {}
    index = 0
    for event, elem in ET.iterparse(xml_file, events = ("start", "end")):        
        if index < 200:
            if event == 'end' and "title" in elem.tag:
                title_ids[index]=str(elem.text)
                index += 1    
                elem.clear()
        else:
            break
    return title_ids           
                
def build_dictionary(xml_file):
    index = 0
    first_elem = True
    # loop through all nodes
    for event, elem in ET.iterparse(xml_file, events = ("start", "end")):        
        if index < num_documents:
            # check if current node contains a document
            if event == "end" and "text" in elem.tag:
                # preprocess the text
                text = preprocess_text(elem.text)
                # if this is the first document found, create a new dictionary with it
                if first_elem:
                    dictionary = Dictionary([text])
                    first_elem = False
                    index += 1
                # all documents after the first one get appended to the dictionary
                else:
                    dictionary.add_documents([text])
                    index += 1
                # clear the node
                elem.clear()
        else:
            break
    return dictionary