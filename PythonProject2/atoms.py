import sys

def main():
    # user inputs vaues for a,b and c

    a=float(input("a: "))
    b=float(input("b: "))
    c=float(input("c: "))

    # calculate the discriminant
    discriminant = b**2 - 4*a*c
    #output to user value
    print(f"{discriminant = }")
    return 0

if __name__ == "__main__":
    sys.exit(main())

