import random

top_of_range = input("type a number: ")

if top_of_range.isdigit():
    top_of_range = int(top_of_range)

    if top_of_range <= 0:
        print(" Please write number bigger then 0 ")
        quit()
    
else:
    print(" Type a number next time ")
    quit()

random_number = random.randint(0, top_of_range)
gusses = 0

while True:
    user_guess = input("make a guess: ")

    if user_guess.isdigit():
       user_guess = int(user_guess)
    else:
        print(" type a number next time ")
        continue
    if user_guess == random_number:
        print(" you got it ")
        break
    elif user_guess < random_number:
        print("Your guessed number is less than random number ")
    else:
        print("your number is more than random number ")
    gusses += 1
    continue

print (" You got rght answer in ", gusses, " gusses")

