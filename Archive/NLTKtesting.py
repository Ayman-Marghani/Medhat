import nltk
import re
nltk.download('averaged_perceptron_tagger')
#https://spotintelligence.com/2023/01/24/part-of-speech-pos-tagging-in-nlp-python/#The_benefits_of_rule-based_Part-of-speech_POS_tagging
sentence = "Ayman enjoys very good"
tokens = nltk.word_tokenize(sentence)
pos_tags = nltk.pos_tag(tokens, tagset='universal', tagger='averaged_perceptron')
print(pos_tags)
#__
patterns = [
    r"(?<!not\s+)(I\s+have\s+a\s+\w+)",
    r"(?<!not\s+)(My\s+\w+\s+hurts)",
    r"(?<!not\s+)(I\s+am\s+having\s+a\s+\w+)",
    r"(?<!not\s+)(I\s+experience\s+\w+)",
    r"(?<!not\s+)(I'm\s+suffering\s+from\s+\w+)",
    r"(?<!not\s+)(I'm\s+dealing\s+with\s+\w+)",
    r"(?<!not\s+)(I\s+think\s+I\s+have\s+a\s+\w+)",
    r"(?<!not\s+)(I\s+believe\s+I\s+have\s+\w+)",
    r"(?<!not\s+)(I\s+think\s+it's\s+\w+)",
    r"(?<!not\s+)(I\s+might\s+have\s+a\s+\w+)",
    r"(?<!not\s+)(I\s+seem\s+to\s+have\s+a\s+\w+)",
    r"(?<!not\s+)(I\s+have\s+symptoms\s+of\s+\w+)",
    r"(?<!not\s+)(I\s+manifest\s+\w+)",
    r"(?<!not\s+)(I\s+show\s+signs\s+of\s+\w+)",
    r"(?<!not\s+)(I\s+exhibit\s+\w+)",
    r"(?<!not\s+)(I\s+have\s+pain\s+in\s+my\s+\w+)",
    r"(?<!not\s+)(I\s+have\s+an\s+ache\s+in\s+my\s+\w+)",
]
