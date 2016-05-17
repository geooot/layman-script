import json
f = open("wordbank\\adverbs\\adverbs.txt")
lines = f.read().splitlines()
f.close()

indexes = open("wordbank\\adverbs\\index.json")
letter_index = json.loads(indexes.read())
indexes.close()

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

def isverb(word):
    result = False
    first_letter = word[:1].lower()

    f = open("wordbank\\verbs\\verbs.txt")
    lines = f.read().splitlines()
    f.close()

    indexes = open("wordbank\\verbs\\index.json")
    letter_index = json.loads(indexes.read())
    indexes.close()

    look  = letter_index[first_letter]
    for item in lines[look:]:
        if item.lower() in word:
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
