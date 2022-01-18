import camelot
import requests

from tables import MacroAndMicronutrientsTable, AminoAcidsTable


class TACO:
    URL = 'https://www.nepa.unicamp.br/taco/contar/taco_4_edicao_ampliada_e_revisada.pdf?arquivo=1'
    FILENAME = 'taco_4_ed.pdf'

    @staticmethod
    def _download_pdf():
        response = requests.get(TACO.URL)
        return response.content

    @staticmethod
    def _write_pdf(content):
        with open(TACO.FILENAME, 'wb') as file:
            file.write(content)

    @staticmethod
    def get_document():
        TACO._write_pdf(TACO._download_pdf())


if __name__ == '__main__':
    TACO.get_document()

    tables = camelot.read_pdf(filepath=TACO.FILENAME, pages=MacroAndMicronutrientsTable().range(), flavor='stream')

    print()
