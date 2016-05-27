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
    for index, item in enumerate(arr[:len(arr) - 1]):
        tmp = arr[index] + " " + arr[index + 1]
        if item == term or term == tmp:
            return index
    return 0

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
            # ['george,', 'bill,', 'and', 'bob', 'likes', 'pie']
            if types[count-1] != "":
                types[count] = "" 
                print("nullifying: " + words[count])  
            else:
                tmp = words[:count]
                print(t + " "  + words[count],tmp)
                for wr in tmp:
                    m = wr.replace(",","")

            # if types[count-1] != "" and types[count-1] != "and_conj":
            #     types[count] = ""
            # else:
            #     print("else:",findSubject(words,types,count-1))
            #     possible_subjects.append(findSubject(words,types,count-1))
            #     ## possible_subjects.append(words[count-1])
            # if types[count-2] == 'and_conj':
            #     possible_subjects.append(findSubject(words,types,count-3))
            # elif "," in words[count-3]:
            #     print("count-3:",words[count-3])
            #     tmp = words[count-3].replace(",","").split()
            #     for t in tmp:
            #         possible_subjects.append(t)
        count = count + 1

    print(types)
    print("words:", words)
    print("possible:",possible_subjects)
    for w in possible_subjects:
        i = indexOf(words,w)
        if types[i] == "":
            final_subjects.append(w)

    print(final_subjects)
def isverb(word):
    result = False
    first_letter = word[:1].lower()
    look  = f_letter_index[first_letter]
    for item in f_lines[look:]:
        if word == item.lower() or word == (item.lower() + "ed"):
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
##TODO FIX PLS
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

