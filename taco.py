import requests


class TACO:
    URL = 'https://nepa.unicamp.br/publicacoes/tabela-taco-pdf/'
    FILENAME = '_Taco_4_ed.pdf'

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
