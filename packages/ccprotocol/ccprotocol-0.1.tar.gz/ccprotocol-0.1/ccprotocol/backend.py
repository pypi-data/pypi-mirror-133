import time
from typing import Any, Union
from fluxhelper import joinPath, loadJson
from .exceptions import *

INPUT_FILE = "__in.coms"
OUTPUT_FILE = "__out.json"


class Backend:
    def __init__(self, path: str) -> None:
        self.path = path

        self.input_file = joinPath([path, INPUT_FILE])
        self.output_file = joinPath([path, OUTPUT_FILE])

        self.__clear()

    def __write(self, data: str) -> None:
        with open(self.input_file, "w") as f:
            f.write(data)
    
    def __clear(self, f: str = "out") -> None:
        m = {"out": self.output_file, "in": self.input_file}

        with open(m[f], "w") as f:
            f.write("")
        
    def __read(self) -> Union[None, dict]:
        out = None
        status = False
        t = time.time()
        while not status:
            try:
                out, status = loadJson(self.output_file)

                if time.time() - t > 2:
                    raise TimeoutError

            except KeyboardInterrupt:
                out = None
                break
        
        self.__clear()
        return out
    
    def _raise_for_status(self, parsed: dict) -> None:
        m = {
            "moduleNotFound": ModuleNotFound,
            "functionNotFound": FunctionNotFound
        }
        exception = m.get(parsed["status"])
        if exception:
            raise exception(parsed["msg"])
        
    def _reformat_args(self, args: list) -> list:
        f = []
        for arg in args:
            s = str(arg)
            if s == "True":
                s = "true"
            elif s == "False":
                s = "false"
            f.append(s)
        
        return f
    
    def _call(self, module: str, func: str, args: list = None) -> Union[None, dict]:

        """Writes a command to __in.coms and returns the raw output if it succeeded, else it will return None"""

        if args is None:
            args = []

        # Construct the command
        s = f"{module} {func} {' '.join(self._reformat_args(args))}".strip()
        out = self.__read()

        if out and out["status"] == "clear":
            self.__clear() # Just to be sure
            self.__write(s)

            out = self.__read()
            if out:
                # Raises an exception if it is not a success
                self._raise_for_status(out)
                return out
        
        if out is None:
            raise IOError
        return {"out": None}

    def call(self, module: str, func: str, *args) -> Any:
        """Runs self._call to return the raw data and then return the parsed output."""

        r = self._call(module, func, args)
        out = r.get("out")

        if isinstance(out, list):
            if len(out) == 1:
                return out[0]
            return tuple(out)
