# app/controller/app_controller.py

from __future__ import annotations
from typing import Protocol

from model.app_model import Model


class View(Protocol):

    def init_ui(self, controller: Controller) -> None:
        ...

    def handle_finished_execution(self) -> None:
        ...

    def write_to_progress_display(self, text: str) -> None:
        ...

    def mainloop(self) -> None:
        ...


class Controller:
    def __init__(self, model: Model, view: View):
        self.model: Model = model
        self.view: View = view

    def run(self) -> None:
        self.model.init_model(self)
        self.view.init_ui(self)
        # TODO: Any other initialization here...?
        self.view.mainloop()

    def handle_started_execution(self, input_path: str, output_path: str, options_dict: dict[str, bool]) -> None:

        # Set printing callback:
        self.model.set_output_callback(self.view.write_to_progress_display)

        # Set the paths and start the powershell script:
        try:
            # Set Model options:
            self.model.input_path = input_path
            self.model.output_path = output_path
            self.model.is_safe_mode = options_dict["is_safe_mode"]
            self.model.is_creating_new_directories = options_dict["is_creating_new_directories"]
            self.model.is_deleting_empty_directories = options_dict["is_deleting_empty_directories"]
            self.model.is_moving_files = options_dict["is_moving_files"]
            self.model.is_adding_count_str = options_dict["is_adding_count_str"]
            self.model.is_adding_date_str = options_dict["is_adding_date_str"]

            self.model.run_powershell_list_files()

        except ValueError as e:
            self.view.write_to_progress_display(f"Error setting input/output paths:\n\t{e}")
            self.view.write_to_progress_display(f"\n\nRestart the application and try again...")
            # TODO: Handle error better...?

    def handle_finished_execution(self) -> None:
        self.view.handle_finished_execution()
