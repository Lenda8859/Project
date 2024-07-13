def is_email(email):
    """

    Эта функция проверяет, является ли заданный адрес электронной почты допустимым.

    Аргументы:
    email -- строка для проверки.

    Возвращаемое значение:
    True, если адрес электронной почты допустимый, иначе False.

    Примеры:

    >>> is_valid_email("test@example.com")
    True

    >>> is_valid_email("user@domain.com")
    True

    >>> is_valid_email("invalid-email")
    False

    >>> is_valid_email("another.test@domain.co.uk")
    True

    >>> is_valid_email("missing_at_sign.com")
    False

    >>> is_valid_email("missingdot@domain")
    False
    """
    if '@' not in email:
        return False
    local.part, domain_part = email.split('@', 1)
    if "." not in domain_part:
        return False
    return True

if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)