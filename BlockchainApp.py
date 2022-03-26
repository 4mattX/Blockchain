import pathlib
from tkinter import Tk, Text, BOTH, W, N, E, S, Frame, Button, PhotoImage, Button, Label, Canvas
import tkinter.font as font
import os
import subprocess


class HoverButton(Button):
    def __init__(self, master, **kw):
        Button.__init__(self, master=master, **kw)
        self.defaultBackground = self["background"]
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        self['background'] = self['activebackground']

    def on_leave(self, e):
        self['background'] = self.defaultBackground

class BlockchainApp(Frame):

    def __init__(self):
        super().__init__()
        self.mainCanvas = None
        self.miniCanvas = None
        self.notifications = []
        self.lineCounter = 0
        self.balance = 0

        self.initUI()

    def displayBlockchain(self):
        self.mainCanvas.create_text(300, 300, text='Hello World')

    def sendFriend(self):
        friendsNames = []
        friendsDirectory = os.listdir('friends')
        friendButtons = []

        iconColor = '#2c2f33'
        iconActiveColor = '#60666e'
        iconClickColor = '#767c85'
        buttonFont = font.Font(family='Uni Sans', size=16)
        BUTTON_WIDTH = 50
        BUTTON_HEIGHT = 5

        friendButtons = []

        for friend in friendsDirectory:
            if (str(friend).__contains__("README")):
                friendsDirectory.remove(friend)

        counter = 0
        for friends in friendsDirectory:
            friendText = friends.split(".", 1)[0]
            friendButtons.append(None)
            friendButtons[counter] = HoverButton(self.mainCanvas, text=friendText, width=BUTTON_WIDTH, background=iconColor, foreground='white', activeforeground='white', relief='flat', overrelief='flat', activebackground=iconActiveColor, font=buttonFont, highlightcolor=iconActiveColor, command=lambda friendText=friendText: self.addLine(">> selected: " + friendText)).place(x=0, y=counter * 50 + 40)
            counter += 1


    def addLine(self, lineText):
        notificationFont = font.Font(family='Uni Sans', size=16)

        self.notifications = [lineText] + self.notifications
        yPos = (self.master.winfo_height()/4) - 20

        self.miniCanvas.delete("notification")

        for notification in self.notifications:
            self.miniCanvas.create_text(100, yPos, text=notification, font=notificationFont, fill='white', tag='notification')
            yPos -= 20



    def openFriendsFolder(self):
        directory = os.path.dirname(__file__)
        friendsDirectory = "friends\README.txt"
        absoluteDirectory = os.path.join(directory, friendsDirectory)
        subprocess.Popen(r'explorer /select,' + friendsDirectory)

    def initUI(self):

        BUTTON_WIDTH = 16
        BUTTON_HEIGHT = 5

        self.master.title("Blockchain")
        self.pack(fill=BOTH, expand=1)

        self.master.update_idletasks()
        width = self.master.winfo_width()
        height = self.master.winfo_height()

        frameColor = '#2c2f33'
        # Canvas Stuff
        self.mainCanvas = Canvas(self, background=frameColor, width=width, height=height, highlightthickness=0)
        self.mainCanvas.place(x=265, y=0)

        self.miniCanvas = Canvas(self.mainCanvas, background='#23272a', width=width, height=height/4, highlightthickness=0)
        self.miniCanvas.place(x=0, y=450)

        # Button Stuff
        buttons = []
        iconColor = '#7289da'
        iconActiveColor = '#a1b6ff'
        buttonFont = font.Font(family='Uni Sans', weight='bold', size=16)

        sendButton = Button(self, text="Send", width=BUTTON_WIDTH, background=iconColor, foreground='white', activeforeground='white', relief='flat', overrelief='sunken', activebackground=iconActiveColor, font=buttonFont, command=lambda: self.sendFriend())
        addFriendButton = Button(text="Add Friend", width=BUTTON_WIDTH, background=iconColor, foreground='white', activeforeground='white', relief='flat', overrelief='sunken', activebackground=iconActiveColor, font=buttonFont, command=lambda: self.openFriendsFolder())
        mineButton = Button(text="Mine", width=BUTTON_WIDTH, background=iconColor, foreground='white', activeforeground='white', relief='flat', overrelief='sunken', activebackground=iconActiveColor, font=buttonFont)
        viewChainButton = Button(text="View Chain", width=BUTTON_WIDTH, background=iconColor, foreground='white', activeforeground='white', relief='flat', overrelief='sunken', activebackground=iconActiveColor, font=buttonFont)
        viewTransactionsButton = Button(text="View Transactions", width=BUTTON_WIDTH, background=iconColor, foreground='white', activeforeground='white', relief='flat', overrelief='sunken', activebackground=iconActiveColor, font=buttonFont)

        buttons.append(sendButton)
        buttons.append(addFriendButton)
        buttons.append(mineButton)
        buttons.append(viewChainButton)
        buttons.append(viewTransactionsButton)

        counter = 0
        for button in buttons:
            yPlace = counter * (height / 8)
            button.place(x=20, y=yPlace + 20)
            counter += 1

        # Labels for balance
        balanceString = "Balance: " + str(self.balance)
        nodeString = "   Nodes: "
        balanceLabel = Label(self, text=balanceString, background='#23272a', foreground='white', font=buttonFont).place(x=20, y=420)
        nodesLabel = Label(self, text=nodeString, background='#23272a', foreground='white', font=buttonFont).place(x=20, y=460)