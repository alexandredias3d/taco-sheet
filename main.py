import camelot


if __name__ == '__main__':
    filename = 'taco_4_edicao_ampliada_e_revisada.pdf'
    tables = camelot.read_pdf(filepath=filename, pages='all', flavor='stream')

    print()
