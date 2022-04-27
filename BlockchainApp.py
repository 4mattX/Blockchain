import gc
import math
import threading
import traceback
from tkinter import Tk, Text, BOTH, W, N, E, S, Frame, Button, PhotoImage, Button, Label, Canvas, Text
import tkinter.font as font
import os
import subprocess

from Cryptodome.PublicKey import RSA
from BlockChainProject.Blockchain import Blockchain

balance = 0
balanceLabel = None
blockchain = Blockchain()

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
        self.frameColor = '#2c2f33'
        self.selectedFriend = ""
        self.transactionAmount = 0
        self.balanceLabel = Label(self, text="balance: ", background='#23272a', foreground='white')
        self.blocksLabel = Label(self, text="balance: ", background='#23272a', foreground='white')
        self.nonseLabel = Label(self.mainCanvas, background=self.frameColor, foreground='white')
        self.hashLabel = Label(self.mainCanvas, background=self.frameColor, foreground='white')
        self.miningButton = HoverButton(self.mainCanvas, text="Begin Mining", foreground='white', activeforeground='white', relief='flat', overrelief='flat')
        self.nonse = 0
        self.hashRate = 0
        self.inMiner = False
        self.hashTimer = 100
        self.isMining = False
        self.counter = 10
        self.client = None

        self.isAutoMining = False

        self.thread = threading.Thread(target=self.mineBlock, name="mineThread")
        self.thread.daemon = True

        self.miniCanvasComponents = []

        # Establish Blockchain here
        directory = os.listdir("blockchain")
        if (len(directory) == 0):
            print("no blocks recorded")
        else:
            try:
                blockchain.getBlockChainFromData()
            except:
                print("no blocks recorded")

        blockchain.app = self

        print(str(blockchain.app))

        self.initUI()

    def addClient(self, client):
        self.client = client

    def updateSideBar(self):
        buttonFont = font.Font(family='Uni Sans', weight='bold', size=16)
        with open('sender/public.pem', "rb") as file:
            senderKey = RSA.import_key(file.read())
            file.close()
        balanceString = "Balance: " + str(blockchain.getWalletBalance(senderKey))
        self.balanceLabel = Label(self, text=balanceString, background='#23272a', foreground='white', font=buttonFont).place(x=20, y=420)

        blocksString = "Blocks: " + str(len(blockchain.chain))
        self.blocksLabel = Label(self, text=blocksString, background='#23272a', foreground='white', font=buttonFont).place(x=20, y=460)

    def updateMinerScreen(self):
        if (not self.inMiner):
            return

        lotsOfSpace = "                                                                                                 "

        nonseString = "Nonse: " + str(self.nonse)
        labelFont = font.Font(family='Uni Sans', weight='bold', size=16)
        statusFont = font.Font(family='Uni Sans', weight='bold', size=24)
        Label(self.mainCanvas, text=lotsOfSpace, background=self.frameColor, foreground='white', font=labelFont).place(x=20, y=170)
        self.nonseLabel = Label(self.mainCanvas, text=nonseString, background=self.frameColor, foreground='white', font=labelFont).place(x=20, y=170)

        hashString = "Hash Rate: " + str(self.truncate(self.hashRate / 10, 1)) + " h/ms"
        Label(self.mainCanvas, text=lotsOfSpace, background=self.frameColor, foreground='white', font=labelFont).place(x=20, y=100)
        Label(self.mainCanvas, text=hashString, background=self.frameColor, foreground='white', font=labelFont).place(x=20, y=100)

        amountTransactions = str(len(blockchain.pendingTransactions))
        amountTransactions = "Amount Transactions: " + amountTransactions
        Label(self.mainCanvas, text=amountTransactions, background=self.frameColor, foreground='white', font=labelFont).place(x=20, y=205)

        blockNum = str(len(blockchain.chain))
        blockNum = "Block Index: " + blockNum
        Label(self.mainCanvas, text=blockNum, background=self.frameColor, foreground='white', font=labelFont).place(x=20, y=135)

        if (self.isMining):
            if (self.isAutoMining):
                Label(self.mainCanvas, text="Waiting...          ", background=self.frameColor, foreground='orange', font=statusFont).place(x=190, y=16)
            else:
                Label(self.mainCanvas, text="Mining               ", background=self.frameColor, foreground='lime', font=statusFont).place(x=190, y=16)
        else:
            if (self.isAutoMining):
                Label(self.mainCanvas, text="Waiting...          ", background=self.frameColor, foreground='orange', font=statusFont).place(x=190, y=16)
            else:
                Label(self.mainCanvas, text="Suspended", background=self.frameColor, foreground='red', font=statusFont).place(x=190, y=16)

    def truncate(self, number, digits) -> float:
        stepper = 10.0 ** digits
        return math.trunc(stepper * number) / stepper

    def addFriend(self):
        self.inMiner = False
        self.resetMainCanvas()

        iconColor = '#2c2f33'
        iconActiveColor = '#60666e'
        iconClickColor = '#767c85'
        buttonFont = font.Font(family='Uni Sans', size=16)
        labelFont = font.Font(family='Uni Sans', weight='bold', size=18)
        instructionFont = font.Font(family='Uni Sans', size=12)
        BUTTON_WIDTH = 50
        BUTTON_HEIGHT = 5

        Label(self.mainCanvas, text='How to add friends ', background=self.frameColor, foreground='white', font=labelFont, anchor='w').place(x=20, y=20)

        instructions = "1. After receiving your friend's public key file (.PEM), click on the 'Open Friend Directory' button\n" + \
                       "2. Place the file in the folder and then right click and select 'rename'\n" + \
                       "3. Enter your friend's name or anything that will allow you to know who owns that wallet\n" + \
                       "4. Make sure to keep the file type as .PEM or it will not be listed \n"

        Label(self.mainCanvas, text=instructions, background=self.frameColor, foreground='white', font=instructionFont, anchor='w', justify='left').place(x=40, y=60)

        instructions2 = "1. Click on the 'Personal Keys' button\n" + \
                       "2. Right click on the 'public.pem' file and click copy\n" + \
                       "3. Paste this file somewhere outside of this projects directory\n" + \
                       "4. Right click on the pasted file and then select 'rename' and rename it \n" + \
                       "5. Send the file to your friend through any secure application such as email or discord"

        Label(self.mainCanvas, text='How to send your public key', background=self.frameColor, foreground='white', font=labelFont, anchor='w').place(x=20, y=200)
        Label(self.mainCanvas, text=instructions2, background=self.frameColor, foreground='white', font=instructionFont, anchor='w', justify='left').place(x=40, y=240)

        pubKey = HoverButton(self.mainCanvas, text='Personal Keys', foreground='white', background=iconColor, activebackground=iconActiveColor, relief='flat', overrelief='flat', font=buttonFont, highlightcolor=iconActiveColor, command=lambda BUTTON_HEIGHT=BUTTON_HEIGHT: self.openPersonalKeys()).place(x=40, y=400)
        generateNew = HoverButton(self.mainCanvas, text='Open Friend Directory', foreground='white', background=iconColor, activebackground=iconActiveColor, relief='flat', overrelief='flat', font=buttonFont, highlightcolor=iconActiveColor, command=lambda BUTTON_HEIGHT=BUTTON_HEIGHT: self.openFriendsFolder()).place(x=400, y=400)

    def sendFriend(self):
        self.inMiner = False
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
                file.close()

            with open('sender/private.pem', "rb") as file:
                privateKey = RSA.import_key(file.read())
                file.close()

            with open('friends/' + self.selectedFriend + ".pem", "rb") as file:
                receiverKey = RSA.import_key(file.read())
                file.close()

            blockchain.addTransaction(receiverKey, amount, publicKey, privateKey)
            self.addLine("lime@$>> pending transaction created")
            self.addLine("lime@$>> " + str(amount) + " to " + self.selectedFriend)
        except:
            traceback.print_exc()
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
        subprocess.Popen(r'explorer /select,' + friendsDirectory)

    def openPersonalKeys(self):
        directory = os.path.dirname(__file__)
        personalDirectory = "sender\public.pem"
        subprocess.Popen(r'explorer /select,' + personalDirectory)

    def displayPersonalTransactions(self):
        self.inMiner = False
        self.resetMainCanvas()

        labelFont = font.Font(family='Uni Sans', weight='bold', size=18)
        tranFont = font.Font(family='Uni Sans', weight='bold', size=12)
        Label(self.mainCanvas, text='Your Transactions: ', background=self.frameColor, foreground='white', font=labelFont, anchor='w').place(x=20, y=20)

        transactionsText = ""
        for block in reversed(blockchain.chain):
            for transaction in block.getTransactions():

                amount = "Amount: "
                sender = "Sender: "
                receiver = "Receiver: "

                amount += str(transaction.getAmount())

                friendsDirectory = os.listdir('friends')
                for friend in friendsDirectory:
                    if (str(friend).__contains__("README")):
                        friendsDirectory.remove(friend)

                for friend in friendsDirectory:
                    name = friend.split(".", 1)[0]
                    with open('friends/' + name + ".pem", "rb") as file:
                        receiverKey = RSA.import_key(file.read())
                        file.close()
                    if (transaction.getReceiver() == receiverKey):
                        receiver += name
                    try:
                        if (transaction.getSender() == receiverKey):
                            sender += name
                    except:
                        sender = "Sender: Miner Rewards"

                with open('sender/public.pem') as file:
                    key = RSA.import_key(file.read())
                    file.close()

                try:
                    if (key == transaction.getSender()):
                        sender += "You"
                except:
                    sender = "Sender: Miner Rewards"

                if (key == transaction.getReceiver()):
                    receiver += "You"

                if (len(receiver) < 11):
                    receiver += str(transaction.getReceiver())[:8] + "..."

                if (len(sender) < 9):
                    try:
                        sender += str(transaction.getSender())[:8] + "..."
                    except:
                        sender = "Sender: Miner Rewards"


                transactionsText += amount + " " + sender + " " + receiver + "\n"

        Label(self.mainCanvas, text=transactionsText, background=self.frameColor, foreground='#adadad', font=tranFont).place(x=40, y=60)

    def displayTransactions(self):
        self.inMiner = False
        self.resetMainCanvas()

        labelFont = font.Font(family='Uni Sans', weight='bold', size=18)
        tranFont = font.Font(family='Uni Sans', weight='bold', size=12)
        Label(self.mainCanvas, text='Pending Transactions: ', background=self.frameColor, foreground='white', font=labelFont, anchor='w').place(x=20, y=20)

        transactionsText = ""

        for transaction in blockchain.pendingTransactions:
            amount = "Amount: "
            sender = "Sender: "
            receiver = "Receiver: "

            amount += str(transaction.getAmount())

            friendsDirectory = os.listdir('friends')
            for friend in friendsDirectory:
                if (str(friend).__contains__("README")):
                    friendsDirectory.remove(friend)

            for friend in friendsDirectory:
                name = friend.split(".", 1)[0]
                with open('friends/' + name + ".pem", "rb") as file:
                    receiverKey = RSA.import_key(file.read())
                    file.close()
                if (transaction.getReceiver() == receiverKey):
                    receiver += name
                try:
                    if (transaction.getSender() == receiverKey):
                        sender += name
                except:
                    sender = "Sender: Miner Rewards"

            with open('sender/public.pem') as file:
                key = RSA.import_key(file.read())
                file.close()

            try:
                if (key == transaction.getSender()):
                    sender += "You"
            except:
                sender = "Sender: Miner Rewards"

            if (key == transaction.getReceiver()):
                receiver += "You"

            if (len(receiver) < 11):
                receiver += str(transaction.getReceiver())[:8] + "..."

            if (len(sender) < 9):
                try:
                    sender += str(transaction.getSender())[:8] + "..."
                except:
                    sender = "Sender: Miner Rewards"


            transactionsText += amount + " " + sender + " " + receiver + "\n"

        Label(self.mainCanvas, text=transactionsText, background=self.frameColor, foreground='#adadad', font=tranFont).place(x=40, y=60)

    def resetMainCanvas(self):
        width = self.master.winfo_width()
        height = self.master.winfo_height()
        self.mainCanvas.destroy()
        self.mainCanvas = Canvas(self, background=self.frameColor, width=width, height=450, highlightthickness=0)
        self.mainCanvas.place(x=265, y=0)

    def mineBlockchain(self):
        self.inMiner = True
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
        nonse = "Nonse: " + str(self.nonse)

        Label(self.mainCanvas, text=mineStatus, background=self.frameColor, foreground='white', font=statusFont).place(x=20, y=20)

        self.miningButton = HoverButton(self.mainCanvas, text="Begin Mining", width=BUTTON_WIDTH, background=iconColor, foreground='white', activeforeground='white', relief='flat', overrelief='flat', activebackground=iconActiveColor, font=buttonFont, highlightcolor=iconActiveColor, command=lambda: self.intermediateMine()).place(x=60, y=400)
        autoMiningButton = HoverButton(self.mainCanvas, text="Toggle Auto Mine", width=int(BUTTON_WIDTH / 3), background=iconColor, foreground='white', activeforeground='white', relief='flat', overrelief='flat', activebackground=iconActiveColor, font=buttonFont, highlightcolor=iconActiveColor, command=lambda: self.toggleAutoMine()).place(x=500, y=15)

        self.updateMinerScreen()

    def toggleAutoMine(self):
        if(self.isAutoMining):
            self.isAutoMining = False
        else:
            self.isAutoMining = True

        self.updateMinerScreen()

    def updateBlockchain(self):
        # print("request for " + str(len(blockchain.getChain())))
        blockchain.getClient().disconnect()
        blockchain.getClient().setUsername("request")
        blockchain.getClient().createConnection()
        blockchain.getClient().sendMessage(str(len(blockchain.getChain())).encode())

    def generateNewKeys(self):
        blockchain.generateKeys()

        directory = os.path.dirname(__file__)
        friendsDirectory = "generate\README.txt"
        subprocess.Popen(r'explorer /select,' + friendsDirectory)

    def intermediateMine(self):

        self.isMining = not self.isMining
        if (self.isAutoMining):
            self.isMining = True

        BUTTON_WIDTH = 50
        iconColor = '#2c2f33'
        iconActiveColor = '#60666e'
        buttonFont = font.Font(family='Uni Sans', size=16)

        if (self.isMining):
            blockchain.killMine = False
            self.miningButton = HoverButton(self.mainCanvas, text="Stop Mining", width=BUTTON_WIDTH, background=iconColor, foreground='white', activeforeground='white', relief='flat', overrelief='flat', activebackground=iconActiveColor, font=buttonFont, highlightcolor=iconActiveColor, command=lambda: self.intermediateMine()).place(x=60, y=400)
            try:
                self.thread.join()
            except:
                print("First Mining")
            self.thread = threading.Thread(target=self.mineBlock, name="mineThread")
            self.thread.daemon = True
            self.thread.start()
        else:
            blockchain.killMine = True
            self.nonse = 0
            self.miningButton = HoverButton(self.mainCanvas, text="Start Mining", width=BUTTON_WIDTH, background=iconColor, foreground='white', activeforeground='white', relief='flat', overrelief='flat', activebackground=iconActiveColor, font=buttonFont, highlightcolor=iconActiveColor, command=lambda: self.intermediateMine()).place(x=60, y=400)

    def mineBlock(self):

        BUTTON_WIDTH = 50
        iconColor = '#2c2f33'
        iconActiveColor = '#60666e'
        buttonFont = font.Font(family='Uni Sans', size=16)

        with open('sender/public.pem', "rb") as file:
            minerKey = RSA.import_key(file.read())
            file.close()

        try:
            if (blockchain.minePendingTransactions(minerKey)):
                self.addLine("lime@$>> BLOCK MINED!")
                if ( not self.isAutoMining):
                    self.isMining = False
                    self.miningButton = HoverButton(self.mainCanvas, text="Start Mining", width=BUTTON_WIDTH, background=iconColor, foreground='white', activeforeground='white', relief='flat', overrelief='flat', activebackground=iconActiveColor, font=buttonFont, highlightcolor=iconActiveColor, command=lambda: self.intermediateMine()).place(x=60, y=400)
            else:
                if (blockchain.killMine):
                    self.addLine("red@$>> Mining Suspended")
                else:
                    self.addLine("red@$>> There must be at least one pending transaction to mine")
        except:
            self.intermediateMine()

    def initUI(self):

        BUTTON_WIDTH = 17
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
        addFriendButton = Button(text="Add Friend", width=BUTTON_WIDTH, background=iconColor, foreground='white', activeforeground='white', relief='flat', overrelief='sunken', activebackground=iconActiveColor, font=buttonFont, command=lambda: self.addFriend())
        mineButton = Button(text="Mine", width=BUTTON_WIDTH, background=iconColor, foreground='white', activeforeground='white', relief='flat', overrelief='sunken', activebackground=iconActiveColor, font=buttonFont, command=lambda: self.mineBlockchain())
        viewChainButton = Button(text="Your Transactions", width=BUTTON_WIDTH, background=iconColor, foreground='white', activeforeground='white', relief='flat', overrelief='sunken', activebackground=iconActiveColor, font=buttonFont, command=lambda: self.displayPersonalTransactions())
        viewTransactionsButton = Button(text="Pending Transactions", width=BUTTON_WIDTH, background=iconColor, foreground='white', activeforeground='white', relief='flat', overrelief='sunken', activebackground=iconActiveColor, font=buttonFont, command=lambda: self.displayTransactions())

        buttons.append(sendButton)
        buttons.append(addFriendButton)
        buttons.append(mineButton)
        buttons.append(viewChainButton)
        buttons.append(viewTransactionsButton)

        counter = 0
        for button in buttons:
            yPlace = counter * (height / 8)
            button.place(x=17, y=yPlace + 20)
            counter += 1

        # Labels for balance
        balanceString = "Balance: " + str(balance)

        # Generate New Keys
        updateButton = Button(text="Generate New Keys", width=BUTTON_WIDTH, background=self.frameColor, foreground='gray', activeforeground='white', relief='flat', overrelief='sunken', activebackground='gray', font=buttonFont, command=lambda: self.generateNewKeys()).place(x=17, y=550)

if __name__ == '__main__':
    root = Tk()
    root.geometry("1000x600+300+300")
    app = BlockchainApp()
    app.configure(bg='#23272a')

    blockchain.getClient().startThread()

    def update():
        app.counter += 1
        if (app.counter > 10):
            app.updateSideBar()

            if (len(blockchain.getChain()) > 1):
                if (app.isAutoMining):
                    app.intermediateMine()


            app.counter = 0

        if (app.isMining):
            app.updateMinerScreen()
        # app.hashTimer += 100
        app.hashRate = 0

        try:
            if (not app.isAutoMining):
                if (not app.isMining):
                    app.updateBlockchain()
        except:
            print("error sending update")

        if (not app.isMining):
            try:
                app.thread.join()
            except:
                gc.collect()
        gc.collect()

        root.after(500, update)
    update()

    root.mainloop()