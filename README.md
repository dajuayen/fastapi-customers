# fastapi-customers

![Python](https://img.shields.io/badge/python-3.8%20%7C%203.9%20%7C%203.10-blue.svg)
![PyPI - Version](https://img.shields.io/pypi/v/:packageName)

[![CircleCI](https://circleci.com/gh/dajuayen/fastapi-customers/tree/develop.svg?style=svg)](https://circleci.com/gh/dajuayen/fastapi-customers/tree/develop)
[![Build Status](https://app.travis-ci.com/dajuayen/fastapi-customers.svg?branch=develop "Travis")](https://app.travis-ci.com/dajuayen/fastapi-customers)
[![codecov](https://codecov.io/gh/dajuayen/fastapi-customers/branch/develop/graph/badge.svg?token=0EA0ZI526H)](https://codecov.io/gh/dajuayen/fastapi-customers)

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)
[![linting: pylint](https://img.shields.io/badge/linting-pylint-yellowgreen)](https://github.com/pylint-dev/pylint)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

Create ApiRest with FastApi:

## Run

> uvicorn main:app --reload


## Content

### 1- Endpoints. 
  - Customers (CRUD)
  - Users (CRUD)
  - Token
  - Main

### 2- Enviroments: 

  | DB      | Env. Var. |
  |---------|-----------|
  | SqlLite | ENV=test  |
  | PostgresSql | ENV=postgres|


### 3- Tests:

Unit test with [pytest](https://docs.pytest.org/en/stable/index.html) and coverage.

  - Controller:
    - Customer
  - Routers:
      - Main
      - Securities
      - Users
      - Customers

### 4- Linters:

  - [pre-commit](https://pre-commit.com/):
    - definido en el archivo .pre-commit-config.yaml
    - importante ejecutar el siguiente comando para instalar los hooks:
      - pre-commit install
    - ejecutar el siguiente comando para ejecutar los hooks y comprobar que funciona:
      - pre-commit run --all-files
  - [pylint](https://pylint.pycqa.org/en/latest/)
  - [Black](https://black.readthedocs.io/en/stable/)
  - [ruff](https://docs.astral.sh/ruff/)

### 5- C.I.

  - [GitHub Actions](https://docs.github.com/en/actions)

    The url to search for public actions: [Marketplace - Actions](https://github.com/marketplace?type=actions)

    - [setup-python](https://github.com/actions/setup-python)
    - [py-actions/py-dependency-install](https://github.com/marketplace/actions/python-dependency-installation)
  - Circle
  - Travis
  - [Coverage](https://coverage.readthedocs.io/):
    - Installation:
      - pip install coverage
      - pip install pytest-cov
      - pip install pytest
      - pip install pytest-asyncio
      - pip install pytest-mock
    - Run:
      - coverage run -m pytest
      - coverage report
      - coverage html
    - Codecov
