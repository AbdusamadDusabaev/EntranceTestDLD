import datetime
from django.http import HttpRequest


def validate_registration_data(request: HttpRequest) -> tuple[bool, (list[str], None)]:
    first_name: str = request.POST.get("first_name", None)
    second_name: str = request.POST.get("second_name", None)
    date_of_birthday: str = request.POST.get("date_of_birthday", None)

    first_name_is_valid: bool = False
    second_name_is_valid: bool = False
    date_of_birthday_is_valid: bool = False
    error_messages: list[str] = list()

    if first_name is not None:
        if first_name.isalpha():
            first_name_is_valid: bool = True
        else:
            error_messages.append('Поле "Имя" может содержать только буквы в верхнем и нижнем регистре')
    else:
        error_messages.append('Поле "Имя" обязательное')

    if second_name is not None:
        if second_name.isalpha():
            second_name_is_valid: bool = True
        else:
            error_messages.append('Поле "Фамилия" может содержать только буквы в верхнем и нижнем регистре')
    else:
        error_messages.append('Поле "Фамилия" обязательное')

    if date_of_birthday is not None:
        try:
            datetime.datetime.strptime(date_of_birthday, "%Y-%m-%d")
            date_of_birthday_is_valid: bool = True
        except ValueError:
            error_messages.append("Введите корректную дату рождения в формате 'день.месяц.год'")
    else:
        error_messages.append('Поле "Дата рождения" обязательное')

    if all([first_name_is_valid, second_name_is_valid, date_of_birthday_is_valid]):
        result_validate_of_registration_data: tuple[bool, None] = True, None
        return result_validate_of_registration_data

    result_validate_of_registration_data: tuple[bool, list[str]] = False, error_messages
    return result_validate_of_registration_data


def validate_create_book_data(request: HttpRequest) -> tuple[bool, (list[str], None)]:
    title: str = request.data.get("title", "")
    description: str = request.data.get("description", "")
    title_is_valid: bool = title != "" and isinstance(title, str)
    description_is_valid: bool = description != "" and isinstance(description, str)

    if title_is_valid and description_is_valid:
        result_of_validate_request_data: tuple[bool, None] = True, None
        return result_of_validate_request_data

    error_messages: list[str] = list()
    if not title_is_valid:
        error_messages.append("Ошибка! Похоже вы забыли ввести значение 'title' или ввели его неправильно")
    if not description_is_valid:
        error_messages.append("Ошибка! Похоже вы забыли ввести значение 'description' или ввели его неправильно")

    result_of_validate_request_data: tuple[bool, list[str]] = False, error_messages
    return result_of_validate_request_data
