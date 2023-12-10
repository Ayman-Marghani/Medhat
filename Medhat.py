# Import HelperFunctions.py file
from HelperFunctions import *

################################ FUNCTIONS ################################
# Finds all listed symptoms in user input and updates the score for associated diseases
# Handles cases of multi-word symptoms [sore_throat] and if the sentence has "not" in it.
def detect_symptoms(user_input):
    #formatted_input = format(user_input)
    detected_symptoms = []
    stemmed_sentence = [stem(word) for word in user_input]
    SymptomsDB = CallDB("symptom", "*")
    for symptom_id, symptom_name in SymptomsDB:
        filtered_symptom = '_'.join([word for word in symptom_name.split('_') if word.lower() not in prepositions])
        stemmed_symptom = '_'.join([stem(word) for word in filtered_symptom.split('_')])
        if all(word in stemmed_sentence for word in stemmed_symptom.split('_')):
            detected_symptoms.append(symptom_name)
    if (len(detected_symptoms) == 0): return []
    detected_symptoms = remove_substrings(detected_symptoms)
    not_count = user_input.count("not")
    not_symptom_count = 0
    for symptom in detected_symptoms:
        if "not" in format(symptom):
            not_symptom_count += 1
    if not_count > not_symptom_count:
        negation = True
    else:
        negation = False
    print("detected symptoms list inside detect_symptoms func: ", detected_symptoms)
    if not negation:
        user_symptoms.update(set(detected_symptoms))
    print("user symptoms list inside detect_symptoms func: ", user_symptoms)
    detected_symptoms_ids = []
    associated_diseases_ids = []
    for symptom in detected_symptoms:
        detected_symptoms_ids.append(
            QueryDB(f"SELECT S.symptom_id FROM Symptom S WHERE S.symptom_name = '{symptom}';")[0])
    for id in detected_symptoms_ids:
        associated_diseases_ids.append(
            QueryDB(f"SELECT HS.disease_id FROM Has_Symptoms HS WHERE HS.symptom_id = {id[0]};")[0])
    for id in associated_diseases_ids:
        if (negation):
            Disease_Scores[id[0]] -= 10
        else:
            Disease_Scores[id[0]] += 10
    return detected_symptoms


def detect_diseases(user_input):
    #formatted_input = format(user_input)
    detected_diseases = []
    stemmed_sentence = [stem(word) for word in user_input]
    DiseasesDB = CallDB("disease", "*")
    for disease_id, disease_name in DiseasesDB:
        filtered_disease = ' '.join([word for word in disease_name.split(' ') if word.lower() not in prepositions])
        stemmed_disease = ' '.join([stem(word) for word in filtered_disease.split(' ')])
        if all(word in stemmed_sentence for word in stemmed_disease.split(' ')):
            detected_diseases.append(disease_name)
    return detected_diseases


# Takes the user input and recognizes its input by getting the intent with the pattern having the highest similarity matching.
def recognize_intent(user_input):
    max_similarity = 0
    recognized_intent = None
    user_input = ' '.join(user_input)  # Convert user input to lowercase

    for intent in intents['intents']:
        for pattern in intent['patterns']:
            formatted_pattern = ' '.join(format(pattern))  # Convert pattern to lowercase
            # Check that at least one word matches in the pattern
            if (not has_common_word(user_input, formatted_pattern)):
                continue
            similarity = compute_similarity(formatted_pattern, user_input)
            if similarity > max_similarity:
                max_similarity = similarity
                recognized_intent = intent['tag']
                print(f"S: {similarity} , Intent: {recognized_intent} , Pattern: {formatted_pattern} \n")
    return recognized_intent if max_similarity > 0.35 else None


# Based on the diseases scores and user symptoms, gives the user a diagnosis
def giveDiagnosis():
    print_response("Based on your given symptoms:-")
    symptoms = list(user_symptoms)
    print_list(symptoms, True)
    top_diseases = sortDictionary(Disease_Scores)[:3]
    top3 = [disease_id for disease_id, value in top_diseases.items() if value > 100]
    if len(top3) == 0:
        print_response("\nI could not determine a diagnosis.")
    else:
        diseases = []
        print_response("\nYou could have the following diseases:\n-")
        for disease_id in top3:
            disease = QueryDB(f"SELECT disease_name FROM Disease where disease_id = {disease_id};")
            diseases.append(disease)
        diseases_print = [disease[0][0] for disease in diseases]
        print_list(diseases_print)

        treatments = QueryDB(f"SELECT treatment FROM Disease where disease_name = {diseases[0]};")
        causes = QueryDB(f"SELECT cause FROM Disease where disease_name = {diseases[0]};")
        print_response(f"{diseases[0]} Treatments: \n{treatments[0][0]}")
        print_response(f"{diseases[0]} Causes: \n{causes[0][0]}")
        print_response("Would you like to know more about the other diseases?")
        user_input = process_input(take_input())
        remaining = diseases[1:3]
        for word in user_input:
            if (word in affirmations):
                for disease in remaining:
                    treatments = QueryDB(f"SELECT treatment FROM Disease where disease_name = {disease};")
                    causes = QueryDB(f"SELECT cause FROM Disease where disease_name = {disease};")
                    print_response(f"{disease} Treatments: \n{treatments[0][0]}")
                    print_response(f"{disease} Causes: \n{causes[0][0]}")
                    break
            elif (word in negations):
                break
        #Recommendation, should change
        print_response("I recommend visiting a specialized doctor.")


# Get the user back on track if he doesn't continue listing symptoms
def handleInterruption():
    # Could recognize intent and answer it first then handle interruption
    print_response("I'm still in the process of finishing your diagnosis, would you like to end your diagnosis? (y/n)")
    user_input = process_input(take_input())
    for word in user_input:
        if (word in affirmations):
            giveDiagnosis(findPotentialSymptoms())
            return
        elif (word in negations):
            enhanceDiagnosis(findPotentialSymptoms())
            giveDiagnosis()
            return
        else:
            print_response("Terminating diagnosis, Progress is saved)")
    print_response("Sorry, I did not understand that.")
    return


# Dialogue Flow -> List symptom -> List rest of symptoms [What else you have? ] -> [User: That is all ] -> Get most potential symptoms [Yes/No | List them]
# At the current moment, finds the 3 most likely next symptoms that the user could have.
def findPotentialSymptoms():
    potential_symptoms = []

    # Get the id of the top 3 diseases
    top_diseases = sortDictionary(Disease_Scores)[:3]

    # Get the symptoms associated with each of the top diseases that the user doesn't already have
    SymptomsTable = [
        QueryDB(
            f"SELECT DISTINCT S.symptom_name FROM Symptom S , Has_Symptoms HS WHERE S.symptom_id = HS.symptom_id AND HS.disease_id = {dis[0]};")
        for dis in top_diseases
    ]

    symptoms_list = [
        set(x[0] for x in SymptomsTable[i] if SymptomsTable[i] is not None and x[0] not in user_symptoms)
        for i in range(len(SymptomsTable))
    ]
    print("symptoms list inside findpotential func: ", symptoms_list)
    # Find common symptoms among all three diseases
    common_symptoms = set.intersection(*symptoms_list)
    common_symptoms = common_symptoms.difference(user_symptoms)
    print("common_symptoms inside findpotential func: ", common_symptoms)

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


# At the end of the diagnosis, ask for the potential symptoms to reduce error rate of diagnosis.
def enhanceDiagnosis(potential_symptoms):
    print_response("Would you say you experienced the following symptoms lately?")
    for symptom in potential_symptoms:
        symptom_print = symptom.replace("_", " ")
        print_response(f"{symptom_print} ?")
        user_input = process_input(take_input())
        for neg in negations:
            if neg in user_input:
                detect_symptoms("not " + symptom)
        for aff in affirmations:
            if aff in user_input:
                detect_symptoms(symptom)
                user_symptoms.add(symptom)
                break


def findMatchingDisease(user_input, user_intent, parameter):
    # remove pattern words from user_input
    for intent in intents['intents']:
        if intent["tag"] == user_intent:
            for pattern in intent['patterns']:
                formatted_pattern = format(pattern)
                for word in formatted_pattern:
                    if word in user_input:
                        user_input.remove(word)

    user_input = ' '.join(user_input)

    DiseasesDB_names = CallDB("disease", "disease_name")
    diseases_similarity = {disease[0]: similar(user_input, disease[0].lower()) for disease in DiseasesDB_names}
    top_diseases = sortDictionary(diseases_similarity)[:parameter]
    for disease in top_diseases:
        print_response(f'do you mean {disease[0]}?')
        user_input = process_input(take_input())
        if user_input in affirmations:
            return disease[0]
    if (user_intent != 'symptom'):
        print_response("I could not recognize that disease,try again.")
    return None


# Given a certain intent, produce a random response listed in the JSON file.
def giveResponse(tag):
    for intent in intents['intents']:
        if intent["tag"] == tag:
            print_response(random.choice(intent["responses"]))


def verifyDisease(disease):
    symptoms = QueryDB(
        f"SELECT S.symptom_name FROM Has_Symptoms HS , Disease D, Symptom S WHERE D.disease_name = '{disease}' AND HS.disease_id = D.disease_id AND S.symptom_id = HS.symptom_id;")
    symptoms = [s[0] for s in symptoms]
    enhanceDiagnosis(symptoms)
    disease_id = QueryDB(f"SELECT D.disease_id FROM Disease D WHERE D.disease_name = '{disease}'")[0]
    if (Disease_Scores[disease_id[0]] > 110):
        print_response(f"It is probable that you have {disease}. I suggest visiting a specialized doctor")
    elif (Disease_Scores[disease_id[0]] > 100):
        print_response(f"It is improbable that you have {disease}. I suggest performing a check-up")
    else:
        print_response(f"You have a low chance of having {disease}. It is probably nothing serious but make sure to consult a doctor")


# Given the user intent, and the context of the previous conversation [Last intent], generate a fitting response.
# This function handles the dialogue flow for the chatbot.
def generate_response(user_input, context):
    user_intent = recognize_intent(user_input)
    detected_symptoms = detect_symptoms(user_input)
    if user_intent:  # If the intent is recognized
        if user_intent == "goodbye":
            if (len(user_symptoms) > 0):
                enhanceDiagnosis(findPotentialSymptoms())
                giveDiagnosis()
            else:
                giveResponse("goodbye")
                return "quit"
        elif user_intent == "symptom":
            detected_diseases = detect_diseases(user_input)
            if (len(detected_diseases) > 0):
                for disease in detected_diseases:
                    verifyDisease(disease)
            elif (len(detected_symptoms) > 0):  # This should be a valid call to detectSymptoms, when we find intent is to mention a symptom.
                if (context == user_intent):
                    giveResponse("followup")
                else:
                    giveResponse(user_intent)
            else:
                matching_disease = findMatchingDisease(user_input, user_intent, 1)
                if matching_disease:
                    verifyDisease(matching_disease)
                else:
                    '''
                    matching_symptom = findMatchingSymptom(user_input, user_intent, 1)
                    if matching_symptom: detect_symptoms(matching_symptom)
                    '''
                    print_response("I could not recognize that symptom/disease,try again.")
        elif user_intent == "diagnosis":
            if (len(user_symptoms) > 0):
                enhanceDiagnosis(findPotentialSymptoms())
                giveDiagnosis()
            else:
                print_response("I need information to try and diagnose you, could you provide your symptoms?")
        elif user_intent == "potential_symptoms":
            enhanceDiagnosis(findPotentialSymptoms())
            print_response("These were the most likely symptoms you could have.")
        elif user_intent == "description":
            detected_diseases = detect_diseases(user_input)
            if (len(detected_diseases) > 0):
                for disease in detected_diseases:
                    description = \
                    QueryDB(f"SELECT D.description FROM Disease D WHERE D.disease_name = '{disease}';")[0][0]
                    print_response(f"{disease} Description:\n {description}")
            else:
                matched_disease = findMatchingDisease(user_input, user_intent, 3)
                if (matched_disease):
                    description = \
                    QueryDB(f"SELECT D.description FROM Disease D WHERE D.disease_name = '{matched_disease}';")[0][0]
                    print_response(f"{matched_disease} Description:\n {description}")
        elif user_intent == "treatments":
            detected_diseases = detect_diseases(user_input)
            if (len(detected_diseases) > 0):
                for disease in detected_diseases:
                    treatments = QueryDB(f"SELECT D.treatments FROM Disease D WHERE D.disease_name = '{disease}';")[0][
                        0]
                    print_response(f"{disease} Treatments:\n {treatments}")
            else:
                matched_disease = findMatchingDisease(user_input, user_intent, 3)
                if (matched_disease):
                    treatments = \
                    QueryDB(f"SELECT D.treatments FROM Disease D WHERE D.disease_name = '{matched_disease}';")[0][0]
                    print_response(f"{matched_disease} Treatments:\n {treatments}")
        elif user_intent == "causes":
            detected_diseases = detect_diseases(user_input)
            if (len(detected_diseases) > 0):
                for disease in detected_diseases:
                    causes = QueryDB(f"SELECT D.causes FROM Disease D WHERE D.disease_name = '{disease}';")[0][0]
                    print_response(f"{disease} Causes:\n {causes}")
            else:
                matched_disease = findMatchingDisease(user_input, user_intent, 3)
                if (matched_disease):
                    causes = QueryDB(f"SELECT D.causes FROM Disease D WHERE D.disease_name = '{matched_disease}';")[0][
                        0]
                    print_response(f"{matched_disease} Causes:\n {causes}")
        elif user_intent == "associated_symptoms":
            detected_diseases = detect_diseases(user_input)
            if (len(detected_diseases) > 0):
                for disease in detected_diseases:
                    symptoms = QueryDB(
                        f"SELECT S.symptom_name FROM Symptom S, Has_Symptoms HS , Disease D WHERE D.disease_name = '{disease}' AND HS.symptom_id = S.symptom_id AND D.disease_id = HS.disease_id;")
                    print_response(f"The symptoms for {disease} are: ")
                    print_list(symptoms)
            else:
                matched_disease = findMatchingDisease(user_input, user_intent, 3)
                if (matched_disease):
                    symptoms = QueryDB(
                        f"SELECT S.symptom_name FROM Symptom S, Has_Symptoms HS , Disease D WHERE D.disease_name = '{matched_disease}' AND HS.symptom_id = S.symptom_id AND D.disease_id = HS.disease_id;")
                    print_response(f"The symptoms for {matched_disease} are: ")
                    print_list(symptoms)

        else:
            if context == "symptom" and user_intent in ["greeting" , "funny"]:
                handleInterruption()
            else:
                giveResponse(user_intent)
    else:  # If the sentence was gibberish
        if (len(detected_symptoms) > 0):
            giveResponse("symptom")
        else:
            print_response("Sorry, I did not understand that.")
    return user_intent


# Main function
def main():
    # print Welcome Message
    print_response("Hi how are ya?")
    context = "greeting"
    # Chatbot Main loop
    while True:
        user_input = process_input(take_input())
        context = generate_response(user_input, context)
        if (context == "quit"):
            break


# Call the main function
#main()

'''
input processing pipeline: correct_spelling -> format


Refactor all duplicated code
'''
