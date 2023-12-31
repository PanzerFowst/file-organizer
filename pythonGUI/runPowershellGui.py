import subprocess
import sys
import os

from tkinter import *
from tkinter import ttk
from tkinter import filedialog



class GUI:

    def __init__(self):

        # Initialize the root widget
        self.root = Tk()
        # Title of the window
        self.root.title("File Lister")
        # Window color, size, & cursor
        self.root.configure(bg='#f3f0ea', width = 800, height = 500)
        # Whether the window is x, y resizable (False)
        self.root.resizable(False, False)

        self.is_creating_output_dir = BooleanVar()
        self.is_safe_mode = BooleanVar()
        self.is_creating_new_directories = BooleanVar()
        self.is_deleting_empty_directories = BooleanVar()
        self.is_adding_count_str = BooleanVar()
        self.is_adding_date_str = BooleanVar()
        self.is_moving_files = BooleanVar()

        # Title for main window
        self.LabelMainWindow = Label(self.root,
                                text = "File Lister",
                                font = ("Segoe UI", 14, 'bold'),
                                fg = '#3d4244',
                                justify = LEFT,
                                bg='#f3f0ea')
        self.LabelMainWindow.place(relheight = 0.15, relx = 0.10, rely = 0.00)


        # Label for the filepath row header
        self.LabelInputPath = Label(self.root,
                                        text = "Input Path: ",
                                        bg='#f3f0ea')
        self.LabelInputPath.place(relheight = 0.2, relx = 0.117, rely = 0.3)

        # Label for the filepath text
        self.LabelSelectedInputPath = Label(self.root,
                                            text = "Select the input path.",
                                            bg='#f3f0ea')
        self.LabelSelectedInputPath.place(relheight = 0.2, relx = 0.23, rely = 0.3)

        # Label for the output path row header
        self.LabelOutputPath = Label(self.root,
                                            text = "Output Path: ",
                                            bg='#f3f0ea')
        self.LabelOutputPath.place(relheight = 0.2, relx = 0.1, rely = 0.51)

        # Label for the output path text
        self.LabelSelectedOutputPath = Label(self.root,
                                            text = "Select an output path.",
                                            bg='#f3f0ea')
        self.LabelSelectedOutputPath.place(relheight = 0.2, relx = 0.228, rely = 0.51)


        # Input File Browse button
        self.button_input_browse = ttk.Button(self.root,
                                                text = "Browse...",
                                                command = self.get_input_path_cb,
                                                cursor="hand2")
        self.button_input_browse.place(relx = 0.53, rely = 0.315)

        # Output Path Browse button
        self.button_output_browse = ttk.Button(self.root,
                                                text = "Browse...",
                                                command = self.get_output_path_cb,
                                                cursor="hand2")
        self.button_output_browse.place(relx = 0.53, rely = 0.52)

        # Output Path Create Output Directory Checkbox
        self.checkbutton_create_output_dir = Checkbutton(self.root, text = "Create ./output/ Directory",
                                                            variable = self.is_creating_output_dir,
                                                            command = self.check_button_create_output_dir_cb,
                                                            cursor="hand2")
        self.checkbutton_create_output_dir.place(relx = 0.7, rely = 0.52)

        # Safe Mode Checkbox
        self.checkbutton_safe_mode = Checkbutton(self.root, text = "Prints potential files to console without copying or moving the files",
                                                            variable = self.is_safe_mode,
                                                            cursor="hand2")
        self.checkbutton_safe_mode.place(relx = 0.1, rely = 0.65)

        # Create New Directories Checkbox
        self.checkbutton_create_new_dir = Checkbutton(self.root, text = "Should the script create folders if they don't exist?",
                                                            variable = self.is_creating_new_directories,
                                                            cursor="hand2")
        self.checkbutton_create_new_dir.place(relx = 0.1, rely = 0.70)

        # Delete Empty Directories Checkbox
        self.checkbutton_delete_empty_dir = Checkbutton(self.root, text = "Should the script delete folders if they are empty?",
                                                            variable = self.is_deleting_empty_directories,
                                                            cursor="hand2")
        self.checkbutton_delete_empty_dir.place(relx = 0.1, rely = 0.75)

        # Move/Copy Radio Buttons
        self.radiobutton_move_files = Radiobutton(self.root, text = "Move Files",
                                                            variable = self.is_moving_files,
                                                            value=True,
                                                            cursor="hand2")
        self.radiobutton_move_files.place(relx = 0.1, rely = 0.80)
        self.radiobutton_copy_files = Radiobutton(self.root, text = "Copy Files",
                                                            variable = self.is_moving_files,
                                                            value=False,
                                                            cursor="hand2")
        self.radiobutton_copy_files.place(relx = 0.1, rely = 0.85)

        # Add Count Strings Checkbox
        self.checkbutton_add_count_str = Checkbutton(self.root, text = "Should the script add count string?",
                                                            variable = self.is_adding_count_str,
                                                            cursor="hand2")
        self.checkbutton_add_count_str.place(relx = 0.1, rely = 0.90)

        # Add Date Strings Checkbox
        self.checkbutton_add_date_str = Checkbutton(self.root, text = "Should the script add date string?",
                                                            variable = self.is_adding_date_str,
                                                            cursor="hand2")
        self.checkbutton_add_date_str.place(relx = 0.1, rely = 0.95)

        # Cancel button
        self.button_cancel = ttk.Button(self.root,
                                            text = "Cancel",
                                            command = self.cancel_button_cb,
                                            cursor="hand2")
        self.button_cancel.place(relx = 0.78, rely = 0.92)

        # Add Run button
        self.button_run = ttk.Button(self.root,
                                        text = "Run",
                                        command = self.run_button_cb)
        self.button_run.place(relx = 0.89, rely = 0.92)
        self.button_run["state"] = DISABLED

        #####################
        # Uses display; responds to input until termination
        #####################

        self.root.mainloop()


    #####################
    # Button Callbacks:
    #####################

    def get_input_path_cb(self):
        # Set global file_path var
        global input_path
        # Open file dialog accepting only .pbix files; path will be the file_path var
        input_path = filedialog.askdirectory(title = "Select An Input Directory")

        if not os.path.exists(input_path):
            # Do nothing if the path is empty or not valid:
            return

        # Hide button after push
        self.button_input_browse.place_forget()
        # Update text label with file path
        self.LabelSelectedInputPath.config(text=input_path, bg='#f3f0ea')
        # Call checkbox callback to update in case box is checked:
        self.check_button_create_output_dir_cb()
        # Update 'OK' button state once the file dialog is done
        self.button_run["state"] = NORMAL
        self.button_run["cursor"] = "hand2"

    def get_output_path_cb(self):
        # Set global file_path var
        global output_path
        # Open and return file path as file_path var
        output_path = filedialog.askdirectory(title = "Select An Output Destination")

        if not os.path.exists(output_path):
            # Do nothing if the path is empty or not valid:
            return

        # Hide button after push
        self.button_output_browse.place_forget()
        # Update text label with file path
        self.LabelSelectedOutputPath.config(text=output_path, bg='#f3f0ea')

    def check_button_create_output_dir_cb(self):
        global output_path
        if self.is_creating_output_dir.get():
            # Hide the output browse button when checkbox is selected:
            self.button_output_browse.place_forget()
            # Catch if user selects the checkbox before selecting the input path:
            try:
                temp = input_path + f'/output'
                output_path = temp
            except NameError:
                temp = "Select an input path."
            self.LabelSelectedOutputPath.config(text=temp)
        else:
            # Show the output browse button when checkbox is not selected:
            self.button_output_browse.place(relx = 0.53, rely = 0.52)
            # Clear output path:
            output_path = None
            self.LabelSelectedOutputPath.config(text="Select an output path.")

    def cancel_button_cb(self):
        self.root.destroy()
        exit()

    def run_button_cb(self):
        run_powershell_list_files(input_path)
        # Ends the tkinter window and continues the script; doesn't exit()
        self.root.destroy()


def run_powershell_list_files(file_path):

    powershell_script_path = os.path.abspath(".\\listFiles.ps1")

    p = subprocess.Popen(
        f'powershell.exe -ExecutionPolicy RemoteSigned -file "{powershell_script_path}" -basepath "{file_path}"',
        stdout=sys.stdout,
    )
    p.communicate()


def main():
    GUI()
    exit()


if __name__ == "__main__":
    main()
