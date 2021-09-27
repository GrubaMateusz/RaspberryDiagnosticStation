import tkinter as tk

from PyQt5 import QtWidgets, QtGui, QtCore

import tkinter as tk


class Foo(tk.Tk):
    def __init__(self):
        super().__init__()
        self.callId = None
        self.button = tk.Button(self, text="Stop", command=self.stop)
        self.button.pack()

    def periodically_speak(self):
        print("Hello world!")
        self.callId = self.after(1000, self.periodically_speak)

    def stop(self):
        if self.callId is not None:
            self.after_cancel(self.callId)


foo = Foo()
foo.periodically_speak()






class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.btnStartMes = tk.Button(self)
        self.btnStartMes["text"] = "Left Wheel"
        self.btnStartMes["command"] = self.runMesurment
        self.btnStartMes.pack(side="bottom")

        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.pack(side="bottom")

    def runMesurment(self):
        print("hi there, everyone!")


root = tk.Tk()
root.geometry("600x600")

app = Application(master=root)
app.mainloop()
