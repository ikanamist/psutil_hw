import json

"""Функции, которые собирают данные, у меня возвращают строку
Поэтому для корректной записи в json я создаю словарь с одним и тем же значением My_PC 
для всех полученных данных при сборе информации"""


def get_file(file_name=None):
    def decorator(func):
        def wrapper():
            nonlocal file_name
            if file_name is None:
                file_name = f"{func.__name__}.json"
            
            result = func()
            
            added_data = "My_PC"
            json_dict = dict.fromkeys(result, added_data)
            with open(file_name, "a") as file:                   
                json_string = json.dumps(json_dict)
                file.write(f"{json_string}\n")

            return result
        return wrapper
    return decorator