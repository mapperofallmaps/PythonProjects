name = input("Please enter your name: ")
age = int(input("How old are you, {0}? ".format(name)))
print(age)

if age >= 18:
    print("You are old enough to vote")
    print("Please put an X in the box")
else:
    print("Please come back in {0} years".format(18 - age))

print("Please guess a number between 1 and 10: ")
guess = int(input())

if guess != 5:
    if guess <5:
        print("Please guess higher")
    else:
        print("Please guess lower")

    guess = int(input())
    if guess == 5:
        print("Well done, you guessed it")
    else:
        print("Sorry, you have not guess correctly")
else:
    print("You got it")

age = int(input("How old are you? "))


if 15 < age < 66:
    print("Have a good day at work")

if (age < 16) or (age > 65):
    print("Enjoy your free time")
else:
    print("Have a good day at work")

x = input("Please enter some text ")
if x:
    print("You enter '{}'".format(x))
else:
    print("You did nto enter anything")

age = int(input("How old are you? "))
if not(age < 18):
    print("You are old enough to vote")
else:
    print("Please come back in {0} years".format(18 - age))

parrot = "Norwegian Blue"

letter = input("Enter a character: ")

if letter not in parrot:
    print("I don't need that letter")
else:
    print("Give me an {}, Bob".format(letter))