import datetime

from django.test import TestCase
from django.urls import reverse
from rest_framework.response import Response
from api.models import Author, Book


class TestGetBookListAPI(TestCase):
    fixtures = ["users.json", "authors.json", "books.json", "tokens.json"]

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        api_token: str = Author.objects.get(user=2).api_token
        cls.api_token: str = api_token

    def test_get_book_list_data(self) -> None:
        response: Response = self.client.get(reverse("api:books"), headers={"Authorization": f"Token {self.api_token}"})
        expected_response_data: list[dict[str, (str, int, dict[str, (str, int)])]] = [
            {
                "id": 15,
                "title": "Русский язык для 7 класса",
                "description": "Учебник, признаный лучшим по мнению Министерства Образования",
                "author": {
                    "id": 5,
                    "first_name": "Иван",
                    "second_name": "Кулинов",
                    "date_of_birthday": "1997-03-09"
                },
                "date_of_published": "2023-04-30"
            },
            {
                "id": 14,
                "title": "Как объяснить коту, что ты не его раб ?",
                "description": "Если вы недавно завели кошку и не понимаете, почему контакт с любимым питомцем у вас идет не так, как вам того бы хотелось, то эта книга точно для вас!",
                "author": {
                    "id": 4,
                    "first_name": "Илья",
                    "second_name": "Соловьев",
                    "date_of_birthday": "2002-05-22"
                },
                "date_of_published": "2023-04-30"
            },
            {
                "id": 13,
                "title": "История развития модных журналов",
                "description": "Книга расскажет, как развивались модные журналы с течением времени и что на это влияло",
                "author": {
                    "id": 3,
                    "first_name": "Азамат",
                    "second_name": "Дусабаев",
                    "date_of_birthday": "1999-07-10"
                },
                "date_of_published": "2023-04-30"
            },
            {
                "id": 12,
                "title": "Основы домашнего хозяйства. Как выращивать домашний скот",
                "description": "Всегда думали о том, чтобы заняться домашним хозяйством ? Тогда эта книга для вас - она поможет понять, как обращаться с домашним скотом и выносить из этого прибыль",
                "author": {
                    "id": 2,
                    "first_name": "Алина",
                    "second_name": "Соловьева",
                    "date_of_birthday": "2000-10-02"
                },
                "date_of_published": "2023-04-30"
            },
            {
                "id": 11,
                "title": "Основы Linux",
                "description": "Книга полезна всем разработчикам, которые хотят улучшить свои знания ОС Linux. На сегодняшний день знания Linux являются критически важныи для любого веб-разработчика ",
                "author": {
                    "id": 1,
                    "first_name": "Абдусамад",
                    "second_name": "Дусабаев",
                    "date_of_birthday": "2001-08-17"
                },
                "date_of_published": "2023-04-30"
            },
            {
                "id": 10,
                "title": "Как найти общий язык со школьниками, если кажется, что это вообще не люди",
                "description": "Книга будет полезна всем преподавателям, которые хотят лучше понимать своих учеников и выстроить с ними теплые отношения",
                "author": {
                    "id": 5,
                    "first_name": "Иван",
                    "second_name": "Кулинов",
                    "date_of_birthday": "1997-03-09"
                },
                "date_of_published": "2023-04-30"
            },
            {
                "id": 9,
                "title": "Основы моды",
                "description": "История развития мировой моды и мировых брендов",
                "author": {
                    "id": 4,
                    "first_name": "Илья",
                    "second_name": "Соловьев",
                    "date_of_birthday": "2002-05-22"
                },
                "date_of_published": "2023-04-30"
            },
            {
                "id": 8,
                "title": "Кто такие геймеры и чем кормить ?",
                "description": "Книга для начинающих Game Developer, которые хотят понять найти и понять свою аудиторию",
                "author": {
                    "id": 3,
                    "first_name": "Азамат",
                    "second_name": "Дусабаев",
                    "date_of_birthday": "1999-07-10"
                },
                "date_of_published": "2023-04-30"
            },
            {
                "id": 7,
                "title": "Веб-дизайн. Основы UI",
                "description": "Книга для начинающих веб-дизайнеров. Она поможет понять самые основы индустрии и научит работать с базвыми инструментами любого веб-дизайнера",
                "author": {
                    "id": 2,
                    "first_name": "Алина",
                    "second_name": "Соловьева",
                    "date_of_birthday": "2000-10-02"
                },
                "date_of_published": "2023-04-30"
            },
            {
                "id": 6,
                "title": "Чистый код",
                "description": "Книга, которая больше подойдет опытным программистам, которая хотят глубже понять, что такое \"хороший код\" и чем он отличается от \"плохого\". Считается своего рода \"Библией\" среди разработчиков",
                "author": {
                    "id": 1,
                    "first_name": "Абдусамад",
                    "second_name": "Дусабаев",
                    "date_of_birthday": "2001-08-17"
                },
                "date_of_published": "2023-04-30"
            }
        ]
        actual_response_data: list[dict[str, (str, int, dict[str, (str, int)])]] = response.json()["results"]
        error_msg: str = "При запросе списка книг выдается неверный результат"
        self.assertEqual(first=expected_response_data, second=actual_response_data, msg=error_msg)


class TestCreateNewBookAPI(TestCase):
    fixtures = ["users.json", "authors.json", "books.json", "tokens.json"]

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        author: str = Author.objects.get(user=2)
        data: dict[str, str] = {
            "title": "Test Book",
            "description": "Description of Test Book"
        }
        cls.author: Author = author
        cls.data: dict[str, str] = data

    def test_create_new_book_on_valid_input_values(self) -> None:
        input_values: list[dict[str, str]] = [
            {
                "title": "Тестовая Книга 1",
                "description": "Тестовое Описание 1"
            },

            {
                "title": "Test Book 1",
                "description": "Test Description 1"
            },

            {
                "title": "1234567890",
                "description": "1234567890"
            },

            {
                "title": "!@#$%^&*()_+=-}{|][|/",
                "description": "|}?:/+_)(*&^%$#@!"
            },

            {
                "title": 12345,
                "description": 54321
            },
        ]
        error_msg: str = "API не корректно обрабатывает создание книги на валидных данных"

        for input_value in input_values:
            with self.subTest(input_value=input_value):
                response: Response = self.client.post(path=reverse("api:books"), data=input_value,
                                                      headers={"Authorization": f"Token {self.author.api_token}"})

                expected_response_data: dict[str, (str, int, dict[str, (str, int)])] = {
                    'id': Book.objects.all()[0].id,
                    'title': str(input_value["title"]),
                    'description': str(input_value["description"]),
                    'author': {
                        "id": self.author.pk,
                        "first_name": self.author.first_name,
                        "second_name": self.author.second_name,
                        "date_of_birthday": str(self.author.date_of_birthday)
                    },
                    'date_of_published': str(datetime.date.today())
                }
                actual_response_data: dict[str, (str, int, dict[str, (str, int)])] = response.json()
                self.assertEqual(first=expected_response_data, second=actual_response_data, msg=error_msg)

                expected_response_status_code: int = 201
                actual_response_status_code: int = response.status_code
                self.assertEqual(first=expected_response_status_code, second=actual_response_status_code, msg=error_msg)

    def test_create_new_book_on_invalid_input_values(self) -> None:
        input_values: list[dict[str]] = [
            {
                "title": "",
                "description": "",
            },

            {
                "title": "Test Book"
            },

            {
                "description": "Test Description"
            }
        ]
        error_msg: str = "API не корректно обрабатывает создание книги на невалидных данных"
        for input_value in input_values:
            with self.subTest(input_value=input_value):
                response: Response = self.client.post(path=reverse("api:books"), data=input_value,
                                                      headers={"Authorization": f"Token {self.author.api_token}"})

                expected_status_code: int = 400
                actual_status_code: int = response.status_code
                self.assertEqual(first=expected_status_code, second=actual_status_code, msg=error_msg)
