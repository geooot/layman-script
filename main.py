import sys
import time
import parse
import traceback
import re

memory = {
	"recent_subjects":[]
}
m_arr = []

def repl():
	print("_    ____ _   _ _  _ ____ _  _    ____ ____ ____ _ ___  ___")
	print("|    |__|  \_/  |\/| |__| |\ | __ [__  |    |__/ | |__]  | ")
	print("|___ |  |   |   |  | |  | | \|    ___] |___ |  \ | |     | ")
	print("----------------- By: George Thayamkery -------------------")
	print("")
	print("Remember:")
	print("1. Grammmer and spelling matters")
	print("2. Only write one simple sentance in the repl. ")
	print("3. Type at a \"Level 2\" reading level (nothing to complex).")
	print("")
	while(True):
		inp = input("> ")
		if inp == "!q":
			break
		elif inp == "!json":
			print(parse.json.dumps(memory,indent=4))
		else:
			try:
				parse.interpret(inp, memory, m_arr)
			except Exception as e:
				print("ERR: an error has occured, memory might be affected ---")
				print(traceback.format_exc())
				print(e)
def main():
	args = sys.argv
	fp = ""
	fArg = False
	sentance = ""
	count = 0
	for item in args:
		if item == "-f":
			fp = args[count + 1]
			fArg = True
		count += 1
	if fp == "" and len(args) != 1:
		print(len(args), args)
		sentance = args[1]
		parse.interpret(sentance, memory, m_arr)
	elif fArg:
		file = open(fp)
		sentances = re.split(r'(?<=[^A-Z].[.?]) +(?=[A-Z])', file.read())
		for s in sentances:
			if s[0] != "#":
				try:
					parse.interpret(s, memory, m_arr)
				except Exception as e:
					print("ERR: an error has occured, memory might be affected ---")
					print(traceback.format_exc())
					print(e)
		print("------READ FILE \"" +fp+ "\" ------")
		repl()
	else:
		repl()

if __name__ == "__main__":
	main()
