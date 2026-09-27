import json

from parse_law import parse_law_structure


with open("paragraph_test.txt", "r", encoding="utf-8") as file:
    text = file.read()


result = parse_law_structure(text)


for record in result:
    print(record)