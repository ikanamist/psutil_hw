def get_file(func):
    def decorator():
        result = func() 
        with open(f"{func.__name__}.txt", "a") as file:
            for item in result:
                file.write(f"{item} \n")
        return result
    return decorator