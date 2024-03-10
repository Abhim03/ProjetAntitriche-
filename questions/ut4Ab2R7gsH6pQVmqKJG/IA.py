import re


def extract_animal_sounds(text):
    return re.findall(r"\b\w*([a-zA-Z])\1{2,}\w*\b", text)
