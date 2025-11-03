import re

def clean_markdown(text):
    # Dummy cleaning
    text = re.sub(r'#+', '', text)
    return text.strip()
