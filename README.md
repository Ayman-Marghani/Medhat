# Medhat Chatbot

Medhat is a medical chatbot application developed to assist users in obtaining information about various medical conditions, symptoms, and potential diagnoses. This Chatbot project was developed as part of the Software engineering course in the first term of the third level at Egypt University of Informatics.

## Overview

Medhat aims to provide users with a personalized communication channel where they can inquire about specific medical issues, receive information about diseases and symptoms, and even request potential diagnoses based on the symptoms provided.

### Key Features

- **User-Driven Inquiry**: Users can input symptoms, ask about diseases, or seek potential diagnoses, facilitating personalized medical interactions.
- **Smart Response Generation**: Utilizing NLP tools, Medhat generates contextually relevant responses, catering to user queries effectively.
- **Accurate Symptom and Disease Identification**: Through robust database querying, Medhat accurately identifies and matches user-provided symptoms and diseases.
- **Enhanced Medical Understanding**: Users can learn about potential diagnoses, understand disease characteristics, and take necessary precautions based on Medhat's insights.

## Usage

Medhat is a Python-based chatbot application integrated with Flutter for its user interface. Follow the steps below to set up and run the application:

### Prerequisites

- Python 3.7 (or above)
- Flutter SDK
- PostgreSQL

### Steps

1. Clone the repository:
  ```bash
  git clone https://github.com/Ayman-Talat/Medhat.git
  ```
2. Navigate to the application folder:
  ```bash
  cd medhat_python
  ```
3. Install required Python dependencies:
  ```bash
  pip install -r requirements.txt
  ```
  - Ensure you have downloaded the English model for spaCy:
  ```bash
  python -m spacy download en_core_web_md
  ```
4. Run the Medhat application:
  ```bash
  python Medhat.py
  ```
