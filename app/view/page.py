# app/view/page.py

from typing import Callable

from tkinter.ttk import Frame
from tkinter import Tk


class Page(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent: Tk = parent
        self.input_path: str = ""
        self.output_path: str = ""
        self.next_page_cb: Callable[[], None]

    def set_next_page_cb(self, next_page_cb: Callable[[], None]) -> None:
        self.next_page_cb = next_page_cb
