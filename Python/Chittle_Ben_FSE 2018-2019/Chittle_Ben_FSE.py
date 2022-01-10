#-------------------------------------------------------------------------------
"""
Name:       Ben Chittle
StudentNo:  31601061
FileName:   Chittle_Ben_FSE.py
Date:       23 January 2019
Teacher:    Mr. Sarros
Purpose:    This is the main part of the program: it deals with the logic of the
            game of Nines and calls methods on the classes created in the
            other module to display information to the screen.
"""
#-------------------------------------------------------------------------------
import random, time, importlib, sys
import tkinter as tk
import GUI, config

################################################################################
##               INSTRUCTIONS CAN BE FOUND IN THE USER MANUAL                 ##
################################################################################

class Game:
    def __init__(self, isProgQuitMain, matchScores, isNewGame, isFullScreen, currentRound):
        """
        Initializes variables to begin the game.

        Arguments:
        isProgQuitMain -- a list containing a boolean used to determine if the program should be exitted and properly close
        matchScores -- a list containing integers for each player's score in the match
        isNewGame -- a boolean used to determine whether the program is running a new game and to initialize certain variables
        isFullScreen -- a boolean used to keep track of whether the window was fullscreen when starting a new round
        currentRound -- an integer used to keep track of the current round
        """

        # Initializes the main window, giving it a title, preventing it from
        # being resizable, and setting its background.
        self.root = tk.Tk()
        self.root.title("Nines")
        self.root.resizable(width=False, height=False)
        self.root.configure(background='black')

        # tkiner BooleanVar used to determine when the player has pressed "Start" on the
        # start menu, allowing the game to begin.
        self.isGameStart = tk.BooleanVar(self.root)
        self.isGameStart.set(tk.FALSE)

        # tkinter BooleanVar used to determine when GUI window has been exitted and
        # properly close.
        self.isProgQuitGUI = tk.BooleanVar(self.root)
        self.isProgQuitGUI.set(tk.FALSE)

        self.isProgQuitMain = isProgQuitMain
        self.isNewGame = isNewGame

        # tkinter BooleanVar used to determine when the player has clicked a
        # card on the GUI. It is created here because it must be updated when
        # the program closes to end any possible wait_var loops which would
        # prevent the program from closing properly.
        self.isCardPicked = tk.BooleanVar(self.root)
        self.isCardPicked.set(tk.FALSE)

        self.isFullScreen = isFullScreen

        # Applies the given fullscreen setting.
        self.root.attributes("-fullscreen", self.isFullScreen)

        # Binds a function to properly close the window to the event broadcasted
        # when the window is closed via the window manager (e.g. the 'X' button
        # on Windows).
        self.root.protocol("WM_DELETE_WINDOW", self.quitProg)

        # If it's a new game, opens the start menu before starting the game.
        if self.isNewGame:
            # Opens the start menu and deletes it when the player either exits
            # or begins the game
            self.startMenu = GUI.Start_Window(self, self.root, self.isGameStart, self.isProgQuitGUI)
            del self.startMenu

            # If the start menu was closed, ends the program.
            if self.isProgQuitGUI.get():
                sys.exit()

            # Removes all of the widgets from the start menu to allow it to be
            # used as the game window.
            for oldWidget in self.root.slaves():
                oldWidget.destroy()

        # Refreshes the settings in case they were modified in the start menu
        # and aquires the dictionary containing all of the settings from the
        # module.
        importlib.reload(config)
        settings = config.settingsDict

        # List constants containing the characters which represent each suit and
        # card value (other than the Joker).
        self.SUITS = ['H', 'S', 'D', 'C']
        self.VALUES = list(map(str, range(1, 9))) + ['K', 'Q', 'J']

        # Aquires settings for the number of players and the number of decks.
        self.numOfPlayers = int(settings["numOfPlayers"])
        self.numOfDecks = int(settings["numOfDecks"])

        self.currentRound = currentRound

        # Creates a list which will contain each player's score for the current
        # game.
        self.gameScores = [0] * self.numOfPlayers

        # Initializes the match scores list in the case of a new game.
        self.matchScores = matchScores
        if self.isNewGame:
            for i in range(self.numOfPlayers):
                self.matchScores.append(0)

        # Integer variable used to count down the number of turns when a player
        # has gone out.
        self.finalTurnCounter = self.numOfPlayers

        # Determines which resolution type was chosen. If it was "auto", sets
        # a variable to "auto". If a default resolution was chosen, converts it
        # to a tuple containing the width and the height.
        resolutionSetting = settings["resolution"]
        if resolutionSetting.strip() == "auto":
            self.resolution = "auto"
        else:
            self.resolution = tuple(map(int, settings["resolution"].split('x')))

        # Creates a list of strings containing card values to represent the
        # deck's data.
        self.drawPile = self.createDrawPile()

        # Creates the discard pile as an empty list.
        self.discardPile = list()

        # Calls a function to shuffle the deck.
        self.shuffleDeck()

        # Creates a dictionary containing each player's hand. Each key is an
        # integer, each value is a list of strings containing card values.
        self.playerHandsDict = self.createHands()

        # Creates an instance of the "Game_Window" class from the GUI module
        # to display the game graphically.
        self.app = GUI.Game_Window(self.root, self.SUITS, self.VALUES, self.numOfPlayers, self.resolution, self.playerHandsDict, self.matchScores, self.currentRound, self.isCardPicked)

        # Creates the menu bar at the of the window.
        self.menubar = tk.Menu(self.root)
        self.menubar.add_command(label="Quit", command=self.quitProg)
        self.menubar.add_separator()
        self.menubar.add_command(label="Toggle Fullscreen", command=self.app.toggleFullscreen)
        self.menubar.add_separator()
        self.menubar.add_command(label="New Game", state="disabled", command=self.newGame)
        self.menubar.add_separator()
        self.menubar.add_command(label="New Round", state="disabled", command=self.newRound)
        self.root.config(menu=self.menubar)

        # Draws the first card to be used as the discard pile.
        self.discardPile.append(self.drawPile.pop() + 'u')

        # Plays the setup animation in the GUI.
        self.app.setupAnim(self.discardPile[0][:-1])


    def createDrawPile(self):
        """Returns a list of strings containing card values."""

        # If there aren't enough decks for the number of players, increases
        # the number of decks to the minimum.
        if self.numOfPlayers >= 5 and self.numOfDecks < 2:
            self.numOfDecks = 2

        drawPile = []

        # Creates however many decks of cards were specified. Iterates over the
        # two lists containing the suits and values to create a card of each
        # value in each suit.
        for deck in range(self.numOfDecks):
            for suit in self.SUITS:
                for value in self.VALUES:
                    drawPile.append("{}{}".format(suit, value))

        # Adds 2 jokers for each deck.
        drawPile += ["_O"] * (2 * self.numOfDecks)

        return drawPile


    def shuffleDeck(self):
        """Places all of the discard pile cards into the draw pile and randomizes their order."""

        self.drawPile += [self.discardPile.pop()[:2] for card in range(len(self.discardPile))]
        random.shuffle(self.drawPile)


    def createHands(self):
        """Returns a dictionary with integer keys corresponding to the hand's index and values that are lists of strings containing the card values in that player's hand."""

        playerHandsDict = {}

        # For each player, creates a hand of 9 cards by taking them from the
        # draw pile.
        for player in range(self.numOfPlayers):
            playerHandsDict[player] = [self.drawPile.pop(0) + 'd' for card in range(9)]

        return playerHandsDict


    def drawCard(self, whereDrawn):
        """
        Returns a card value from either the draw or discard pile depending on the player's choice.

        Arguments:
        whereDrawn -- a string describing from which pile the player wants to draw a card
        """

        # If the player chose to draw a card from the discard pile, returns the
        # top discard pile card value.
        if whereDrawn == "discardPile" and len(self.discardPile) > 0:
            cardValue = self.discardPile.pop()
            cardValue = cardValue.replace('d', 'u')
            return cardValue

        # If the player chose to draw a card from the draw pile, returns the top
        # draw pile card value.
        elif whereDrawn == "drawPile":
            # Checks to see if the draw pile is empty to shuffle cards back into
            # it.
            if len(self.drawPile) < 1:
                self.shuffleDeck()
            cardValue = self.drawPile.pop(0) + 'u'
            self.app.drawNewCard(cardValue)
            return cardValue

        else:
            raise NameError("whereDrawn has unrecognized value or the discard pile is empty.")


    def replaceCard(self, whereDrawn, handIndex, oldCardIndex, newCardValue, cardAction):
        """
        Replaces a given card in the player's hand with a given drawn card.

        Arguments:
        whereDrawn -- a string describing from which pile the player wants to draw a card
        handIndex -- an integer containing a hand index
        oldCardIndex -- the index of the card being replaced in the player's hand
        newCardValue -- the suit and value of the drawn card
        cardAction -- a string describing what action the player wants to do with the drawn card
        """

        # Performs the animation for the swap.
        self.app.replaceAndDiscardAnim(whereDrawn, float(handIndex), oldCardIndex, newCardValue)

        # Reflects the swap in the player's hand and the discard pile.
        self.discardPile.append(self.playerHandsDict[handIndex][oldCardIndex])
        self.playerHandsDict[handIndex][oldCardIndex] = newCardValue


    def tryRemoveColumn(self, handIndex):
        """
        Checks to see if a sweep can be made in a given hand and performs it if possible.

        Arguments:
        handIndex -- an integer containing a card index
        """

        # Gets the list of card values for the given hand.
        cardsInHand = self.playerHandsDict[handIndex]

        # Checks each column to see if each card's value is the same and is face
        # up.
        for column in range(3):
            if cardsInHand[column] is not None:
                topCardIndex = column
                midCardIndex = column + 3
                bottomCardIndex = column + 6

                # If there are 3 cards of the same value in a column that are
                # face up, sets there values to None to eliminate their score
                # and displays the sweep animation in the GUI.
                if cardsInHand[topCardIndex][1:] == cardsInHand[midCardIndex][1:] == cardsInHand[bottomCardIndex][1:] == cardsInHand[topCardIndex][1:-1] + 'u':
                    cardsInHand[topCardIndex] = cardsInHand[midCardIndex] = cardsInHand[bottomCardIndex] = None

                    self.app.sweepColumnAnim(float(handIndex), [topCardIndex, midCardIndex, bottomCardIndex])


    def firstTurn(self):
        """Allows each player to flip over their first two cards for their first turn."""

        # For each player:
        for turn in range(self.numOfPlayers):
            cardsChosen = list()

            # Lets the player choose 1 card at a time via the GUI and saves
            # its index before flipping the card in the GUI.
            for choice in range(2):
                self.app.highlightHand(float(turn))
                cardsChosen.append(self.app.chooseCardFlip(float(turn)))
                self.app.flipCard("{}{}".format(float(turn), cardsChosen[choice]))

            # Reflects the flip in the player's card data.
            for cardPos in cardsChosen:
               self.playerHandsDict[turn][cardPos] = self.playerHandsDict[turn][cardPos].replace('d', 'u')

            # Updates each player's score.
            self.determineScores()


    def isThisPlayerOut(self, cardsInHand):
        """
        Returns False if the player has any face down cards, True otherwise.

        Arguments:
        cardsInHand -- a list of strings containing the card values for a hand
        """

        # Checks each card to see if it is not swept and face down. If there are
        # face down cards, returns False. If all cards are facing up, returns
        # True
        for cardValue in cardsInHand:
            if cardValue is not None:
                if cardValue[-1] == 'd':
                    return False
        return True


    def turn(self, handIndex):
        """
        Organizes functions and logic to allow a given player to take their turn.

        Arguments:
        handIndex -- an integer containing a hand index
        """

        # Aquires a list of all of the card values in the current hand.
        cardsInHand = self.playerHandsDict[handIndex]

        # Highlights the hand and scoreboard name on the GUI.
        self.app.highlightHand(float(handIndex))

        # Allows the player to decide from which pile they would like to draw
        # using the GUI.
        whereDrawn = self.app.chooseCardFlip("SOURCES")

        # Aquires a card's value from either the draw or discard pile depending
        # on the player's choice.
        newCard = self.drawCard(whereDrawn)

        # Allows the player to decide what to do with the card they have drawn
        # using the GUI.
        cardAction = self.app.chooseCardAction(float(handIndex), whereDrawn)

        # If the player chose to replace a card in their hand, performs the
        # "replaceCard" fucntion and checks to see if any sweeps can be made.
        if cardAction[0] == "replace":
            self.replaceCard(whereDrawn, handIndex, cardAction[1], newCard, cardAction[0])
            self.tryRemoveColumn(handIndex)

        # If the player chose to discard the drawn card, displays the discard
        # animation on the GUI and adds the card value to the discard pile data.
        elif cardAction == "discard":
            self.app.discardAnim(newCard)
            self.discardPile.append(newCard)

        else:
            raise ValueError("'cardAction' has unrecognized value: {}.".format(cardAction))

        # Updates each player's score.
        self.determineScores()


    def determineScores(self):
        """Calculates each player's score and refreshes the scoreboard on the GUI."""

        # Flips all cards when the game has ended.
        if self.finalTurnCounter == 0:
            self.flipAll()

        # Resets the score list to be recalculated.
        self.gameScores = [0] * self.numOfPlayers

        # For each player:
        for handIndex in self.playerHandsDict:
            # For each card in that hand, adds the card's value, if it hasn't
            # been swept, to that player's score.
            for cardIndex, card in enumerate(self.playerHandsDict[handIndex]):
                # If the card hasn't been swept:
                if card is not None:
                    # Looks for any possible sweeps with all of the cards now
                    # flipped.
                    self.tryRemoveColumn(handIndex)

                    # Checks to make sure the card hasn't been swept after the
                    # previous "tryRemoveColumn" function call.
                    if self.playerHandsDict[handIndex][cardIndex] is not None:

                        # If the card is face up:
                        if card[-1] == 'u':
                            value = card[1:-1]

                            # Adds the card's value directly if it's a number
                            # card.
                            if value.isnumeric():
                                self.gameScores[handIndex] += int(value)

                            # Adds 10 points if the card is a queen or jack.
                            elif value == 'Q' or value == 'J':
                                self.gameScores[handIndex] += 10

                            # Subtracts 2 points if the card is a joker.
                            elif value == 'O':
                                self.gameScores[handIndex] -= 2

                            elif value != 'K':
                                raise ValueError("'value' has unrecognized value: {}.".format(value))

        # Applies the new scores to the GUI.
        self.app.showScores(self.gameScores)


    def flipAll(self):
        """Flips all cards on the board to be face up."""

        # For each hand:
        for handIndex in self.playerHandsDict:

            # For each card in that hand, if the card hasn't been swept and it's
            # face down, flips the card and applies the change both on the GUI
            # and in the player's hand data.
            for cardIndex, card in enumerate(self.playerHandsDict[handIndex]):
                if card is not None:
                    if card[-1] == 'd':
                        self.app.flipCard("{:.1f}{}".format(handIndex, cardIndex))
                        self.playerHandsDict[handIndex][cardIndex] = card.replace('d', 'u')


    def playGame(self):
        """Organizes functions and logic to create the playable game."""

        # Initiates the first turn where each player can flip 2 of their cards.
        self.firstTurn()

        self.root.update()

        # Booleans used to mark when the round should end.
        isLastRound = False
        isPlaying = True

        # Iterates over each player, allowing them to take their turn while
        # every player has at least one face down card. When a player no longer
        # has any face down cards, "finalTurnCounter" counts down, allowing each
        # subsequent player 1 last turn.
        while isPlaying:
            for player in range(self.numOfPlayers):

                # If the last turn hasn't passed, the game plays out normally.
                if self.finalTurnCounter > 0:
                    self.turn(player)

                # When the last turn has passed, breaks the game loop.
                else:
                    isPlaying = False
                    break

                # Determines when the turn counter should begin.
                isLastRound = isLastRound or self.isThisPlayerOut(self.playerHandsDict[player])
                if isLastRound:
                    self.finalTurnCounter -= 1

        # Updates each player's score.
        self.determineScores()

        # Determines each player's final score and saves it to carry over into
        # the next round.
        for player, gameScore in enumerate(self.gameScores):
            self.matchScores[player] += gameScore

        self.root.update()

        time.sleep(2)

        # Displays the dialogue box containing the outcome of the game.
        self.app.showGameOutcome(self.getGameOutcome())

        # Enables the "New Game" and "New Round" buttons on the menu bar.
        self.menubar.entryconfig("New Game", state=tk.NORMAL)
        self.menubar.entryconfig("New Round", state=tk.NORMAL)

        # Temporary mainloop until the user either starts a new round / game or
        # closes the window.
        self.root.waitvar(self.isProgQuitGUI)


    def getGameOutcome(self):
        """Returns a string containing dialogue to display the round and match winners."""

        # Finds the lowest game score and determines whether there were more
        # than one which would signify a tie.
        lowRoundScore = min(self.gameScores)
        numOfLowRoundScores = self.gameScores.count(lowRoundScore)

        # If there was a tie, "roundWinner" will be assigned a string containing
        # dialogue about the top players.
        if numOfLowRoundScores > 1:
            roundWinners = ["Player {}".format(player) for player, score in enumerate(self.gameScores) if score == lowRoundScore]
            roundWinners.insert(numOfLowRoundScores - 1, "and")

            roundDialogue = "There was a {} way tie between {} this round!".format(numOfLowRoundScores, ', '.join(roundWinners))
            if numOfLowRoundScores == 2:
                roundDialogue = roundDialogue.replace(", and,", " and")
            else:
                roundDialogue = roundDialogue.replace("and,", "and")

        # If there was a only one winner, "roundWinner" will be assigned a
        # string containing dialogue about the winner.
        else:
            roundWinners = "Player {}".format(self.gameScores.index(lowRoundScore))
            roundDialogue = "{} wins this round!".format(roundWinners)

        # Finds the lowest match score and determines whether there were more
        # than one which would signify a tie.
        lowMatchScore = min(self.matchScores)
        numOfLowMatchScores = self.matchScores.count(lowMatchScore)

        # If there was a tie, "matchWinner" will be assigned a string containing
        # dialogue about the top players.
        if numOfLowMatchScores > 1:
            matchWinners = ["Player {}".format(player) for player, score in enumerate(self.matchScores) if score == lowMatchScore]
            matchWinners.insert(numOfLowMatchScores - 1, "and")

            matchDialogue = "{} are tied for first place overall!".format(', '.join(matchWinners))
            if numOfLowMatchScores == 2:
                matchDialogue = matchDialogue.replace(", and,", " and")
            else:
                matchDialogue = matchDialogue.replace("and,", "and")

        # If there was a only one winner, "matchWinner" will be assigned a
        # string containing dialogue about the winner.
        else:
            matchWinners = "Player {}".format(self.matchScores.index(lowMatchScore))
            matchDialogue = "{} has the lead overall!".format(matchWinners)

        return roundDialogue + "\n\n" + matchDialogue


    def newGame(self):
        """Sets variables that will close the current game window and begin a new game."""
        self.isProgQuitGUI.set(tk.TRUE)
        self.isNewGame = True
        self.root.destroy()


    def newRound(self):
        """Sets variables that will close the current game window and begin a new round."""
        self.isProgQuitGUI.set(tk.TRUE)
        self.isNewGame = False
        self.isFullScreen = self.root.attributes("-fullscreen")
        self.root.destroy()


    def quitProg(self):
        """Modifies variables to allow the program to exit properly."""
        self.isGameStart.set(tk.FALSE)
        self.isProgQuitGUI.set(tk.TRUE)
        self.isCardPicked.set(tk.FALSE)
        self.isProgQuitMain[0] = True
        self.root.destroy()
        sys.exit()


def main(isProgQuitMain, isNewGame):
    """
    Initiates and runs the program.

    Arguments:
    isProgQuitMain -- a list containing a boolean used to determine if the program should be exitted and properly close
    isNewGame -- a boolean used to determine whether the program is running a new game and to initialize certain variables
    """

    # While the program is supposed to be running, initializes variables for
    # new games and calls the "playGame" function on a "Game" object to begin
    # the game. Aquires scores and information about what the user wants to
    # do next when a round ends.
    while not isProgQuitMain[0]:
        if isNewGame:
            matchScores = list()
            isFullScreen = False
            currentRound = 1

        game = Game(isProgQuitMain, matchScores, isNewGame, isFullScreen, currentRound)
        game.playGame()

        matchScores = game.matchScores
        isNewGame = game.isNewGame
        isFullScreen = game.isFullScreen
        currentRound += 1


if __name__ == "__main__":
    isProgQuitMain = [False]

    # Catches any tk.TclError errors that are thrown. If the program is
    # supposed to be exitting (according to "isProgQuitMain"), the errors won't
    # be displayed; however, if one of these errors are thrown while the program
    # is supposed to be running, it will raise another error.
    #
    # ** This was done to hide errors that kept being thrown when the main
    #    window was destroyed on purpose, as I couldn't find another way around
    #    them, probably due to my slightly unorthodox use of moving items and
    #    wait_var. It only hides errors that have no impact on the program, as
    #    would be closing anyways.
    try:
        main(isProgQuitMain, True)
    except tk.TclError:
        if not isProgQuitMain[0]:
            raise tk.TclError("Tk error raised with window still open.")
        sys.exit()