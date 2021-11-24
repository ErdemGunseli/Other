distinct_prime_factors = []
productOfDistinctPrimeFactors = 1


def primeOrNot(number): 
    if number == 2:
        return True
    for i in range(2,number):
        if number % i == 0:
            return False
    return True

def factors(number): #working
    factorsList = []
    for i in range(2,number):
        if number % i == 0:
            factorsList.append(i)
    return factorsList




inputNumber = int(input())

if primeOrNot(inputNumber) == True:
    print(inputNumber)
else:
    for i in factors(inputNumber):
        if (primeOrNot(i) == True): # and (i in list == False):
            distinct_prime_factors.append(i)

    for i in distinct_prime_factors:
        productOfDistinctPrimeFactors = i * productOfDistinctPrimeFactors
    print(productOfDistinctPrimeFactors)
  

