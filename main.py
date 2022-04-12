from taco import TACO
from tables import AminoAcidsTable,  FattyAcidsTable, MacroAndMicronutrientsTable

if __name__ == '__main__':
    TACO.get_document()

    tables = [
        AminoAcidsTable(),
        FattyAcidsTable(),
        MacroAndMicronutrientsTable(),
    ]

    for table in tables:
        table.extract()
        table.save()
