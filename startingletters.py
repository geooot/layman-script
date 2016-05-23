import json

f = open("wordbank/adverbs/adverbs.txt")
indexes = open("wordbank/adverbs/index.json", "w")
lines = f.read().splitlines()
current_letter = ""
payload = {}
index = 1
for word in lines:
    first_letter = word[:1]
    if first_letter == "'":
        first_letter = word[1:2]
    if first_letter.lower() != current_letter:
        current_letter = first_letter.lower()
        payload[first_letter.lower()] = index
    index = index + 1

result = json.dumps(payload, indent=4)
indexes.write(result)
indexes.close()
f.close()
print(result)
