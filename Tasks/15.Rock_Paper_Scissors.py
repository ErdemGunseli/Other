import random

moves = ["R", "P", "S"]

user_move = input("Enter R for Rock, P for Paper, S for Scissors: ").upper()
computer_move = random.choice(moves) #The computer picks a random move.

user_index = moves.index(user_move) #This is the index of the move made by the user.
computer_index = moves.index(computer_move) #This is the index of the move made by the computer.

print("I say {}.".format(computer_move))

if (user_move == computer_move): #If same, it is a draw.
    print("Draw")
elif computer_move == "R" and user_move == "S": #Rock beats Scissors
    print("I win.")
elif computer_move == "S" and user_move == "R":
    print( "You win.")
elif computer_index > user_index: #Since scissors beats paper, and paper beats rock, by ordering the list correctly, we can utilise the indexes to determine who won.
    print("I win")
else:
    print("You win")

#I first used nested if statements but I think it is shorter this way?
