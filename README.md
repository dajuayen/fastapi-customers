# fastapi-customers

[![CircleCI](https://circleci.com/gh/dajuayen/fastapi-customers/tree/develop.svg?style=svg)](https://circleci.com/gh/dajuayen/fastapi-customers/tree/develop)
[![Build Status](https://app.travis-ci.com/dajuayen/fastapi-customers.svg?branch=develop "Travis")](https://app.travis-ci.com/dajuayen/fastapi-customers)
[![codecov](https://codecov.io/gh/dajuayen/fastapi-customers/branch/develop/graph/badge.svg?token=0EA0ZI526H)](https://codecov.io/gh/dajuayen/fastapi-customers)


Create ApiRest with FastApi:

## Run

> uvicorn main:app --reload


## Content

1- Endpoints. 
  - Customers (CRUD)
  - Users (CRUD)
  - Token
  - Main

2- Enviroments: 

  | DB      | Env. Var. |
  |---------|-----------|
  | SqlLite | ENV=test  |
  | PostgresSql | ENV=postgres|


3- Tests:
- Routers:
    - Main
    - Securities
    - Users
    - Customers

## C.I.

- GitHub Actions
- Circle
- Travis
- Coverage
- Codecov