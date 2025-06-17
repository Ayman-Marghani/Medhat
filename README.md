# 🩺 Medhat — A Personalized Medical Assistant App

Medhat is a cross-platform medical chatbot application developed as part of the Software Engineering course at Egypt University of Informatics. It is designed to assist users in learning more about medical conditions, symptoms, and potential diagnoses through an interactive and accessible chatbot experience.

The system includes a **Flutter mobile frontend**, a **Python NLP-powered backend**, and a **PostgreSQL database** populated with structured medical information from sources such as the NHS.

---

## 🎞️ Demo

https://github.com/user-attachments/assets/968189ec-db8e-47ad-852a-1c84aae5b63f

---

## 🧠 Overview

Medhat provides a conversational platform for users to:
- Inquire about symptoms and receive possible disease matches.
- Learn about known diseases, treatments, and precautions.
- Explore medical awareness content through an intuitive mobile interface.

---

## 🎯 Key Features

- **User-Driven Inquiry**  
  Users input symptoms, ask about specific conditions, or seek potential diagnoses.

- **Smart Response Generation**  
  Contextual replies generated through NLP models using `spaCy` and `NLTK`.

- **Accurate Symptom & Disease Matching**  
  Backend queries a PostgreSQL database to match user input with structured medical data.

- **Profile-Based Customization**  
  Users create accounts storing age, weight, chronic conditions, and medical history.

- **Medical Awareness Feed**  
  Frontend provides curated news from trusted sources like the CDC and NHS.

---

## 📁 Repository Structure

```
lib/                  # Flutter app source code
medhat_python/        # Python chatbot backend and logic
medhat_python/CSVs    # Cleaned datasets used to populate the medical DB
assets/               # App icons, fonts, images
docs/                 # Documentation and presentation files
```

---

## 🤖 Backend — Chatbot Engine

The Python-based chatbot supports:

- Intent detection and entity recognition
- Matching symptoms to potential conditions
- Providing responses with advice and treatment info
- Querying structured PostgreSQL tables for accuracy

Dependencies:
- `spaCy`
- `NLTK`
- `NumPy`
- `psycopg2`

---

## 📱 Frontend — Flutter App

The Flutter mobile app features:

- Page routing and clean UI
- Form validation and history tracking
- Menu-driven navigation optimized for mobile devices
- Secure user login and input handling

---

## 🧪 Setup & Usage

### 🔧 Prerequisites

- Python 3.7+
- Flutter SDK
- PostgreSQL (with a local or cloud-hosted instance)

---

### ⚙️ Backend Setup (Python)

1. Clone the repository:
   ```bash
   git clone https://github.com/Ayman-Talat/Medhat.git
   ```

2. Navigate to the Python backend:
   ```bash
   cd medhat_python
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   python -m spacy download en_core_web_md
   ```

4. Run the chatbot:
   ```bash
   python Medhat.py
   ```

> ⚠️ Ensure PostgreSQL is running and populated using the provided CSVs under `medhat_python/CSVs`.

---

### 📱 Frontend Setup (Flutter)

1. From the project root:
   ```bash
   flutter pub get
   flutter run
   ```

---

## 📄 Documentation

- [📘 Medhat Software Specification Document (SRS)](./docs/Medhat%20Software%20Specifications%20Document.docx.pdf)  
- [📊 Medhat Presentation](./docs/Medhat%20Presentation.pptx)

---

## 👥 Contributors

- **Mahmoud Barbary** – Backend logic, architecture & NLP  
- **Mennatallah Mohei Eldin** – Frontend development, UI/UX design  
- **Ayman Talat** – Integration & Python functionality  
- **Gehad Abdelrahman** – Data collection & research  
- **Mohamed Salem** – Testing & coordination

---

## 📌 Disclaimer

This project is intended **strictly for academic use** and is not a replacement for professional medical advice, diagnosis, or treatment.
