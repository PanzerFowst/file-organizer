# app/model/app_model.py

import subprocess
import sys
import os


class Model:
    def __init__(self):
        self.ps_script_path: str = ".\\model\\listFiles.ps1"

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

    def run_powershell_list_files(self):

        run_path = os.path.abspath(self.ps_script_path)

        p = subprocess.Popen(
            f'powershell.exe -ExecutionPolicy RemoteSigned -file "{run_path}" -basepath "{self.input_path}"',
            stdout=sys.stdout,
        )
        p.communicate()
