# Import python libraries
import json
import nltk
import numpy as np
import random
import spacy
from SQLConnection import *
from nltk.tokenize import word_tokenize
from collections import Counter
from nltk.stem.porter import PorterStemmer
stemmer = PorterStemmer()
# Load the English language model
nlp = spacy.load("en_core_web_md")
######################################################################################################################################################
################################# TABLES ##################################
# list of pairs (word, intent)
with open('intents.json' , 'r') as f:
    intents = json.load(f)
# list of symbols that to ignore when doing tokenization
ignore_punctuation = ['?', '.', '!', ',', ';', ':', '-', '(', ')', '[', ']', '{', '}', '<', '>', '/', '\\'
                , '|', '`', '~', '@', '#', '$', '%', '^', '&', '*', '_', '+', '=', '"', "'"]
# list of pairs (contraction, expanded form)
contractions = [("'m" , "am") , ("'s" , "is") , ("n't" , "not")]
affirmations = ["yes", "yeah", "yep", "yup", "sure", "probably", "I think so", 'y']
negations = ["no", "nope", "nah", "not really", "not sure", "negative", "never", "don't", "not", "refuse", "decline", "reject" , "n"]
pronouns = ['i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them',
                'my', 'a', 'an', 'the', 'your', 'his', 'her', 'its', 'our', 'their', 'mine', 'yours', 'his', 'hers',
                'ours', 'theirs', 'myself', 'yourself', 'himself', 'herself', 'itself', 'ourselves',
                'yourselves', 'themselves']

prepositions = ['at', 'but', 'by', 'for', 'from', 'in', 'of', 'off', 'on', 'out', 'to']
######################################################################################################################################################
# Data from the Database
Disease_scores = {disease[0] : 0 for disease in DiseasesDB}
#symptom_words = ['sore_throat', 'cough', 'runny_nose', 'fever', 'headache', 'diarrhea', 'stomach_ache', "finger_very_ouch"]
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
def removeIgnored(sentence):
    new_sentence = ""
    for letter in sentence:
        if letter not in ignore_punctuation or letter == "'":
            new_sentence+=letter
        else : new_sentence += " "
    return new_sentence
# Input: a string containing the user's input
# Output: list of all the words (strings) in the sentence (tokenized sentence)
def tokenize(sentence):
    return sentence.lower().split()
# this function calls stem function on a string
def stem(word):
    return stemmer.stem(word.lower())
# Input: a string containing the user's input
# Output: list of all the words (strings) in the sentence after applying tokenization and stemming
# I think we shoud call it process input
def formatStem(sentence):
    formatted = contraction_transformer(tokenize(removeIgnored(sentence)))
    return [stem(word.replace("'" , "")) for word in formatted]
def format(sentence):
    formatted = contraction_transformer(tokenize(removeIgnored(sentence)))
    return [word.replace("'" , "") for word in formatted]
######################################################################################################################################################
######################################################################################################################################################
################################ FUNCTIONS ################################
def remove_substrings(input_list):
    new_list = input_list
    for symptom in input_list:
        for symptom2 in input_list:
            if(symptom != symptom2):
                if symptom in symptom2:
                    new_list.remove(symptom)
                    break
    return new_list
#Finds all listed symptoms in user input and updates the score for associated diseases
#Handles cases of multi-word symptoms [sore_throat] and if the sentence has "not" in it.
def detect_symptoms(tokenized_sentence):
    detected_symptoms = []
    stemmed_sentence = [stem(word) for word in tokenized_sentence]  
    SymptomsDB = CallDB(connection,"symptom","*")
    for tuple in SymptomsDB:
        symptom = tuple[1] 
        filtered_symptom = '_'.join([word for word in symptom.split('_') if word.lower() not in prepositions])
        stemmed_symptom = '_'.join([stem(word) for word in filtered_symptom.split('_')])
        if all(word in stemmed_sentence for word in stemmed_symptom.split('_')):
            if "not" in stemmed_sentence:
                for disease, symptoms in Associated_Symptoms.items():
                    if symptom in symptoms:
                        Disease_scores[disease] -= 10
            else:
                detected_symptoms.append(symptom)
                user_symptoms.append(symptom)
                for disease, symptoms in Associated_Symptoms.items():
                    if stemmed_symptom in symptoms:
                        Disease_scores[disease] += 10
    #detected_symptoms = remove_substrings(detected_symptoms)
    #user_symptoms = remove_substrings(user_symptoms)
    print(user_symptoms)
    return detected_symptoms


#Using spacy, computes similarity between 2 sentences
def compute_similarity(pattern, user_input):
    pattern_doc = nlp(pattern)
    user_input_doc = nlp(user_input)
    similarity = pattern_doc.similarity(user_input_doc)
    return similarity
#Removes less "significant" words to similarity computation, to better the matching
def remove_pronouns_prepositions(word_list):
    filtered_list = [word for word in word_list if word.lower() not in (pronouns + prepositions)]
    return filtered_list
#Checks that 2 sentences have a common word , also to better the matching.
def has_common_word(sentence1, sentence2):
    # Split the sentences into words
    words1 = format(sentence1)
    words2 = format(sentence2)

    # Convert the words to sets for efficient comparison
    set1 = set(words1)
    set2 = set(words2)

    # Check for common words
    common_words = set1.intersection(set2)
    common_words = set(remove_pronouns_prepositions(list(common_words)))
    # Return True if there's at least one common word, False otherwise
    return bool(common_words)
#Takes the user input and recognizes its input by getting the intent with the pattern having the highest similarity matching.
def recognize_intent(user_input):
    #Implement spell checking in has common word
    max_similarity = 0
    recognized_intent = None
    user_input = ' '.join(format(user_input))  # Convert user input to lowercase

    for intent in intents['intents']:
        for pattern in intent['patterns']:
            formatted_pattern = ' '.join(format(pattern))  # Convert pattern to lowercase
            #Check that at least one word matches in the pattern
            if(not has_common_word(user_input,formatted_pattern)):
                continue
            similarity = compute_similarity(formatted_pattern, user_input)
            if similarity > max_similarity:
                max_similarity = similarity
                recognized_intent = intent['tag']
                print(f"S: {similarity} , Intent: {recognized_intent} , Pattern: {formatted_pattern} \n")
    return recognized_intent if max_similarity > 0.35 else None
#Based on the diseases scores and user symptoms, gives the user a diagnosis
def giveDiagnosis():
    print("\n Medhat: Based on your given symptoms:-")
    symptoms = list(set(user_symptoms))
    sz = len(symptoms)
    for i in range(sz):

        print(symptoms[i].replace("_", " ") , end = "")
        if(i < sz-1):
            print(" - ", end = "")
    print("\n Medhat:You could have the following diseases:")
    for disease,value in Disease_scores.items():
        if(value > 100):
            print(disease + " - " , end = "")
    #Recommendation, should change
    print("\nMehdat: I recommend visiting a specialized doctor.")
#Get the user back on track if he doesn't continue listing symptoms  
def handleInterruption():
    #Could recognize intent and answer it first then handle interruption
    print("\nMedhat: I'm still in the process of finishing your diagnosis, would you like to end your diagnosis? (y/n)")
    inp = input("\nUser: ")
    if(inp.lower() == "y"):
        giveDiagnosis()
    else:
        enhanceDiagnosis()
        giveDiagnosis()
#Dialogue Flow -> List symptom -> List rest of symptoms [What else you have? ] -> [User: That is all ] -> Get most potential symptoms [Yes/No | List them]
#To follow up on the user mentioning more of his symptoms.
def followUp():
    pass
#At the current moment, finds the 3 most likely next symptoms that the user could have.
def findPotentialSymptoms():
    potential_symptoms = []
    # Get the top 3 diseases
    top_diseases = sorted(Disease_scores.items(), key=lambda x: x[1], reverse=True)[:3]
    
    # Get the symptoms associated with each of the top diseases that the user doesn't already have
    symptoms_list = [set(Associated_Symptoms[disease]).difference(set(user_symptoms)) for disease,score in top_diseases]
    print(symptoms_list)
    print(user_symptoms)
    # Find common symptoms among all three diseases
    common_symptoms = set.intersection(*symptoms_list)
    
    if len(common_symptoms) >= 3:
        potential_symptoms = list(common_symptoms)[:3]
    else:
        # If there are fewer than three common symptoms, supplement with symptoms from each disease
        for symptoms in symptoms_list:
            potential_symptoms.extend(list(symptoms)[:3 - len(common_symptoms)])
            potential_symptoms = list(set(potential_symptoms))
            if len(potential_symptoms) == 3:
                break
    return potential_symptoms[:3]
#At the end of the diagnosis, ask for the potential symptoms to reduce error rate of diagnosis.
def enhanceDiagnosis():
    potential_symptoms = findPotentialSymptoms()
    #Ask after finding potential symptoms
    print("\nMedhat: Would you say you experienced the following symptoms lately?")
    fal7ana_string_yes = " "
    fal7ana_string_no = "not "
    for symptom in potential_symptoms:
        symptom_print = symptom.replace("_", " ")
        print(f"\nMedhat: {symptom_print} ?")
        user_input = input("\nUser: ").lower()
        for neg in negations:
            if neg in user_input:
                fal7ana_string_no += symptom + " "
        for aff in affirmations:
            if aff in user_input:
                fal7ana_string_yes += symptom + " "
                user_symptoms.append(symptom)
                break
    detect_symptoms(tokenize(fal7ana_string_yes))
    detect_symptoms(tokenize(fal7ana_string_no))
#Given a certain intent, produce a random response listed in the JSON file.
def giveResponse(tag):
    for intent in intents['intents']:
        if intent["tag"] == tag:
            print("\nMedhat:", random.choice(intent["responses"]))
#Given the user intent, and the context of the previous conversation [Last intent], generate a fitting response.
#This function handles the dialogue flow for the chatbot.
def generate_response(user_input , context): 
    user_intent = recognize_intent(user_input)
    if user_intent: #If the intent is recognized
        if user_intent ==  "goodbye":
            if(context == "symptom"):
                enhanceDiagnosis()
                giveDiagnosis()
            else:
                giveResponse("goodbye")
                return "quit"
        elif user_intent == "symptom":
            if(len(detect_symptoms(format(user_input))) == 0): #This should be a valid call to detectSymptoms, when we find intent is to mentio a symptom.
                if("not" in format(user_input)):
                    #Do nothing, probably detected a symptom but is not in the returned list
                    pass
                else:
                    print("\nMedhat: I could not recognize that symptom, try again.")
            elif (context == user_intent):
                giveResponse("followup")
            else:
                giveResponse(user_intent)
        elif context == "symptom":
            if (user_intent != context):
                handleInterruption()
        elif user_intent == "diagnosis":
            if(context == "symptom"):
                giveDiagnosis()
            else:
                print("\nMedhat: I need information to try and diagnose you, could you provide your symptoms?")
        elif user_intent == "disease": #User states he has a certain disease, we try to confirm.
            pass 
        elif user_intent == "description":
            pass
        elif user_intent == "help":
            pass
        else:
            giveResponse(user_intent)
    else: #If the sentence was gibberish
        if(len(detect_symptoms(format(user_input))) > 0): 
            giveResponse("symptom")
        else:
            print("\nMedhat: Sorry, I did not understand that.")
    return user_intent
def main():#
    print("Medhat: Hi how are ya?") #Welcome Message
    context = "greeting"
    # Chatbot Main loop
    while True:
        user_input = input("\nUser: ")
        context = generate_response(user_input , context)
        if (context == "quit"):
            break
# Call the main function
main()

