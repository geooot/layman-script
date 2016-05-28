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

fPrep = open("wordbank"+ os.sep + "prepositions" + os.sep + "prepositions.txt")
arr_of_prep = fPrep.read().splitlines()
fPrep.close()

def indexOf(arr,term):
    for index, item in enumerate(arr[:len(arr) - 1]):
        tmp = arr[index] + " " + arr[index + 1]
        if item == term or term == tmp:
            return index
    return 0

def interpret(sentance, memory, m_arr):
    ## check if question or assertion
    if "?" in sentance.lower() or "who" in sentance.lower() or "what" in sentance.lower() or "when" in sentance.lower() or "why" in sentance.lower():
        print(interpret_question(sentance.replace("?",""),memory, m_arr))
    else:
        interpret_assertion(sentance.replace(".","").replace("!",""), memory, m_arr)

def interpret_question(sentance, memory, m_arr):
    # who, what, when, where why
    words = sentance.split()
    types = assign_pos(words)
    types[0] = "asker"
    question_type = words[0]
    possible_subjects = []
    verb_and_subject = {
        "verb": "",
        "subject":[]
    }
    count = 0
    for t in types[1:]:
        if t == 'verb' or words[count] == "is" and types[count-1] != "asker":
            possible_subjects = findSubject(words[1:],types[1:],count,verb_and_subject)
        elif words[count] == "is" and types[count-1] == "asker":
            findSplit(words[count+1:],possible_subjects)
        count = count + 1
    result = []
    print(possible_subjects, verb_and_subject, types)
    if verb_and_subject["subject"] == [""] and verb_and_subject["verb"] != "":
        for subject in possible_subjects:
            for v in memory[subject.replace("does ","")]:
                if verb_and_subject["verb"] in v:
                    if question_type == "who":
                            for p in memory[subject][v]:
                                if p in memory:
                                    result.append(p)
    elif verb_and_subject["subject"] != [""]:
        if question_type == "who":
            for p in memory:
                if p != "recent_subjects":
                    for v in memory[p]:
                        if verb_and_subject["verb"] in v:
                            for person in verb_and_subject["subject"]:
                                if person in memory[p][v]:
                                    result.append(p)
    else:
        if question_type == "who":
            for person in possible_subjects:
                result.append(memory[p])



    return result



def assign_pos(words):
    types = []
    count = 0
    for word in words:
        if isverb(word) and count != 0:
            types.append("verb")
        elif ispreposition(word) and count != 0:
            types.append("prepostion")
        elif isadverb(word) and count != 0:
            types.append("adverb")
        elif isconnector(word) and count != 0:
            types.append("and_conj")
        else:
            types.append("")
        count = count + 1
    return types

def interpret_assertion(sentance, memory, m_arr):
    ## loop through sentance and assign pos
    words = sentance.split()
    types = assign_pos(words)
    count = 0


    # finding possible subjects
    count = 0
    assigners = []
    possible_subjects = []
    final_subjects = []
    verb_and_subject = {
        "verb": "",
        "subject":[]
    }
    for t in types:
        if t == 'verb' and words[count-1] != "to":
            possible_subjects = findSubject(words,types,count,verb_and_subject)
        count = count + 1

    for w in possible_subjects:
        i = indexOf(words,w)
        if types[i] == "":
            final_subjects.append(w)

    ## assign subjects to their verbs
    for s in final_subjects:
        memory[s] = {}
        m_arr.append(s)
        memory[s][verb_and_subject["verb"]] = verb_and_subject["subject"]
    memory["recent_subjects"] = final_subjects

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
def ispreposition(word):
    result = False
    for item in arr_of_prep:
        if word == item.lower():
            result = True
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
def findSplit(tmp, possible_subjects):
    split_by_comma = []
    split_by_and = []
    restructured_sent = ""
    restructured_sent = tmp[0]
    for wr in tmp[1:]:
        restructured_sent = restructured_sent + " " + wr
    split_by_comma = restructured_sent.split(",")
    split_by_and = restructured_sent.split("and")
    if len(split_by_comma) > 1:
        for sub in split_by_comma:
            possible_subjects.append(sub.replace(" and ", "").lstrip())
    else:
        for sub in split_by_and:
            possible_subjects.append(sub.strip())
def findSubject(words, types, count, verb_and_subject):
    possible_subjects = []
    if types[count-1] != "":
        types[count] = ""
    else:
        tmp = words[:count]
        type_tmp = types[:count]
        verb_seg = words[count:]
        verb_type_seg = types[count:]
        if "and" in tmp:
            findSplit(tmp,possible_subjects)
        else:
            full_subject = ""
            cnt = 0
            for w in tmp:
                if type_tmp[cnt] == "":
                    full_subject = full_subject + " " + w
                cnt += 1
            possible_subjects.append(full_subject.lstrip())
        if "and" in verb_seg:
            verb_and_subject["verb"] = verb_seg[0]
            split_by_comma = []
            split_by_and = []
            restructured_sent = ""
            restructured_sent = verb_seg[1]
            for wr in verb_seg[2:]:
                restructured_sent = restructured_sent + " " + wr
            split_by_comma = restructured_sent.split(",")
            split_by_and = restructured_sent.split("and")
            if len(split_by_comma) > 1:
                for sub in split_by_comma:
                    verb_and_subject["subject"].append(sub.replace(" and ", "").lstrip())
            else:
                for sub in split_by_and:
                    verb_and_subject["subject"].append(sub.strip())
        else:
            verb_and_subject["verb"] = verb_seg[0]
            sub = ""
            for s in verb_seg[1:]:
                if sub == "":
                    sub = sub + s
                else:
                    sub = sub + " " + s
            verb_and_subject["subject"].append(sub)
    return possible_subjects
