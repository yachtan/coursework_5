import psycopg2


class DBManager:
    """подключается к БД PostgreSQL и получает нужную информацию"""

    def __init__(self, db_name, db_params):
        self.db_name = db_name
        self.db_params = db_params
        self.conn = psycopg2.connect(dbname=self.db_name, **self.db_params)
        self.conn.autocommit = True
        self.cur = self.conn.cursor()

    def get_companies_and_vacancies_count(self):
        """получает список всех компаний и количество вакансий у каждой компании"""

        self.cur.execute(
            """
            SELECT company_name, total_vacancies FROM companies
            """
        )
        return self.cur.fetchall()

    def get_all_vacancies(self):
        """получает список всех вакансий с указанием названия вакансии, названия компании, зарплаты,
        ссылки на вакансию"""

        self.cur.execute(
            """
            SELECT vacancy_id, vacancy_name, company_name, vacancy_salary_from, vacancy_salary_to, vacancy_url
            FROM vacancies
            """
        )
        return self.cur.fetchall()

    def get_avg_salary(self):
        """получает среднюю зарплату по всем вакансиям"""

        self.cur.execute(
            """
            SELECT AVG(vacancy_salary_using) FROM vacancies
            """
        )
        return self.cur.fetchone()[0]

    def get_vacancies_with_higher_salary(self, avg_salary):
        """получает список всех вакансий, у которых зарплата выше средней по всем вакансиям"""
        self.avg_salary = avg_salary

        self.cur.execute(
            f"""
            SELECT vacancy_id, vacancy_name, company_name, vacancy_salary_from, vacancy_salary_to, vacancy_url
            FROM vacancies WHERE vacancy_salary_using > {self.avg_salary}
            """
        )
        return self.cur.fetchall()

    def get_vacancies_with_keyword(self, key_word):
        """получает список всех вакансий, в названии которых содержатся переданные в метод слова"""
        self.key_word = key_word

        self.cur.execute(
            f"""
            SELECT vacancy_id, vacancy_name, company_name, vacancy_salary_from, vacancy_salary_to, vacancy_url
            FROM vacancies WHERE vacancy_name LIKE '%{self.key_word}%'
            """
        )
        return self.cur.fetchall()
