# app/main.py

from controller.app_controller import Controller
from model.app_model import Model
from view.app_view import View


def main():

    # create a model
    model = Model()

    # create a view
    view = View()

    # create a controller (might technically be called a presenter?)
    controller = Controller(model, view)
    controller.run()


if __name__ == "__main__":
    main()
