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
def indexOf(arr,term):
    for index, item in enumerate(arr[:len(arr) - 2]):
        tmp = arr[index] + " " + arr[index + 1]
        if item == term or term == tmp:
            return index

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

    ## loop through sentance and assign pos
    types = []
    count = 0
    for word in words:
        if isverb(word) and count != 0:
            types.append("verb")
        elif isadverb(word) and count != 0:
            types.append("adverb")
        elif isconnector(word) and count != 0:
            types.append("and_conj")
        else:
            types.append("")
        count = count + 1


    # finding possible subjects
    count = 0
    assigners = []
    possible_subjects = []
    final_subjects = []
    for t in types:
        if t == 'verb' and words[count-1] != "to":
            if types[count-1] != "":
                types[count] = ""
            else:
                possible_subjects.append(findSubject(words,types,count-1))
                ## possible_subjects.append(words[count-1])
            if types[count-2] == 'and_conj':
                possible_subjects.append(findSubject(words,types,count-3))
        count = count + 1
    print(types)
    print(possible_subjects)

    for w in possible_subjects:
        i = indexOf(words,w)
        print(i)
        if types[i] == "":
            final_subjects.append(w)
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

def isconnector(word):
    result = False
    # TODO Incorporate "and" and its synonyms in the grammer.json file
    and_synonyms = ["and", "along with", "with", "in addition to"]
    if word in and_synonyms:
        result = True
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

def findSubject(wordArr, typesArr, index):
    count = index
    subject = ""
    while count >= 0:
        sp = " "
        if typesArr[count] == "":
            if subject == "":
                sp = ""
            subject = wordArr[count] + sp + subject 
        else:
            break
        count = count -1
    return subject

