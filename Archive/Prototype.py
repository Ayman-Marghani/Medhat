
from data import *
# Modify chatbot to recognize spelling mistakes
#_________________________________________________________________________

#_________________________________________________________________________
# Detect each symptom in input and increase the score of associated diseases accordingly.
# Also updates the user symptoms list
def detectSymptoms(word_list):
    word_list = tokenize(' '.join(word_list))
    words = nltk.pos_tag(word_list)
    for word, pos in words:
        if word in symptom_words:
            user_symptoms.append(symptom_words[word])
            for k, lst in Associated_Symptoms.items():
                if symptom_words[word] in lst:
                    Diseases[k] += 10
#_________________________________________________________________________
def generateResponse():
    global user_symptoms  # Declare user_symptoms as a global variable
    sorted_diseases = dict(sorted(Diseases.items()))
    temp_sympt_list = []
    for k, v in sorted_diseases.items():
        if v > 100:
            temp_sympt_list += Associated_Symptoms[k]
    potential_sympt_list = [x for x in temp_sympt_list if x not in user_symptoms]
    count_dict = Counter(potential_sympt_list)
    unique_elements = list(set(potential_sympt_list))
    sorted_unique_elements = sorted(unique_elements, key=lambda x: count_dict[x], reverse=True)
    for i in range(min(3, len(sorted_unique_elements))):
        print("Do you have any of the following symptoms? [y/n]\n") 
        symptom = sorted_unique_elements[i]
        print(i, ". " , symptom)
        inp = input("\nUser: ")
        has_symptom = inp == 'y'
        for k, v in Associated_Symptoms.items():
            if symptom in v and has_symptom:
                user_symptoms += symptom
                Diseases[k] += 15
            else:
                Diseases[k] -= 10
    sorted_diseases = dict(sorted(Diseases.items()))
    for k, v in sorted_diseases.items():
        print("You might have " + k + ", We suggest visiting a suitable doctor\n")
        break
#_________________________________________________________________________
# Main loop
while True:
    user_input = input("Chatbot: Ezayak 3amel Eh? ")
    if user_input == "quit":
        break
    tokenized = nltk.word_tokenize(user_input)
    # User Inquiry About -> [Disease|Associated Treatments|Preventative Measures|Associated Symptoms] -> overall general info
    # Detect Symptoms
    detectSymptoms(tokenized)
    generateResponse()
