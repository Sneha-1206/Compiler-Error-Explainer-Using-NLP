import re

def preprocess(text):
    return re.sub(r"[^a-z0-9 ]", " ", text.lower())

def clean_error(error):
    return error.lower().replace("error:", "").strip()