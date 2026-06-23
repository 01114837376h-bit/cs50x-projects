def assist_readability(text):
    word_count = len(text.split())

    letter_count = 0
    sentence_count = 0

    for c in text:
        if c.isalpha():
            letter_count += 1
        elif c in ".!?":
            sentence_count += 1

    L = letter_count / word_count * 100
    S = sentence_count / word_count * 100

    index = round(0.0588 * L - 0.296 * S - 15.8)

    return index


def main():

         text = input("Text: ")
         index = assist_readability(text)

         if index < 1:
            print("Before Grade 1")
         elif index >= 16:
           print("Grade 16+")
         else:
           print(f"Grade {index}")


main()