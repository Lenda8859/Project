import  re

def is_password(password):
    """
     Эта функция проверяет, соответствует ли заданный пароль требованиям безопасности.

    Аргументы:
    password -- строка для проверки.

    Возвращаемое значение:
    True, если пароль соответствует требованиям, иначе False.

    Примеры:

    >>> is_valid_password("Password123!")
    True

    >>> is_valid_password("password")
    False

    >>> is_valid_password("PASSWORD123")
    False

    >>> is_valid_password("Pass123")
    False

    >>> is_valid_password("Password!")
    False

    >>> is_valid_password("P@ssw0rd")
    True
    :param password:
    :return:
    """
    if len(password) < 8:
        return False
    if not re.search(r'\d', password):
        return False
    if not re.search(r'[A-Z]', password):
        return False
    if not re.search(r'[a-z]', password):
        return False
    if not re.search(r'[@#$%^&+=]', password):
        return False
    return True
if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)