import sys
import lexer

def run(source):
    return lexer.scan_tokens(source)
def run_file(file):
    with open(file, "r") as f:
        byte_array = f.read()
    print(run(byte_array))
    print(byte_array)

def run_prompt():
    while True:
        line = input("> ")
        if line != "":
            print(run(line))

def main():
    if len(sys.argv) > 2:
        print("Usage: lox [script]")
        sys.exit(64)
    elif len(sys.argv) == 2:
        run_file(sys.argv[1])
    else: 
        run_prompt()
    
if __name__ == "__main__":
    main()
