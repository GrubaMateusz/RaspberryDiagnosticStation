import tkinter as tk


class Foo(tk.Tk):
    def __init__(self):
        super().__init__()
        self.callId = None
        self.button = tk.Button(self, text="Stop", command=self.stop)
        self.button.pack()

    def periodically_speak(self):
        print("Hello world!")
        self.callId = self.after(2000, self.periodically_speak)

    def stop(self):
        if self.callId is not None:
            self.after_cancel(self.callId)


foo = Foo()
foo.periodically_speak()
