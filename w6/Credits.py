def credit_sheck(cridet_numper):
    tupe = 0
    total = 0
    if len(cridet_numper) == 15 and (cridet_numper[0] == '3' and (cridet_numper[1] == '4' or cridet_numper[1] == '7')):
        tupe = 1
    elif len(cridet_numper) == 16 and (cridet_numper[0] == '5' and (cridet_numper[1] == '1' or cridet_numper[1] == '2' or cridet_numper[1] == '3' or cridet_numper[1] == '4' or cridet_numper[1] == '5')):
        tupe = 2
    elif len(cridet_numper) == 16 and (cridet_numper[0] == '4'):
        tupe = 3
    elif len(cridet_numper) == 13 and (cridet_numper[0] == '4'):
        tupe = 3
    if tupe == 0:
        return -1
    for i in range(len(cridet_numper)):
        if i % 2 == 0:
            total += int(cridet_numper[len(cridet_numper) - 1 - i])
        else:
            temp = int(cridet_numper[len(cridet_numper) - 1 - i]) * 2
            if temp > 9:
                total += (temp % 10) + (temp // 10)
            else:
                total += temp

    if total % 10 == 0:
        return tupe
    else:
        return -1
def main():
    cridet_numper = input("Number: ")
    tupe = credit_sheck(cridet_numper)
    if tupe == 1:
        print("AMEX")
    elif tupe == 2:
        print("MASTERCARD")
    elif tupe == 3:
        print("VISA")
    else:
        print("INVALID")
main()