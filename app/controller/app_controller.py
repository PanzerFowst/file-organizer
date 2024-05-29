# app/controller/app_controller.py

from model.app_model import Model
from view.app_view import View


class Controller:
    def __init__(self, model, view):
        self.model: Model = model
        self.view: View = view

        # Set save action of the view:
        self.view.set_action_on_save(self.save)

    def save(self, email: str) -> None:
        """
        Save the email
        :param email:
        :return:
        """
        try:

            # Save to the model:
            self.model.email = email
            self.model.save()

            # Show a success message:
            self.view.show_success(f'The email {email} saved!')

        except ValueError as error:
            # Show an error message:
            self.view.show_error(str(error))
