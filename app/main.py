# app/main.py

import tkinter as tk

from controller.app_controller import Controller
from model.app_model import Model
from view.app_view import View


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        # Title of the window:
        self.title("File Lister")
        # Window background color, size, & cursor:
        self.configure(bg='#f3f0ea', width=800, height=500)
        # Whether the window is x, y resizable (False)
        self.resizable(False, False)

        # create a model
        model = Model()

        # create a view and place it on the root window
        view = View(self)
        view.grid(row=0, column=0, padx=10, pady=10)

        # create a controller
        controller = Controller(model, view)


def main():

    # Start application:
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()
