# app/main.py

from controller.app_controller import Controller
from model.app_model import Model
from view.app_view import View


VERSION: int = 0
MAJOR: int = 1
MINOR: int = 0
VERSION_STRING: str = f"v{MAJOR}.{MINOR}.{VERSION}"


def main():

    # create a model
    model = Model()

    # create a view
    view = View(version_major_minor=(VERSION, MAJOR, MINOR))

    # create a controller (might technically be called a presenter?)
    controller = Controller(model, view)
    controller.run()


if __name__ == "__main__":
    main()
