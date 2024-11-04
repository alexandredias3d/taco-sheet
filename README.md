# TACO Sheet

## Description

[TACO](https://nepa.unicamp.br/publicacoes/tabela-taco-pdf/) is a Brazilian food nutrition table created by [NEPA](https://nepa.unicamp.br/publicacoes/).  
In 2022, I tried to download the .xls from the official website but the link was broken.  
Therefore, I created this script to download the official .pdf and extract tables from it, storing them on .csv files.  
There is no guarantee that the values were read correctly.

As of 2024, the NEPA website was updated and the links were fixed.  
- [TACO PDF](https://nepa.unicamp.br/publicacoes/tabela-taco-pdf/): official PDF used by the script to extract information.
- [TACO Excel](https://nepa.unicamp.br/publicacoes/tabela-taco-excel/): official Excel sheet of the nutrition table.  

Therefore, this repository is no longer needed and will be kept active only as a reference for future projects using Camelot to extract information from PDF files.

## Getting Started

### Dependencies

* Python >= 3.11
* Pipenv

### Installing

```
  git clone https://github.com/alexandredias3d/taco-sheet
  cd taco-sheet
  pipenv install
```

### Executing

```
  pipenv run python main.py
```

## License

This project is licensed under the MIT License - see the LICENSE.md file for details
