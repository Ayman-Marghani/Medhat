# Import Data.py file
from Data import *

######################################################################################################################################################
############################## Helper Functions ##############################

def similarity_ratio(a, b):
    return SequenceMatcher(None, a, b).ratio()

# this function sorts a dictionary based on the values
# returns a list of pairs (key, value)
def sort_dictionary(dict):
    return sorted(dict.items(), key=lambda x: x[1], reverse=True)

def remove_substrings(input_list):
    for symptom in input_list:
        for symptom2 in input_list:
            if symptom != symptom2:
                remove_flag = True
                for w in lemmatize(symptom):
                    if w not in symptom2:
                        remove_flag = False
                        break
                if remove_flag:
                    input_list.remove(symptom)
                    break  # Exit the inner loop after removal
    return input_list

def remove_patterns(user_input, user_intent):
    # remove pattern words from user_input
    for intent in intents['intents']:
        if intent["tag"] == user_intent:
            for pattern in intent['patterns']:
                formatted_pattern = format(pattern)
                for word in formatted_pattern:
                    if word in user_input:
                        user_input.remove(word)

    user_input = ' '.join(user_input)
    return user_input

# Using spacy, computes similarity between 2 sentences
def compute_similarity(pattern, user_input):
    pattern_doc = nlp(pattern)
    user_input_doc = nlp(user_input)
    similarity = pattern_doc.similarity(user_input_doc)
    return similarity


# Checks that 2 sentences have a common word , also to better the matching.
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

######################################################################################################################################################
################################ INPUT PROCESSING FUNCTIONS ################################

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
                    transformed_split_sentence.append(word.replace(contraction, ""))
                    transformed_split_sentence.append(expanded_word)
                    break
            # if the word is not a contraction then just add it to the result list
            if not contraction_flag:
                transformed_split_sentence.append(word)
    return transformed_split_sentence


def correct_spelling(sentence):
    # Tokenize the sentence
    words = sentence.split()

    # Check and correct spelling for each word
    corrected_words = [spell.correction(word) if spell.correction(word) else word for word in words]

    # Join the corrected words back into a sentence
    corrected_sentence = ' '.join(corrected_words)

    return corrected_sentence


def removeIgnored(sentence):
    new_sentence = ""
    for letter in sentence:
        if letter not in ignore_punctuation or letter == "'":
            new_sentence += letter
        else:
            new_sentence += " "
    return new_sentence

# Input: a string containing the user's input
# Output: list of all the words (strings) in the sentence (tokenized sentence)
def tokenize(sentence):
    return sentence.lower().split()

def lemmatize(text):
    doc = nlp(text)
    lemmatized_text = " ".join([token.lemma_ for token in doc])
    return lemmatized_text
# this function calls stem function on a string
def stem(word):
    return stemmer.stem(word.lower())

def format(sentence):
    formatted = contraction_transformer(tokenize(removeIgnored(sentence)))
    return [word.replace("'", "") for word in formatted]

# Removes less "significant" words to similarity computation, to better the matching
def remove_pronouns_prepositions(word_list):
    filtered_list = [word for word in word_list if word.lower() not in (pronouns + prepositions)]
    return filtered_list

def process_input(input):
    user_input = format(correct_spelling(input))
    return user_input

######################################################################################################################################################
################################ INPUT/OUTPUT FUNCTIONS ################################
def take_input():
    user_input = input("User: ").lower()
    return user_input


def print_response(response):
    print(f"- Medhat: {response}")
    # OR for the app: send_response(response)

def print_list(lst, replace = False):
    sz = len(lst)
    for i in range(sz):
        if replace:
            print(lst[i].replace("_", " "), end = '')
        else:
            print(lst[i], end="")
        if (i < sz - 1):
            print(" - ", end ="")
    print("")

