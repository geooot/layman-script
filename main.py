## @main.py
import sys
def main():
	args = sys.argv
	fp = ""
	count = 0
	for item in args:
		if item == "-f":
			fp = args[count + 1]
		count += 1
	

if __name__ == "__main__":
	main()
