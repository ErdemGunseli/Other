import random
moves = ["R", "P", "S"]
user_move = input("Enter R for Rock, P for Paper, S for Scissors: ").upper()
computer_move = random.choice(moves)
user_index = moves.index(user_move)
computer_index = moves.index(computer_move)
if (user_move == computer_move): print("Draw")
elif computer_move == "R" and user_move == "S": print("I win.")
elif computer_move == "S" and user_move == "R": print( "You win.")
elif computer_index > user_index: print("I win")
else: print("You win")