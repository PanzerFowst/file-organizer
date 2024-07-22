# app/view/app_view.py

from os import path
from typing import Protocol

from tkinter import ttk, filedialog, scrolledtext
import tkinter as tk


class Controller(Protocol):
    def handle_started_execution(self, input_path: str, output_path: str, options_dict: dict[str, bool]) -> None:
        ...


class View(tk.Tk):
    def __init__(self, version_major_minor: tuple[int, int, int]):
        super().__init__()

        self.VERSION: int = version_major_minor[0]
        self.MAJOR: int = version_major_minor[1]
        self.MINOR: int = version_major_minor[2]

        # Title of the window:
        self.title("File Lister")
        # Window background color & size:
        self.configure(bg='#f3f0ea')
        # Place window:
        width = 800  # self.winfo_width()
        height = 800  # self.winfo_height()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - width) // 2 + 500
        y = (screen_height - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")
        # Whether the window is x, y resizable (False):
        self.resizable(False, False)
        # Set the application to always remain on top:
        self.wm_attributes("-topmost", True)

    def init_view(self, controller: Controller) -> None:

        self.main_window = MainWindow(self, controller)

        # Application version frame label:
        version_frame = ttk.Frame(master=self.main_window)
        version_label = tk.Label(  # ttk.Label(
            master=version_frame,
            text=f"v{self.VERSION}.{self.MAJOR}.{self.MINOR}",
            font=("Segoe UI", 8),
        )

        # version_frame:
        version_label.pack(padx=(5, 0), side=tk.LEFT)
        version_frame.place(relx=0, rely=1, anchor=tk.SW)

    def write_to_progress_display(self, text: str) -> None:
        # Update the progress display text widget:
        self.main_window.progress_display_text.insert(tk.END, text)
        self.main_window.progress_display_text.see(tk.END)
        # Update the progress bar:
        self.main_window.progressbar.step()

    def handle_finished_execution(self) -> None:
        # self.main_window.button_run.configure(text="OK", command=lambda: ...)
        self.main_window.progressbar.stop()


class MainWindow(ttk.Frame):
    def __init__(self, master: tk.Tk, controller: Controller) -> None:
        super().__init__(master)

        self.place(relx=0, rely=0, relwidth=1, relheight=1)

        # Class variables:
        self.master: tk.Tk = master
        self.input_path: str = ""
        self.output_path: str = ""

        # tkinter variables:
        self.options_dict: dict[str, tk.Variable] = {}

        # TODO: Is this the best way to save reference?
        self.controller: Controller = controller

        ##
        ### Create widgets:

        title_frame = self.init_title_frame(master=self)
        self.body_frame = self.init_body_frame(master=self)

        ##
        ### Place widgets:

        title_frame.pack(fill=tk.X)
        self.body_frame.pack(expand=True, fill=tk.BOTH)

    ###########################
    # Frame Creation Methods: #
    ###########################

    def init_title_frame(self, master) -> ttk.Frame:

        ### Create widgets:

        title_frame: ttk.Frame = ttk.Frame(master=master)

        # Title for main window
        title_frame_label = tk.Label(  # ttk.Label(
            master=title_frame,
            text="File Lister",
            font=("Segoe UI", 20, 'bold'),
            fg='#3d4244',
            bg='#f3f0ea',
        )

        ##
        ### Place widgets:

        title_frame_label.pack(padx=15, pady=10, anchor=tk.W)

        return title_frame

    def init_body_frame(self, master) -> ttk.Frame:

        ### Create widgets:

        body_frame: ttk.Frame = ttk.Frame(master=master)

        # Frame containing the buttons and labels to select the paths for the application:
        run_paths_frame = self.init_run_paths_frame(master=body_frame)

        # Frame containing the buttons to select different options of the application:
        options_frame = self.init_options_frame(master=body_frame)

        # Application actions frame:
        actions_frame = ttk.Frame(master=body_frame)
        actions_subframe = ttk.Frame(master=actions_frame)
        # Cancel Button
        self.button_cancel = ttk.Button(
            master=actions_subframe,
            text="Cancel",
            command=self.cancel_button_cb,
            cursor="hand2",
        )
        # Run Button
        self.button_run = ttk.Button(
            master=actions_subframe,
            text="Run",
            command=self.run_button_cb,
            cursor="",
            state=tk.DISABLED,
        )

        ##
        ### Place widgets:

        # Configure rows & columns:
        body_frame.grid_columnconfigure(index=0, weight=1, uniform='a')
        body_frame.grid_columnconfigure(index=1, weight=25, uniform='a')

        # actions_frame:
        self.button_cancel.pack(padx=7, side=tk.LEFT)
        self.button_run.pack(padx=7, side=tk.LEFT)
        actions_subframe.pack(padx=15, pady=15)
        # Frames:
        run_paths_frame.grid(row=0, column=1, pady=(5, 10), sticky=tk.W)
        options_frame.grid(row=1, column=1, pady=(0, 10), sticky=tk.W)
        actions_frame.place(relx=1, rely=1, anchor=tk.SE)

        ttk.Style().configure('Custom.TFrame', background='blue')
        body_frame.configure(style='Custom.TFrame')
        return body_frame

    def init_run_paths_frame(self, master) -> ttk.Frame:

        ### Create widgets:

        run_paths_frame = ttk.Frame(master=master)

        ## Title for the run_paths_frame:
        run_paths_frame_title = ttk.Frame(master=run_paths_frame)
        run_paths_frame_title_label = tk.Label(  # ttk.Label(
            master=run_paths_frame_title,
            text="Script Run Paths:",
            font=("Segoe UI", 12, 'underline'),
            fg='#194D33',
            bg='#ff00c8',
        )

        ## Options for the run_paths_frame:
        run_paths_frame_options = ttk.Frame(master=run_paths_frame)

        # Label for the filepath row header
        input_path_label = tk.Label(  # ttk.Label(
            master=run_paths_frame_options,
            text="Input Path: ",
            bg='#f3f0ea',
        )
        # Label for the output path row header
        output_path_label = tk.Label(  # ttk.Label(
            master=run_paths_frame_options,
            text="Output Path: ",
            bg='#f3f0ea',
        )

        # Label for the filepath text
        self.label_selected_input_path = tk.Label(  # ttk.Label(
            master=run_paths_frame_options,
            text="Select the input path.",
            bg='#f3f0ea',
        )
        # Label for the output path text
        self.label_selected_output_path = tk.Label(  # ttk.Label(
            master=run_paths_frame_options,
            text="Select an output path.",
            bg='#f3f0ea',
        )

        # Input File Browse button
        self.button_input_browse = ttk.Button(
            master=run_paths_frame_options,
            text="Browse...",
            command=self.get_input_path_cb,
            cursor="hand2",
        )
        # Output Path Browse button
        self.button_output_browse = ttk.Button(
            master=run_paths_frame_options,
            text="Browse...",
            command=self.get_output_path_cb,
            cursor="hand2",
        )

        # Output Path Create Output Directory Checkbox
        self.is_creating_output_dir = tk.BooleanVar(name="is_creating_output_dir", value=False)
        self.options_dict[str(self.is_creating_output_dir)] = self.is_creating_output_dir
        self.checkbutton_create_output_dir = ttk.Checkbutton(
            master=run_paths_frame_options, text="Create ./output/ Directory",
            variable=self.is_creating_output_dir,
            command=self.check_button_create_output_dir_cb,
            cursor="hand2",
        )

        ##
        ### Place widgets:

        # Place in run_paths_frame_title placement:
        run_paths_frame_title_label.pack(anchor=tk.W)

        # Place in run_paths_frame_options grids:
        run_paths_frame_options.grid_rowconfigure(index=(0, 1), weight=1, uniform='a')

        input_path_label.grid(row=0, column=0, sticky=tk.E)
        output_path_label.grid(row=1, column=0, sticky=tk.E)

        self.label_selected_input_path.grid(row=0, column=1, sticky=tk.W)
        self.label_selected_output_path.grid(row=1, column=1, sticky=tk.W)

        self.button_input_browse.grid(row=0, column=2, sticky=tk.EW)
        self.button_output_browse.grid(row=1, column=2, sticky=tk.EW)

        self.checkbutton_create_output_dir.grid(row=1, column=3, padx=20, sticky=tk.W)

        # Place subframes:
        run_paths_frame_title.pack(fill=tk.X)
        run_paths_frame_options.pack()

        return run_paths_frame

    def init_options_frame(self, master) -> ttk.Frame:

        ### Create widgets:

        options_frame = ttk.Frame(master=master)

        ## Title for the options_frame:
        options_frame_title = ttk.Frame(master=options_frame)
        options_frame_title_label = tk.Label(  # ttk.Label(
            master=options_frame_title,
            text="Script Options:",
            font=("Segoe UI", 12, 'underline'),
            fg='#194D33',
            bg='#ff00c8',
        )

        ## Button options for the options_frame:
        options_frame_buttons = ttk.Frame(master=options_frame)

        # Safe Mode Checkbox
        self.is_safe_mode = tk.BooleanVar(name="is_safe_mode", value=True)
        self.options_dict[str(self.is_safe_mode)] = self.is_safe_mode
        style = ttk.Style()     # Configure a unique style with bold text
        style.configure("CustomBold.TCheckbutton", font=("TkDefaultFont", 10, "bold"))
        self.checkbutton_safe_mode = ttk.Checkbutton(
            master=options_frame_buttons,
            text="Safe Mode",
            style="CustomBold.TCheckbutton",
            variable=self.is_safe_mode,
            cursor="hand2",
            command=self.update_options_cb,
        )
        self.is_safe_mode_label = tk.Label(  # ttk.Label(
            master=options_frame_buttons,
            text="...",
        )
        # Move/Copy Radio Buttons
        self.is_moving_files = tk.BooleanVar(name="is_moving_files", value=False)
        self.options_dict[str(self.is_moving_files)] = self.is_moving_files
        self.move_copy_radio_frame = ttk.Frame(master=options_frame_buttons)
        self.radiobutton_move_files = ttk.Radiobutton(
            master=self.move_copy_radio_frame,
            text="Move Files",
            variable=self.is_moving_files,
            value=True,
            cursor="hand2",
            command=self.update_options_cb,
        )
        self.radiobutton_copy_files = ttk.Radiobutton(
            master=self.move_copy_radio_frame,
            text="Copy Files",
            variable=self.is_moving_files,
            value=False,
            cursor="hand2",
            command=self.update_options_cb,
        )
        self.is_moving_files_label = tk.Label(  # ttk.Label(
            master=options_frame_buttons,
            text="...",
        )
        # Create New Directories Checkbox
        self.is_recursive_search = tk.BooleanVar(name="is_recursive_search", value=False)
        self.options_dict[str(self.is_recursive_search)] = self.is_recursive_search
        self.checkbutton_recursive_search_dir = ttk.Checkbutton(
            master=options_frame_buttons,
            text="Recursive Directory Search",
            variable=self.is_recursive_search,
            cursor="hand2",
            command=self.update_options_cb,
        )
        self.is_recursive_search_label = tk.Label(  # ttk.Label(
            master=options_frame_buttons,
            text="...",
            justify="left",
        )
        # Delete Empty Directories Checkbox
        self.is_deleting_empty_directories = tk.BooleanVar(name="is_deleting_empty_directories", value=False)
        self.options_dict[str(self.is_deleting_empty_directories)] = self.is_deleting_empty_directories
        self.checkbutton_delete_empty_dir = ttk.Checkbutton(
            master=options_frame_buttons,
            text="Delete Empty Folders",
            variable=self.is_deleting_empty_directories,
            cursor="hand2",
            command=self.update_options_cb,
        )
        self.is_deleting_empty_directories_label = tk.Label(  # ttk.Label(
            master=options_frame_buttons,
            text="...",
        )
        # Count Strings Checkbox
        self.is_adding_count_str = tk.BooleanVar(name="is_adding_count_str", value=True)
        self.options_dict[str(self.is_adding_count_str)] = self.is_adding_count_str
        self.checkbutton_add_count_str = ttk.Checkbutton(
            master=options_frame_buttons,
            text="Add count string?",
            variable=self.is_adding_count_str,
            cursor="hand2",
            command=self.update_options_cb,
        )
        self.is_adding_count_str_label = tk.Label(  # ttk.Label(
            master=options_frame_buttons,
            text="...",
            justify="left",
        )
        # Date Strings Checkbox
        self.is_adding_date_str = tk.BooleanVar(name="is_adding_date_str", value=False)
        self.options_dict[str(self.is_adding_date_str)] = self.is_adding_date_str
        self.checkbutton_add_date_str = ttk.Checkbutton(
            master=options_frame_buttons,
            text="Add date string?",
            variable=self.is_adding_date_str,
            cursor="hand2",
            command=self.update_options_cb,
        )
        self.is_adding_date_str_label = tk.Label(  # ttk.Label(
            master=options_frame_buttons,
            text="...",
            justify="left",
        )

        ##
        ### Place widgets:

        # Place in options_frame_title placement:
        options_frame_title_label.pack(anchor=tk.W)

        # Place in options_frame_buttons grids:
        self.checkbutton_safe_mode.grid(row=0, column=0, sticky=tk.W)
        self.is_safe_mode_label.grid(row=0, column=1, sticky=tk.W, padx=(10, 0))

        self.radiobutton_move_files.pack(side=tk.LEFT)
        self.radiobutton_copy_files.pack(side=tk.LEFT)
        self.move_copy_radio_frame.grid(row=1, column=0, sticky=tk.W)
        self.is_moving_files_label.grid(row=1, column=1, sticky=tk.W, padx=(10, 0))

        self.checkbutton_recursive_search_dir.grid(row=2, column=0, sticky=tk.NW)
        self.is_recursive_search_label.grid(row=2, column=1, sticky=tk.W, padx=(10, 0))
        self.checkbutton_delete_empty_dir.grid(row=3, column=0, sticky=tk.W)
        self.is_deleting_empty_directories_label.grid(row=3, column=1, sticky=tk.W, padx=(10, 0))
        self.checkbutton_add_count_str.grid(row=4, column=0, sticky=tk.NW)
        self.is_adding_count_str_label.grid(row=4, column=1, sticky=tk.W, padx=(10, 0))
        self.checkbutton_add_date_str.grid(row=5, column=0, sticky=tk.NW)
        self.is_adding_date_str_label.grid(row=5, column=1, sticky=tk.W, padx=(10, 0))

        # Place subframes:
        options_frame_title.pack(fill=tk.X)
        options_frame_buttons.pack()

        # Update the options explanation labels:
        self.update_options_cb()

        return options_frame

    def init_progress_frame(self, master) -> ttk.Frame:

        ### Create widgets:

        progress_frame = ttk.Frame(master=master)

        ## Title for the progress_frame:
        progress_frame_title = ttk.Frame(master=progress_frame)
        progress_frame_title_label = tk.Label(  # ttk.Label(
            master=progress_frame_title,
            text="Progress:",
            font=("Segoe UI", 12, 'underline'),
            fg='#194D33',
            bg='#ff00c8',
        )

        ## Button options for the options_frame:
        progress_frame_status = ttk.Frame(master=progress_frame)

        # Add progressbar:
        self.progressbar = ttk.Progressbar(
            progress_frame_status,
            orient='horizontal',
            mode='indeterminate',
            # length=500,
        )
        self.progressbar.start(3)

        # Add text box for displaying the output from the script:
        self.progress_display_text = scrolledtext.ScrolledText(
            master=progress_frame_status,
            wrap='word',
            width=90,  # in characters
            height=20,  # in lines
            bg='#f3f0ea',
        )
        self.progress_display_text.insert(tk.END, "Progress and output will be displayed here.\n\n")

        def on_keypress(event: tk.Event):
            # List of keys to allow:
            allowed_keys = {
                "Left",
                "Right",
                "Up",
                "Down",
                "Shift_L",
                "Shift_R",
                "Control_L",
                "Control_R",
                "Alt_L",
                "Alt_R",
            }

            if (event.keysym == "c" or event.keysym == "C") and (int(event.state) & (1 << 2)):
                return  # Allow Ctrl + C for copying
            elif event.keysym in allowed_keys:
                return  # Allow other allowed keys
            else:
                # Ignore all other keypress events
                return "break"
        self.progress_display_text.bind("<KeyPress>", on_keypress)

        ##
        ### Place widgets:

        # Place in options_frame_title placement:
        progress_frame_title_label.pack(anchor=tk.W)

        self.progressbar.grid(row=0, column=0, padx=10, pady=20, sticky=tk.W)
        self.progress_display_text.grid(row=1, column=0)

        # Place subframes:
        progress_frame_title.pack(fill=tk.X)
        progress_frame_status.pack()

        return progress_frame

    ############################
    # Frame Adjusting Methods: #
    ############################

    def update_options_cb(self) -> None:

        # Safe mode explanation:
        if self.is_safe_mode.get():
            self.is_safe_mode_label.configure(
                text="App will not move or copy any files but still prints their new locations."
            )
            self.move_copy_radio_frame.grid_remove()
            self.is_moving_files_label.grid_remove()
        else:
            self.is_safe_mode_label.configure(
                text="App will %s files to new locations." % ("move" if self.is_moving_files.get() else "copy")
            )
            self.move_copy_radio_frame.grid()
            self.is_moving_files_label.grid()

        # Creating new directories explanation:
        if self.is_recursive_search.get():
            self.is_recursive_search_label.configure(
                text="App will recursively search input folder and all subfolders."
            )
        else:
            self.is_recursive_search_label.configure(
                text="App will only search the input folder and ignore any subfolders."
            )

        # Deleting empty directories explanation:
        if self.is_deleting_empty_directories.get():
            self.is_deleting_empty_directories_label.configure(
                text="App will delete empty folders/directories in the input path."
            )
        else:
            self.is_deleting_empty_directories_label.configure(
                text="App will not delete empty folders/directories in the input path."
            )

        # Moving / Copying files explanation:
        if self.is_moving_files.get():
            # TODO: Check for other side effects...
            self.is_moving_files_label.configure(text="App will move and modify ORIGINAL files to new directories.")
        else:
            self.is_moving_files_label.configure(
                text="App will NOT touch ORIGINAL files.  Instead, they will be copied to their new locations."
            )

        # Count strings explanation:
        if self.is_adding_count_str.get():
            self.is_adding_count_str_label.configure(
                text="App will add \"@000\" to the end in cases of same file names and dates.\n" +
                "Example: file@000.txt, file@001.txt, file@002.txt, other_file@000.txt, another_file@000.txt"
            )
        else:
            self.is_adding_count_str_label.configure(text="App will not add count strings.")
            # TODO: Add a warning that files with the same name and date will be
            # overwritten by each other and that it is recommended to use count strings
            # first and then to verify there are no duplicates and run the program again
            # with this option disabled.

        # Date strings explanation:
        if self.is_adding_date_str.get():
            self.is_adding_date_str_label.configure(
                text="App will add the date to the end of the file name.\n" +
                "Example: FILL IN EXAMPLES HERE..."
            )
        else:
            self.is_adding_date_str_label.configure(text="App will not add date strings.")

    def adjust_to_execution_view(self) -> None:

        # Delete run path buttons:
        if hasattr(self, 'button_input_browse'):
            self.button_input_browse.destroy()
            del self.button_input_browse
        if hasattr(self, 'button_output_browse'):
            self.button_output_browse.destroy()
            del self.button_output_browse
        if hasattr(self, 'checkbutton_create_output_dir'):
            self.checkbutton_create_output_dir.destroy()
            del self.checkbutton_create_output_dir

        # Disable script option buttons:
        # self.checkbutton_safe_mode.configure(state=tk.DISABLED, cursor="")
        # self.checkbutton_create_new_dir.configure(state=tk.DISABLED, cursor="")
        # self.checkbutton_delete_empty_dir.configure(state=tk.DISABLED, cursor="")
        # self.radiobutton_move_files.configure(state=tk.DISABLED, cursor="")
        # self.radiobutton_copy_files.configure(state=tk.DISABLED, cursor="")
        # self.checkbutton_add_count_str.configure(state=tk.DISABLED, cursor="")
        # self.checkbutton_add_date_str.configure(state=tk.DISABLED, cursor="")

        # Create and initialize progress frame inside of the body frame:
        if not hasattr(self, 'progress_frame'):
            self.progress_frame = self.init_progress_frame(self.body_frame)
            self.progress_frame.grid(row=2, column=1, sticky=tk.W)

    def check_if_ready_to_run(self):
        # Update 'Run' button state once the file dialog is done:
        if path.exists(self.input_path) and (path.exists(self.output_path) or self.is_creating_output_dir.get()):
            self.button_run.configure(state=tk.NORMAL, cursor="hand2")
        else:
            self.button_run.configure(state=tk.DISABLED, cursor="")

    #####################
    # Button Callbacks: #
    #####################

    def get_input_path_cb(self):
        # Open and return file path for input_path:
        self.input_path = filedialog.askdirectory(title="Select An Input Directory")

        if not path.exists(self.input_path):
            # Do nothing if the path is empty or not valid:
            return

        # Update text label with file path:
        self.label_selected_input_path.configure(text=self.input_path, bg='#f3f0ea')
        # Call checkbox callback to update in case box is checked:
        self.check_button_create_output_dir_cb()
        # Update 'Run' button status:
        self.check_if_ready_to_run()

    def get_output_path_cb(self):
        # Open and return file path for output_path:
        self.output_path = filedialog.askdirectory(title="Select An Output Destination")

        if not path.exists(self.output_path):
            # Do nothing if the path is empty or not valid:
            return

        # Update text label with file path
        self.label_selected_output_path.configure(text=self.output_path, bg='#f3f0ea')
        # Update 'Run' button status:
        self.check_if_ready_to_run()

    def check_button_create_output_dir_cb(self):

        if self.is_creating_output_dir.get():
            # Hide the output browse button when checkbox is selected:
            self.button_output_browse.grid_remove()
            # Catch if user selects the checkbox before selecting the input path:
            if path.exists(self.input_path):
                temp = self.input_path + f'/output'
                self.output_path = temp
            else:
                temp = "Select an input path."
            self.label_selected_output_path.configure(text=temp)
        else:
            # Show the output browse button when checkbox is not selected:
            self.button_output_browse.grid()
            # Clear output path:
            if not path.exists(self.output_path):
                self.output_path = ""
                self.label_selected_output_path.configure(text="Select an output path.")

        # Update 'Run' button status:
        self.check_if_ready_to_run()

    def cancel_button_cb(self):
        self.master.destroy()
        # TODO: Figure out how to shutdown the subprocess if it's running...
        # exit()

    def run_button_cb(self):
        # Ends the tkinter window and continues the script; doesn't exit()

        self.adjust_to_execution_view()

        # Call the controller with the selected options:
        self.controller.handle_started_execution(self.input_path, self.output_path, self.convert_options_to_dict())

    ###################
    # Helper Methods: #
    ###################

    def convert_options_to_dict(self) -> dict[str, bool]:

        # Create a new dictionary out of base variable types using the options dictionary:
        simplified_options_dict: dict[str, bool] = {
            name: var.get() for name, var in self.options_dict.items()
        }

        return simplified_options_dict
