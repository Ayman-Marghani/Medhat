import json
import nltk
import numpy as np
import random
from nltk.tokenize import word_tokenize
from collections import Counter
from nltk.stem.porter import PorterStemmer
stemmer = PorterStemmer()

#NLTK UTILTIES

def contraction_transformer(split_sentence):
    transformed_split_sentence = []
    for word in split_sentence:
        if word == "won't":
            transformed_split_sentence.append("will")
            transformed_split_sentence.append("not")
        else :
            isPresent = False
            for (cntrc, eng) in contractions:
                if cntrc in word:
                    isPresent = True
                    transformed_split_sentence.append(word.replace(cntrc , ""))
                    transformed_split_sentence.append(eng)
                    break
            if not isPresent:
               transformed_split_sentence.append(word)
            
    return transformed_split_sentence
def tokenize(sentence):
    return contraction_transformer(sentence.split())
def stem(word):
    return stemmer.stem(word.lower())
def format(sentence):
    tokenized = tokenize(sentence)
    stemmed = [stem(w.lower()) for w in tokenized]
    return stemmed

#FUNCTIONS

def detectSymptom(tokenized_sentence): #Throw away function later
    for word in tokenized_sentence:
        if word in symptom_words: #Symptom keyword detected
            tag = priority_bag_of_words(tokenized_sentence)
            if (tag == "symtpom" and "not" in tokenized_sentence): #Doesn't have symptom
                for k, lst in Associated_Symptoms.items():
                    if symptom_words[word] in lst:
                        Diseases[k] -= 10   
                return tag
            elif (tag == "symtpom") :    #Has symptom
                user_symptoms.append(symptom_words[word])
                for k, lst in Associated_Symptoms.items():
                    if symptom_words[word] in lst:
                        Diseases[k] += 10
                return tag
            elif (tag == "description"):    #Asking for description of symptom
                return tag #get description from table
            else:
                return "none"
def detectSymptoms(tokenized_sentence): #returns the detected symptom
    detected = []
    for word in tokenized_sentence:
        if word in symptom_words: #Symptom keywords detected
            detected.append(word)
    return detected

def our_bag_of_words(tokenized_sentence, all_words):
    intent_count = dict.fromkeys(tags, 0)
    stemmed_words = [stem(word) for word in tokenized_sentence]
    for sw in stemmed_words:
        for (word,tag) in all_words:
            if sw == word:
                intent_count[tag] += 1
    return intent_count

def priority_bag_of_words(tokenized_sentence):
    intent_count = dict.fromkeys(["symptom" , "description"], 0)
    stemmed_words = [stem(word) for word in tokenized_sentence]
    for sw in stemmed_words:
        for (word,tag) in all_words:
            if sw == word:
                intent_count[tag] += 1
    if (intent_count["symptom"] >= intent_count["description"]) :
        return "symptom" 
    else : return "description"

def recognize_intent(sentence):
    tokenized_sentence = tokenize(sentence)
    detected_symptoms = detectSymptoms(tokenized_sentence)
    intent_count = our_bag_of_words(tokenized_sentence, all_words) 
    #Check first if "priority" intents have appeared or not, with a detected symptom
    symptom_count = intent_count["symptom"] , description_count = intent_count["description"]
    if ((symptom_count > 1 or description_count > 1) and len(detected_symptoms) > 0):
        if(symptom_count >= description_count):
            if ("not" in tokenized_sentence): #Doesn't have symptom
                for k, lst in Associated_Symptoms.items():
                    for symptom in detected_symptoms:
                        if symptom_words[symptom] in lst:
                            Diseases[k] -= 10   
            else :                            #Has symptom
                for k, lst in Associated_Symptoms.items():
                    for symptom in detected_symptoms:
                        user_symptoms.append(symptom_words[symptom])
                        if symptom_words[symptom] in lst:
                            Diseases[k] -= 10   
            return ["symptom"]
        else :
            return ["description"] #Problem, need to return detected_symptoms like this, or recalculate them , probably the latter.
            for symptom in detected_symptoms:
                print("Description of [" + symptom + "] : \n")
    else:
        sorted_intent_list = [x[0] for x in sorted(intent_count.items(), key=lambda item: item[1], reverse=True)] #All intents , sorted by word appearance
        sorted_counts = [x[1] for x in sorted(intent_count.items(), key=lambda item: item[1], reverse=True)]
        if sorted_counts[0] < 3: #If the symptom doesn't make sense
            return []
        else: return sorted_intent_list

def generate_response(user_input):
    intents_list = recognize_intent(user_input)
    if len(intents_list) == 0:
        print("Sorry, I did not understand that.")
    else : pass #Options for description, symptom or otherwise.
    for intent in intents['intents']:
        if intents_list[0] == intent['tag']:
            sz = len(intent['responses'])
            rnd = random.randint(0,sz-1)
            print(intent['responses'][rnd])
            pass

#INTENTS JSON DEFINITION

with open('intents.json' , 'r') as f:
    intents = json.load(f)

all_words = [] # (word , tag)
tags = []
pattern_tag_list = []
# loop through each sentence in our intents patterns
for intent in intents['intents']:
    tag = intent['tag']
    # add to tag list
    tags.append(tag)
    for pattern in intent['patterns']:
        # tokenize each word in the sentence
        tokenized_pattern = tokenize(pattern)
        tokenized_pair = [(word, tag) for word in tokenized_pattern ]
        # add to our words list
        all_words.extend(tokenized_pair)
        # add to xy pair
        pattern_tag_list.append((tokenized_pattern, tag))
        
all_words = [(stem(p[0]) , p[1]) for p in all_words if p[0] not in ignore_words]
# remove duplicates and sort
all_words = sorted(set(all_words))
tags = sorted(set(tags))



#TABLES

ignore_words = ['?', '.', '!', ',', ';', ':', '-', '(', ')', '[', ']', '{', '}', '<', '>', '/', '\\'
                , '|', '`', '~', '@', '#', '$', '%', '^', '&', '*', '_', '+', '=', '"', "'"]
contractions = [("'m" , "am") , ("'s" , "is") , ("n't" , "not")]
valid_symptoms = {
    'sore throat': 'sore_throat',
    'cough': 'cough',
    'runny nose': 'runny_nose',
    'fever': 'fever',
    'headache': 'headache',
    'diarrhea': 'diarrhea',
    'stomach ache': 'stomach_ache'
}
Diseases = {"common cold": 100, "flu": 100, "food poisoning": 100}
Associated_Symptoms = {
    "common cold": ['sore throat', 'cough', 'runny nose'],
    "flu": ['cough', 'fever', 'headache'],
    "food poisoning": ['diarrhea', 'stomach ache', 'headache']
}
symptom_words = ['sore_throat', 'cough', 'runny_nose', 'fever', 'headache', 'diarrhea', 'stomach_ache']
user_symptoms = []
#Use only relevant keywords for intents, and have priorities for them.
#Add all symptoms to all_words with diagnosis tag
#Issue: symptoms of multiple words