import json
import os
shouldPrint = False
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

fComp = open("wordbank"+ os.sep + "comparators" + os.sep + "comparators.txt")
arr_of_comp = fComp.read().splitlines()
fComp.close()

def indexOf(arr,term):
    for index, item in enumerate(arr[:len(arr) - 1]):
        tmp = arr[index] + " " + arr[index + 1]
        if item == term or term == tmp:
            return index
    return 0

def interpret(sentance, memory, m_arr):
    ## check if question or assertion
    if "?" in sentance.lower() or "who" in sentance.lower() or "what" in sentance.lower() or "when" in sentance.lower() or "why" in sentance.lower() or ("does" in sentance.lower() and sentance.lower().split()[0] == "does"):
        print(interpret_question(sentance.replace("?",""),memory, m_arr))
    else:
        interpret_assertion(sentance.replace(".","").replace("!",""), memory, m_arr)

    if shouldPrint:
        print("---json")
        print(json.dumps(memory))
        print("json---")

def interpret_question(sentance, memory, m_arr):
    # who, what, when, where why

    sentance = sentance.lower()
    sentance = getPronoun_refrence(memory["recent_subjects"], sentance)
    words = sentance.split()
    types = assign_pos(words)
    types[0] = "asker"
    question_type = words[0]
    possible_subjects = []
    verb_and_subject = {
        "verb": "",
        "subject":[]
    }
    count = 1
    for t in types[1:]:
        if t == 'verb' and words[count] != "does":
            # print("the verb", words[count])
            if types[count-1] == "comparator":
                # print("found comparator")
                possible_subjects = findSubject(words[1:],types[1:],count-2,verb_and_subject, False)
            else:
                possible_subjects = findSubject(words[1:],types[1:],count-1,verb_and_subject, False)
            break
        elif words[count] == "is" and types[count-1] == "asker":
            findSplit(words[count+1:],possible_subjects)
        count = count + 1
    result = []
    # print(verb_and_subject,possible_subjects)
    if verb_and_subject["subject"] == [""] and "does" in words:
        # print("who does (subject) like")
        for subject in possible_subjects:
            if subject in memory:
                for v in memory[subject.replace("does ","")]:
                    if verb_and_subject["verb"] in v:
                        if question_type == "who":
                            for p in memory[subject][v]:
                                if p in memory:
                                    result.append(p)
                        else:
                            for p in memory[subject][v]:
                                result.append(p)
            else:
                print("ERR: Could not find \"" + subject + "\" in memory. Spelling is important!")
    elif verb_and_subject["subject"] != [""] and (possible_subjects == [] or possible_subjects == [""]) and "is" not in sentance:
        for p in memory:
            if p != "recent_subjects":
                for v in memory[p]:
                    if verb_and_subject["verb"] in v:
                        for person in verb_and_subject["subject"]:
                            if person in memory[p][v]:
                                result.append(p)       

    elif verb_and_subject["subject"] != [""] and (possible_subjects != [] or possible_subjects != [""]) and "is" not in sentance:
        for subject in possible_subjects:
            verb_seg = verb_and_subject["verb"]
            subject_seg = verb_and_subject["subject"]
            split_verb_seg = verb_seg.split()
            r = False
            if subject in memory:
                for v in memory[subject]:
                    if "not" in split_verb_seg:
                        cur_verb = split_verb_seg[1]
                        if cur_verb in v:
                            for item in memory[subject][v]:
                                for possible_sub in subject_seg:
                                    if possible_sub not in item:
                                        r = True
                                    else:
                                        r = False
                    else:
                        if verb_seg in v:
                            for item in memory[subject][v]:
                                for possible_sub in subject_seg:
                                    if possible_sub in item:
                                        r = True
                                    else:
                                        r = False
            result.append(r)
    else:
        NotDirectedQuestion = True
        for x in verb_and_subject["subject"]:
            if x in memory:
                NotDirectedQuestion = False

        if NotDirectedQuestion:
            for person in memory:
                if "is" in memory[person]:
                    result.append(person)
        else:
            for person in verb_and_subject["subject"]:
                if "is" in memory[person]:
                    result.append(memory[person]["is"])
                else:
                    result.append(memory[person])


    if shouldPrint:
        print(types)
    return result



def assign_pos(words):
    types = []
    count = 0
    for word in words:
        if isverb(word) and count != 0:
            types.append("verb")
        elif ispreposition(word) and count != 0:
            if count < len(word) and word == "to" and types[count + 1] == "verb":
                types.append("infinitive")
            else:
                types.append("preposition")
        elif iscomparator(word) and count != 0:
            types.append("comparator")
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
    sentance = sentance.lower()
    sentance = getPronoun_refrence(memory["recent_subjects"], sentance)
    words = sentance.split()
    types = assign_pos(words)
    count = 0

    mini_c = 0
    
    

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
            possible_subjects = findSubject(words,types,count,verb_and_subject, True)
            break
        count = count + 1

    for w in possible_subjects:
        i = indexOf(words,w)
        if types[i] == "":
            final_subjects.append(w)

    ## assign subjects to their verbs
    for s in final_subjects:
        if s not in memory:
            memory[s] = {}
        m_arr.append(s)
        if verb_and_subject["verb"] in memory[s]:
            for sub in verb_and_subject["subject"]:
                memory[s][verb_and_subject["verb"]].append(sub)
        else:
            memory[s][verb_and_subject["verb"]] = verb_and_subject["subject"]
    memory["recent_subjects"] = final_subjects
    if shouldPrint:
        print(types)

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

def iscomparator(word):
    result = False
    for item in arr_of_comp:
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
def findSubject(words, types, count, verb_and_subject, override):
    possible_subjects = []
    if types[count-1] != "" and override:
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
        # print(verb_seg)
        findAssignedSubject(verb_seg, verb_type_seg, verb_and_subject)

    return possible_subjects

def findAssignedSubject(verb_seg,verb_type_seg, verb_and_subject):
    if "and" in verb_seg:
        splitPoint = 0
        verb_phrase = ""
        loop = 0
        for thing in verb_seg:
            if (verb_type_seg[loop] == "verb") and "," not in thing:
                splitPoint = loop
                verb_phrase = verb_phrase + " " + thing
            else:
                break
            loop += 1
        # print( splitPoint, verb_seg[splitPoint+1:], verb_and_subject["subject"], verb_phrase)
        verb_and_subject["verb"] = verb_phrase.lstrip()
        findSplit(verb_seg[splitPoint+1:], verb_and_subject["subject"])
    else:
        # print("verb_seg",verb_seg)
        sub = ""
        verb_phrase = ""
        loop = 0
        splitPoint = 0

        for thing in verb_seg:
            # print((verb_type_seg[loop] == "verb" or verb_type_seg[loop] == "comparator"),verb_type_seg[loop], thing) 
            if (verb_type_seg[loop] == "verb" or verb_type_seg[loop] == "comparator" or (thing == "is" and loop < len(verb_seg) and verb_seg[loop + 1] == "a")):
                splitPoint = loop
                verb_phrase = verb_phrase + " " + thing
                if verb_type_seg == "verb":
                    verb_type_seg[loop:] = ["subject"] * (len(verb_type_seg) - loop)
            else:
                break
            loop += 1
        verb_and_subject["verb"] = verb_phrase.lstrip()
        for s in verb_seg[splitPoint+1:]:
            if sub == "":
                sub = sub + s
            else:
                sub = sub + " " + s
        verb_and_subject["subject"].append(sub)
def getPronoun_refrence(recent_subjects, words):
    result = ""
    for pronoun in words.split():
        pronoun = pronoun.lower()
        should_replace = False
        sent = ""
        if pronoun == "he" or pronoun == "she" or pronoun == "it" and len(recent_subjects) > 0:
            should_replace = True
        elif pronoun == "they" and len(recent_subjects) > 0:
            count = 0
            should_replace = True
            for s in recent_subjects:
                if sent == "":
                    sent = sent + s
                elif count > 0 and count < len(recent_subjects):
                    sent = sent + ", " + s
                else:
                    sent = sent + ", and " + s
        else:
            should_replace = False

        if should_replace and sent != "":
            result = result + " " + sent
        elif should_replace:
            result = result + " " + recent_subjects[0]
        else:
            result = result + " " + pronoun
    result = result.lstrip()
    return result




