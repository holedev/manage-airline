# MANAGE AIRLINE

## `PYTHON FLASK` + `BOOTSTRAP 5` + `SQL WORKBENCH`

## Recommend: Python `3.10` + Sql Workbench `8.0.31` + Pycharm IDE

> DEMO
[manage-airline.undefine.tech](https://manage-airline.undefine.tech)

Flow: STAFF create flight list -> ADMIN accept flight list -> USER book ticket.\
Note: Momo payment need download [MOMO UAT](https://developers.momo.vn/v3/vi/docs/payment/onboarding/test-instructions/)
#### `TEST ACCOUNT`
- ADMIN: anonymous - 123456
- STAFF: staff - 123456
- USER: user - 123456
> How to use (dev + tester):

1. Clone repository and open
2. Add Interpreter (venv) (Pycharm: File -> Setting -> Project: manage-airline -> Python Interpreter -> Add Interperter)
3. Run in venv `pip install -r requirements.txt`
4. Edit `.env` (NAME + PASSWORD DATABASE + OAUTH LOGIN GOOGLE) 
// u need an account in Google Cloud Console to have OAUTH LOGIN
5. Add models in `models.py`
6. Run `index.py`
7. ![image](https://user-images.githubusercontent.com/82250843/205350973-a6013ae6-10f3-46b9-8f22-58ba40cda29d.png)

> CORE Concepts (All in index.py)
#### `AUTHENTICATION`

- LOGIN
- SIGN UP
- LOGOUT
- LOGIN WITH GOOGLE

#### `FLIGHT SCHEDULE`

- GET LIST
- CREATE
- SEARCH
- DELETE

#### `FORM TICKET`

- GET FORM
- PREVIEW TICKET
- CREATE TICKET FROM FORM

#### `ADMIN`

- CREATE RULES
- GET STATIST




> ## Goodluck!
