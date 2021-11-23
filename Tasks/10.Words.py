input_string = input("Please enter a sentence: ")
space = "false"
count = 0


for i in input_string:

    if space == "true" and i != " ":
        count += 1
    
    if i == " ":
      space = "true"
    else:
        space = "false"

   
    #endif
#loop
print(count)
    
    # ACS Very good work. A few more comments required! It helps to remember what algorithm you used. 