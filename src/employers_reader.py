import json


def emp_reader(file_name):
    """возвращает список id работодателей из файла"""
    emp_ids = []
    with open(file_name) as file:
        emp_data = json.load(file)
        for i in emp_data:
            emp_ids.append(i['employer_id'])
    return emp_ids
