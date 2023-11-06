import requests
import psycopg2



def get_vacancies_hh(employer_id):
    """получение данных по вакансиям с сайта hh.ru по id работодателей"""
    HH_API_URL = 'https://api.hh.ru/vacancies/'
    param = {'employer_id': employer_id, 'only_with_salary': True, 'per_page': 100}
    responce = requests.get(HH_API_URL, param)
    return responce.json()['items']


def create_database(database_name: str, params: dict):
    """cоздание базы данных и таблиц для сохранения данных о вакансиях"""

    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()

    try:
        cur.execute(f"DROP DATABASE {database_name}")
    except psycopg2.errors.InvalidCatalogName:
        pass
    finally:
        cur.execute(f"CREATE DATABASE {database_name}")

    conn.close()

    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE vacancies (
                vacancy_id SERIAL PRIMARY KEY,
                vacancy_name VARCHAR NOT NULL,
                vacancy_url VARCHAR NOT NULL,
                vacancy_salary_from INTEGER,
                vacancy_salary_to INTEGER,
                vacancy_salary_using INTEGER,
                company_name VARCHAR(100) NOT NULL,
                publish_date DATE,
                city VARCHAR(50),
                employment VARCHAR(30),
                schedule VARCHAR(30)
            )
        """)

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE companies (
                company_id SERIAL PRIMARY KEY,
                company_name VARCHAR(100) UNIQUE,
                total_vacancies INTEGER
            )
        """)

    conn.commit()
    conn.close()


def save_data_to_database(data, database_name, params):
    """сохранение данных о вакансиях и компаниях в базу данных"""

    conn = psycopg2.connect(dbname=database_name, **params)
    with conn.cursor() as cur:
        for i in data:

            if i['salary']['from'] == None:
                cur.execute(
                    """
                    INSERT INTO vacancies (vacancy_name, vacancy_url, vacancy_salary_from, vacancy_salary_to,
                    vacancy_salary_using, company_name, publish_date, city, employment, schedule)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (i['name'], i['alternate_url'], i['salary']['from'], i['salary']['to'], i['salary']['to'],
                     i['employer']['name'], i['created_at'], i['area']['name'], i['employment']['name'],
                     i['schedule']['name'])
                )
            else:
                cur.execute(
                    """
                    INSERT INTO vacancies (vacancy_name, vacancy_url, vacancy_salary_from, vacancy_salary_to,
                    vacancy_salary_using, company_name, publish_date, city, employment, schedule)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (i['name'], i['alternate_url'], i['salary']['from'], i['salary']['to'], i['salary']['from'],
                     i['employer']['name'], i['created_at'], i['area']['name'], i['employment']['name'],
                     i['schedule']['name'])
                )
        conn.commit()

        cur.execute(
            """
            INSERT INTO companies(company_name, total_vacancies)
            SELECT company_name, COUNT(*) FROM vacancies GROUP BY company_name ORDER BY company_name;
            ALTER TABLE vacancies ADD CONSTRAINT fk_vacancies_company_name FOREIGN KEY(company_name) 
            REFERENCES companies(company_name)
            """,
        )

    conn.commit()
    conn.close()
