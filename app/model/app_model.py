# app/model/app_model.py

import subprocess
import os
import threading
from typing import Callable, Protocol


class Controller(Protocol):
    def handle_finished_execution(self) -> None:
        ...


class Model:
    def __init__(self):
        self.ps_script_path: str = ".\\model\\listFiles.ps1"
        self.output_callback: Callable[[str], None] | None = None

    @property
    def input_path(self) -> str:
        return self.__input_path

    @input_path.setter
    def input_path(self, path: str) -> None:

        if os.path.exists(path):
            self.__input_path = path
        else:
            raise ValueError(f'Invalid file path: {path}')

    @property
    def output_path(self) -> str:
        return self.__output_path

    @output_path.setter
    def output_path(self, path: str) -> None:
        self.__output_path = path

    @property
    def is_safe_mode(self) -> str:
        return self.__is_safe_mode

    @is_safe_mode.setter
    def is_safe_mode(self, flag: bool) -> None:
        if flag:
            self.__is_safe_mode = "$true"
        else:
            self.__is_safe_mode = "$false"

    @property
    def is_creating_new_directories(self) -> str:
        return self.__is_creating_new_directories

    @is_creating_new_directories.setter
    def is_creating_new_directories(self, flag: bool) -> None:
        if flag:
            self.__is_creating_new_directories = "$true"
        else:
            self.__is_creating_new_directories = "$false"

    @property
    def is_deleting_empty_directories(self) -> str:
        return self.__is_deleting_empty_directories

    @is_deleting_empty_directories.setter
    def is_deleting_empty_directories(self, flag: bool) -> None:
        if flag:
            self.__is_deleting_empty_directories = "$true"
        else:
            self.__is_deleting_empty_directories = "$false"

    @property
    def is_moving_files(self) -> str:
        return self.__is_moving_files

    @is_moving_files.setter
    def is_moving_files(self, flag: bool) -> None:
        if flag:
            self.__is_moving_files = "$true"
        else:
            self.__is_moving_files = "$false"

    @property
    def is_adding_count_str(self) -> str:
        return self.__is_adding_count_str

    @is_adding_count_str.setter
    def is_adding_count_str(self, flag: bool) -> None:
        if flag:
            self.__is_adding_count_str = "$true"
        else:
            self.__is_adding_count_str = "$false"

    @property
    def is_adding_date_str(self) -> str:
        return self.__is_adding_date_str

    @is_adding_date_str.setter
    def is_adding_date_str(self, flag: bool) -> None:
        if flag:
            self.__is_adding_date_str = "$true"
        else:
            self.__is_adding_date_str = "$false"

    def init_model(self, controller: Controller) -> None:
        self.controller: Controller = controller

    def set_output_callback(self, callback: Callable[[str], None]):
        self.output_callback = callback

    def run_powershell_list_files(self):

        run_path = os.path.abspath(self.ps_script_path)

        def powershell_thread():

            command: list[str] = [
                "powershell.exe",
                "-ExecutionPolicy", "RemoteSigned",
                "-File", run_path,
                "-input_path", self.input_path,
                "-output_path", self.output_path,
                "-is_safe_mode", self.is_safe_mode,
                "-is_creating_new_directories", self.is_creating_new_directories,
                "-is_deleting_empty_directories", self.is_deleting_empty_directories,
                "-is_moving_files", self.is_moving_files,
                "-is_adding_count_str", self.is_adding_count_str,
                "-is_adding_date_str", self.is_adding_date_str,
            ]
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            if process.stdout is not None:
                if self.output_callback is not None:
                    for line in process.stdout:
                        self.output_callback(line)

                process.stdout.close()
            if process.stderr is not None:
                process.stderr.close()
            process.wait()

            # Once execution is done, notify the controller:
            self.controller.handle_finished_execution()

        thread = threading.Thread(target=powershell_thread)
        thread.start()
