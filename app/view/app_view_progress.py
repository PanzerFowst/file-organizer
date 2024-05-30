# app/view/app_view_progress.py

# from typing import Callable

from tkinter.ttk import Button, Progressbar
from tkinter import Tk
from tkinter import Label
import tkinter as tk

from view.page import Page


class GuiProgressPage(Page):
    def __init__(self, parent):
        super().__init__(parent)

        # Title for main window
        self.LabelMainWindow = Label(self,
                                     text="File Lister",
                                     font=("Segoe UI", 14, 'bold'),
                                     fg='#3d4244',
                                     justify=tk.LEFT,
                                     bg='#f3f0ea')
        self.LabelMainWindow.grid(row=0, column=0, pady=20)

        # Label for the filepath row header
        self.LabelInputPath = Label(self, bg='#f3f0ea')
        self.LabelInputPath.grid(row=1, column=0, columnspan=3, padx=10, sticky=tk.W)

        # Label for the output path row header
        self.LabelOutputPath = Label(self, bg='#f3f0ea')
        self.LabelOutputPath.grid(row=2, column=0, columnspan=3, padx=10, sticky=tk.W)

        # Add progressbar
        self.progressbar = Progressbar(
            self,
            orient='horizontal',
            mode='indeterminate',
            # length=500,
        )
        self.progressbar.grid(row=3, column=0, padx=10, pady=20, sticky=tk.W)
        self.progressbar.start(3)

        # Cancel button
        self.button_cancel = Button(self,
                                    text="Cancel",
                                    command=self.cancel_button_cb,
                                    cursor="hand2")
        self.button_cancel.grid(row=3, column=1, padx=5, sticky=tk.E)

        # OK button
        self.button_ok = Button(self,
                                text="OK",
                                command=self.ok_button_cb)
        self.button_ok.grid(row=3, column=2, padx=5, sticky=tk.W)
        self.button_ok["state"] = tk.DISABLED
        self.button_ok["cursor"] = ""

    def update_labels(self):
        self.LabelInputPath["text"] = f"Input Path:\t{self.input_path}"
        self.LabelOutputPath["text"] = f"Output Path:\t{self.output_path}"
        self.progressbar["length"] = max(
            self.LabelInputPath.winfo_reqwidth(),
            self.LabelOutputPath.winfo_reqwidth()
        ) - self.button_cancel.winfo_reqwidth() - self.button_ok.winfo_reqwidth()

    def cancel_button_cb(self):
        self.parent.destroy()

    def ok_button_cb(self):
        # Waits for progress to finish...
        self.next_page_cb()
