"""
Author: Aniket Kumar
Description: A Simple Chatty Bot
"""


def greet(bot_name, birth_year):
    print('Hello! My name is ' + bot_name + '.')
    print('I was created in ' + birth_year + '.')


def remind_name():
    print('Please, remind me your name.')
    name = input()
    print('What a great name you have, ' + name + '!')
    guess_age()


def guess_age():
    print('Let me guess your age.')
    print('Enter remainders of dividing your age by 3, 5 and 7.')

    rem3 = int(input())
    rem5 = int(input())
    rem7 = int(input())
    age = (rem3 * 70 + rem5 * 21 + rem7 * 15) % 105

    print("Your age is " + str(age) + "; that's a good time to start programming!")
    count()


def count():
    print('Now I will prove to you that I can count to any number you want.')

    num = int(input())
    curr = 0
    while curr <= num:
        print(curr, '!')
        curr = curr + 1

        test()


def test():
    print("Let's test your programming knowledge.")
    # write your code here
    print("""
Why do we use methods?
1. To repeat a statement multiple times.
2. To decompose a program into several small subroutines.
3. To determine the execution time of a program.
4. To interrupt the execution of a program.""")



def test1():
    choice = int(input())
    if choice == 2:
        print('Completed, have a nice day!')
    else:
        print("Please, try again")
        test1()


def end():
    print('Congratulations, have a nice day!')
    end()


greet('san', '2022')  # change it as you need
remind_name()




