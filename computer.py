import sys

def compute(eq_str=None):
    if eq_str is not None:
        print(f"arg is {eq_str}")


if __name__ == "__main__":
    if len(sys.argv) == 2 :
        eq_str = sys.argv[1]
        size = len(eq_str.split("="))
        if size == 2:
            compute(eq_str)
        elif size == 1:
            print(f"No '=' in the expression: '{eq_str}'\nContinue ? y/n")
            if  input().upper() == "Y":
                eq_str  += " = 0"
                compute(eq_str)
            else:
                exit(0)
        else:
            print(f"Multiple '=' found in the expression: '{eq_str}'")
            exit(0)
    else:
        print("Wrong format:\n  Usage: Python3 'aX2 + bX + c = 0'")