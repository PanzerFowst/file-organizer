# app/main.py

import tkinter as tk

# from view.gui import GUI
from controller.app_controller import Controller
from model.app_model import Model
from view.app_view import View


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Tkinter MVC Demo')

        # create a model
        model = Model()

        # create a view and place it on the root window
        view = View(self)
        view.grid(row=0, column=0, padx=10, pady=10)

        # create a controller
        controller = Controller(model, view)


def main():

    # Start GUI:
    # gui = GUI()

    #####################
    # Uses display; responds to input until termination
    #####################

    # gui.root.mainloop()

    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()
