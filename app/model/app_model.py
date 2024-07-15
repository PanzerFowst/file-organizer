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

    def init_model(self, controller: Controller) -> None:
        self.controller: Controller = controller

    def set_output_callback(self, callback: Callable[[str], None]):
        self.output_callback = callback

    def run_powershell_list_files(self):

        run_path = os.path.abspath(self.ps_script_path)

        def powershell_thread():
            process = subprocess.Popen(
                f'powershell.exe -ExecutionPolicy RemoteSigned -file "{run_path}" -basepath "{self.input_path}"',
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )

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
