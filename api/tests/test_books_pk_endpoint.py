from django.test import TestCase
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from api.models import Author, Book


class TestGetBookDetailAPIView(TestCase):
    fixtures = ["users.json", "authors.json", "books.json", "tokens.json"]

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        api_token: int = Author.objects.get(user=2).api_token
        max_book_id: int = Book.objects.all()[0].id

        cls.api_token = api_token
        cls.max_book_id = max_book_id

    def test_get_detail_info(self) -> None:
        error_msg: str = "API выдает некорректный ответ на запрос детальной информации о книге"
        for pk in range(1, self.max_book_id + 1):
            response = self.client.get(path=f"{reverse('api:books')}{pk}/",
                                       headers={"Authorization": f"Token {self.api_token}"})

            book = Book.objects.get(pk=pk)
            expected_response_data: dict[str, (str, int, dict[str, (str, int)])] = {
                "id": int(book.pk),
                "title": str(book.title),
                "description": str(book.description),
                "author": {
                    "id": int(book.author.id),
                    "first_name": str(book.author.first_name),
                    "second_name": str(book.author.second_name),
                    "date_of_birthday": str(book.author.date_of_birthday)
                },
                "date_of_published": str(book.date_of_published)
            }
            actual_response_data: dict[str, (str, int, dict[str, (str, int)])] = response.json()
            self.assertEqual(first=expected_response_data, second=actual_response_data, msg=error_msg)

            expected_response_status_code: int = 200
            actual_response_status_code: int = response.status_code
            self.assertEqual(first=expected_response_status_code, second=actual_response_status_code, msg=error_msg)

    def test_update_book(self) -> None:
        error_msg: str = "API не корректно обновляет записи книг"
        for pk in range(1, self.max_book_id + 1):
            response = self.client.put(path=f"{reverse('api:books')}{pk}/",
                                       data={"title": "Updated Title", "description": "Updated Description"},
                                       content_type="application/json",
                                       headers={"Authorization": f"Token {self.api_token}"})

            book = Book.objects.get(pk=pk)
            expected_response_data: dict[str, (str, int, dict[str, (str, int)])] = {
                "id": int(book.pk),
                "title": "Updated Title",
                "description": "Updated Description",
                "author": {
                    "id": int(book.author.id),
                    "first_name": str(book.author.first_name),
                    "second_name": str(book.author.second_name),
                    "date_of_birthday": str(book.author.date_of_birthday)
                },
                "date_of_published": str(book.date_of_published)
            }
            actual_response_data: dict[str, (str, int, dict[str, (str, int)])] = response.json()
            self.assertEqual(first=expected_response_data, second=actual_response_data, msg=error_msg)

            expected_response_status_code: int = 200
            actual_response_status_code: int = response.status_code
            self.assertEqual(first=expected_response_status_code, second=actual_response_status_code, msg=error_msg)

    def test_delete_book(self) -> None:
        error_msg: str = "API не корректно удаляет запись книги"
        for pk in range(1, self.max_book_id + 1):
            self.client.delete(path=f"{reverse('api:books')}{pk}/",
                               headers={"Authorization": f"Token {self.api_token}"})

            with self.assertRaises(expected_exception=ObjectDoesNotExist, msg=error_msg):
                Book.objects.get(pk=pk)

        books = Book.objects.all()
        expected_amount_books: int = 0
        actual_amount_books: int = len(books)
        self.assertEqual(first=expected_amount_books, second=actual_amount_books, msg=error_msg)
