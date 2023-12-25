# Import HelperFunctions.py file
from HelperFunctions import *


################################ FUNCTIONS ################################
# Finds all listed symptoms in user input and updates the score for associated diseases
# Handles cases of multi-word symptoms [sore_throat] and if the sentence has "not" in it.
def detect_symptoms(user_input):
    #formatted_input = process_input(user_input)
    detected_symptoms = []
    stemmed_sentence = [stem(word) for word in user_input]
    SymptomsDB = QueryDB("SELECT * FROM symptoms")
    for symptom_id, symptom_name in SymptomsDB:
        filtered_symptom = ' '.join([word for word in symptom_name.split(' ') if word.lower() not in prepositions])
        stemmed_symptom = ' '.join([stem(word) for word in filtered_symptom.split(' ')])
        if all(word in stemmed_sentence for word in stemmed_symptom.split(' ')):
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
    #print("detected symptoms list inside detect_symptoms func: ", detected_symptoms)
    if not negation:
        user_symptoms.update(set(detected_symptoms))
    #print("user symptoms list inside detect_symptoms func: ", user_symptoms)
    detected_symptoms_ids = []
    associated_diseases_ids = []
    for symptom in detected_symptoms:
        detected_symptoms_ids.append(QueryDB(f"SELECT S.symptom_id FROM Symptoms S WHERE S.symptom_name = '{symptom}';")[0])
    for id in detected_symptoms_ids:
        associated_diseases_ids.append(
            QueryDB(f"SELECT HS.disease_id FROM Has_Symptoms HS WHERE HS.symptom_id = {id[0]};")[0])
    for id in associated_diseases_ids:
        weight = calculateWeight(id[0])
        if (negation):
            Disease_Scores[id[0]] -= weight
        else:
            Disease_Scores[id[0]] += weight
    return detected_symptoms


def calculateWeight(disease_id):
    symptoms_count = QueryDB(f"SELECT COUNT(HS.symptom_id) FROM Has_Symptoms HS WHERE HS.disease_id = {disease_id};")
    return 80/math.sqrt(symptoms_count[0][0])
def detect_diseases(user_input):
    #formatted_input = process_input(user_input)
    detected_diseases = []
    stemmed_sentence = [stem(word) for word in user_input]
    DiseasesDB = QueryDB("SELECT disease_id,disease_name FROM diseases")
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
    stemmed_user_input = [stem(word) for word in user_input]
    user_input = ' '.join(stemmed_user_input)
    for intent in intents['intents']:
        for pattern in intent['patterns']:
            formatted_pattern = format(pattern)
            stemmed_pattern = [stem(word) for word in formatted_pattern]
            formatted_pattern = ' '.join(stemmed_pattern)  # Convert pattern to lowercase
            # Check that at least one word matches in the pattern
            if (not has_common_word(user_input, formatted_pattern)):
                continue
            similarity = compute_similarity(formatted_pattern, user_input)
            if similarity > max_similarity:
                #print(f"user input: {user_input} , \n pattern: {formatted_pattern} ")
                max_similarity = similarity
                recognized_intent = intent['tag']
                #print(f"S: {similarity} , Intent: {recognized_intent} , Pattern: {formatted_pattern} \n")
    return recognized_intent if max_similarity > 0.35 else None


# Based on the diseases scores and user symptoms, gives the user a diagnosis
def giveDiagnosis():
    global response
    if len(user_symptoms) == 0:
        response += "\nI could not determine a diagnosis.\n"
    response += "Based on your given symptoms:-\n"
    symptoms = list(user_symptoms)
    response += print_list(symptoms, True)
    top_diseases = sort_dictionary(Disease_Scores)[:3]
    top3 = [disease_id for disease_id, value in top_diseases if value > 100]
    print("USER_ID", user_id)
    QueryDB(f"INSERT INTO diagnoses(disease_id, user_id) values ({top3[0]}, {user_id});" , fetch = False)
    if len(top3) == 0:
        response += "\nI could not determine a diagnosis.\n"
    else:
        diseases = []
        response += "\nYour most probable diseases are:-\n"
        for disease_id in top3:
            disease = QueryDB(f"SELECT disease_name FROM Diseases where disease_id = {disease_id};")
            diseases.append(disease[0][0])
        response += print_list(diseases)
        response += "With probabilties [respectively]\n"
        sz = len(top3)
        for i in range(sz):
            probability = (Disease_Scores[top3[i]]-100)
            if probability > 100:
                while probability > 100:
                    probability -= 20
            elif probability < 20:
                probability += 15
            if(i < sz-1):
                response += f"{round(probability)}%,\n"
            else:
                response += f"{round(probability)}%.\n"
        treatments = QueryDB(f"SELECT treatments FROM Diseases where disease_name = '{diseases[0]}';")
        causes = QueryDB(f"SELECT causes FROM Diseases where disease_name = '{diseases[0]}';")
        if(treatments):
            response += f"{diseases[0]} Treatments: \n{treatments[0][0]}\n"
        if(causes):
            response += f"{diseases[0]} Causes: \n{causes[0][0]}\n"
        disease_properties = QueryDB(f"SELECT description,severity,specialist,frequency,contagiousness FROM Diseases where disease_name = '{diseases[0]}';")
        description = disease_properties[0][0]
        severity = disease_properties[0][1]
        specialist = disease_properties[0][2]
        frequency = disease_properties[0][3]
        contagiousness = disease_properties[0][4]
        response += f"For {diseases[0]}, its details: \n{description}\n"
        response += f"{diseases[0]} is a {frequency.lower()} disease that is {severity.lower()}\n"
        if(contagiousness.lower() == 'yes'):
            response += f"{diseases[0]} is a contagious disease/condition, please take the necessary precautions.\n"
        response += f"For {diseases[0]}, I recommend visiting a/an {specialist} for a checkup.\n"
        remaining = diseases[1:3]
        if len(remaining) > 0:
            response += "Would you like to know more about the other diseases?\n"
        else:
            return
        #user_input = format(take_input())
        user_input = str(request.args['query'])
        user_input = format(user_input.lower())
        for word in user_input:
            if (word in affirmations):
                for disease in remaining:
                    treatments = QueryDB(f"SELECT treatments FROM Diseases where disease_name = '{disease}';")
                    if (treatments):
                        response += f"{diseases[0]} Treatments: \n{treatments[0][0]}\n"
                    causes = QueryDB(f"SELECT causes FROM Diseases where disease_name = '{disease}';")
                    if (causes):
                        response += f"{diseases[0]} Causes: \n{causes[0][0]}\n"

                    disease_properties = QueryDB( f"SELECT description,severity,specialist,frequency,contagiousness FROM Diseases where disease_name = '{disease}';")
                    description = disease_properties[0][0]
                    severity = disease_properties[0][1]
                    specialist = disease_properties[0][2]
                    frequency = disease_properties[0][3]
                    contagiousness = disease_properties[0][4]
                    response += f"For {disease}, its details: \n{description}\n"
                    response += f"{disease} is a {frequency.lower()} disease that is {severity.lower()}\n"
                    if (contagiousness.lower() == 'yes'):
                        response += f"{disease} is a contagious disease/condition, please take the necessary precautions.\n"
                    response += f"For {disease}, I recommend visiting a/an {specialist} for a checkup.\n"
                break
            elif (word in negations):
                break

# Get the user back on track if he doesn't continue listing symptoms
def handleInterruption():
    global response
    # Could recognize intent and answer it first then handle interruption
    response += "I'm still in the process of finishing your diagnosis, would you like to recieve it? (y/n)\n"
    #user_input = process_input(take_input())
    user_input = str(request.args['query'])
    user_input = process_input(user_input.lower())
    for word in user_input:
        if (word in affirmations):
            #enhanceDiagnosis(findPotentialSymptoms())
            giveDiagnosis()
            return ""
        elif (word in negations):
            response += "Terminating diagnosis, Progress is not saved\n"
            return "quit"
    response += "Sorry, I did not understand that.\n"
    return ""


# Dialogue Flow -> List symptom -> List rest of symptoms [What else you have? ] -> [User: That is all ] -> Get most potential symptoms [Yes/No | List them]
# At the current moment, finds the 3 most likely next symptoms that the user could have.
def findPotentialSymptoms():
    potential_symptoms = []

    # Get the id of the top 3 diseases
    top_diseases = sort_dictionary(Disease_Scores)[:3]

    # Get the symptoms associated with each of the top diseases that the user doesn't already have
    SymptomsTable = [
        QueryDB(
            f"SELECT DISTINCT S.symptom_name FROM Symptoms S , Has_Symptoms HS WHERE S.symptom_id = HS.symptom_id AND HS.disease_id = {dis[0]};")
        for dis in top_diseases
    ]

    symptoms_list = [
        set(x[0] for x in SymptomsTable[i] if SymptomsTable[i] is not None and x[0] not in user_symptoms)
        for i in range(len(SymptomsTable))
    ]
    #print("symptoms list inside findpotential func: ", symptoms_list)
    # Find common symptoms among all three diseases
    common_symptoms = set.intersection(*symptoms_list)
    common_symptoms = common_symptoms.difference(user_symptoms)
    #print("common_symptoms inside findpotential func: ", common_symptoms)

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

def updateDiseasesScores(symptom, negation_parameter):
    diseases_ids = QueryDB(f"SELECT HS.disease_id FROM Has_Symptoms HS, Symptoms S WHERE HS.symptom_id = S.symptom_id AND S.symptom_name = '{symptom}'")
    for id in diseases_ids:
        weight = calculateWeight(id[0])
        Disease_Scores[id[0]] += weight*negation_parameter

# At the end of the diagnosis, ask for the potential symptoms to reduce error rate of diagnosis.
def enhanceDiagnosis(potential_symptoms):
    global response
    response += "Would you say you experienced the following symptoms lately?\n"
    for symptom in potential_symptoms:
        symptom_print = symptom.replace("_", " ")
        response += f"{symptom_print} ?\n"
        #user_input = take_input()
        user_input = str(request.args['query'])
        user_input = user_input.lower()
        for neg in negations:
            if neg in user_input:
                updateDiseasesScores(symptom, -1)
                break
        for aff in affirmations:
            if aff in user_input:
                updateDiseasesScores(symptom, 1)
                user_symptoms.add(symptom)
                break



def findMatchingDisease(user_input, user_intent, parameter):
    global response
    user_input = remove_patterns(user_input, user_intent)
    DiseasesDB_names = QueryDB("SELECT disease_name FROM diseases")
    diseases_similarity = {disease[0]: similarity_ratio(user_input, disease[0].lower()) for disease in DiseasesDB_names}
    top_diseases = sort_dictionary(diseases_similarity)[:parameter]
    for disease in top_diseases:
        response += f"do you mean {disease[0]}?\n"
        #user_input = format(take_input())
        user_input = str(request.args['query'])
        user_input = format(user_input.lower())
        for word in user_input:
            if word in affirmations:
                return disease[0]
    if (user_intent != 'symptom'):
        response += "I could not recognize that disease,try again.\n"
    return None

def findMatchingSymptoms(user_input, user_intent, parameter):
    global response
    user_input = remove_patterns(user_input, user_intent)
    SymptomDB_names = QueryDB("SELECT symptom_name FROM symptoms")
    symptoms_similarity = {symptom[0]: similarity_ratio(user_input, symptom[0].lower()) for symptom in SymptomDB_names}
    top_symptoms = sort_dictionary(symptoms_similarity)[:parameter]
    for symptom in top_symptoms:
        print(f"symptom ok:  {symptom} | {user_symptoms}")
        if symptom[0] in user_symptoms:
            response += "This symptom was already detected!\n"
            continue
        response += f"do you mean {symptom[0]}?\n"
        #user_input = format(take_input())
        user_input = str(request.args['query'])
        user_input = format(user_input.lower())
        for word in user_input:
            if word in affirmations:
                return symptom[0]
    if (user_intent != 'symptom'):
        response += "I could not recognize that symptom,try again.\n"
    return None

# REFACTORING: These 2 functions could be made as a single function but you need to provide and additional input: symptom or disease
# findMatching(x, user_input, user_intent, parameter) -> x is either "symptom" or "disease"

# Given a certain intent, produce a random response listed in the JSON file.
def giveResponse(tag):
    global response
    for intent in intents['intents']:
        if intent["tag"] == tag:
            response += random.choice(intent["responses"])


def verifyDisease(disease):
    global response
    symptoms = QueryDB(
        f"SELECT S.symptom_name FROM Has_Symptoms HS , Diseases D, Symptoms S WHERE D.disease_name = '{disease}' AND HS.disease_id = D.disease_id AND S.symptom_id = HS.symptom_id;")
    symptoms = [s[0] for s in symptoms]
    enhanceDiagnosis(symptoms)
    disease_id = QueryDB(f"SELECT D.disease_id FROM Diseases D WHERE D.disease_name = '{disease}'")[0]
    #print(Disease_Scores[disease_id[0]])
    if (Disease_Scores[disease_id[0]] > 110):
        response += f"It is probable that you have {disease}. I suggest visiting a specialized doctor\n"
    elif (Disease_Scores[disease_id[0]] > 100):
        response += f"It is improbable that you have {disease}. I suggest performing a check-up\n"
    else:
        response += f"You have a low chance of having {disease}. It is probably nothing serious but make sure to consult a doctor\n"


# Given the user intent, and the context of the previous conversation [Last intent], generate a fitting response.
# This function handles the dialogue flow for the chatbot.
def generate_response(user_input, context, diagnosis_flag):
    global response
    user_intent = recognize_intent(user_input)
    if user_intent:  # If the intent is recognized
        if user_intent == "goodbye":    #If the user means to end current diagnosis/quit program.
            if (len(user_symptoms) > 0 and not diagnosis_flag):
                if handleInterruption() == "quit":
                    giveResponse("goodbye")
                    return "quit" , diagnosis_flag
            else:
                giveResponse("goodbye")
                return "quit" , diagnosis_flag
        elif user_intent == "symptom":  #If the user means to mention a symptom/disease they have.
            detected_symptoms = detect_symptoms(user_input)
            for word in user_input:
                if word in ["think" , "might" , "check"]:
                    detected_diseases = detect_diseases(user_input)
                    if (len(detected_diseases) > 0):
                        for disease in detected_diseases:
                            verifyDisease(disease)
                        return user_intent , diagnosis_flag
            if(len(detected_symptoms) > 0):  # This should be a valid call to detectSymptoms, when we find intent is to mention a symptom.
                if (context == user_intent):
                    giveResponse("followup")
                else:
                    giveResponse(user_intent)
            else:
                matching_disease = None
                for word in user_input:
                    if word in ["think", "might", "check"]:
                        matching_disease = findMatchingDisease(user_input, user_intent, 1)
                if matching_disease:
                    verifyDisease(matching_disease)
                else:
                    matching_symptom = findMatchingSymptoms(user_input, user_intent, 1)
                    #print(matching_symptom)
                    if matching_symptom:
                        updateDiseasesScores(matching_symptom , 1)
                        user_symptoms.add(matching_symptom)
                        # should print a response or change the user intent here <<<------
                    else: response += "I could not recognize that symptom/disease,try again.\n"
        elif user_intent == "diagnosis":    #if the user wants to finish the diagnosis process.
            if (len(user_symptoms) > 0):
                #enhanceDiagnosis(findPotentialSymptoms())
                giveDiagnosis()
                diagnosis_flag = True
            else:
                response += "I need information to try and diagnose you, could you provide your symptoms?\n"
        elif user_intent == "potential_symptoms": #The user wants to know other symptoms they could have.
            enhanceDiagnosis(findPotentialSymptoms())
            response += "These were the most likely symptoms you could have.\n"
            #giveDiagnosis()
            diagnosis_flag = True
        elif user_intent == "description":
            detected_diseases = detect_diseases(user_input)
            if (len(detected_diseases) > 0):
                for disease in detected_diseases:
                    description = \
                    QueryDB(f"SELECT D.description FROM Diseases D WHERE D.disease_name = '{disease}';")[0][0]
                    if (description):
                        response += f"{disease} Description:\n {description}\n"
                    else:
                        response += f"There is no description for this disease in the database.\n"
            else:
                matched_disease = findMatchingDisease(user_input, user_intent, 3)
                if (matched_disease):
                    description = \
                    QueryDB(f"SELECT D.description FROM Diseases D WHERE D.disease_name = '{matched_disease}';")[0][0]
                    if (description):
                        response += f"{matched_disease} Description:\n {description}\n"
                    else:
                        response += f"There is no description for this disease in the database.\n"
        elif user_intent == "treatments":
            detected_diseases = detect_diseases(user_input)
            if (len(detected_diseases) > 0):
                for disease in detected_diseases:
                    treatments = QueryDB(f"SELECT D.treatments FROM Diseases D WHERE D.disease_name = '{disease}';")[0][0]
                    if (treatments):
                        response += f"{disease} Treatments:\n {treatments}\n"
                    else:
                        response += f"There is no Treatments for this disease in the database.\n"
            else:
                matched_disease = findMatchingDisease(user_input, user_intent, 3)
                if (matched_disease):
                    treatments = \
                    QueryDB(f"SELECT D.treatments FROM Diseases D WHERE D.disease_name = '{matched_disease}';")[0][0]
                    if (treatments):
                        response += f"{matched_disease} Treatments:\n {treatments}\n"
                    else:
                        response += f"There is no Treatments for this disease in the database.\n"
        elif user_intent == "causes":
            detected_diseases = detect_diseases(user_input)
            if (len(detected_diseases) > 0):
                for disease in detected_diseases:
                    causes = QueryDB(f"SELECT D.causes FROM Diseases D WHERE D.disease_name = '{disease}';")[0][0]
                    if (causes):
                        response += f"{disease} Causes:\n {causes}\n"
                    else:
                        response += f"There is no Causes for this disease in the database.\n"
            else:
                matched_disease = findMatchingDisease(user_input, user_intent, 3)
                if (matched_disease):
                    causes = QueryDB(f"SELECT D.causes FROM Diseases D WHERE D.disease_name = '{matched_disease}';")[0][0]
                    if (causes):
                        response += f"{matched_disease} Causes:\n {causes}\n"
                    else:
                        response += f"There is no Causes for this disease in the database.\n"
        elif user_intent == "associated_symptoms":
            detected_diseases = detect_diseases(user_input)
            if (len(detected_diseases) > 0):
                for disease in detected_diseases:
                    symptoms = QueryDB(
                        f"SELECT S.symptom_name FROM Symptoms S, Has_Symptoms HS , Diseases D WHERE D.disease_name = '{disease}' AND HS.symptom_id = S.symptom_id AND D.disease_id = HS.disease_id;")
                    response += f"The symptoms for {disease} are: \n"
                    response += print_list(symptoms)
            else:
                matched_disease = findMatchingDisease(user_input, user_intent, 3)
                if (matched_disease):
                    symptoms = QueryDB(
                        f"SELECT S.symptom_name FROM Symptoms S, Has_Symptoms HS , Diseases D WHERE D.disease_name = '{matched_disease}' AND HS.symptom_id = S.symptom_id AND D.disease_id = HS.disease_id;")
                    response += f"The symptoms for {matched_disease} are: \n"
                    response += print_list(symptoms)

        else:
            if context == "symptom" and user_intent in ["greeting" , "funny"]:
                if handleInterruption() == "quit":
                    return "quit" , diagnosis_flag
            else:
                giveResponse(user_intent)
    else:  # If the sentence was gibberish
        detected_symptoms = detect_symptoms(user_input)
        if (len(detected_symptoms) > 0):
            giveResponse("symptom")
        else:
            response += "Sorry, I did not understand that.\n"
    return user_intent, diagnosis_flag

#gpt code
app = Flask(__name__)

prev_context = ""  # Initialize prev_context and response here, so they are not global variables
response = ""



@app.route('/api', methods=['GET'])
def return_response():
    global prev_context
    global response
    response = ""
    context = "greeting" if not prev_context else prev_context

    user_input = str(request.args.get('query', '')).lower()
    user_input = process_input(user_input)
    prev_context, diagnosis_flag = generate_response(user_input, context, diagnosis_flag=False)

    return jsonify({'output': response})

@app.route('/register', methods=['POST'])
def register_user():
    try:
        data = request.get_json()
        password = data.get('password')
        name = data.get('name')
        date_of_birth = data.get('date_of_birth')
        gender = data.get('gender')
        chronic_illness = data.get('chronic_illness')
        username = data.get('username')

        # Validate and process user registration data as needed

        # Example: Insert user data into the data storage file
        QueryDB(f"INSERT INTO log_in_info (username, password) VALUES ('{username}', '{password}');", fetch=False)
        QueryDB(f"INSERT INTO users (name, date_of_birth, gender, chronic_illness, username) VALUES ('{name}', '{date_of_birth}', '{gender}', '{chronic_illness}', '{username}');" , fetch = False)

        return jsonify({'message': 'User registration successful'})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/login', methods=['POST'])
def login_user():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        tuple = QueryDB(f"SELECT * FROM log_in_info WHERE username = '{username}' and password = '{password}';", fetch=True)

        if tuple != []:
            return jsonify({'message': 'Login successful'})
        else:
            return jsonify({'message': 'Login failed. Invalid username or password'})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/retrieve', methods=['POST'])
def retrieve_user_info():
    try:
        global user_id
        data = request.get_json()
        username = data.get('username')

        # Query user information based on the provided username
        user_info = QueryDB(f"SELECT user_id,name,date_of_birth,gender,chronic_illness FROM users WHERE username = '{username}';", fetch=True)
        user_id= user_info[0][0]
        print("User_id assigned:", user_id)
        prev_diag = QueryDB(f"""
        SELECT D.disease_name, TO_CHAR(G.event_datetime, 'DD-MM-YYYY at HH24:MI')
        FROM Diagnoses G, Diseases D
        WHERE D.disease_id = G.disease_id and G.user_id={user_id}
        ORDER BY G.event_datetime DESC;
        """,fetch=True)

        result = '\n'.join([' '.join(inner_list) for inner_list in prev_diag])
        print("RESULT:\n", result)
        # print(prev_diag)

        print("USER_INFO:\n", user_info)
        if user_info:
            # Extract relevant user information here, customize as needed
            name = user_info[0][1]
            date_of_birth = user_info[0][2]
            gender = user_info[0][3]
            chronic_illness = user_info[0][4]

            return jsonify({
                'message': 'User information retrieval successful',
                'name': name,
                'date_of_birth': date_of_birth,
                'gender': gender,
                'chronic_illness': chronic_illness,
                'diag': result,
            })
        else:
            return jsonify({'message': 'User not found'})

    except Exception as e:
        return jsonify({'error': str(e)})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000,debug = True)
