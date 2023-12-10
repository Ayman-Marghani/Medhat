# Import your chatbot script as a module
import Medhat as Chatbot

# Path to your input file
input_file = "input.txt"  # Replace with your input file's name or path

# Open the input file and read lines
with open(input_file, "r") as file:
    lines = file.readlines()

# Iterate through each line in the file
for line in lines:
    # Simulate user input by passing the line to the chatbot function
    response = Chatbot.generate_response(line.strip(), "greeting")

    # Print the conversation
    print(f"User input: {line.strip()}")
    print(f"The Chatbot recognized the following intent: {response}")

