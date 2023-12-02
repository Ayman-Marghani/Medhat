from data import *
# Main loop
print ("Medhat: Hi how are ya?")
while True:
    user_input = input("\nUser: ")
    if user_input == "quit":
        break
    generate_response(user_input)
