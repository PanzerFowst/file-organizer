# app/controller/app_controller.py

from enum import Enum
from tkinter import Tk
from tkinter.ttk import Frame
import tkinter as tk

from view.page import Page
from model.app_model import Model
from view.app_view import GuiStartPage
from view.app_view_progress import GuiProgressPage


class PossiblePages(Enum):
    NONE = "None"
    START = GuiStartPage.__name__
    PROGROSS = GuiProgressPage.__name__
    DONE = "Done"


class Controller:
    def __init__(self, parent: Tk, model: Model, views: list[Page]):
        self.parent = parent
        self.model = model

        self.current_frame: Frame
        self.current_page: PossiblePages

        self.views: dict[str, Page] = {}
        for view in views:
            page_name = view.__class__.__name__
            self.views[page_name] = view
            # Set callback function to get to next frame:
            view.set_next_page_cb(self.advance_frame)
            # Set each frame on top of each other:
            view.grid(row=0, column=0, sticky=tk.NSEW)

        self.current_page = PossiblePages.NONE
        self.advance_frame()

    def show_frame(self, page: PossiblePages):
        '''Show a frame for the given page name'''
        self.current_page = page
        self.current_frame = self.views[page.value]
        self.current_frame.tkraise()

    def advance_frame(self):
        '''Show a frame for the given page name'''
        if self.current_page == PossiblePages.NONE:
            self.show_frame(PossiblePages.START)
        elif self.current_page == PossiblePages.START:
            start_page = self.views[PossiblePages.START.value]
            assert isinstance(start_page, GuiStartPage), f"Expected GuiStartPage, got {type(start_page).__name__}"
            progress_page = self.views[PossiblePages.PROGROSS.value]
            assert isinstance(
                progress_page, GuiProgressPage), f"Expected GuiProgressPage, got {
                type(progress_page).__name__}"
            progress_page.input_path = start_page.input_path
            progress_page.output_path = start_page.output_path
            progress_page.update_labels()
            self.model.input_path = progress_page.input_path
            self.model.output_path = progress_page.output_path
            self.show_frame(PossiblePages.PROGROSS)
            self.model.run_powershell_list_files()
        else:
            self.parent.destroy()
