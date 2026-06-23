def cash(amount):    
    if amount <= 0:
        return -1
    amount = int(amount * 100)  
    quarters = int(amount / 25)
    amount -= quarters*25
    dimes = int(amount / 10)
    amount -= dimes*10
    nickels = int(amount / 5)
    amount -= nickels*5
    pennies = int(amount / 1)
    amount -= pennies*1
    sum_of_coins = quarters + dimes + nickels + pennies
    return sum_of_coins
def main():
    amount = float(input("Enter the amount of cash: "))
    total_coins = cash(amount)
    if total_coins == -1:
        print("Invalid amount. Please enter a positive value.")
    else:
        print(f"Total number of coins needed: {total_coins}")
if __name__ == "__main__":
    main()