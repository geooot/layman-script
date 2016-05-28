import sys
import time
import parse
import json
memory = {}
m_arr = []

def repl():
	print("_    ____ _   _ _  _ ____ _  _    ____ ____ ____ _ ___  ___")
	print("|    |__|  \_/  |\/| |__| |\ | __ [__  |    |__/ | |__]  | ")
	print("|___ |  |   |   |  | |  | | \|    ___] |___ |  \ | |     | ")
	print("----------------- By: George Thayamkery -------------------")
	while(True):
		inp = input("> ")
		if inp == "!q":
			break
		elif inp == "!json":
			print(json.dumps(memory,indent=4))
		else:
			parse.interpret(inp, memory, m_arr)
def main():
	args = sys.argv
	fp = ""
	sentance = ""
	count = 0

	for item in args:
		if item == "-f":
			fp = args[count + 1]
		count += 1
	if fp == "" and len(args) != 1:
		print(len(args), args)
		sentance = args[1]
		parse.interpret(sentance, memory, m_arr)
	else:
		repl()

if __name__ == "__main__":
	main()
