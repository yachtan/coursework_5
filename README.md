# Программа по поиску вакансий

Для работы программы необходимо:
1) создать файл формата json, в котором должны быть указаны id 
выбранных работодателей на сайте hh.ru

Ожидаемый формат данных:
[{"employer_name": "<работодатель>", "employer_id": "<id работодателя>"},
  {...}]

В папке уже есть созданный файл 'src\employers.json' - можно редактировать его, либо создать свой.

2) Создать файл database.ini для подключения к БД PostgreSQL


Далее необходимо запустить файл main.py и следовать инструкциям.
