
def get_file(file_name=None):
    def decorator(func):
        def wrapper():
            nonlocal file_name
            if file_name is None:
                file_name = func.__name__
            file_name_extension = f"{file_name}.json"

            result = func()

            with open(file_name_extension, "a") as file:
                for item in result:
                    file.write(f"{item}\n")

            return result
        return wrapper
    return decorator