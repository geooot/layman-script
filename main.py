import sys
import parse
def main():
	args = sys.argv
	fp = ""
	sentance = ""
	count = 0
	for item in args:
		if item == "-f":
			fp = args[count + 1]
		count += 1
	if fp == "":
		sentance = args[1]
		parse.interpret(sentance)

if __name__ == "__main__":
	main()