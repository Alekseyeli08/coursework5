import requests
import psycopg2
from typing import Any
employer_ids = [9694561, 80, 5919632, 5667343, 9301808, 774144, 10571093, 198614, 6062708, 4306]
def get_employee_data():
    employers = []
    for employer_id in employer_ids:
        url_emp = f"https://api.hh.ru/employers/{employer_id}"
        employer_info = requests.get(url_emp, ).json()
        employers.append(employer_info)

    return employers

def get_vacancies_data():
    vacancy = []
    for vacacies_id in employer_ids:
        url_vac = f"https://api.hh.ru/vacancies?employer_id={vacacies_id}"
        vacancy_info = requests.get(url_vac, params= {'page' : 1, 'per_page': 5}).json()
        vacancy.extend(vacancy_info['items'])
    return vacancy


def create_database(database_name: str, params: dict) -> None:

    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f'DROP DATABASE IF EXISTS {database_name}')
    cur.execute(f'CREATE DATABASE {database_name}')

    conn.close()

    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE employers (
                id INTEGER,
                name text not null,
                area text
            )
        """)

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE vacancy (
                id INTEGER,
                name VARCHAR,
                area VARCHAR,
                salary INTEGER,
                url VARCHAR
            )
        """)

    conn.commit()
    conn.close()


def save_data_to_database_emp(data_emp: list[dict[str, Any]], database_name: str, params: dict) -> None:

    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        for emp in data_emp:
            cur.execute("""
                INSERT INTO employers (id, name, area, url)
                VALUES (%s, $s, $s, $s)
                """,
            (emp['id'], emp['name'], emp['area'])
                        )

    conn.commit()
    conn.close()


# def save_data_to_database_vac(data_vac, database_name, params):
#
#     conn = psycopg2.connect(dbname=database_name, **params)
#
#     with conn.cursor() as cur:
#         for vac in data_vac:
#             cur.execute("""
#                 INSERT INTO vacancy (name, area, salary, url)
#                 VALUES (%s, $s, $s, $s)
#                 """,
#                 (vac['name'], vac.get('area').get('name'), vac.get('salary').get('to'), vac['alternate_url'])
#                         )
#
#     conn.commit()
#     conn.close()