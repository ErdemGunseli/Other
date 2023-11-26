# Could be improved by checking if the known digits contains all the 0s or 1s in the final string
# and converting all the remaining digits to 1s or 0s respectively.
def guess_code(n):
    # Contains the list of digits that the algorithm will guess at each stage:
    guess = [0] * n

    # Contains the final answer as it is being deduced:
    answer = [0] * n

    zero_count = int(input(f"How many digits of {guess} match your code? "))
    if n == 1: answer[0] = [1, 0][zero_count]

    for index in range(n - 1):
        # Guessing a string with n-1 0s, and one 1, the position of which shifts:
        guess[index] = 1

        matches = int(input(f"How many digits of {guess} match your code? "))

        # The answer to the guess reveals the digit at this index:
        # If matches == zero_count + 1, that digit is 1:
        if matches > zero_count:
            answer[index] = 1

        # Reverting the guess back to its original state:
        guess[index] = 0

    # Deducing the last digit from the number of 0s:
    answer[n-1] = [0, 1][answer.count(0) - zero_count]
    print(f"Your code is {answer}.")


if __name__ == "__main__":
    guess_code(10)
