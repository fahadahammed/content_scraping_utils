# Content Scraping Utils
The purpose of this repository is to have different content scraping utility functions and codes to make workflow 
easier to implement.

## Introduction of the repository
Repositry structure is as follows:

```bash
.
├── examples
│   └── for_cnn.py
├── Makefile
├── output
├── README.md
├── requirements.txt
├── src
│   ├── __init__.py
│   └── utility_functions.py
└── tests
    └── utility_functions_test.py

4 directories, 7 files
```

## How?
### Prerequisite and Environment
- Codes are done in python 3.11.1
- libraries involved
```ini
beautifulsoup4==4.12.3
lxml==5.1.0
requests==2.31.0
soupsieve==2.5
urllib3==2.2.0
certifi==2024.2.2
charset-normalizer==3.3.2
idna==3.6
```
### Installation Steps

#### Prepare environment with virtualenv
```bash
$ virtualenv .venv --python=python3.11
```
#### Activate the Virtualenv
```bash
$ source .venv/bin/activate
```
#### Install required Libraries
```bash
$ pip install -r requirements.txt
```

or Using Make

```bash
$ make init
```

### Run Examples
```bash
$ make cnn
```

### Run Test?
Used pythons unittest module to prepare some test.

```bash
$ python3 -m unittest -v tests/*.py -v;
```

or using Make

```bash
$ make test
```

## Why CNN?

The purpose of choosing CNN is because it seems straight forward and without 
any issue involved with rendering the conents via JS. If that was the case and I could give enough 
time I might have choosen other ways to handle it. 

## Prospect
- Reusuable code in `src/`
- Working version of other scraping factors involved PDF, Video, html table etc.