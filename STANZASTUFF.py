import stanza

# Download and initialize the English pipeline
nlp = stanza.Pipeline('en', package='craft')

# Annotate example text
doc = nlp('The patient had a sore throat and was treated with Cepacol lozenges.')

# Print out named entities
for ent in doc.ents:
    print(f"Entity: {ent.text}, Type: {ent.type}")
