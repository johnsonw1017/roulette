#Import
import time
import random
import sys

#Global variables/parameters
valid_locations = ["R1", "R2", "R3", "1-12", "13-24", "25-36", "1-18", "19-36", "EVEN", "ODD", "RED", "BLACK"]
location_syntax = ["u", "l", "d", "r", "c"]
user_commands = ["help", "board", "quit"]
red_numbers = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
black_numbers = [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35]

# Create string for the roulette game board
def draw_board():
    row_top1 = "+---" * 14 + "+"
    row_top2 = "+   " + "+---" * 13 + "+"
    row_top3 = "    " + "+---" * 12 + "+"

    for row in range(3, -1, -1):

        if row in [1, 2]:
            print(row_top2)
        else:
            print(row_top1)
            if row == 0:
                break
        
        if row == 2:
            print("| 0", end=" ")
        else:
            print("|  ", end=" ")

        for col in range(1, 13):
            boardnum = row + 3 * (col - 1)

            if boardnum / 10 < 1:
                print(f"| {boardnum}", end=" ")
            else:
                print(f"| {boardnum}", end="")
        
        print(f"| R{row}|")

    print("    |     1-12      |     13-24     |     25-36     |")
    print(row_top3)
    print("    |  1-18 |  EVEN |  RED  | BLACK |  ODD  | 19-36 |")
    print(row_top3, end="\n\n")

#Player instructions
def print_instructions():
    print("    u\n  +---+ \nl | 1 | r\n  +---+ \n    d")
    print("Use the above diagram to add chips to edges of a number (except 0). For example u1 to add chips on top edge of number 1.")
    print("To place chip at the corner between 3-4 numbers, use cN, where N is the largest of the numbers.")
    print("For the remainder, add chips as appeared on the board.")
    print("To remove chips, use a negative number (-x) when prompted.\n")

#Input handling
def get_input(prompt):
    
    user_input = input(prompt)

    # when player inputs "board", "help" or "quit"
    if user_input == "board":
        draw_board()

    elif user_input == "help":
        print_instructions()

    elif user_input == "quit":
        raise KeyboardInterrupt

    return user_input

#Check if user input for chip placement is valid
def is_location(user_input):
    location_number = 0

    if user_input in valid_locations:
        return True
    
    # For user input beginning with u, d, l, r, c
    elif user_input[0] in location_syntax:
        try:
            location_number = int(user_input[1:])
        except ValueError:
            return False

        #syntax r is only valid for numbers between 1 and 33
        if user_input[0] == "r" and location_number in range(1, 34):
            return True
        #syntax c is only valid for R2 and R3 numbers
        elif user_input[0] == "c" and location_number in range(1, 37) and location_number % 3 != 1:
            return True
        #syntax u, d, l is valid as long as number is between 1 and 36
        elif user_input[0] in location_syntax[:3] and location_number in range(1, 37):
            return True
        else:
            return False

    # For numerical user input
    elif len(user_input) <= 2:
        try:
            location_number = int(user_input)
        except ValueError:
            return False
        
        if location_number in range(0, 37):
            return True
        else:
            return False

    else:
        return False

def test_is_location_HappyPath():
    assert is_location("U2") == False

def test_calculate_winnings_HappyPath():
    chip_placement = {"6":2}
    winnings = calculate_winnings(chip_placement)
    assert winnings[6] == 72

# Roulette wheel spin

def spin_wheel():
    print("Ready? Let's spin the wheel!")
    time.sleep(1)
    print("Spinning. . .")
    time.sleep(2)

    #Choose random integar between 0 and 36
    selected_number = random.randrange(0, 37)
    print(f"The silver ball has chosen! The selected number is {selected_number}!")
    time.sleep(2)
    return selected_number

# Returns a number list of the betted numbers given a location string
def location_to_number(location):
    betted_numbers = []

    if location == "1-12":
        betted_numbers = list(range(1, 13))

    elif location == "13-24":
        betted_numbers = list(range(13, 25))

    elif location == "25-36":
        betted_numbers = list(range(25, 37))

    elif location == "1-18":
        betted_numbers = list(range(1, 19))

    elif location == "19-36":
        betted_numbers = list(range(19, 37))

    elif location == "ODD":
        betted_numbers = list(range(1, 37, 2))

    elif location == "EVEN":
        betted_numbers = list(range(2, 37, 2))

    elif location == "R1":
        betted_numbers = list(range(1, 37, 3))

    elif location == "R2":
        betted_numbers = list(range(2, 37, 3))

    elif location == "R3":
        betted_numbers = list(range(3, 37, 3))

    elif location == "BLACK":
        betted_numbers = black_numbers

    elif location == "RED":
        betted_numbers = red_numbers

    elif location[0] == "u":
        number = int(location[1:])

        # u of numbers in the top row (R3) represents the entire column
        if number % 3 == 0:
            betted_numbers = [number, number - 1, number - 2]
        else:
            betted_numbers = [number, number + 1]

    elif location[0] == "d":
        number = int(location[1:])
        # d of numbers in the bottom row (R1) represents the entire column
        if number % 3 == 1:
            betted_numbers = [number, number + 1, number + 2]
        else:
            betted_numbers = [number, number - 1]

    elif location[0] == "l":
        number = int(location[1:])
        if number < 3:
            betted_numbers = [number, 0]
        else:
            betted_numbers = [number, number - 3]

    elif location[0] == "r":
        number = int(location[1:])
        betted_numbers = [number, number + 3]

    elif location[0] == "c":
        number = int(location[1:])
        if number <= 3:
            betted_numbers = [0, number, number - 1]
        else:
            betted_numbers = [number, number - 1, number - 3, number - 4]

    else:
        betted_numbers.append(int(location))

    return betted_numbers

# Calculate the payout amount for each number based on player's chip placement
def calculate_winnings(chip_placement):
    winnings = [0] * 37

    for location, num_chips in chip_placement.items():
        betted_numbers = location_to_number(location)
        for number in betted_numbers:
            winnings[number] += 36 * num_chips / len(betted_numbers)
        
    return winnings

#  Game play loop
def main_loop(chip_amount=100, num_spins=0):
    # Introduction and Board
    print("Welcome to a game of Roulette! Let's start with 100 chips. Enter 'done' to spin the wheel.")
    draw_board()
    print("Type the following at any time during the game:\nhelp - for instructions\nboard - to view board\nquit - to quit game")

    user_input = ""
    location = ""
    num_chips = 0

    try:
        while True:
            #Variables that refresh after each spin
            chip_placement = {}
        
            while user_input != "done":

                #Ask player the positions to place chips
                while user_input != "done":

                    user_input = get_input("Where would you like to place your chips? ")
                    if user_input == "done":
                        break

                    location = user_input

                    if is_location(location):
                        break
                    elif user_input in user_commands:
                        continue
                    else:
                        print("Error: Please enter a valid location on the board")
                        continue

                #Ask how many chips to add at that location
                while user_input != "done":
                    user_input = get_input(f"How many chips to place at {location}? ")

                    if user_input == "done":
                        break

                    try:
                        num_chips = int(user_input)
                        
                        #Check if there is enough chips to add
                        if num_chips > chip_amount:
                            print(f"Unfortunately you can't bet more than you have ({chip_amount} chips). Please try again")
                            continue

                        #Removing chips
                        elif num_chips < 0:
                            #Check if there are enough chips to remove
                            if location not in chip_placement:
                                print(f"You don't have chips to remove at {location}")
                                continue
                            elif -num_chips > chip_placement[location]:
                                print(f"You only have {chip_placement[location]} chips at {location}.")
                                continue
                            else:
                                chip_placement[location] += num_chips
                                chip_amount -= num_chips
                                break

                        # Adding chips
                        else:
                            if location in chip_placement:
                                chip_placement[location] += num_chips
                            else:
                                chip_placement[location] = num_chips
                            chip_amount -= num_chips
                            break

                    except ValueError:
                        print("Error: value provided is not numerical.")
                        continue
        
            # Spin the wheel
            selected_number = spin_wheel()
            num_spins += 1

            #Calculate winning amount
            winnings = calculate_winnings(chip_placement)
            amount_won = winnings[selected_number]

            #Update player chip stack and inform player of current game state
            if amount_won > 0:
                chip_amount += amount_won
                print(f"Congratulations! You won {amount_won} chips. You now have {chip_amount} chips in your stack.")

            elif chip_amount == 0:
                sys.exit(f"Game over! You have ran out of chips. You lasted {num_spins} spins. Rerun the application to play again.")

            else:
                print(f"I'm sure you will win on the next spin! You have {chip_amount} chips remaining.")

            user_input = ""
    
    # When player enters "quit" when prompted
    except KeyboardInterrupt:
        print(f"Thanks for playing! You finished with {chip_amount} chips in your stack and you lasted {num_spins} spins.")
    
main_loop()