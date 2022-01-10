# Chittle, Ben - FSE.py
# 21 June 2018
# Ben Chittle
# This program contains 2 playable games, Tic Tac Toe and Guess the Number,
# which can be chosen, played, and replayed by the user(s).


# For pacing the program.
from time import sleep
# For generating random numbers used in the Tic Tac Toe A.I. and the number in
# the Guess the Number game.
from random import randint
# For retrieving multiple arbitrary values from lists.
from operator import itemgetter as get


# Allows the user to choose a game. It returns a number corresponding to the
# game that should run.
def chooseGame():
    sentStart = 0   # Variable determining the start position of a sentence.
    while True:
    # Asks the player which game to play until a valid value is given.
        try:
            game = int(input("What game would you like to play?\n(1 - Tic Tac Toe ||"
                             " 2 - Guess the Number)\n"[sentStart:]))
            if game < 1 or game > 2:
                raise inputError
        except:
            sentStart = 34  # Sentence starts at "(1 - Tic Tac Toe...".
            continue
        return game


# Introduces the player to Tic Tac Toe and acquires the symbol they want to use,
# the number of players, and the 2nd player's symbol (if there are 2 players).
def introTTT_1():
    badChars = ['', ' ']   # List containing characters not to be chosen.
    sentStart = 0   # Variable determining the start position of a sentence.

    print ("Welcome to Tic Tac Toe!\n")
    sleep(1)
    print ("Your goal is to match 3 of your symbols in a row, column, or "
           "diagonal while\npreventing your opponent from doing the same.\n")
    sleep(1)

    while True:
    # Asks the user for the number of players until a valid value is given.
        try:
            players = int(input("Are you playing alone or with a friend? (1 or 2)\n"
                                [sentStart:]))
            if players < 1 or players > 2:
                raise inputError
        except:
            sentStart = 40 # Sentence starts at "(1 or 2)".
            continue
        if players == 1:
        # Player 1 cannot pick the computer's character if playing alone.
            badChars.append('O')
            badChars.append('o')

        sleep(0.5)
        # P1 chooses their symbol. It's added to "badChars".
        sym1 = input("\nP1: What letter would you like to use? (single character)\n")
        while len(sym1) > 1 or sym1 in badChars:    #Repeats until valid input.
            sym1 = input("P1: Try something else. (single character)\n")
        badChars.append(sym1.upper())
        badChars.append(sym1.lower())

        sleep(0.5)
        # P2 chooses their symbol.
        if players == 2:
            sym2 = input("\nP2: What letter would you like to use? (single character)\n")
            while len(sym2) > 1 or sym2 in badChars:    #Repeats until valid input.
                sym2 = input("P2: Try something else. (single character)\n")
        else:
            sym2 = 'O'
        # Answers are added to a list which is returned.
        info = [players, sym1, sym2]
        return info


# Draws the board with the appropriate symbols each time it is called using the
# indices list to represent each position.
def createBoard_1():
    print (title)
    print ("7    |8    |9")
    print (" ", board[7], " | ", board[8], " | ", board[9])
    print ("_____|_____|_____")
    print ("4    |5    |6")
    print (" ", board[4], " | ", board[5], " | ", board[6])
    print ("_____|_____|_____")
    print ("1    |2    |3")
    print (" ", board[1], " | ", board[2], " | ", board[3])
    print ("     |     |\n")


# Creates a copy of the list representing the board for the computer to test moves.
def copyBoard_1(Board):
    copy = []
    for space in Board:
    # Loops through each index in the list and appends it to the copy.
        copy.append(space)
    return copy


# Returns True if the specified space on the board is unoccupied (a blank space).
def isOccupied_1(Board, Move):
    return Board[Move] == ' '


# Acquires a player's move.
def getMove_1(Board, Move):
    sentStart = 0
    nums = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    while Move not in nums or isOccupied_1(Board, Move) == False:
    # Repeats until valid value given.
        try:
            Move = int(input(title[:2] + ": " + "Make your move. (1-9)\n"[sentStart:]))
        except:
            sentStart = 15 # Sentence starts at "(1-9)".
            continue
    return Move


# Acquires the computer's move.
def computerMove_1(Board, Move, sym1, sym2):
    # Contains the values of the corners from the list representing the board.
    corners = list(get(1, 3, 7, 9)(Board))
    # Contains the values of the middle sides, top, and bottom.
    sideTop = list(get(2, 4, 6, 8)(Board))
    while True:
        # Used for choosing a random value from one of the lists when there is
        # more than one option.
        ranNum = randint(0, 3)

        for space in range(0, 10):
        # Determines whether the computer can make the winning move.
            copy = copyBoard_1(Board)   # Creates a copy of the board.
            if copy[space] == ' ':
            # Makes each possible move. If it results in a win, it makes the
            # move.
                copy[space] = sym2
                if winner_1(copy, sym2):
                    return space

        for space in range(0, 10):
        # Determines whether the player can make the winning move.
            copy = copyBoard_1(Board)   # Creates a copy of the board.
            if copy[space] == ' ':
            # Makes each possible move using the player's symbol. If it results
            # in a win, it makes the move to block it.
                copy[space] = sym1
                if winner_1(copy, sym1):
                    return space

        if ' ' in corners:
        # If any of the corners are free, it will make a move on an open one.
            Move = corners[ranNum]  # Tries a random corner.
            if Move != ' ':   # Retry if occupied.
                continue
            else:
                Move = [1, 3, 7, 9][ranNum]  # Choose that space if free.

        elif Board[5] == ' ': # Moves in the center if free.
            Move = 5

        else:
            # If the middle top, sides, or bottom are free, it will make a move
            # on an open one.
            Move = sideTop[ranNum] # Tries a random position from list.
            if Move != ' ':   # Retry if occupied.
                continue
            else:
                Move = [2, 4, 6, 8][ranNum]  # Choose that space if free.
        break
    return Move


# Determines whether the most recent move should win.
def winner_1(Board, symbol):
    # Returns True if any of the following formations contain 3 of the same
    # symbols.
    # Top row.
    return ((Board[7] == symbol and Board[8] == symbol and Board[9] == symbol) or
    # Middle row.
    (Board[4] == symbol and Board[5] == symbol and Board[6] == symbol) or
    # Bottom row.
    (Board[1] == symbol and Board[2] == symbol and Board[3] == symbol) or
    # Left column.
    (Board[7] == symbol and Board[4] == symbol and Board[1] == symbol) or
    # Middle column.
    (Board[8] == symbol and Board[5] == symbol and Board[2] == symbol) or
    # Right column.
    (Board[9] == symbol and Board[6] == symbol and Board[3] == symbol) or
    # Backward diagonal (top left to bottom right).
    (Board[7] == symbol and Board[5] == symbol and Board[3] == symbol) or
    # Forward diagonal (bottom left to top right).
    (Board[9] == symbol and Board[5] == symbol and Board[1] == symbol))


# Determines whether there is a tie.
def tie_1(Board):
    # Returns True if there are no empty spaces left on the board.
    return ' ' not in Board[1:9]


# Introduces the user to the Guess the Number game and acquires their name.
def introGuessGame_2():
    name = input("What's your name?\n")
    sleep(1)
    print ("Welcome to Guess the Number!\n")
    sleep(1)
    print ("Your goal is to guess a random number from 1 to 20 in 6 guesses"
           " or less.")
    return name


# Acquires the player's guess.
def getGuess_2(guess):
    sentStart = 0 # Variable determining the start position of a sentence.
    sleep(0.5)
    print ("\n\nGuess %i out of 6" %guess) # Prints how many guess the user has.
    while True:
        # Asks the user to input a number until valid input is given.
        try:
            pick = int(input("P1: Pick a number from 1 to 20.\n"[sentStart:]))
            if pick < 1 or pick > 20:
                raise inputError
        except:
            sentStart = 23 # Sentence starts at "1 to 20".
            continue
        sleep(0.5)
        return pick


# Returns whether the player would like to play again.
def playAgain(subject):
    badAns = ('Y', 'y', 'N', 'n')
    ans = ''
    ans = input("\nWould you like to play %s? (y / n)\n" %subject)
    # Asks the user for input until valid input is given.
    while ans not in badAns:
        ans = input("y / n\n")
    return ans


##############################


while True:
    subject = "again"
    # This variable changes a sentence used in asking the player to play again
    # (allows the same sub-process to be used).
    game = chooseGame()     # The player chooses the game they'd like to play.
    gamePlayed = False      # Introduction to the game will be able to run.

    while game == 1:    # Runs if the user chooses Tic Tac Toe.
        if not gamePlayed:  # Runs the introduction on the first time through.
            info = introTTT_1()
            players = info[0]
            sym1 = info[1]
            sym2 = info[2]
            # Introduction won't run again until a new game is chosen.
            gamePlayed = True


        move = 0
        board = [" "] * 10 # The board is set up as a series of spaces.
        while True:
            title = "P1's turn." # The words at the top of the board.
            createBoard_1() # The current board is drawn.
            move = getMove_1(board, move) # Aquires the player's move.
            sleep(0.5)
            # The move is made on the board with Player 1's symbol.
            board[move] = sym1


            if winner_1(board, sym1):
            # If there is a winner, the board will be printed with the specified
            # title and the loop will break.
                title = "\nWINNER PLAYER 1!"
                createBoard_1()
                break
            elif tie_1(board):
            # If there is a tie, the board will be printed with the specified
            # title printed and the loop will break. There will only ever be a
            # tie on Player 1's turn.
                title = "\nTIE GAME!"
                createBoard_1()
                break


            if players == 2:
            # The program will get Player 2's turn in the same way as Player 1
            # if there are 2 players.
                title = "P2's turn."
                createBoard_1()
                move = getMove_1(board, move)
                sleep(0.5)
                board[move] = sym2
            else:
            # If there is only 1 player, the program will acquire the computer's
            # move similarly to Player 1.
                title = "Computer's Turn"
                createBoard_1()
                # The program will run an algorithm to acquire the computer's
                # move.
                move = computerMove_1(board, move, sym1, sym2)
                sleep(1)
                board[move] = sym2

            if winner_1(board, sym2):
            # If there is a winner, the board will be printed with the specified
            # title and the loop will break.
                if players == 2:
                    title = "WINNER PLAYER 2!"
                else:
                    title = "THE COMPUTER WINS!"
                createBoard_1()
                break

        ans = playAgain(subject) # Asks the player if they want to play again.
        if ans == 'y' or ans == 'Y':
            continue # Restarts at the beginning of the loop.
        else:
            # Jumps to asking the player if they want to play a different game.
            break



    while game == 2: # Runs if the player chooses the Number Guessing game.
        if not gamePlayed:  # Runs the introduction on the first time through.
            name = introGuessGame_2()
            # Introduction won't run again until a new game is chosen.
            gamePlayed = True

        lower = 1   # Constant variables are set for randint parameters.
        upper = 20
        ranNum = randint(lower, upper)
        # Generates a random integer within the parameters.

        while True:
            sleep(1)
            for guess in range(1,7):    # The player gets 6 chances.
                pick = getGuess_2(guess)
                if pick == ranNum:
                # If the player guesses the number, this runs and breaks the
                # loop.
                    sleep(0.5)
                    print ("Good job %s, you guessed my number!" %name)
                    break
                elif guess == 6:
                # If the player is out of guesses, this runs.
                    sleep(0.5)
                    print ("You ran out of guesses!\nMy number was %i.\nBetter"
                           " luck next time!" %ranNum)
                elif pick < ranNum:
                # If the player's guess is less than the number, this runs.
                    print ("\nGo higher.")
                else:
                # This runs if none of the others are true, meaning the guess is
                # higher than the number.
                    print ("\nGo lower.")
            break

        ans = playAgain(subject) # Asks the player if they want to play again.
        if ans == 'y' or ans == 'Y':
            continue # Restarts at the beginning of the loop.
        else:
            # Jumps to asking the player if they want to play a different game.
            break

    sleep(0.5)
    subject = "a different game"
    # Asks the player if they want to play a different game.
    ans = playAgain(subject)
    if ans == 'y' or ans == 'Y':
        # Restarts at the beginning of the loop, allowing the player to choose a
        # different game.
        continue
    else:
        break # Ends the program.


print("Thanks for playing!")
