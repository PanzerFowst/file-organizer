# app/view/app_view.py

import subprocess
import sys
import os

# from typing import Callable

from tkinter.ttk import Frame, Button
from tkinter import Tk, filedialog
from tkinter import Label, Checkbutton, Radiobutton, BooleanVar
import tkinter as tk


class View(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent: Tk = parent
        self.input_path: str = ""
        self.output_path: str = ""

        # # set the save action callback
        # self.save_action: Callable[[str], None]

        self.is_creating_output_dir = BooleanVar()
        self.is_safe_mode = BooleanVar()
        self.is_creating_new_directories = BooleanVar()
        self.is_deleting_empty_directories = BooleanVar()
        self.is_adding_count_str = BooleanVar()
        self.is_adding_date_str = BooleanVar()
        self.is_moving_files = BooleanVar()

        # Title for main window
        self.LabelMainWindow = Label(self,
                                     text="File Lister",
                                     font=("Segoe UI", 14, 'bold'),
                                     fg='#3d4244',
                                     justify=tk.LEFT,
                                     bg='#f3f0ea')
        self.LabelMainWindow.grid(row=0, column=0, pady=20)

        # Label for the filepath row header
        self.LabelInputPath = Label(self,
                                    text="Input Path: ",
                                    bg='#f3f0ea')
        self.LabelInputPath.grid(row=1, column=0, sticky=tk.E)

        # Label for the filepath text
        self.LabelSelectedInputPath = Label(self,
                                            text="Select the input path.",
                                            bg='#f3f0ea')
        self.LabelSelectedInputPath.grid(row=1, column=1, sticky=tk.W)

        # Label for the output path row header
        self.LabelOutputPath = Label(self,
                                     text="Output Path: ",
                                     bg='#f3f0ea')
        self.LabelOutputPath.grid(row=2, column=0, sticky=tk.E)

        # Label for the output path text
        self.LabelSelectedOutputPath = Label(self,
                                             text="Select an output path.",
                                             bg='#f3f0ea')
        self.LabelSelectedOutputPath.grid(row=2, column=1, sticky=tk.W)

        # Input File Browse button
        self.button_input_browse = Button(self,
                                          text="Browse...",
                                          command=self.get_input_path_cb,
                                          cursor="hand2")
        self.button_input_browse.grid(row=1, column=2, sticky=tk.E)

        # Output Path Browse button
        self.button_output_browse = Button(self,
                                           text="Browse...",
                                           command=self.get_output_path_cb,
                                           cursor="hand2")
        self.button_output_browse.grid(row=2, column=2, sticky=tk.E)

        # Output Path Create Output Directory Checkbox
        self.checkbutton_create_output_dir = Checkbutton(self, text="Create ./output/ Directory",
                                                         variable=self.is_creating_output_dir,
                                                         command=self.check_button_create_output_dir_cb,
                                                         cursor="hand2")
        self.checkbutton_create_output_dir.grid(row=2, column=3, padx=20, sticky=tk.W)

        buttonOptionsFrame = Frame(self)
        buttonOptionsFrame.grid(row=3, column=1, sticky=tk.W)

        # Safe Mode Checkbox
        self.checkbutton_safe_mode = Checkbutton(
            buttonOptionsFrame,
            text="Prints potential files to console without copying or moving the files",
            variable=self.is_safe_mode,
            cursor="hand2")
        self.checkbutton_safe_mode.grid(row=0, column=0, sticky=tk.W)

        # Create New Directories Checkbox
        self.checkbutton_create_new_dir = Checkbutton(
            buttonOptionsFrame,
            text="Should the script create folders if they don't exist?",
            variable=self.is_creating_new_directories,
            cursor="hand2")
        self.checkbutton_create_new_dir.grid(row=1, column=0, sticky=tk.W)

        # Delete Empty Directories Checkbox
        self.checkbutton_delete_empty_dir = Checkbutton(
            buttonOptionsFrame,
            text="Should the script delete folders if they are empty?",
            variable=self.is_deleting_empty_directories,
            cursor="hand2")
        self.checkbutton_delete_empty_dir.grid(row=2, column=0, sticky=tk.W)

        # Move/Copy Radio Buttons
        moveCopyRadioFrame = Frame(buttonOptionsFrame)
        moveCopyRadioFrame.grid(row=3, column=0, sticky=tk.W)
        self.radiobutton_move_files = Radiobutton(moveCopyRadioFrame, text="Move Files",
                                                  variable=self.is_moving_files,
                                                  value=True,
                                                  cursor="hand2")
        self.radiobutton_move_files.grid(row=0, column=0, sticky=tk.E)
        self.radiobutton_copy_files = Radiobutton(moveCopyRadioFrame, text="Copy Files",
                                                  variable=self.is_moving_files,
                                                  value=False,
                                                  cursor="hand2")
        self.radiobutton_copy_files.grid(row=0, column=1, sticky=tk.W)

        # Add Count Strings Checkbox
        self.checkbutton_add_count_str = Checkbutton(buttonOptionsFrame, text="Should the script add count string?",
                                                     variable=self.is_adding_count_str,
                                                     cursor="hand2")
        self.checkbutton_add_count_str.grid(row=4, column=0, sticky=tk.W)

        # Add Date Strings Checkbox
        self.checkbutton_add_date_str = Checkbutton(buttonOptionsFrame, text="Should the script add date string?",
                                                    variable=self.is_adding_date_str,
                                                    cursor="hand2")
        self.checkbutton_add_date_str.grid(row=5, column=0, sticky=tk.W)

        # Cancel button
        self.button_cancel = Button(self,
                                    text="Cancel",
                                    command=self.cancel_button_cb,
                                    cursor="hand2")
        self.button_cancel.grid(row=4, column=3, padx=0, sticky=tk.E)

        # Add Run button
        self.button_run = Button(self,
                                 text="Run",
                                 command=self.run_button_cb)
        self.button_run.grid(row=4, column=4, padx=0, sticky=tk.W)
        self.button_run["state"] = tk.DISABLED
        self.button_run["cursor"] = ""

    # def set_action_on_save(self, action_on_save: Callable[[str], None]) -> None:
    #     """
    #     Set the controller
    #     :param controller:
    #     :return:
    #     """
    #     self.save_action = action_on_save

    def check_if_ready_to_run(self):
        # Update 'Run' button state once the file dialog is done:
        if os.path.exists(self.input_path) and (os.path.exists(self.output_path) or self.is_creating_output_dir.get()):
            self.button_run["state"] = tk.NORMAL
            self.button_run["cursor"] = "hand2"
        else:
            self.button_run["state"] = tk.DISABLED
            self.button_run["cursor"] = ""

    #####################
    # Button Callbacks:
    #####################

    def get_input_path_cb(self):
        # Open file dialog accepting only .pbix files; path will be the file_path var
        self.input_path = filedialog.askdirectory(title="Select An Input Directory")

        if not os.path.exists(self.input_path):
            # Do nothing if the path is empty or not valid:
            return

        # Hide button after push
        self.button_input_browse.grid_remove()
        # Update text label with file path
        self.LabelSelectedInputPath.config(text=self.input_path, bg='#f3f0ea')
        # Call checkbox callback to update in case box is checked:
        self.check_button_create_output_dir_cb()
        # Update 'Run' button status:
        self.check_if_ready_to_run()

    def get_output_path_cb(self):
        # Open and return file path as file_path var
        self.output_path = filedialog.askdirectory(title="Select An Output Destination")

        if not os.path.exists(self.output_path):
            # Do nothing if the path is empty or not valid:
            return

        # Hide button after push
        self.button_output_browse.grid_remove()
        # Update text label with file path
        self.LabelSelectedOutputPath.config(text=self.output_path, bg='#f3f0ea')
        # Update 'Run' button status:
        self.check_if_ready_to_run()

    def check_button_create_output_dir_cb(self):

        if self.is_creating_output_dir.get():
            # Hide the output browse button when checkbox is selected:
            self.button_output_browse.grid_remove()
            # Catch if user selects the checkbox before selecting the input path:
            if os.path.exists(self.input_path):
                temp = self.input_path + f'/output'
                self.output_path = temp
            else:
                temp = "Select an input path."
            self.LabelSelectedOutputPath.config(text=temp)
        else:
            # Show the output browse button when checkbox is not selected:
            self.button_output_browse.grid()
            # Clear output path:
            self.output_path = ""
            self.LabelSelectedOutputPath.config(text="Select an output path.")

        # Update 'Run' button status:
        self.check_if_ready_to_run()

    def cancel_button_cb(self):
        self.parent.destroy()
        # exit()

    def run_button_cb(self):
        run_powershell_list_files(self.input_path)
        # Ends the tkinter window and continues the script; doesn't exit()
        self.parent.destroy()


def run_powershell_list_files(file_path):

    powershell_script_path = os.path.abspath(".\\model\\listFiles.ps1")

    p = subprocess.Popen(
        f'powershell.exe -ExecutionPolicy RemoteSigned -file "{powershell_script_path}" -basepath "{file_path}"',
        stdout=sys.stdout,
    )
    p.communicate()
