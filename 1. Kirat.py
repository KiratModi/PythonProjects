print ("Kirat")

playing = input("Do you wanna play: ")
if playing.lower() != "yes": 
    quit()

print ("Okay lets play! ")
score = 0

answer = input(" What does CPU stands for: ")
if answer.lower() == "central processing unit":
    print("Correct!")
    score += 1
else:
    print("Thats wrong!!")

answer = input(" What does GPU stands for: ")
if answer.lower() == "graphic processing unit":
    print("Correct!")
    score += 1
else:
    print("Thats wrong!!")

answer = input(" What does RAM stands for: ")
if answer.lower() == "random access memory":
    print("Correct!")
    score +=1
else:
    print("Thats wrong!!")

print ("You got "+ str(score) + " Questions correct! which is equal to " + str((score / 3)*100) + " %.")
   
