import random
symbols = ["Cherry", "Bell", "Lemon", "Orange", "Star", "Skull"]
credit = float(1)
roll_or_not = " "

while roll_or_not != "QUIT" and credit > 0: #Ends when the player enters 'quit' or when their credit is depleted.
    selected_symbol_counter = [0, 0, 0, 0, 0, 0] #The counter list is reset at the beginning of each turn.
    roll_or_not = " "
    while roll_or_not != "ROLL": #Begins when the user types 'roll'
        print("You have £{} of credit. Each round costs £0.20. Good Luck.".format(credit))
        print("If you get 2 of the same symbol, you will win 50p. If you get 3 of the same symbol, you will win £1, or £5 for 3 Bells.")
        print("If you get 2 skulls, you will lose £1.")
        roll_or_not = input("Type 'ROLL' to play or type 'OUIT' to quit: ").upper()
        print()
    #endwhile
#endwhile

    credit += -0.2 #decrease 20p from the credit.
    print("You Got:")
    for i in range(3):
        symbol_index = int(random.randint(0,5)) #Chooses a random integer between 1 and 3.
        current_symbol = symbols[symbol_index] #Finds the corresponding symbol
        selected_symbol_counter[symbol_index] += 1 #Adds 1 to the counter list, corresponding to the location of the symbol.
        print(current_symbol)  #Prints The corresponding symbol.
    #loop

    if selected_symbol_counter[5] > 1: #If there are 2 or more skulls rolled, -£1.
            credit += -1
    #endif
    for i in range(6): #Goes through the counter array to determine the results
        if selected_symbol_counter[i] ==  3 and i != 5: #If 3 of the same symbol are rolled and the symbol is not the skull
            if selected_symbol_counter[1] == 3: #If the symbol is the bell, +£5
                credit += 5
            else: #If the symbol is not the bell, +£1
                credit += 1
            #endif
        elif selected_symbol_counter[i] == 2 and i != 5: #If 2 of the same symbol are rolled and they are not the skull, +£0.5
            credit += 0.5
        #endif
    #loop
    #endif

    if credit < 0: #If the player runs out of credit, their credit is set to 0. (Although this allows for an exploit in a real-life situation as the player could add 20p at a time, decreasing overall losses.)
        credit = 0
    #endif

    print("You now have £{}. Press ENTER to continue".format(credit))
    input()
 



   


