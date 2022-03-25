from tkinter import Tk, Text, BOTH, W, N, E, S, Frame, Button, PhotoImage, Button, Label, Canvas
import tkinter.font as font

class BlockchainApp(Frame):

    def __init__(self):
        super().__init__()
        self.mainCanvas = None

        self.initUI()

    def displayBlockchain(self):
        self.mainCanvas.create_text(300, 300, text='Hello World')


    def initUI(self):

        BUTTON_WIDTH = 16
        BUTTON_HEIGHT = 5

        self.master.title("Blockchain")
        self.pack(fill=BOTH, expand=1)

        self.master.update_idletasks()
        width = self.master.winfo_width()
        height = self.master.winfo_height()

        frameColor = '#2c2f33'
        # Frame Stuff
        self.mainCanvas = Canvas(self, background=frameColor, width=width, height=height, highlightthickness=0)
        self.mainCanvas.place(x=265, y=0)

        # Button Stuff
        buttons = []
        iconColor = '#7289da'
        iconActiveColor = '#a1b6ff'
        buttonFont = font.Font(family='Uni Sans', weight='bold', size=16)

        sendButton = Button(self, text="Send", width=BUTTON_WIDTH, background=iconColor, foreground='white', activeforeground='white', relief='flat', overrelief='sunken', activebackground=iconActiveColor, font=buttonFont, command=lambda: self.displayBlockchain())
        addFriendButton = Button(text="Add Friend", width=BUTTON_WIDTH, background=iconColor, foreground='white', activeforeground='white', relief='flat', overrelief='sunken', activebackground=iconActiveColor, font=buttonFont)
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
        balanceString = "Balance: "
        nodeString = "   Nodes: "
        balanceLabel = Label(self, text=balanceString, background='#23272a', foreground='white', font=buttonFont).place(x=20, y=420)
        nodesLabel = Label(self, text=nodeString, background='#23272a', foreground='white', font=buttonFont).place(x=20, y=460)