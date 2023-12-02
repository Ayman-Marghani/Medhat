#from Medhat import *
from autocorrect import Speller
from spellchecker import SpellChecker
#print(compute_similarity("stomachache" , "tummy pain"))
spell = SpellChecker()
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