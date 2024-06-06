# app/controller/app_controller.py

import tkinter as tk

from model.app_model import Model
from view.app_view import View


class Controller:
    def __init__(self, parent: tk.Tk, model: Model, view: View):
        self.parent: tk.Tk = parent
        self.model: Model = model
        self.view: View = view

    #     self.current_frame: Frame
    #     self.current_page: PossiblePages

    #     self.views: dict[str, Page] = {}
    #     for view in views:
    #         page_name = view.__class__.__name__
    #         self.views[page_name] = view
    #         # Set callback function to get to next frame:
    #         view.set_next_page_cb(self.advance_frame)
    #         # Set each frame on top of each other:
    #         view.grid(row=0, column=0, sticky=tk.NSEW)

    #     self.current_page = PossiblePages.NONE
    #     self.advance_frame()

    # def show_frame(self, page: PossiblePages):
    #     '''Show a frame for the given page name'''
    #     self.current_page = page
    #     self.current_frame = self.views[page.value]
    #     self.current_frame.tkraise()

    # def advance_frame(self):
    #     '''Show a frame for the given page name'''
    #     if self.current_page == PossiblePages.NONE:
    #         self.show_frame(PossiblePages.START)
    #     elif self.current_page == PossiblePages.START:
    #         start_page = self.views[PossiblePages.START.value]
    #         assert isinstance(start_page, GuiStartPage), f"Expected GuiStartPage, got {type(start_page).__name__}"
    #         progress_page = self.views[PossiblePages.PROGROSS.value]
    #         assert isinstance(
    #             progress_page, GuiProgressPage), f"Expected GuiProgressPage, got {
    #             type(progress_page).__name__}"
    #         progress_page.input_path = start_page.input_path
    #         progress_page.output_path = start_page.output_path
    #         progress_page.update_labels()
    #         self.model.input_path = progress_page.input_path
    #         self.model.output_path = progress_page.output_path
    #         self.show_frame(PossiblePages.PROGROSS)
    #         self.model.run_powershell_list_files()
    #     else:
    #         self.parent.destroy()

    #     # Set save action of the view:
    #     self.view.set_action_on_save(self.save)

    # def save(self, email: str) -> None:
    #     """
    #     Save the email
    #     :param email:
    #     :return:
    #     """
    #     try:

    #         # Save to the model:
    #         self.model.email = email
    #         self.model.save()

    #         # Show a success message:
    #         self.view.show_success(f'The email {email} saved!')

    #     except ValueError as error:
    #         # Show an error message:
    #         self.view.show_error(str(error))
