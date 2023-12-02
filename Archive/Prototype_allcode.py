# Import python libraries
import json
import nltk
import numpy as np
import random
from nltk.tokenize import word_tokenize
from collections import Counter
from nltk.stem.porter import PorterStemmer
stemmer = PorterStemmer()

######################################################################################################################################################
################################# TABLES ##################################
# list of intents in the json file
intents = []
# list of pairs (word, intent)
all_words = []
tags = []
pattern_tag_list = []
# list of symbols that to ignore when doing tokenization
ignore_words = ['?', '.', '!', ',', ';', ':', '-', '(', ')', '[', ']', '{', '}', '<', '>', '/', '\\'
                , '|', '`', '~', '@', '#', '$', '%', '^', '&', '*', '_', '+', '=', '"', "'"]
# list of pairs (contraction, expanded form)
contractions = [("'m" , "am") , ("'s" , "is") , ("n't" , "not")]
# Data from the Database
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
######################################################################################################################################################
############################## NLTK UTILTIES ##############################
# Input: list of strings of the user's input sentence separated by space
# Output: list of all the strings in the sentence
def contraction_transformer(split_sentence):
    transformed_split_sentence = []
    # Loop on all words in split_sentence
    for word in split_sentence:
        # if the word is "won't" convert it to "will" and "not"
        if word == "won't":
            transformed_split_sentence.append("will")
            transformed_split_sentence.append("not")
        else:
            # this flag represents whether the word is contraction or not
            contraction_flag = False 
            # loop on all contractions
            for (contraction, expanded_word) in contractions:
                # if the word contains a contraction replace it with the expanded word (Ex: n't -> not)
                if contraction in word:
                    contraction_flag = True 
                    transformed_split_sentence.append(word.replace(contraction , ""))
                    transformed_split_sentence.append(expanded_word)
                    break
            # if the word is not a contraction then just add it to the result list
            if not contraction_flag: 
               transformed_split_sentence.append(word)
    return transformed_split_sentence
# Input: a string containing the user's input
# Output: list of all the words (strings) in the sentence (tokenized sentence)
def tokenize(sentence):
    return contraction_transformer(sentence.split())
# this function calls stem function on a string
def stem(word):
    return stemmer.stem(word.lower())
# Input: a string containing the user's input
# Output: list of all the words (strings) in the sentence after applying tokenization and stemming
# I think we shoud call it process input
def format(sentence):
    tokenized_sentence = tokenize(sentence)
    # stem all the words in tokenized_sentence
    stemmed_sentence = [stem(word) for word in tokenized_sentence]
    return stemmed_sentence

######################################################################################################################################################
############################## prerequiste function ##############################
#def prepare_data(tags, all_words): 
    #INTENTS JSON DEFINITION
    # Store all the intents (in intents.json) in intents variable
with open('intents.json' , 'r') as f:
    intents = json.load(f)
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

######################################################################################################################################################
################################ FUNCTIONS ################################
# Input: list of words (string) tokenized sentence 
# Output: list of Symptomps that exists in the sentence
# Input: list of words (string) tokenized sentence
# Output: list of Symptoms that exist in the sentence
def detectSymptoms(tokenized_sentence):
    detected_symptoms = []
    # Loop through all possible lengths of phrases (e.g., single word, two-word, three-word)
    for length in range(1, len(tokenized_sentence) + 1):
        for start in range(len(tokenized_sentence) - length + 1):
            phrase = " ".join(tokenized_sentence[start:start + length])
            if phrase in symptom_words:
                detected_symptoms.append(phrase)
    return detected_symptoms
# Input: list of words (string) tokenized sentence
# Output: dictionary of each intent with its calculated score (probability)
def our_bag_of_words(tokenized_sentence, all_words):
    # construct a dictionary of each intent with its calculated score (starts with 0)
    intent_count_dict = dict.fromkeys(tags, 0)
    # stem all the words in tokenized_sentence
    stemmed_sentence = [stem(word) for word in tokenized_sentence]
    # if the stemmed word exists in all_words increase the count of its corresponding intents by 1
    for stemmed_word in stemmed_sentence:
        for (word,intent) in all_words:
            if stemmed_word == word:
                intent_count_dict[intent] += 1
    return intent_count_dict
# Input: list of words (string) tokenized sentence
# Output: symptom if the sentence talks about a symptom, description if the sentence asks for a description of a specific symptom
def priority_bag_of_words(tokenized_sentence):
    # construct a dictionary (symptom, description) with their calculated score (starts with 0)
    intent_count_dict = dict.fromkeys(["symptom" , "description"], 0)
    # stem all the words in tokenized_sentence
    stemmed_sentence = [stem(word) for word in tokenized_sentence]
    # if the stemmed word exists in all_words increase the count of its corresponding intents by 1
    for stemmed_word in stemmed_sentence:
        for (word,intent) in all_words:
            if stemmed_word == word:
                intent_count_dict[intent] += 1
    if (intent_count_dict["symptom"] >= intent_count_dict["description"]) :
        return "symptom" 
    else: return "description"
# Input: a string containing the user's input
# Output: list of the most possible intents
def recognize_intent(sentence):
    tokenized_sentence = tokenize(sentence)
    detected_symptoms = detectSymptoms(tokenized_sentence)
    intent_count = our_bag_of_words(tokenized_sentence, all_words) 
    #Check first if "priority" intents have appeared or not, with a detected symptom
    symptom_count = intent_count["symptom"]
    description_count = intent_count["description"]
    if ((symptom_count > 0 or description_count > 0) and (len(detected_symptoms) > 0)):
        if(symptom_count >= description_count):
            if ("not" in tokenized_sentence): #Doesn't have symptom
                for k, lst in Associated_Symptoms.items():
                    for symptom in detected_symptoms:
                        if symptom in lst:
                            Diseases[k] -= 10   
            else :                            #Has symptom
                for symptom in detected_symptoms:
                    user_symptoms.append(symptom)
                    for k, lst in Associated_Symptoms.items():   
                        if symptom in lst:
                            Diseases[k] += 10   
            return ["symptom"]
        else :
            return ["description"] #Problem, need to return detected_symptoms like this, or recalculate them , probably the latter.
            for symptom in detected_symptoms:
                print("Description of [" + symptom + "] : \n")
    else:
        intent_count.pop("symptom")
        intent_count.pop("description")
        sorted_intent_list = [x[0] for x in sorted(intent_count.items(), key=lambda item: item[1], reverse=True)] #All intents , sorted by word appearance
        sorted_counts = [x[1] for x in sorted(intent_count.items(), key=lambda item: item[1], reverse=True)]
        if sorted_counts[0] < 1: #If the sentence doesn't make sense
            return []
        
        else: 
            return sorted_intent_list
def GiveDiagnosis():
    print("\n Medhat: Based on your given symptoms:- \n")
    symptoms = set(user_symptoms)
    symptoms = list(symptoms)
    sz = len(symptoms)
    for i in range(sz):
        print(symptoms[i])
        if(i < sz-1):
            print(" - ")
    print("\n Medhat:You could have the following diseases: \n")
    for disease,value in Diseases.items():
        if(value > 100):
            print(disease + "\n")
    #Recommendation, should change
    print("I recommend visiting a specialized doctor.")

def handleInterruption():
    print("\nMedhat: I'm still in the process of finishing your diagnosis, would you like to end your diagnosis? (y/n)")
    inp = input("\nUser: ")
    if(inp.lower() == "y"):
        #GiveDiagnosis()
        pass
    else : pass
# Input: list of responses
# output: random response
def get_random_response(responses_list):
    sz = len(responses_list)
    random_idx = random.randint(0,sz-1)
    return responses_list[random_idx]
# Input: user input
# Output: the appropriate response
def generate_response(intents_list): #Options for description, symptom, or otherwise.
    for intent in intents['intents']:
        if intents_list[0] == intent['tag']:
            print("\nMedhat: ", get_random_response(intent['responses']))
                
######################################################################################################################################################
########################## MAIN FUNCTION ##########################
def main():
    #prepare_data(tags, all_words)
    # the chatbot starts the conversation
    context = "start"
    print ("Medhat: Hi how are ya?")
    # Chatbot Main loop
    while True:
        user_input = input("\nUser: ")
        intents_list = recognize_intent(user_input)
        if(len(intents_list) == 0):
            print("\nMedhat: Sorry, I did not understand that.")
            continue
        if(intents_list[0] ==  "goodbye"):
            if(context != "symptom"):
                generate_response(["goodbye"])
                break
            else:
                GiveDiagnosis()
                continue
        if (context == "symptom"):
            if(intents_list[0] == "diagnosis"):
                GiveDiagnosis()
                continue
            else: 
                handleInterruption()
                continue
        context = intents_list[0]
        generate_response(intents_list)
### Call the main function
main()


'''
#Issue: Words detected in multiple intents, need to make them more distinct.
#Issue: symptoms of multiple words
#Dialogue flow for symptom checking, after first symptom, chatbot should check for more symptoms, recognize interruptions [user not typing symptoms]
#Maybe recognize that there is a symptom the chatbot does not recognize, guide the user and ask them for more symptoms on his own etc..
#Detect when the "symptom checking" state is done to get out a diagnosis.
#Recognize mispellings
- Idea:
make a class for the chatbot and for the user to make the code more organized
'''