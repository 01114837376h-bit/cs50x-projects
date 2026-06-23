def piramite (height):
    for i in range(1, height + 1):
        for j in range(height - i):
            print(" ", end="")
        for k in range(i):
            print("#", end="")
        print()
def piramith(height):
    for i in range(1, height + 1):
        for j in range(height - i):
            print(" ", end="")
        for k in range(i):
            print("#", end="")
        print("  ", end="")
        for k in range(i):
            print("#", end="")
        print()

def main():
    height = int(input("Height: "))
    diff=input("Choose a difficulty (e, h): ").lower()
    if diff == "e":
        piramite(height)
    elif diff == "h":
        piramith(height)
    else:
        print("Invalid difficulty. Please choose 'e' or 'h'.")

if __name__ == "__main__":
    main()