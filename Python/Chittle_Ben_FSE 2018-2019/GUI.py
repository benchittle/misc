#-------------------------------------------------------------------------------
"""
Name:       Ben Chittle
StudentNo:  31601061
FileName:   Chittle_Ben_FSE.py
Date:       23 January 2019
Teacher:    Mr. Sarros
Purpose:    This part of the program contains the algorithms for displaying
            the cards and other output to the screen that are used in the
            main module.
"""
#-------------------------------------------------------------------------------
import random, importlib
from tkinter import *
import config


class Start_Window:
    def __init__(self, game, root, isGameStart, isProgQuitGUI):
        """
        Initializes the master window to create a start menu.

        Configures some of the window settings (resolution, background) and adds
        "Start", "Settings", and "Quit" buttons.

        Arguments:
        game -- a "Game" object containing a quit function
        root -- the master window
        isGameStart -- a tkinter BooleanVar describing whether or not the game should start
        isProgQuitGUI -- a tkinter BooleanVar describing whether or not the program has been quit and the GUI be destroyed
        """

        self.root = root

        self.isGameStart = isGameStart
        self.isProgQuitGUI = isProgQuitGUI

        # Determines the width and height of the current screen.
        screenWidth = self.root.winfo_screenwidth()
        screenHeight = self.root.winfo_screenheight()

        # Determines what width and height the window itself should have based
        # on the size of the screen.
        windowWidth = screenWidth // 10
        windowHeight = screenHeight // 5

        # Sets the size and position of the window.
        self.root.geometry("{}x{}+{}+{}".format(windowWidth, windowHeight, screenWidth // 2 - windowWidth, screenHeight // 2 - windowHeight))

        # Creates and places a label containing an image of a face down card to
        # use as a background picture.
        self.backgroundImage = PhotoImage(file=r"other_1080\down.png")#.zoom(2, 2)
        self.background = Label(self.root, image=self.backgroundImage, bg="Black")
        self.background.place(relx=0.1, rely=0.2, relwidth=0.8, relheight=0.8)

        # Creates and packs a label containing a title for the program
        # ("NINES").
        self.title = Label(root, text="NINES", font="TkTextFont 30", fg="White", bg="Black")
        self.title.pack(side=TOP)

        # Creates and packs a button bound to the "quitProg" function (from the
        # "Game" class) to exit the program.
        self.quitButton = Button(root, text="Quit", command=game.quitProg)
        self.quitButton.pack(side=BOTTOM)

        # Creates and packs a button bound to the "openSettings" function which
        # opens a window to edit the settings for the game.
        self.settingButton = Button(root, text="Settings", command=self.openSettings)
        self.settingButton.pack(side=BOTTOM)

        # Creates and packs a button bound to a function which begins the game.
        self.startButton = Button(root, text="Start", command=lambda: self.isGameStart.set(TRUE))
        self.startButton.pack(side=BOTTOM)

        # Waits until the the game has been triggered to start.
        self.root.wait_variable(self.isGameStart)


    def openSettings(self):
        """Opens a new window containing options to edit the game's settings using a "Settings_Window" object."""

        window = Toplevel(self.root)
        window.resizable(width=False, height=False)

        # Sets the title of the window and sets the program to only responds to
        # input in the new window.
        window.title("Settings")
        window.grab_set()
        self.settingsScreen = Settings_Window(window)




class Settings_Window:
    def __init__(self, window):
        """
        Configures a tkinter Toplevel window to create a settings menu.

        Adds dropdown menus to allow the player to change some of the game's
        settings, along with buttons to accept or cancel their changes.

        Arguments:
        window -- a tkinter Toplevel object
        """

        self.window = window

        # Used to allow the program to know when the user closes the window.
        self.isSettingsQuit = BooleanVar(window)
        self.isSettingsQuit.set(FALSE)

        # Binds a function to properly close the window to the event broadcasted
        # when the window is closed via the window manager (e.g. the 'X' button
        # on Windows).
        self.window.protocol("WM_DELETE_WINDOW", self.closeWindow)

        # Creates and grids a title label along with the "accept" and "cancel"
        # buttons.
        Label(self.window, text="Settings", font="TkTextFont 16").grid(row=0, column=0, columnspan=7)
        Button(window, text="Accept", command=self.saveSettings).grid(row=3, column=6, sticky=E, columnspan=2)
        Button(window, text="Cancel", command=self.closeWindow).grid(row=3, column=6, sticky=W, columnspan=2)

        # Refreshes the settings module in case the user has changed something
        # and wants to reopen the settings window to change something else
        # again.
        importlib.reload(config)

        # Gets the settings dictionary from the config module.
        currentSettings = config.settingsDict

        # Creates and grids the first dropdown menu for changing the number of
        # players. Assigns its current value to a tkinter StringVar.
        self.setting1Val = StringVar(self.window)
        self.setting1Val.set(currentSettings["numOfPlayers"])
        OptionMenu(self.window, self.setting1Val, '2', '3', '4', '5', '6').grid(row=2, column=2)
        Label(self.window, text="Number of players:").grid(row=2, column=1)

        # Creates and grids the second dropdown menu for changing the number of
        # decks. Assigns its current value to a tkinter StringVar.
        self.setting2Val = StringVar(self.window)
        self.setting2Val.set(currentSettings["numOfDecks"])
        OptionMenu(self.window, self.setting2Val, '1', '2', '3', '4').grid(row=2, column=4)
        Label(self.window, text="Number of decks:").grid(row=2, column=3)

        # Creates and grids the third dropdown menu for changing the resolution
        # Assigns its current value to a tkinter StringVar.
        self.setting3Val = StringVar(self.window)
        self.setting3Val.set(currentSettings["resolution"])
        OptionMenu(self.window, self.setting3Val, "1920x1080", "1280x1024", "     auto     ").grid(row=2, column=6)  ##
        Label(self.window, text="Resolution:").grid(row=2, column=5)

        Label(self.window, text="** See user manual for instructions.").grid(row=3, column=0, columnspan=3, sticky=W)

        # A temporary mainloop that runs until the user has exitted the window.
        self.window.wait_variable(self.isSettingsQuit)


    def closeWindow(self):
        """Properly closes the settings window."""
        self.isSettingsQuit.set(TRUE)
        self.window.destroy()


    def saveSettings(self):
        """Saves the settings with their current values and closes the window."""

        # Recreates the settings dictionary with the new settings.
        newSettings = {"numOfPlayers" : self.setting1Val.get(),
                       "numOfDecks" : self.setting2Val.get(),
                       "resolution" : self.setting3Val.get()}

        # Writes the new settings to the config file.
        with open("config.py", "w") as settingsFile:
            settingsFile.write("settingsDict={}".format(newSettings))

        self.closeWindow()




class Game_Window:

    def __init__(self, root, SUITS, VALUES, numOfPlayers, resolution, playerHandsDict, matchScores, currentRound, isCardPicked):
        """
        Initializes variables for settings and data storage and begins the animation in the GUI.

        Creates any of the class-wide variables that will be used in the program
        and opens a window with settings based on previous user input.

        Arguments:
        root -- the master GUI window
        SUITS -- a list constant containing the 4 card suits in shortform as strings
        VALUES -- a list constant containing the 14 different card values (ace to joker)
        numOfPlayers -- an integer representing the number of players
        resolution -- a string representing the resolution of the window
        playerHandsDict -- a dictionary containing a list of strings for each card in each player's hand
        matchScores -- a list of integers representing each player's score in the match
        currentRound -- an integer representing the current round
        isCardPicked -- a tkinter BooleanVar describing whether or not a card has been chosen by the player


        Tags on canvas items:
        [0] <"itemType">
            Identifies the type of item.
                "CARD" -- found on any item used as a card that isn't in the draw or
                          discard pile
                "SOURCES" -- found on any item used a source of cards (the draw or
                             discard pile)
                "TABLE" -- found on the any item used as a background as part of the
                           table
                "HIGHLIGHT" -- found on the rectangle that surrounds a player's hand,
                               highlighting their turn

        [1] <"cardValue">
            On a "CARD" or "SOURCES" type, identifies the suit and value.
                "{card suit}{card face value}{face up or face down}"
                E.g. "D1u" = ace of diamonds, face up

        [2] <"handIndex">
            On a "CARD" type, identifies which hand the card is in.
                {hand index} -- a float from 0 to one less than the number of players

            On a "SOURCES" type, identifies which pile the item is a part of.
                "discardPile" -- the discard pile
                "drawPile" -- the draw pile

        [3] <"cardID">
            On a "CARD" type, identifies the hand and position within the hand that the
            card is in.
                "{hand index}{card index}"
                    card index -- a card's position in a hand, where 0 is top left,
                                  2 is top right, 3 is middle left, etc.: <"cardIndex">

                E.g. 1.03 = the middle-left card in the second hand (Player 1)
                            1.0 is the hand, 3 is the card index.

            On a "SOURCES" type as part of "discardPile", identifies the position of the
            card in the discard pile stack.
                "discardPile{position}"
                E.g. "discardPile0" is the bottom card in the stack

            On a "SOURCES" type as part of "drawPile", identifies the position of the
            card in the draw pile stack.
                "drawPile{position}"
                E.g. "drawPile0" is the top card in the draw pile

                * This isn't useful in the current state of the game, as the draw pile
                  is a single seperate image, but I added it to make it easier to add
                  the draw pile as an actual stack of cards, like the discard pile, if I
                  wanted to in the future.
        """

        self.root = root

        # If the resolution was set as "auto" by the user, the program will
        # find the resolution of the monitor automatically and use it to
        # determine how the images used in the program should be scaled.
        if resolution == "auto":
            self.screenWidth = self.root.winfo_screenwidth()
            self.screenHeight = self.root.winfo_screenheight()

            # The card width and height is determined based off of the ratio
            # of card width to screen width that is used in a 1920x1080
            # resolution, and the base width of the real images is then used
            # to determine a scale factor for how much each image should be
            # zoomed to fit the screen nicely.
            self.BASE_CARD_WIDTH = 720
            self.cardWidth = 85 * self.screenWidth // 1920 + self.screenWidth // 380
            self.cardHeight = round(self.cardWidth * (130/85))
            self.scaleFactor = round(self.BASE_CARD_WIDTH / self.cardWidth)

            self.IMAGES_FOLDER = "playingCards_base\\"
            self.OTHERS_FOLDER = "other_base\\"

        # If the resolution was set to either of the default resolutions,
        # the program uses predetermined settings for the card width and height.
        # A scale factor of 1 is used (meaning no change), as the cards have
        # been scaled manually for the default resolutions to give better
        # quality images.
        else:
            self.screenWidth = resolution[0]
            self.screenHeight = resolution[1]

            if resolution == (1920, 1080):
                self.cardWidth = 85 + 5
                self.cardHeight = 135
            elif resolution == (1280, 1024):
                self.cardWidth = 56 + 5
                self.cardHeight = 86 + 5

            self.IMAGES_FOLDER = "playingCards_{}\\".format(resolution[1])
            self.OTHERS_FOLDER = "other_{}\\".format(resolution[1])

            self.scaleFactor = 1

        # Applies the screen resolution.
        self.root.geometry("{}x{}+{}+{}".format(self.screenWidth, self.screenHeight, 0, 0))
        self.root.update()

        # Sets some of the object's variables to those identified in the
        # docstring.
        self.SUITS = SUITS
        self.VALUES = VALUES
        self.numOfPlayers = numOfPlayers
        self.playerHandsDict = playerHandsDict
        self.matchScores = matchScores
        self.currentRound = currentRound

        # An integer constant that identifies the maximum number of discarded
        # cards that will appear in the discard pile before one is deleted.
        self.MAX_DISCARDS = 6

        # Variables representing various x / y values of the the screen that
        # are used to help simplify how the card positions are determined, along
        # with various other coordinates.
        self.halfX = self.screenWidth / 2
        self.halfY = self.screenHeight / 2
        self.thirdX = self.screenWidth / 3
        self.quarterX = self.screenWidth / 4
        self.fifthX = self.screenWidth / 5
        self.topOfTable = self.cardHeight - self.cardHeight / 5
        self.bottomOfTable = self.screenHeight - 3 * self.cardHeight + self.cardHeight / 5
        self.discardPileX = self.halfX + self.cardWidth
        self.discardPileY = self.halfY

        # A list of integers that will be used to keep track of which position,
        # relative to a given hand, a card is in.
        # E.g. position or index 0 is the top left card in a hand, index 3 is
        # the top right, etc.
        self.POSITIONS = list(range(9))

        # Variables used in more than one function that help coordinate them.
        # E.g. the program will let the user pick a card until a card is picked,
        # but because this requires multiple functions, each has to know when
        # said card has been chosen, so these variables are class wide.
        self.isCardPicked = isCardPicked
        self.choice = None
        self.oldCardIndexID = None

        # Four dictionaries containing all of the images after they have been
        # processed. Each key is a string representing the card's value
        # followed by the value of tkinter PhotoImage object containing the
        # image.
        self.cardImages, self.otherImages, self.activeCardImages, self.activeOtherImages = self._loadImages()

        # Creates and places the canvas object used for most of the animations
        # to the main window.
        self.canvas = Canvas(self.root, width=self.screenWidth, height=self.screenHeight, highlightthickness=0, bg="Black")
        self.canvas.place(anchor='c', relx=0.5, rely=0.5)


        # Creates a Frame widget that will contain all of the scoring
        # information.
        self.scoreFrame = Frame(self.root, bg="Black", relief=RAISED, highlightbackground="Grey", highlightthickness=5)

        # Creates and grids a Label widget that will show the current round at
        # the top of the frame.
        Label(self.scoreFrame, text="Round {}".format(self.currentRound), font="_, 20", bg="Black", fg="Light Blue").grid(row=0, column=0, columnspan=3)

        # Creates and grids 2 more Label widgets identifying the columns for
        # the game and match scores below the round counter.
        Label(self.scoreFrame, text="  Game  ", font="_, 18", bg="Black", fg="White").grid(row=1, column=1)
        Label(self.scoreFrame, text="  Match  ", font="_, 18", bg="Black", fg="White").grid(row=1, column=2)

        # 3 lists used to contain the references to each of the 3 widgets that
        # display a player's score.
        # "playerLabels" refers to each Label displaying the player's name.
        # "gameScoreLabels" refers to each Label displaying the player's score
        #                   for the current game.
        # "matchScoreLabels" refers to each Label displaying the player's score
        #                    for the match.
        self.playerLabels = list()
        self.gameScoreLabels = list()
        self.matchScoreLabels = list()

        # Creates Label widgets for each player's name, game score, and match
        # score and appends their references to the respective lists seen above.
        for player, score in enumerate(self.matchScores):
            # Creates the name Label.
            self.playerLabels.append(Label(self.scoreFrame, text="Player {}:".format(player), font="_, 16", bg="Black", fg="White"))
            self.playerLabels[player].grid(row=player + 2, column=0, ipadx=10)

            # Creates the game score Label.
            self.gameScoreLabels.append(Label(self.scoreFrame, text="000", font="_, 16", bg="Black", fg="White"))
            self.gameScoreLabels[player].grid(row=player + 2, column=1, ipadx=10)

            # Creates the match score Label.
            self.matchScoreLabels.append(Label(self.scoreFrame, text="{:03}".format(score), font="_, 16", bg="Black", fg="White"))
            self.matchScoreLabels[player].grid(row=player + 2, column=2, ipadx=10)

        # Places the Frame containing all of the score information in the
        # bottom left corner of the screen.
        self.scoreFrame.place(anchor='sw', relx=0.0, rely=1.0)

        # Binds any mouse movement to a function that makes a card, if the mouse
        # is currently touching one, pop up a bit as long as it isn't disabled.
        self.root.bind("<Motion>", self.popUp)


    def _loadImages(self):
        """
        Returns 4 dictionaries containing string-PhotoImage pairs for each playing card image.

        Processes all of the images that are needed for the program based on the
        chosen resolution / scale factor. Each dictionary contains pairs of keys
        representing which card it is (its value) as a shortform string and
        values containing the PhotoImage of that card.
        E.g. {"H1" : <PhotoImage>, "H2" : <PhotoImage>,...}

        Card values consist of a a capital letter representing the card's suit
        ('H' = hearts, 'S' = spades, 'D' = diamonds, 'C' = clubs, '_' = joker)
        and either a number for cards ace through 10 or another capital letter
        for jack through joker ('J' = jack, 'Q' = queen, 'K' = king,
        'O' = joker.)
        """

        # 2 dictionaries containing the normal sized images for whichever
        # resolution was chosen, and 2 dictionaries containing their slighly
        # larger copies that make the card appear to pop up.
        cardImages = dict()
        otherImages = dict()
        activeCardImages = dict()
        activeOtherImages = dict()

        # Iterates over the 2 lists containing the suits and values of the cards
        # to create each key in the dictionary while assigning a PhotoImage
        # of the corresponding card to it as well. The cards' files were named
        # similarly to their keys, so the 2 lists are also be used to retrieve
        # them from the file.
        for suit in self.SUITS:
            for value in self.VALUES:
                cardImages["{}{}".format(suit, value)] = PhotoImage(file="{}{}{}.png".format(self.IMAGES_FOLDER, value, suit)).subsample(self.scaleFactor, self.scaleFactor)
        cardImages["_O"] = PhotoImage(file="{}O_.png".format(self.IMAGES_FOLDER)).subsample(self.scaleFactor, self.scaleFactor)

        otherImages["drawPile"] = PhotoImage(file="{}drawPile.png".format(self.OTHERS_FOLDER)).subsample(self.scaleFactor, self.scaleFactor)
        otherImages["down"] = PhotoImage(file="{}down.png".format(self.OTHERS_FOLDER)).subsample(self.scaleFactor, self.scaleFactor)

        # Creates the duplicate dictionaries containing slightly larger versions
        # of the cards.
        for card in cardImages:
            activeCardImages[card] = cardImages[card].zoom(8, 8).subsample(7, 7)
        for card in otherImages:
            activeOtherImages[card] = otherImages[card].zoom(8, 8).subsample(7, 7)

        return cardImages, otherImages, activeCardImages, activeOtherImages


    def _orientHands(self):
        """
        Returns a list of (x, y) coordinate tuples.

        Based on the number of players, the program will choose a preset format
        to arrange the hands. The exact coordinates are then determined based
        on the size of the screen and are in the order in which each player will
        have their turn.
        """

        if self.numOfPlayers == 2:
            # 1 hand at the top, 1 at the bottom.
            return [(self.halfX - self.cardWidth, self.topOfTable),
                    (self.halfX - self.cardWidth, self.bottomOfTable)]

        elif self.numOfPlayers == 3:
            # 2 hands at the top, 1 at the bottom.
            return [(self.thirdX - self.cardWidth, self.topOfTable),
                    (2 * self.thirdX - self.cardWidth, self.topOfTable),
                    (self.halfX - self.cardWidth, self.bottomOfTable)]

        elif self.numOfPlayers == 4:
            # 2 hands at the top, 2 at the bottom.
            return [(self.thirdX - self.cardWidth, self.topOfTable),
                    (2 * self.thirdX - self.cardWidth, self.topOfTable),
                    (2 * self.thirdX - self.cardWidth, self.bottomOfTable),
                    (self.thirdX - self.cardWidth, self.bottomOfTable)]

        elif self.numOfPlayers == 5:
            # 3 hands at the top, 2 at the bottom.
            return [(self.quarterX - self.cardWidth, self.topOfTable),
                    (2 * self.quarterX - self.cardWidth, self.topOfTable),
                    (3 * self.quarterX - self.cardWidth, self.topOfTable),
                    (2 * self.thirdX - self.cardWidth, self.bottomOfTable),
                    (self.thirdX - self.cardWidth, self.bottomOfTable)]

        elif self.numOfPlayers == 6:
            # 2 hands at the top, 2 on the bottom, and 1 at each side.
            return [(2 * self.fifthX - self.cardWidth, self.topOfTable),
                    (3 * self.fifthX - self.cardWidth, self.topOfTable),
                    (4 * self.fifthX - self.cardWidth, self.halfY - self.cardHeight // 2),
                    (3 * self.fifthX - self.cardWidth, self.bottomOfTable),
                    (2 * self.fifthX - self.cardWidth, self.bottomOfTable),
                    (self.fifthX - self.cardWidth, self.halfY - self.cardHeight // 2)]


    def _smoothHandPos(self, handIndex):
        """
        Internal function that finds the position of every card in a given hand and rounds down each value to a whole numbers.

        Iterates over each card in a given hand (based on tags) and aquires the
        card's coordinates using its ID tag, then rounds each coordinate down
        using integer division before setting their newly determined coordinates.

        Arguments:
        handIndex -- a float value which represents which the hand to be modified
        """

        for pos in self.POSITIONS:
            tag = "{}{}".format(handIndex, pos)
            x, y = self.canvas.coords(tag)
            self.canvas.coords(tag, x // 1, y // 1)


    def _moveTo(self, tag, endX, endY, speed=10):
        """
        Internal function that moves one or more given items, based on tags, to given coordinates at a given or default speed.

        Arguments:
        tag -- a string representing a tag on one or more items that will identify it
        endX -- a float or integer representing the x position to which the item should be moved
        endY -- a float or integer representing the y position to which the item should be moved
        speed -- an integer that will alter the rate at which the object will move (higher values are slower)
        """

        # Float representing the distance from a destination at which the item
        # needs to be. It is calculated based on the ratio of a deadzone of
        # 0.0005 to a screen width of 1920 being 3840000:1.
        deadzone = self.screenWidth / 3840000

        # Determines the current x and y coordinates of the given item based
        # on tags. On an item with more than two coordinate points, takes only
        # the first 2.
        xPos, yPos = self.canvas.coords(tag)[:2]

        # Determines the x and y distances from the item's current position
        # to the endpoint.
        distX = endX - xPos
        distY = endY - yPos

        # Integers that will be changed to make sure an item moves properly if
        # it has move in vertical / horizontal line.
        straightLineModifierX = 1
        straightLineModifierY = 1

        # If the move path is a vertical line, ensures that the loop below will
        # be able to move the item by setting variables to fit its
        # conditions; this doesn't move the object off course because of
        # "straightLineModifierX" which will multiply whatever horizontal
        # distance the item would have moved by 0.
        if abs(distX) < deadzone:
            if xPos == 0:
                endX = deadzone * 2
            else:
                endX = (xPos / abs(xPos)) * (deadzone * 2)

            distX = deadzone * 2
            straightLineModifierX = 0

        # If the move path is a horizontal line, ensures that the loop below
        # will be able to move the item by setting variables to fit its
        # conditions; this doesn't move the object off course because of
        # "straightLineModifierY" which will multiply whatever vertical
        # distance the item would have moved by 0.
        elif abs(distY) < deadzone:
            if yPos == 0:
                endY = deadzone * 2
            else:
                endY = (yPos / abs(yPos)) * (deadzone * 2)

            distY = deadzone * 2
            straightLineModifierY = 0

        # While the item's distance from its destination is greater than the
        # deadzone, it will be moved at a decreasing rate towards its target.
        while abs(distX) >= deadzone and abs(distY) >= deadzone:
            # Moves the object once based on its distance from its target and
            # the given speed before refreshing the window.
            self.canvas.move(tag, distX * straightLineModifierX / speed, distY * straightLineModifierY / speed)
            self.root.update()

            # Recalculates the item's position and distance from its target.
            xPos, yPos = self.canvas.coords(tag)[:2]
            distX = endX - xPos
            distY = endY - yPos


    def chooseCardFlip(self, handOrSourceIndex):
        """
        Allows the player to choose a card to flip or choose where to draw depending on the turn.

        On the first turn for each player, the player can choose a card in their
        hand to flip over. On other turns, they will be able to choose either
        the discard or draw pile to draw a card.

        Arguments:
        handOrSourceIndex -- a float or string describing which hand or pile to augment
        """

        # Binds left click to a function that assigns the value of whichever
        # card the player clicks to a class wide variable "choice" to be
        # returned at the end of this function.
        self.root.bind("<Button-1>", self._chooseCardFlipCallback)

        # If the player is supposed to be choosing one of the piles to draw
        # a card, enables the the top card on the discard pile and the draw
        # pile to be interactable.
        if handOrSourceIndex == "SOURCES":
            self.canvas.itemconfig("drawPile", state=NORMAL)
            self.canvas.itemconfig(self.getTopDiscardPileCardID(), state=NORMAL)
        # If the player is supposed to be choosing one of their cards to flip,
        # enables that player's hand to be interactable.
        else:
            self.canvas.itemconfig(handOrSourceIndex, state=NORMAL)

        # A temporary mainloop that runs until a card has been picked or the
        # program quits.
        self.root.waitvar(self.isCardPicked)

        # Disables any items with the passed in tag.
        self.canvas.itemconfig(handOrSourceIndex, state=DISABLED)

        # Unbinds left click from all functions.
        self.root.unbind("<Button-1>")

        # Resets "isCardClicked" to False.
        self.isCardPicked.set(FALSE)

        return self.choice


    def _chooseCardFlipCallback(self, event):
        """
        Callback function that identifies the card or pile that has been clicked while bound.

        If the player clicks on a card, if enabled, the class wide "choice"
        variable will be assigned its value. If they click on the draw or
        discard pile, if enabled, the variable will be assigned which pile the
        player chose.
        """

        # Gets the other tags on whichever item was clicked.
        tags = list(self.canvas.gettags(CURRENT))

        if len(tags) > 0:
            itemType = tags[0]
            # Used in the first turn of the game, this allows the player to
            # click a card and have it flip over. If the clicked item is a card
            # and is face down, that card's value will be saved and the program
            # will then be able to continue.
            if itemType == "CARD" and tags[1][-1] != 'u':
                cardIndex = int(tags[3][-1])
                self.choice = int(cardIndex)
                self.isCardPicked.set(TRUE)

            # Used at the beginning of each player's turn, except on the
            # first turn, this allows the player to click on either of the
            # piles and select that card. If the clicked item is either of the
            # piles, the newly drawn or previously discarded card's value is
            # saved and the program will then be able to continue.
            elif itemType == "SOURCES":
                cardSource = tags[2]
                self.choice = cardSource
                self.isCardPicked.set(TRUE)


    def chooseCardAction(self, handOrSourceIndex, whereDrawn):
        """
        Allows the player to choose what to do with a card after drawing.

        On the first turn for each player, the player can choose a card in their
        hand to flip over. On other turns, they will be able to choose either
        the discard or draw pile to draw a card.

        Arguments:
        handOrSourceIndex -- a float or string describing which hand or pile to augment
        """

        # Binds left click to a function that assigns the action string and
        # possibly the card index to a class wide variable "choice" to be
        # returned at the end of this function.
        self.root.bind("<Button-1>", self._chooseCardActionCallback)

        # Determines whether or not the drawn card is from the draw pile or the
        # discard pile.
        isFromDrawPile = whereDrawn == "drawPile"

        # Enables the player's hand, making those cards interactable.
        self.canvas.itemconfig(handOrSourceIndex, state=NORMAL)

        # If the drawn card was from the draw pile, enables the top card on the
        # discard pile to be interactable as a way for the player to choose to
        # discard the drawn card.
        if isFromDrawPile:
            self.canvas.itemconfig(self.getTopDiscardPileCardID(), state=NORMAL)

        # A temporary mainloop that runs until a card has been picked or the
        # program quits.
        self.root.waitvar(self.isCardPicked)

        # Disables all items that were previously enabled.
        self.canvas.itemconfig(handOrSourceIndex, state=DISABLED)
        if isFromDrawPile:
            self.canvas.itemconfig("discardPile", state=DISABLED)

        # Unbinds left click from all functions.
        self.root.unbind("<Button-1>")

        # Resets "isCardPicked" to False.
        self.isCardPicked.set(FALSE)

        return self.choice


    def _chooseCardActionCallback(self, event):
        """
        Callback function that identifies the card or pile that has been clicked while bound and infers the player's action.

        If the player clicks on a card, if enabled, the class wide "choice"
        variable will be assigned its value and the action string "replace". If
        they click on the draw or discard pile, if enabled, the variable will be
        assigned the action string "discard"
        """

        # Gets the other tags on whichever item was clicked.
        tags = list(self.canvas.gettags(CURRENT))

        if len(tags) > 0:
            itemType = tags[0]
            # Used after the player has drawn a card from either the draw or
            # discard pile, this allows the player to replace a card in their
            # hand with the newly drawn card. If the clicked item is a card,
            # the action string "replace" and the cards index will be saved to
            # a variable before allowing the program to continue.
            if itemType == "CARD":
                cardIndex = int(tags[3][-1])
                self.choice = ("replace", int(cardIndex))
                self.isCardPicked.set(TRUE)

            # Used after the player has drawn a card from the draw pile, this
            # allows the player to discard that card. If the clicked item is
            # one of the piles (though only the discard pile will be enabled at
            # this point), saves the player's action as "discard" and allows the
            # program to continue.
            elif itemType == "SOURCES":
                self.choice = "discard"
                self.isCardPicked.set(TRUE)


    def _checkDiscardPile(self):
        """Internal function that deletes the bottom card image in the discard pile if the number of discarded card images exceeds the maximum and decrements their card ID's."""

        # Aquires a tuple containing all of the itemID's (unique integer tags
        # given to each item automatically) of the cards in the discard pile.
        discardPileUniqueIDs = self.canvas.find_withtag("discardPile")

        # If there are more than 5 cards in the discard pile, removes the bottom
        # card.
        if len(discardPileUniqueIDs) > 5:
            self.canvas.delete("discardPile0")

            # Decreases each discard pile card's cardID by 1 (to fill in the gap
            # of the deleted card).
            # E.g. "discardPile1" -> "discardPile0"
            for uniqueCardID in discardPileUniqueIDs[1:]:
                # Aquires one card's tags as a list.
                tags = list(self.canvas.gettags(uniqueCardID))

                # Decreases its cardID by 1.
                tags[3] = tags[3][:-1] + str(int(tags[3][-1]) - 1)

                # Applies the new tags to the item.
                self.canvas.itemconfig(uniqueCardID, tags=tuple(tags))


    def sweepColumnAnim(self, handIndex, cardIndices):
        """
        Stacks the given cards from a column in a given hand when a player makes a sweep.

        Arguments:
        handIndex -- a float containing a hand index
        cardIndices -- a list containing 3 card indices to be swept
        """

        # Obtains the card ID of the middle card in the column, along with its
        # coordinates.
        middleCardID = "{}{}".format(handIndex, cardIndices[1])
        xPos, yPos = self.canvas.coords(middleCardID)

        # Arranges the card's index data so that the middle card will move
        # first (swaps its index with the actual first card's index in the
        # column). This ends up preventing it from moving, as it's already at
        # its coordinates and no offset has been added. This is done to prevent
        # glitches that result from short distance movements.
        cardIndices[0], cardIndices[1] = cardIndices[1], cardIndices[0]

        # Moves each given card to the middle card in the column, applying a
        # small offset each time to give the cards a stacked appearance.
        # "moveOffset" starts at 0 and increases by 1 each time; it represents
        # the offset multiplier.
        for moveOffset, cardIndex in enumerate(cardIndices):
            # Determines the card's ID tag.
            cardID = "{}{}".format(handIndex, cardIndex)

            self.canvas.tag_raise(cardID)

            # Move the card to the middle card, possible with offset.
            self._moveTo(cardID, xPos + moveOffset * (self.cardWidth / 20) , yPos + moveOffset * (self.cardHeight / 20), 100)

            # Aquires the card's other tags, adds an 'X' to its <"handIndex">
            # tag to distinguish it and prevent it from being enabled as
            # interactable, and applies its new tags.
            tags = list(self.canvas.gettags(cardID))
            tags[2] += "x"
            self.canvas.itemconfig(cardID, tags=tuple(tags))


    def setupAnim(self, firstDrawValue):
        """
        Initiates the game by dealing cards and setting all of the items into position.

        Arguments:
        firstDrawValue -- the card suit and value of the first drawn card (the first card in the discard pile)
        """

        # Creates a hidden rectangle and a rectangular outline that will make up
        # the table before moving them off screen for the moment.
        self.canvas.create_rectangle(0, 0, self.screenWidth, self.screenHeight, fill="#238B50", state=HIDDEN, tags="TABLE")
        self.canvas.create_rectangle(self.cardWidth * 0.3, self.cardWidth * 0.3, self.screenWidth - self.cardWidth * 0.3, self.screenHeight - self.cardWidth * 0.3, outline="#875433", width=self.cardWidth // 4, state=HIDDEN, tags="TABLE" )
        self.canvas.move("TABLE", 0, -self.screenHeight)

        # Creates a list of integers that will be used to map out the positions
        # of the cards when they are first dealt.
        # E.g. for 2 players [0, 3, 1, 4, 2, 5], where column 0 would be player
        # 1's left column and column 3 would be player 2's left column.
        columnOrder = [column + (3 * handIndexMultiplier) for column in range(3) for handIndexMultiplier in range(self.numOfPlayers)]

        # Determines the x coordinates for one total row of cards based on the
        # resolution and the number of players.
        # E.g. for 2 players it would have 6 coordinates, as there are six cards
        # total in a row.
        xStartPositions = [(handIndex / (self.numOfPlayers + 1) * self.screenWidth) + (self.cardWidth * cardIndex) for handIndex in range(1, self.numOfPlayers + 1) for cardIndex in range(-1, 2)]

        # Determines the y coordinates for a single column of cards based on the
        # resolution.
        yStartPositions = [self.cardHeight * row for row in range(1, 4)]

        # Creates the draw pile item.
        self.canvas.create_image(self.halfX, self.screenHeight - 80, activeimage=self.activeOtherImages["drawPile"], image=self.otherImages["drawPile"], state=DISABLED, tags=("SOURCES", "drawPileOrigin", "drawPile"))

        # Counters used to keep track of and assign tags to each card as it's
        # created.
        handIndexCount = 0.0
        cardIndexCount = 0

        # Creates and moves all of the cards to their respective hands. For
        # each y coordinate, goes over the whole list of x coordinates and moves
        # a card to that coordinate pair.
        for y in yStartPositions:
            for index in columnOrder:
                # Maps the correct x coordinate to the current index.
                x = xStartPositions[index]

                # Creates a tag for the current card.
                tags = ("CARD", self.playerHandsDict[int(handIndexCount)][cardIndexCount], handIndexCount, "{}{}".format(handIndexCount, self.POSITIONS[cardIndexCount]))

                # Creates a card item and moves it to the correct position.
                self.canvas.create_image(self.halfX, self.screenHeight - 80, activeimage=self.activeOtherImages["down"], image=self.otherImages["down"], state=DISABLED, tags=tags)
                self._moveTo(tags[3], x, y, 10)

                # Maintains the count of the current hand and card index.
                handIndexCount += 1.0
                if handIndexCount == self.numOfPlayers:
                    handIndexCount = 0.0
                    cardIndexCount += 1

        # Moves all of the cards to the center.
        for handIndex in range(self.numOfPlayers):
            tag = float(handIndex)
            self._moveTo(tag, self.halfX - self.cardWidth, self.halfY - self.cardHeight, 10)
            self._smoothHandPos(tag)

        # Moves the table into position and makes it visible.
        self.canvas.itemconfig("TABLE", state=DISABLED)
        self._moveTo("TABLE", 0, 0, 10)

        # Moves the draw pile to the top left corner.
        self._moveTo("drawPile", self.cardWidth, self.cardHeight, 50)

        # Aquires the coordinate list in which to arrange all of the hands.
        handCoords = self._orientHands()

        # Moves each hand to its final position.
        for handIndex, pos in enumerate(handCoords):
            tag = float(handIndex)
            self._moveTo(tag, pos[0], pos[1], 10)
            self._smoothHandPos(tag)

        # Moves the draw pile back to the center.
        self._moveTo("drawPile", self.halfX - 20, self.halfY, 50)

        # Creates the first card item in the draw pile based on its given value.
        self.canvas.create_image(self.halfX, self.halfY, image=self.otherImages["down"], state=DISABLED, tags=("SOURCES", firstDrawValue + 'u', "discardPile", "discardPile0"))

        # Moves the discard pile card next to the draw pile and flips it.
        self._moveTo("discardPile", self.discardPileX, self.discardPileY, 50)
        self.flipCard("discardPile0")


    def replaceAndDiscardAnim(self, whereDrawn, handIndex, oldCardIndex, newCardValue):
        """
        Moves card items to replace a card in a player's hand with a drawn card and discard the old one.

        When a player chooses to replace a card in their hand on their turn,
        this function will move the drawn card to the given position in their
        hand and then move the card that used to be there to the discard pile.

        Arguments
        whereDrawn -- a string describing from which pile the card was drawn
        handIndex -- a float containing a hand index
        oldCardIndex -- the card index of the card that is being replaced and moved to the discard pile
        newCardValue -- the card value of the drawn card
        """

        # Determines the card ID for the card being replaced.
        oldCardID = "{}{}".format(handIndex, oldCardIndex)

        # If the drawn card was drawn from the draw pile, the new card's ID is
        # determined from the draw pile.
        # If it was drawn from the discard pile, the new card's ID is determined
        # from the discard pile.
        if whereDrawn == "drawPile":
            newCardID = "drawPile0"
        elif whereDrawn == "discardPile":
            newCardID = self.getTopDiscardPileCardID()

        # Acquires all of the tags for the card being replaced.
        oldCardTags = self.canvas.gettags(oldCardID)

        # Because the new card is taking the place of the old one, its tags will
        # be the same, except for the value which will become that of the new
        # card.
        newCardTags = list(oldCardTags)
        newCardTags[1] = newCardValue
        newCardTags.remove("current")

        # Changes the drawn card's tags to reflect that it's now face up.
        if len(newCardValue) < 3:
            newCardValue += 'u'
        else:
            newCardValue = newCardValue.replace('d', 'u')

        # Moves the drawn card to the player's hand in place of the old card.
        xPos, yPos = self.canvas.coords(oldCardID)
        self.canvas.tag_raise(newCardID)
        self._moveTo(newCardID, xPos, yPos, 50)

        # Moves the old card from the player's hand to the discard pile with a
        # random small offset.
        self._moveTo(oldCardID, self.discardPileX + random.randint(-5, 5), self.discardPileY + random.randint(-5, 5), 50)

        # Flips the old card if it was face down.
        if oldCardTags[1][-1] == 'd':
            self.flipCard(oldCardID)

        # Aquires the unique itemID's for the two card images being manipulated
        # to prevent glitches when their tags are being changed.
        oldCardUniqueID = self.canvas.find_withtag(oldCardID)
        newCardUniqueID = self.canvas.find_withtag(newCardID)

        # Applies the new tags to the drawn card now in the player's hand.
        self.canvas.itemconfig(newCardUniqueID, tags=tuple(newCardTags))

        # Creates and applies the tags to the new card in the discard pile.
        newTopDiscardPileCardID = "discardPile{}".format(len(self.canvas.find_withtag("discardPile")))
        self.canvas.itemconfig(oldCardUniqueID, tags=("SOURCES", oldCardTags[1], "discardPile", newTopDiscardPileCardID))

        self._checkDiscardPile()


    def discardAnim(self, newCardValue):
        """
        Moves a card item to the discard pile.

        When a player chooses to discard a new card drawn from the draw pile on
        their turn, this function will move that card to the discard pile.

        Arguments:
        newCardValue -- the card value of the drawn card
        """

        # Aquires the tags from the top draw pile card.
        oldCardID = "drawPile0"
        oldCardTags = self.canvas.gettags(oldCardID)

        # Creates the tags that will be applied to the card when it's moved to
        # the discard pile based on the number of discard cards already there.
        newTopDiscardPileCardID = "discardPile{}".format(len(self.canvas.find_withtag("discardPile")))

        # Moves the drawn card to the discard pile and applies its new tags.
        self.canvas.tag_raise(oldCardID)
        self._moveTo(oldCardID, self.discardPileX + random.randint(-5, 5), self.discardPileY + random.randint(-5, 5), 50)
        self.canvas.itemconfig(oldCardID, tags=("SOURCES", oldCardTags[1], "discardPile", newTopDiscardPileCardID))

        # Deletes the bottom discard card item / image if it exceeds the max.
        self._checkDiscardPile()


    def highlightHand(self, handIndex):
        """
        Draws an orange rectangle around the hand of whichever player currently has their turn and highlights their name on the scoreboard.

        Arguments:
        handIndex -- a float containing a hand index
        """

        handIndexInt = int(handIndex)

        # Identifies the hand index of the previous hand.
        previousHandIndexInt = handIndexInt - 1
        if previousHandIndexInt == -1:
            previousHandIndexInt = self.numOfPlayers - 1

        # Resets the previous player's name and score colour on the scoreboard.
        self.playerLabels[previousHandIndexInt].config(fg="White")
        self.gameScoreLabels[previousHandIndexInt].config(fg="White")
        self.matchScoreLabels[previousHandIndexInt].config(fg="White")

        # Deletes the previous rectangle.
        self.canvas.delete("HIGHLIGHT")

        # Aquires the tag for the middle card in whichever hand is being dealt
        # with.
        tag = "{}{}".format(handIndex, 4)

        # Aquires the coordinates for the middle card in the hand and determines
        # the coordinates for the rectangle based on them.
        xCenter, yCenter = self.canvas.coords(tag)
        x1, y1 = xCenter + 1.5 * self.cardWidth, yCenter + 1.5 * self.cardHeight
        x2, y2 = xCenter - 1.5 * self.cardWidth, yCenter - 1.5 * self.cardHeight

        # Creates the rectangle item.
        self.canvas.create_rectangle(x1, y1, x2, y2, outline="Orange", width=2, tags="HIGHLIGHT")

        # Changes the colour of the current player's name on the scoreboard to
        # orange.
        self.playerLabels[handIndexInt].config(fg="Orange")
        self.gameScoreLabels[handIndexInt].config(fg="Orange")
        self.matchScoreLabels[handIndexInt].config(fg="Orange")


    def drawNewCard(self, cardValue):
        """
        Creates a given card's image on top of the draw pile.

        When the player wants to draw a new card from the draw pile on their
        turn, this function spawns a new card image.

        Arguments:
        cardValue -- a string containing the suit and value of the card
        """
        # Makes the draw pile uninteractable.
        self.canvas.itemconfig("drawPile", state=DISABLED)

        # Creates and flips a new card image based on the given card value.
        self.canvas.create_image(self.halfX - 20, self.halfY, image=self.otherImages["down"], state=NORMAL, tags=("SOURCES", cardValue, "drawPile", "drawPile0"))
        self.canvas.tag_raise("drawPile0")
        self.flipCard("drawPile0")


    def flipCard(self, cardID):
        """
        Flips a given card to face upwards.

        Arguments:
        cardID -- a string containing the hand and card index
        """

        # Aquires the card's other tags.
        tags = list(self.canvas.gettags(cardID))

        # Modifies the card's tags to reflect that it has been flipped.
        tags[1] = tags[1].replace('d', 'u')

        # Saves just the card's suit and value to assign it the correct new
        # images.
        cardValue = tags[1][:-1]

        # Changes the card's images to its actual suit and value to mimic a
        # flip.
        self.canvas.itemconfig(tags[3], activeimage=self.activeCardImages[cardValue], image=self.cardImages[cardValue], state=DISABLED, tags=tuple(tags))
        self.root.update()


    def popUp(self, event):
        """Raises any interactable item to the top layer to work with the item's active image to produce a pop up effect. """

        # Aquires the tags of whichever item the mouse is currently touching.
        tags = list(self.canvas.gettags(CURRENT))
        # If the mouse is touching an actual item created by the program:
        if self.canvas.find_withtag(CURRENT) != 0 and len(tags) > 0:
            # If the item isn't the draw pile image if a card has just been
            # drawn, raise that item to the top layer.
            if tags[1] != "drawPileOrigin" and not self.isCardPicked.get():
                self.canvas.tag_raise(CURRENT)


    def showScores(self, currentScores):
        """
        Displays / updates each player's score based on the score's given.

        Arguments:
        currentScores -- a list containing integers representing each player's score
        """

        # Updates each player's current game score.
        for score, label in zip(currentScores, self.gameScoreLabels):
            label.config(text="{:03}".format(score))

        # Updates each player's current match score.
        for gameScore, matchScore, label in zip(currentScores, self.matchScores, self.matchScoreLabels):
            label.config(text="{:03}".format(gameScore + matchScore))


    def showGameOutcome(self, text):
        """
        Displays a message box telling the players who wins the round and who is winning the match.

        Arguments:
        text -- a string containing the text to be displayed
        """

        outcomeBox = Message(self.root, text=text, font="_, 20", bg="Black", fg="White")
        outcomeBox.place(anchor='c', relx=0.5, rely=0.5, relheight=0.3, relwidth=0.3)


    def getTopDiscardPileCardID(self):
        """
        Determines the ID tag for the top discard pile card.

        Determines the ID tag for the top discard pile card by taking the total
        number of cards with the tag "discardPile", subtracting 1 (because the
        pile begins at "discardPile0, not "discardPile1"), and then adding
        either 0 or 1 depending on whether the discard pile contains the
        maximum number of card images (in which case the program will delete
        the bottom one and modify tags, hence the addition of 1).
        """

        return "discardPile{}".format(len(self.canvas.find_withtag("discardPile")) - 1 + int(len(self.canvas.find_withtag("discardPile")) == self.MAX_DISCARDS))


    def toggleFullscreen(self):
        """Toggles the window between fullscreen and windowed."""
        self.root.attributes("-fullscreen", self.root.attributes("-fullscreen") == False)


def main():
    print("Done")

if __name__ == "__main__":
    main()
