# TACO Sheet

## Description

[TACO](https://www.nepa.unicamp.br/taco/tabela.php?ativo=tabela) is a Brazilian food nutrition table.  
I tried to download the .xls from the website but the link is broken.  
Therefore, I created this script to download the .pdf and extract the tables from it, storing them on .csv files.  
There is no guarantee that the values were read correctly.

## Getting Started

### Dependencies

* Python >= 3.9
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
