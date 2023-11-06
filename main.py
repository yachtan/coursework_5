import os
from src.employers_reader import emp_reader
from src.config import config
from src.utils import get_vacancies_hh, create_database, save_data_to_database
from src.dbmanager import DBManager


def main():
    # приветствие
    print('Начинаем поиск вакансий с сайта hh.ru по выбранным работодателям!')

    # делаем запрос по выбранным работодателям
    employers_file_name = input('Введите имя файла, в котором содержится информация о выбранных работодателях:\n')
    # employers_file_name = 'src\employers.json'

    try:
        file = open(employers_file_name)
    except FileNotFoundError:
        print('Файл не найден! Программа завершена')
        exit()
    else:
        employers_ids = emp_reader(employers_file_name)

    data = get_vacancies_hh(employers_ids)

    # создаем БД и наполняем параметрами из поиска
    db_params = config()
    create_database('vacancy_from_hh', db_params)
    save_data_to_database(data, 'vacancy_from_hh', db_params)
    print('База данных "vacancy_from_hh" создана!')

    # работаем с созданными таблицами
    dbmanager = DBManager('vacancy_from_hh', db_params)
    all_vac = dbmanager.get_all_vacancies()
    if len(all_vac) == 0:
        print('Вакансии не найдены. Попробуйте выбрать других работодателей и начать заново')
        print('Работа программы завершена!')
        exit()
    else:
        while True:
            user_input_1 = input('\nВыберите дальнейшие действия:\n'
                             '0 - выход\n'
                             '1 - получить список всех компаний и количество вакансий у каждой компании\n'
                             '2 - получить список всех вакансий с указанием названия вакансии, названия компании,\n'
                             'зарплаты, ссылки на вакансию\n'
                             '3 - получить среднюю зарплату по всем вакансиям\n'
                             '4 - получить список всех вакансий, у которых зарплата выше средней по всем вакансиям\n'
                             '5 - получить список всех вакансий, в названии которых содержится указанное слово\n')

            if user_input_1 == '0':
                print('Работа программы завершена!')
                exit()

            elif user_input_1 == '1':
                comp_and_vac_count = dbmanager.get_companies_and_vacancies_count()
                print('Количество найденных вакансий по компаниям:')
                for i in comp_and_vac_count:
                    print(f'{i[0]} - {i[1]}')

            elif user_input_1 == '2':
                print('Все найденные вакансии:')
                for i in all_vac:
                    if i[3] == None:
                        print(f'{i[0]} - {i[1]} - {i[2]} - Зарплата до {i[4]} рублей - ссылка на вакансию {i[5]}')
                    elif i[4] == None:
                        print(f'{i[0]} - {i[1]} - {i[2]} - Зарплата от {i[3]} рублей - ссылка на вакансию {i[5]}')
                    else:
                        print(f'{i[0]} - {i[1]} - {i[2]} - Зарплата от {i[3]} до {i[4]} рублей - ссылка на вакансию {i[5]}')

            elif user_input_1 == '3':
                avg_salary = dbmanager.get_avg_salary()
                print(f'Средняя заработная плата по всем вакансиям: {round(avg_salary)} рублей')

            elif user_input_1 == '4':
                all_vac_higher = dbmanager.get_vacancies_with_higher_salary(dbmanager.get_avg_salary())
                print('Найденные вакансии с зарплатой выше среднего по выборке:')
                for i in all_vac_higher:
                    if i[3] == None:
                        print(f'{i[0]} - {i[1]} - {i[2]} - Зарплата до {i[4]} рублей - ссылка на вакансию {i[5]}')
                    elif i[4] == None:
                        print(f'{i[0]} - {i[1]} - {i[2]} - Зарплата от {i[3]} рублей - ссылка на вакансию {i[5]}')
                    else:
                        print(f'{i[0]} - {i[1]} - {i[2]} - Зарплата от {i[3]} до {i[4]} рублей - ссылка на вакансию {i[5]}')

            elif user_input_1 == '5':
                keyword = input('Введите ключевое слово для поиска:\n')
                vac_with_kw = dbmanager.get_vacancies_with_keyword(keyword)
                if len(vac_with_kw) == 0:
                    print('По такому слову вакансии не найдены')
                else:
                    print('Найденные вакансии по ключевому слову:')
                    for i in vac_with_kw:
                        if i[3] == None:
                            print(f'{i[0]} - {i[1]} - {i[2]} - Зарплата до {i[4]} рублей - ссылка на вакансию {i[5]}')
                        elif i[4] == None:
                            print(f'{i[0]} - {i[1]} - {i[2]} - Зарплата от {i[3]} рублей - ссылка на вакансию {i[5]}')
                        else:
                            print(f'{i[0]} - {i[1]} - {i[2]} - Зарплата от {i[3]} до {i[4]} рублей - ссылка на вакансию {i[5]}')

            else:
                print('Не верный ввод, попробуйте еще раз')


# запуск
if __name__ == '__main__':
    main()
