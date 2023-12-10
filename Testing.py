from Medhat import *
from autocorrect import Speller
from spellchecker import SpellChecker
import spacy
#print(compute_similarity("stomachache" , "tummy pain"))
spell = SpellChecker()

#print(spell.correction("golstane"))

'''
def correct_spelling(sentence):
    # Tokenize the sentence
    words = sentence.split()

    # Check and correct spelling for each word
    corrected_words = [spell.correction(word) for word in words]

    # Join the corrected words back into a sentence
    corrected_sentence = ' '.join(corrected_words)

    return corrected_sentence

# Example usage
user_input = "I have excessive farting"
corrected_input = correct_spelling(user_input)
print("Corrected Input:", corrected_input)



spell = Speller()
corrected = spell(user_input)
print(f"Corrected: {corrected}")

'''

nlp = spacy.load("en_core_web_md")
def compute_similarity(pattern, user_input):
    pattern_doc = nlp(pattern)
    user_input_doc = nlp(user_input)
    similarity = pattern_doc.similarity(user_input_doc)
    return similarity
sentence = "tell me something funny"

print(compute_similarity(sentence, input("user: ")))

'''
Ideas:
-Give the user the whole database if he wants? [asks what diseases are in your database?]

-Add patterns to chatbot for (Treatments, causes): 
    I want to know the treatments of [d]
    I want to know the causes of [d]

-Add pattern of "I want to know more about [disease]" -> description?  -> done
    

-What are the symptoms of [disease] -> pattern : Results in all related symptoms. -> done
    "I have the third symptom"

-Search for a [symptom-disease] -> Implicit use only probably [in "i did not recognize symptom"]: -> done
    helps the user pinpoint his symptom
    LIKE in database query (another approach)

-Help menu:
    Shows all functionality and how to access it : [To search -> "search for [_]" , To ask about a disease -> "what is [disease]] -> done




def common_characters(user_input, sentence):
    cnt = 0
    for c in user_input:
        if c in sentence:
            cnt += 1
    return cnt / len(sentence)

# Example sentences
user_input = " fver"
sentence = "fever"

print(common_characters(user_input, sentence))
'''


print(stem("breathlessness"))
