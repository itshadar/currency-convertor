from aiofiles import open
from typing import Final
from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class ParsedInput:
    from_curr: str
    to_curr: str
    values: list[float]


class BaseInputHandler(ABC):

    @abstractmethod
    async def handle_input(self, file_path) -> ParsedInput:
        """
        handle the input in a manner implemented by the concrete class.
        """


class HandleTXTFile(BaseInputHandler):

    FROM_CURR_INDEX: Final[int] = 0
    TO_CURR_INDEX: Final[int] = 1
    VALUES_INDEX: Final[int] = 2

    @staticmethod
    async def read_file(file_path) -> list[str]:

        async with open(file_path, mode='r') as f:
            lines = await f.readlines()

        return lines

    def parse_input(self, lines: list[str]) -> ParsedInput:
        from_curr = lines[self.FROM_CURR_INDEX].strip()
        to_curr = lines[self.TO_CURR_INDEX].strip()
        values = list(map(float, lines[self.VALUES_INDEX:]))
        return ParsedInput(from_curr=from_curr, to_curr=to_curr, values=values)

    async def handle_input(self, file_path) -> ParsedInput:
        lines = await HandleTXTFile.read_file(file_path)
        return self.parse_input(lines)
