import sys
def main():
    name=input("What is your name? ")
    age=int(input("How old are you? "))
    print(f"Hello, {name}! You are {age} years old.")
    return 0
if __name__ == "__main__":
    sys.exit(main())