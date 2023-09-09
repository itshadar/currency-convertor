from aiofiles import open
from typing import Final


class HandleFile:

    FROM_CURR_INDEX: Final[int] = 0
    TO_CURR_INDEX: Final[int] = 1
    VALUES_INDEX: Final[int] = 2

    @staticmethod
    async def read_file(file_path) -> list[str]:

        async with open(file_path, mode='r') as f:
            lines = await f.readlines()

        return lines

    @staticmethod
    def parse_input(lines: list[str]) -> tuple[str, str, list[float]]:
        from_curr = lines[HandleFile.FROM_CURR_INDEX].strip()
        to_curr = lines[HandleFile.TO_CURR_INDEX].strip()
        values = list(map(float, lines[HandleFile.VALUES_INDEX:]))
        return from_curr, to_curr, values

    @staticmethod
    async def handle_input(file_path) -> tuple[str, str, list[float]]:
        lines = await HandleFile.read_file(file_path)
        return HandleFile.parse_input(lines)


