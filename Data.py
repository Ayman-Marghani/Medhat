# import python libraries
import json
import spacy
import random
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.stem.snowball import SnowballStemmer
from spellchecker import SpellChecker
from difflib import SequenceMatcher
import math
from SQLConnection import *


spell = SpellChecker()
stemmer = SnowballStemmer("english")
wnl = WordNetLemmatizer()
# Load the English language model
nlp = spacy.load("en_core_web_md")
######################################################################################################################################################
################################# TABLES ##################################
# list of pairs (word, intent)
with open('intents.json', 'r') as f:
    intents = json.load(f)
# list of symbols that to ignore when doing tokenization
ignore_punctuation = ['?', '.', '!', ',', ';', ':', '-', '(', ')', '[', ']', '{', '}', '<', '>', '/', '\\'
    , '|', '`', '~', '@', '#', '$', '%', '^', '&', '*', '_', '+', '=', '"', "'"]
# list of pairs (contraction, expanded form)
contractions = [("'m", "am"), ("'s", "is"), ("n't", "not"), ("'ve", "have"), ("can't","cannot")]
affirmations = ["yes", "yeah", "yep", "yup", "sure", "probably", "I think so", 'y']
negations = ["no", "nope", "nah", "not really", "not sure", "negative", "never", "don't", "not", "refuse", "decline",
             "reject", "n"]
pronouns = ['i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them',
            'my', 'a', 'an', 'the', 'your', 'his', 'her', 'its', 'our', 'their', 'mine', 'yours', 'his', 'hers',
            'ours', 'theirs', 'myself', 'yourself', 'himself', 'herself', 'itself', 'ourselves',
            'yourselves', 'themselves']

prepositions = ['at', 'but', 'by', 'for', 'from', 'in', 'of', 'off', 'on', 'out', 'to', 'a', 'an' , 'with','during' , 'around' , 'when' , 'after', 'before' , 'outside' , 'inside' , 'over']
######################################################################################################################################################
# Data from the Database
DiseasesDB = QueryDB("SELECT disease_id FROM diseases")
Disease_Scores = {disease[0]: 100 for disease in DiseasesDB}
del DiseasesDB
user_symptoms = set([])

