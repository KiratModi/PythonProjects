import random

user_wins = 0
Computer_wins = 0
options = ["rock", "paper", "scissor"]

while True:
    user_input = input ("Type Rock/Paper/scissor or Q to Quit: ").lower()
    if user_input == "q":
        break
    
    if user_input not in options:
        print(" not a valid option:) ")
        continue
    random_number = random.randint (0,2)
    #0 = rock, 1 = paper, 2= scissor
    computer_choice = options[random_number]
    print("Computer picked", computer_choice + ".")
    if user_input== "rock" and computer_choice == "scissor":
        print("You won!!")
        user_wins += 1
    elif user_input == "paper" and computer_choice == "rock":
        print("You won!!")
        user_wins += 1
    elif user_input == "scissors" and computer_choice == "paper":
        print("You won!!")
        user_wins += 1
    else:
       print("You Lost!")
       Computer_wins += 1
       continue
    
print("You won", user_wins,"times.")
print("computer won", Computer_wins,"times.")
print("GoodBye!")


