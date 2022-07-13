
input_string = input("Please enter your input: ")
counter = 0

for i in range(len(input_string)):
    print(input_string[-(i+1)], end="") #Prints the string starting from the -1 character, so from reverse.
print()


while (input_string[counter] == input_string[-(counter +1)]) and counter <= len(input_string)//2: #Checks that the first and last letter of the word is the same untiil it reaches half the length of the word.
    counter += 1

if counter - 1 == len(input_string)//2: #If when the loop ends, counter-1 (-1 because there is an extra +1 at the end) must be equal to half the world length (integer division) if the loop did not end early. The loop ends early if the string is not a palindrome.
        print("Your input is a palindrome.")
else:
    print("Your input is not a palindrome.")
  
## ACS Very good work well done