# app/view/app_view.py

from os import path
from typing import Protocol

from tkinter import ttk, filedialog, scrolledtext
import tkinter as tk


class Controller(Protocol):
    def handle_started_execution(self, input_path: str, output_path: str, options_dict: dict[str, tk.Variable]) -> None:
        ...


class View(tk.Tk):
    def __init__(self):
        super().__init__()

        # Title of the window:
        self.title("File Lister")
        # Window background color & size:
        self.configure(bg='#f3f0ea')
        # Place window:
        width = 800  # self.winfo_width()
        height = 500  # self.winfo_height()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - width) // 2 + 500
        y = (screen_height - height) // 2 + 250
        self.geometry(f"{width}x{height}+{x}+{y}")
        # Whether the window is x, y resizable (False):
        self.resizable(False, False)
        # Set the application to always remain on top:
        self.wm_attributes("-topmost", True)

    def init_ui(self, controller: Controller) -> None:

        self.main_window = MainWindow(self, controller)

    def write_to_progress_display(self, text: str) -> None:
        self.main_window.progress_display_text.insert(tk.END, text)
        self.main_window.progress_display_text.see(tk.END)

    def handle_finished_execution(self) -> None:
        self.main_window.button_run.configure(state=tk.DISABLED)
        # self.main_window.progress_display_text.configure(state=tk.DISABLED)
        self.main_window.progressbar.stop()


class MainWindow(ttk.Frame):
    def __init__(self, master: tk.Tk, controller: Controller):
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
        body_frame.grid_columnconfigure(index=1, weight=20, uniform='a')
        body_frame.grid_rowconfigure(index=(0, 1, 2, 3), uniform='a')
        body_frame.grid_rowconfigure(index=1, weight=2)
        body_frame.grid_rowconfigure(index=3, weight=5)

        # actions_frame:
        self.button_cancel.pack(padx=7, side=tk.LEFT)
        self.button_run.pack(padx=7, side=tk.LEFT)
        actions_subframe.pack(padx=15, pady=15)
        # Frames:
        run_paths_frame.grid(row=1, column=1, sticky=tk.W)
        options_frame.grid(row=3, column=1, sticky=tk.W)
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
        LabelInputPath = tk.Label(  # ttk.Label(
            master=run_paths_frame_options,
            text="Input Path: ",
            bg='#f3f0ea',
        )
        # Label for the output path row header
        LabelOutputPath = tk.Label(  # ttk.Label(
            master=run_paths_frame_options,
            text="Output Path: ",
            bg='#f3f0ea',
        )

        # Label for the filepath text
        self.LabelSelectedInputPath = tk.Label(  # ttk.Label(
            master=run_paths_frame_options,
            text="Select the input path.",
            bg='#f3f0ea',
        )
        # Label for the output path text
        self.LabelSelectedOutputPath = tk.Label(  # ttk.Label(
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

        LabelInputPath.grid(row=0, column=0, sticky=tk.E)
        LabelOutputPath.grid(row=1, column=0, sticky=tk.E)

        self.LabelSelectedInputPath.grid(row=0, column=1, sticky=tk.W)
        self.LabelSelectedOutputPath.grid(row=1, column=1, sticky=tk.W)

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
        self.is_safe_mode = tk.BooleanVar(name="is_safe_mode", value=False)
        self.options_dict[str(self.is_safe_mode)] = self.is_safe_mode
        self.checkbutton_safe_mode = ttk.Checkbutton(
            master=options_frame_buttons,
            text="Prints potential files to console without copying or moving the files",
            variable=self.is_safe_mode,
            cursor="hand2",
        )
        # Create New Directories Checkbox
        self.is_creating_new_directories = tk.BooleanVar(name="is_creating_new_directories", value=False)
        self.options_dict[str(self.is_creating_new_directories)] = self.is_creating_new_directories
        self.checkbutton_create_new_dir = ttk.Checkbutton(
            master=options_frame_buttons,
            text="Should the script create folders if they don't exist?",
            variable=self.is_creating_new_directories,
            cursor="hand2",
        )
        # Delete Empty Directories Checkbox
        self.is_deleting_empty_directories = tk.BooleanVar(name="is_deleting_empty_directories", value=False)
        self.options_dict[str(self.is_deleting_empty_directories)] = self.is_deleting_empty_directories
        self.checkbutton_delete_empty_dir = ttk.Checkbutton(
            master=options_frame_buttons,
            text="Should the script delete folders if they are empty?",
            variable=self.is_deleting_empty_directories,
            cursor="hand2",
        )
        # Move/Copy Radio Buttons
        self.is_moving_files = tk.BooleanVar(name="is_moving_files", value=False)
        self.options_dict[str(self.is_moving_files)] = self.is_moving_files
        moveCopyRadioFrame = ttk.Frame(master=options_frame_buttons)
        self.radiobutton_move_files = ttk.Radiobutton(
            master=moveCopyRadioFrame,
            text="Move Files",
            variable=self.is_moving_files,
            value=True,
            cursor="hand2",
        )
        self.radiobutton_copy_files = ttk.Radiobutton(
            master=moveCopyRadioFrame,
            text="Copy Files",
            variable=self.is_moving_files,
            value=False,
            cursor="hand2",
        )
        # Count Strings Checkbox
        self.is_adding_count_str = tk.BooleanVar(name="is_adding_count_str", value=False)
        self.options_dict[str(self.is_adding_count_str)] = self.is_adding_count_str
        self.checkbutton_add_count_str = ttk.Checkbutton(
            master=options_frame_buttons,
            text="Should the script add count string?",
            variable=self.is_adding_count_str,
            cursor="hand2",
        )
        # Date Strings Checkbox
        self.is_adding_date_str = tk.BooleanVar(name="is_adding_date_str", value=False)
        self.options_dict[str(self.is_adding_date_str)] = self.is_adding_date_str
        self.checkbutton_add_date_str = ttk.Checkbutton(
            master=options_frame_buttons,
            text="Should the script add date string?",
            variable=self.is_adding_date_str,
            cursor="hand2",
        )

        ##
        ### Place widgets:

        # Place in options_frame_title placement:
        options_frame_title_label.pack(anchor=tk.W)

        # Place in options_frame_buttons grids:
        self.checkbutton_safe_mode.grid(row=0, column=0, sticky=tk.W)
        self.checkbutton_create_new_dir.grid(row=1, column=0, sticky=tk.W)
        self.checkbutton_delete_empty_dir.grid(row=2, column=0, sticky=tk.W)

        self.radiobutton_move_files.pack(side=tk.LEFT)
        self.radiobutton_copy_files.pack(side=tk.LEFT)
        moveCopyRadioFrame.grid(row=3, column=0, sticky=tk.W)

        self.checkbutton_add_count_str.grid(row=4, column=0, sticky=tk.W)
        self.checkbutton_add_date_str.grid(row=5, column=0, sticky=tk.W)

        # Place subframes:
        options_frame_title.pack(fill=tk.X)
        options_frame_buttons.pack()

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

        # Add progressbar
        self.progressbar = ttk.Progressbar(
            progress_frame_status,
            orient='horizontal',
            mode='indeterminate',
            # length=500,
        )
        self.progressbar.start(3)

        # TODO: Add a text box or something to print data received from the model...
        self.progress_display_text = scrolledtext.ScrolledText(
            master=progress_frame_status,
            wrap='word',
            width=65,  # in characters
            height=5,  # in lines
            bg='#f3f0ea',
        )
        self.progress_display_text.insert(tk.END, "Progress and output will be displayed here.\n\n")

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

    def adjust_to_execution_view(self) -> None:

        # Delete run path buttons:
        self.button_input_browse.destroy()
        self.button_output_browse.destroy()
        self.checkbutton_create_output_dir.destroy()
        del self.button_input_browse
        del self.button_output_browse
        del self.checkbutton_create_output_dir

        # Disable script option buttons:
        self.checkbutton_safe_mode.configure(state=tk.DISABLED, cursor="")
        self.checkbutton_create_new_dir.configure(state=tk.DISABLED, cursor="")
        self.checkbutton_delete_empty_dir.configure(state=tk.DISABLED, cursor="")
        self.radiobutton_move_files.configure(state=tk.DISABLED, cursor="")
        self.radiobutton_copy_files.configure(state=tk.DISABLED, cursor="")
        self.checkbutton_add_count_str.configure(state=tk.DISABLED, cursor="")
        self.checkbutton_add_date_str.configure(state=tk.DISABLED, cursor="")

        # Create and initialize progress frame inside of the body frame:
        progress_frame = self.init_progress_frame(self.body_frame)
        progress_frame.grid(row=4, column=1, sticky=tk.W)
        # TODO: Add padding instead of using different rows...

    # def set_action_on_save(self, action_on_save: Callable[[str], None]) -> None:
    #     """
    #     Set the controller
    #     :param controller:
    #     :return:
    #     """
    #     self.save_action = action_on_save

    def check_if_ready_to_run(self):
        # Update 'Run' button state once the file dialog is done:
        # TODO: Remove this True override later...
        if True or (
            path.exists(self.input_path) and (path.exists(self.output_path) or self.is_creating_output_dir.get())
        ):
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

        # Hide and forget button after push (user cannot bring this button back):
        # TODO: Should this button always exist?
        # self.button_input_browse.grid_forget()
        # Update text label with file path:
        self.LabelSelectedInputPath.configure(text=self.input_path, bg='#f3f0ea')
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

        # Hide but remember button after push (in case user unchecks box):
        # TODO: Should this button always exist and only be removed by the checkbox?
        # self.button_output_browse.grid_remove()
        # Update text label with file path
        self.LabelSelectedOutputPath.configure(text=self.output_path, bg='#f3f0ea')
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
            self.LabelSelectedOutputPath.configure(text=temp)
        else:
            # Show the output browse button when checkbox is not selected:
            self.button_output_browse.grid()
            # Clear output path:
            self.output_path = ""
            self.LabelSelectedOutputPath.configure(text="Select an output path.")

        # Update 'Run' button status:
        self.check_if_ready_to_run()

    def cancel_button_cb(self):
        self.master.destroy()
        # exit()

    def run_button_cb(self):
        # Ends the tkinter window and continues the script; doesn't exit()
        # self.next_page_cb()
        print("\n\n\r")
        for name, var in self.options_dict.items():
            print(f"{type(var)} {name}: {var.get()}")

        self.adjust_to_execution_view()

        # Call the controller with the selected options:
        self.controller.handle_started_execution(self.input_path, self.output_path, self.options_dict)
        # TODO: Convert to list of Boolean values before passing to controller...
