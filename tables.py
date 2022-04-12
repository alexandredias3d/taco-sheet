import camelot
import pandas as pd

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Callable

from columns import Columns
from taco import TACO


class TableSide(Enum):
    MAIN = 'M'
    CONTINUATION = 'C'


@dataclass
class Table(ABC):
    start_page: int
    end_page: int
    columns: list[str]
    data: pd.DataFrame = None
    correction_functions: list[Callable[[int, pd.DataFrame], pd.DataFrame]] = None

    FOOD_ID_ORIGINAL_COLUMN: int = 0

    def __post_init__(self):
        self.data = pd.DataFrame()

    def get_page_range(self) -> str:
        return f'{self.start_page}-{self.end_page}'

    def extract(self) -> None:
        dataframes_by_page = self._get_dataframes_by_page()

        self._apply_fixes(dataframes_by_page)
        main_df = pd.concat(dataframes_by_page[TableSide.MAIN].values())
        continuation_df = pd.concat(dataframes_by_page[TableSide.CONTINUATION].values())

        merged_df = self._merge_dataframes(main_df, continuation_df)
        merged_df = self._rename(merged_df)

        self.data = merged_df

    def _get_dataframes_by_page(self) -> dict[TableSide, dict[int, pd.DataFrame]]:
        tables = self._parse_tables()

        dataframes_by_page = {
            TableSide.MAIN: {table.page: table.df for table in tables[0::2]},
            TableSide.CONTINUATION: {table.page: table.df for table in tables[1::2]},
        }

        return dataframes_by_page

    def _parse_tables(self) -> camelot.core.TableList:
        return camelot.read_pdf(filepath=TACO.FILENAME, pages=self.get_page_range(), flavor='stream')

    def save(self) -> None:
            self.data.to_csv(f'_{self.__class__.__name__}.csv', encoding='utf-8')

    def _apply_fixes(self, tables: dict[TableSide, dict[int, pd.DataFrame]]) -> None:
        for side in tables:
            for page in tables[side]:
                df = tables[side][page]

                # Remove first n-rows based on the table side
                df = df.tail(df.shape[0] - 4)

                # Convert Food ID column to int
                series = pd.to_numeric(df[Table.FOOD_ID_ORIGINAL_COLUMN], errors='coerce').dropna().astype('int64')
                df = df.drop(labels=[Table.FOOD_ID_ORIGINAL_COLUMN], axis=1)
                df[Table.FOOD_ID_ORIGINAL_COLUMN] = series

                # Drop rows without an integer Food ID
                df = df.dropna()

                # Set index to Food ID
                df = df.set_index(Table.FOOD_ID_ORIGINAL_COLUMN, drop=True)

                # Hook for specific correction functions
                if self.correction_functions:
                    for function in self.correction_functions:
                        df = function(page, df)

                tables[side][page] = df

    def _rename(self, df: pd.DataFrame) -> pd.DataFrame:
        df.index = df.index.rename(Columns.General.FOOD_ID)
        df.columns = self.columns
        return df

    @staticmethod
    def _merge_dataframes(left: pd.DataFrame, right: pd.DataFrame) -> pd.DataFrame:
        return left.join(right, lsuffix='_caller', rsuffix='_other')


class MacroAndMicronutrientsTable(Table):
    def __init__(self):
        super().__init__(start_page=29, end_page=68,
                         columns=[Columns.General.DESCRIPTION, Columns.MicroAndMacronutrients.HUMIDITY,
                                  Columns.MicroAndMacronutrients.KCAL, Columns.MicroAndMacronutrients.KJ,
                                  Columns.MicroAndMacronutrients.PROTEIN, Columns.MicroAndMacronutrients.LIPID,
                                  Columns.MicroAndMacronutrients.CHOLESTEROL,
                                  Columns.MicroAndMacronutrients.CARBOHYDRATE,
                                  Columns.MicroAndMacronutrients.DIETARY_FIBER, Columns.MicroAndMacronutrients.ASH,
                                  Columns.MicroAndMacronutrients.CALCIUM, Columns.MicroAndMacronutrients.MAGNESIUM,
                                  Columns.MicroAndMacronutrients.MANGANESE, Columns.MicroAndMacronutrients.PHOSPHORUS,
                                  Columns.MicroAndMacronutrients.IRON, Columns.MicroAndMacronutrients.SODIUM,
                                  Columns.MicroAndMacronutrients.POTASSIUM, Columns.MicroAndMacronutrients.COPPER,
                                  Columns.MicroAndMacronutrients.ZINC, Columns.MicroAndMacronutrients.RETINOL,
                                  Columns.MicroAndMacronutrients.RETINOL_EQUIVALENTS,
                                  Columns.MicroAndMacronutrients.RETINOL_ACTIVITY_EQUIVALENTS,
                                  Columns.MicroAndMacronutrients.THIAMINE, Columns.MicroAndMacronutrients.RIBOFLAVIN,
                                  Columns.MicroAndMacronutrients.PYRIDOXINE, Columns.MicroAndMacronutrients.NIACIN,
                                  Columns.MicroAndMacronutrients.VITAMIN_C],
                         correction_functions=[
                             self._fix_misread_columns,
                         ]
                         )

    @staticmethod
    def _fix_misread_columns(page: int, df: pd.DataFrame):
        if page == 64:
            df = df.drop(columns=[13, 14])
            df = df.rename(columns={15: 13, 16: 14, 17: 15})

        return df


class FattyAcidsTable(Table):
    def __init__(self):
        super().__init__(start_page=71, end_page=100,
                         columns=[Columns.General.DESCRIPTION, Columns.FattyAcids.SATURATED,
                                  Columns.FattyAcids.MONO_UNSATURATED, Columns.FattyAcids.POLY_UNSATURATED,
                                  Columns.FattyAcids.LAURIC, Columns.FattyAcids.MYRISTIC, Columns.FattyAcids.PALMITIC,
                                  Columns.FattyAcids.STEARIC, Columns.FattyAcids.ARACHIDIC, Columns.FattyAcids.BEHENIC,
                                  Columns.FattyAcids.LIGNOCERIC, Columns.FattyAcids.MYRISTOLEIC,
                                  Columns.FattyAcids.PALMITOLEIC, Columns.FattyAcids.OLEIC, Columns.FattyAcids.GADOLEIC,
                                  Columns.FattyAcids.LINOLEIC, Columns.FattyAcids.ALPHA_LINOLENIC,
                                  Columns.FattyAcids.ARACHIDONIC, Columns.FattyAcids.TIMNODONIC,
                                  Columns.FattyAcids.CLUPANODONIC, Columns.FattyAcids.CERVONIC,
                                  Columns.FattyAcids.ELAIDIC, Columns.FattyAcids.LINOLELAIDIC])


class AminoAcidsTable(Table):
    def __init__(self):
        super().__init__(start_page=103, end_page=104,
                         columns=[Columns.General.DESCRIPTION, Columns.AminoAcids.TRYPTOPHAN,
                                  Columns.AminoAcids.THREONINE, Columns.AminoAcids.ISOLEUCINE,
                                  Columns.AminoAcids.LEUCINE, Columns.AminoAcids.LYSINE, Columns.AminoAcids.METHIONINE,
                                  Columns.AminoAcids.CYSTINE, Columns.AminoAcids.PHENYLALANINE,
                                  Columns.AminoAcids.TYROSINE, Columns.AminoAcids.VALINE, Columns.AminoAcids.ARGININE,
                                  Columns.AminoAcids.HISTIDINE, Columns.AminoAcids.ALANINE,
                                  Columns.AminoAcids.ASPARTIC_ACID, Columns.AminoAcids.GLUTAMIC_ACID,
                                  Columns.AminoAcids.GLYCINE, Columns.AminoAcids.PROLINE, Columns.AminoAcids.SERINE])
