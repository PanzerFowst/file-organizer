# app/view/app_view.py

from os import path

from tkinter import ttk, filedialog
import tkinter as tk


class View():
    def __init__(self, master: tk.Tk) -> None:
        self.main_window = MainWindow(master)


class MainWindow(ttk.Frame):
    def __init__(self, master: tk.Tk):
        super().__init__(master)
        self.place(relx=0, rely=0, relwidth=1, relheight=1)

        # Class variables:
        self.master: tk.Tk = master
        self.input_path: str = ""
        self.output_path: str = ""

        # tkinter variables:
        self.is_creating_output_dir = tk.BooleanVar()
        self.is_safe_mode = tk.BooleanVar()
        self.is_creating_new_directories = tk.BooleanVar()
        self.is_deleting_empty_directories = tk.BooleanVar()
        self.is_adding_count_str = tk.BooleanVar()
        self.is_adding_date_str = tk.BooleanVar()
        self.is_moving_files = tk.BooleanVar()

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
        checkbutton_create_output_dir = ttk.Checkbutton(
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

        checkbutton_create_output_dir.grid(row=1, column=3, padx=20, sticky=tk.W)

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
        checkbutton_safe_mode = ttk.Checkbutton(
            master=options_frame_buttons,
            text="Prints potential files to console without copying or moving the files",
            variable=self.is_safe_mode,
            cursor="hand2",
        )
        # Create New Directories Checkbox
        checkbutton_create_new_dir = ttk.Checkbutton(
            master=options_frame_buttons,
            text="Should the script create folders if they don't exist?",
            variable=self.is_creating_new_directories,
            cursor="hand2",
        )
        # Delete Empty Directories Checkbox
        checkbutton_delete_empty_dir = ttk.Checkbutton(
            master=options_frame_buttons,
            text="Should the script delete folders if they are empty?",
            variable=self.is_deleting_empty_directories,
            cursor="hand2",
        )
        # Move/Copy Radio Buttons
        moveCopyRadioFrame = ttk.Frame(master=options_frame_buttons)
        radiobutton_move_files = ttk.Radiobutton(
            master=moveCopyRadioFrame,
            text="Move Files",
            variable=self.is_moving_files,
            value=True,
            cursor="hand2",
        )
        radiobutton_copy_files = ttk.Radiobutton(
            master=moveCopyRadioFrame,
            text="Copy Files",
            variable=self.is_moving_files,
            value=False,
            cursor="hand2",
        )
        # Count Strings Checkbox
        checkbutton_add_count_str = ttk.Checkbutton(
            master=options_frame_buttons,
            text="Should the script add count string?",
            variable=self.is_adding_count_str,
            cursor="hand2",
        )
        # Date Strings Checkbox
        checkbutton_add_date_str = ttk.Checkbutton(
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
        checkbutton_safe_mode.grid(row=0, column=0, sticky=tk.W)
        checkbutton_create_new_dir.grid(row=1, column=0, sticky=tk.W)
        checkbutton_delete_empty_dir.grid(row=2, column=0, sticky=tk.W)

        radiobutton_move_files.pack(side=tk.LEFT)
        radiobutton_copy_files.pack(side=tk.LEFT)
        moveCopyRadioFrame.grid(row=3, column=0, sticky=tk.W)

        checkbutton_add_count_str.grid(row=4, column=0, sticky=tk.W)
        checkbutton_add_date_str.grid(row=5, column=0, sticky=tk.W)

        # Place subframes:
        options_frame_title.pack(fill=tk.X)
        options_frame_buttons.pack()

        return options_frame

    # def set_action_on_save(self, action_on_save: Callable[[str], None]) -> None:
    #     """
    #     Set the controller
    #     :param controller:
    #     :return:
    #     """
    #     self.save_action = action_on_save

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
        # Open file dialog accepting only .pbix files; path will be the file_path var
        self.input_path = filedialog.askdirectory(title="Select An Input Directory")

        if not path.exists(self.input_path):
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

        if not path.exists(self.output_path):
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
            if path.exists(self.input_path):
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
        self.master.destroy()
        # exit()

    def run_button_cb(self):
        # Ends the tkinter window and continues the script; doesn't exit()
        # self.next_page_cb()
        pass
