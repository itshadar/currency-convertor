import sys
from abc import ABC, abstractmethod


class BaseOutputEmitter(ABC):

    @abstractmethod
    def emit_output(self, output: any):
        """
        Emit the output in a manner implemented by the concrete class.
        """
        pass


class ConsoleOutputEmitter(BaseOutputEmitter):

    def emit_output(self, output: str):
        sys.stdout.write(output)
