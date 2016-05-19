import json
import os

f = open("wordbank"+ os.sep + "adverbs" + os.sep + "adverbs.txt")
lines = f.read().splitlines()
f.close()

indexes = open("wordbank"+ os.sep + "adverbs"+ os.sep + "index.json")
letter_index = json.loads(indexes.read())
indexes.close()

fVerb = open("wordbank"+ os.sep + "verbs" + os.sep + "verbs.txt")
f_lines = fVerb.read().splitlines()
fVerb.close()

f_indexes = open("wordbank"+ os.sep + "verbs"+ os.sep + "index.json")
f_letter_index = json.loads(f_indexes.read())
f_indexes.close()

def interpret(sentance):
    words = sentance.split()
    isQuestion = False
    isStatement = False

    ## check if question or assertion
    if "?" in sentance:
        isQuestion = True
        isStatement = False
    else:
        isStatement = True
        isQuestion = False

    ## loop through sentance
    types = []
    for word in words:
        if isverb(word):
            types.append("verb")
        elif isadverb(word):
            types.append("adverb")
        else:
            types.append("")
    print(types)

    # Assigning verbs to specific nouns
    count = 0
    assigners = []
    subject = ""
    for t in types:
        if t == 'verb':
            subject = words[count-1]
            break
        count = count + 1
    print(subject)

def isverb(word):
    result = False
    first_letter = word[:1].lower()
    look  = f_letter_index[first_letter]
    for item in f_lines[look:]:
        if word == item.lower():
            result = True
            break
        if item[:1].lower() != first_letter:
            break

    return result

def isadverb(word):
    result = False
    first_letter = word[:1].lower()

    look  = letter_index[first_letter]
    for item in lines[look:]:
        if item.lower() == word:
            result = True
            break
        if item[:1].lower() != first_letter:
            break

    return result
