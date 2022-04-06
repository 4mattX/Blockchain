from tkinter import Tk, Text, BOTH, W, N, E, S, Frame, Button, PhotoImage, Button, Label, Canvas, Text


class SettingsApp(Frame):

    def __init__(self):
        super().__init__()

        self.canvas = None
        self.frameColor = '#2c2f33'

        self.initUI()

    def initUI(self):


        self.pack(fill=BOTH, expand=1)

        self.master.update_idletasks()
        width = self.master.winfo_width()
        height = self.master.winfo_height()

        # Canvas Stuff
        self.canvas = Canvas(self, background=self.frameColor, width=width, height=height, highlightthickness=0).place(x=100, y=0)

