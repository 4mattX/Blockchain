import pathlib
from tkinter import Tk, Text, BOTH, W, N, E, S, Frame, Button, PhotoImage, Button, Label, Canvas, Text
import tkinter.font as font
import os
import subprocess

from Cryptodome.PublicKey import RSA

from BlockChainProject.Blockchain import Blockchain


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
        self.blockchain = Blockchain()

        self.mainCanvas = None
        self.miniCanvas = None
        self.notifications = []
        self.lineCounter = 0
        self.balance = 0
        self.frameColor = '#2c2f33'
        self.selectedFriend = ""
        self.transactionAmount = 0
        
        self.miniCanvasComponents = []

        # Establish Blockchain here
        self.blockchain.addFirstBlock()

        self.initUI()

    def displayBlockchain(self):
        self.mainCanvas.create_text(300, 300, text='Hello World')

    def sendFriend(self):
        self.resetMainCanvas()

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
            friendButtons[counter] = HoverButton(self.mainCanvas, text=friendText, width=BUTTON_WIDTH, background=iconColor, foreground='white', activeforeground='white', relief='flat', overrelief='flat', activebackground=iconActiveColor, font=buttonFont, highlightcolor=iconActiveColor, command=lambda friendText=friendText: self.selectFriend(friendText)).place(x=0, y=counter * 50 + 40)
            self.miniCanvasComponents.append(friendButtons[counter])
            counter += 1
            
        # Text box for user input
        amountLabel = Label(self.mainCanvas, text='Amount:', background=self.frameColor, foreground='white', font=buttonFont).place(x=20, y=400)
        userInput = Text(self.mainCanvas, height=1, width=15, background='#23272a', foreground='white', borderwidth=0)
        userInput.place(x=105, y=405)

        # Send Button to confirm transaction
        sendButton = HoverButton(self.mainCanvas, text='Confirm Transaction', foreground='white', background=iconColor, activebackground=iconActiveColor, relief='flat', overrelief='flat', font=buttonFont, highlightcolor=iconActiveColor, command=lambda userInput=userInput: self.createTransaction(userInput.get(1.0, "end-1c")))
        sendButton.place(x=400, y=392)

    def createTransaction(self, amount):
        newAmount = -1
        try:
            newAmount = float(amount)
        except:
            self.addLine("red@$>> Invalid Transaction Amount")
            return
        if (newAmount == -1):
            self.addLine("red@$>> Invalid Transaction Amount")
            return

        try:

            with open('sender/public.pem', "rb") as file:
                publicKey = RSA.import_key(file.read())

            with open('sender/private.pem', "rb") as file:
                privateKey = RSA.import_key(file.read())

            with open('friends/' + self.selectedFriend + ".pem", "rb") as file:
                receiverKey = RSA.import_key(file.read())

            self.blockchain.addTransaction(receiverKey, amount, publicKey, privateKey)
            self.addLine("lime@$>> pending transaction created")
            self.addLine("lime@$>> " + str(amount) + " to " + self.selectedFriend)
        except:
            self.addLine("red@$>> Error: Creating Transaction")

        
    def selectFriend(self, friend):
        self.selectedFriend = friend
        self.addLine("white@$>> selected: " + friend)

    def addLine(self, lineText):
        notificationFont = font.Font(family='Uni Sans', size=16)

        self.notifications = [lineText] + self.notifications
        yPos = (self.master.winfo_height()/4) - 20

        self.miniCanvas.delete("notification")

        for notification in self.notifications:

            colorCode = notification.split("@$", 1)[0]
            message = notification.split("@$", 1)[1]

            self.miniCanvas.create_text(10, yPos, text=message, font=notificationFont, fill=colorCode, tag='notification', anchor='w')
            yPos -= 20

    def openFriendsFolder(self):
        directory = os.path.dirname(__file__)
        friendsDirectory = "friends\README.txt"
        absoluteDirectory = os.path.join(directory, friendsDirectory)
        subprocess.Popen(r'explorer /select,' + friendsDirectory)
        
    def displayTransactions(self):
        self.resetMainCanvas()

        labelFont = font.Font(family='Uni Sans', weight='bold', size=16)
        tranFont = font.Font(family='Uni Sans', weight='bold', size=6)
        Label(self.mainCanvas, text='Pending Transactions: ', background=self.frameColor, foreground='white', font=labelFont).place(x=20, y=20)

        with open("mempool.csv", "rb") as file:
            Label(self.mainCanvas, text=file.read(), background=self.frameColor, foreground='white', font=tranFont).place(x=40, y=50)

    def resetMainCanvas(self):
        width = self.master.winfo_width()
        height = self.master.winfo_height()
        self.mainCanvas.destroy()
        self.mainCanvas = Canvas(self, background=self.frameColor, width=width, height=450, highlightthickness=0)
        self.mainCanvas.place(x=265, y=0)

    def mineBlockchain(self):
        self.resetMainCanvas()
        labelFont = font.Font(family='Uni Sans', weight='bold', size=16)
        statusFont = font.Font(family='Uni Sans', weight='bold', size=20)

        iconColor = '#2c2f33'
        iconActiveColor = '#60666e'
        iconClickColor = '#767c85'
        buttonFont = font.Font(family='Uni Sans', size=16)
        BUTTON_WIDTH = 50
        BUTTON_HEIGHT = 5

        mineStatus = "Mine Status: "
        hashRate = "Hash Rate: "
        blockNum = "Block Index: "
        nonse = "Nonse: "
        amountTransactions = "Amount Transactions: "

        Label(self.mainCanvas, text=mineStatus, background=self.frameColor, foreground='white', font=statusFont).place(x=20, y=20)
        Label(self.mainCanvas, text=hashRate, background=self.frameColor, foreground='white', font=labelFont).place(x=20, y=100)
        Label(self.mainCanvas, text=blockNum, background=self.frameColor, foreground='white', font=labelFont).place(x=20, y=135)
        Label(self.mainCanvas, text=nonse, background=self.frameColor, foreground='white', font=labelFont).place(x=20, y=170)
        Label(self.mainCanvas, text=amountTransactions, background=self.frameColor, foreground='white', font=labelFont).place(x=20, y=205)

        HoverButton(self.mainCanvas, text='Begin Mining', width=BUTTON_WIDTH, background=iconColor, foreground='white', activeforeground='white', relief='flat', overrelief='flat', activebackground=iconActiveColor, font=buttonFont, highlightcolor=iconActiveColor, command=lambda: self.mineBlock()).place(x=60, y=400)

    def mineBlock(self):
        with open('miner/public.pem', "rb") as file:
            minerKey = RSA.import_key(file.read())

        if (self.blockchain.minePendingTransactions(minerKey)):
            self.addLine("lime@$>> BLOCK MINED!")
        else:
            self.addLine("red@$>> There must be at least one pending transaction to mine")

    def initUI(self):

        BUTTON_WIDTH = 16
        BUTTON_HEIGHT = 5

        self.master.title("Blockchain")
        self.pack(fill=BOTH, expand=1)

        self.master.update_idletasks()
        width = self.master.winfo_width()
        height = self.master.winfo_height()

        # Canvas Stuff
        self.mainCanvas = Canvas(self, background=self.frameColor, width=width, height=height, highlightthickness=0)
        self.mainCanvas.place(x=265, y=0)

        self.miniCanvas = Canvas(self, background=self.frameColor, width=width, height=height/4, highlightthickness=0)
        self.miniCanvas.place(x=265, y=450)

        # Button Stuff
        buttons = []
        iconColor = '#7289da'
        iconActiveColor = '#a1b6ff'
        buttonFont = font.Font(family='Uni Sans', weight='bold', size=16)

        self.miniCanvas.create_line(10, 0, width - 280, 0, fill='white', width=2)

        sendButton = Button(self, text="Send", width=BUTTON_WIDTH, background=iconColor, foreground='white', activeforeground='white', relief='flat', overrelief='sunken', activebackground=iconActiveColor, font=buttonFont, command=lambda: self.sendFriend())
        addFriendButton = Button(text="Add Friend", width=BUTTON_WIDTH, background=iconColor, foreground='white', activeforeground='white', relief='flat', overrelief='sunken', activebackground=iconActiveColor, font=buttonFont, command=lambda: self.openFriendsFolder())
        mineButton = Button(text="Mine", width=BUTTON_WIDTH, background=iconColor, foreground='white', activeforeground='white', relief='flat', overrelief='sunken', activebackground=iconActiveColor, font=buttonFont, command=lambda: self.mineBlockchain())
        viewChainButton = Button(text="View Chain", width=BUTTON_WIDTH, background=iconColor, foreground='white', activeforeground='white', relief='flat', overrelief='sunken', activebackground=iconActiveColor, font=buttonFont)
        viewTransactionsButton = Button(text="View Transactions", width=BUTTON_WIDTH, background=iconColor, foreground='white', activeforeground='white', relief='flat', overrelief='sunken', activebackground=iconActiveColor, font=buttonFont, command=lambda: self.displayTransactions())

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