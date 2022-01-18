from dataclasses import dataclass


@dataclass
class Table:
    start: int
    end: int

    def range(self) -> str:
        return f'{self.start}-{self.end}'


class MacroAndMicronutrientsTable(Table):
    def __init__(self):
        super().__init__(start=29, end=68)


class FattyAcidsTable(Table):
    def __init__(self):
        super().__init__(start=71, end=100)


class AminoAcidsTable(Table):
    def __init__(self):
        super().__init__(start=103, end=104)
