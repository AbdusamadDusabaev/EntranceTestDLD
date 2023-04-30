from django.test import TestCase
from django.urls import reverse
from rest_framework.response import Response
from api.models import Author


class TestAPIToken(TestCase):
    fixtures = ["users.json", "authors.json", "books.json", "tokens.json"]

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        author: str = Author.objects.get(user=2)
        api_token = author.api_token

        cls.api_token = api_token

    def test_api_with_valid_api_token(self) -> None:
        error_msg: str = "API работает некорректно при валидном API Token"
        for url in [reverse("api:books"), f"{reverse('api:books')}2/"]:
            response: Response = self.client.get(path=url, headers={"Authorization": f"Token {self.api_token}"})

            error_response_status_code: int = 401
            actual_response_status_code: int = response.status_code
            self.assertNotEqual(first=error_response_status_code, second=actual_response_status_code, msg=error_msg)

    def test_api_with_invalid_api_token(self) -> None:
        error_msg: str = "API работает некорректно при невалидном API Token"
        for url in [reverse("api:books"), f"{reverse('api:books')}2/"]:
            response = self.client.get(path=url,
                                       headers={"Authorization": f"Token InvalidTokenAPI"})

            expected_response_data: dict[str, str] = {"detail": "Недопустимый токен."}
            actual_response_data: dict[str, (str, int, dict[str, (str, int)])] = response.json()
            self.assertEqual(first=expected_response_data, second=actual_response_data, msg=error_msg)

            expected_response_status_code: int = 401
            actual_response_status_code: int = response.status_code
            self.assertEqual(first=expected_response_status_code, second=actual_response_status_code, msg=error_msg)

    def test_api_without_api_token(self) -> None:
        error_msg: str = "API работает некорректно при отсутствующем API Token"
        for url in [reverse("api:books"), f"{reverse('api:books')}2/"]:
            response = self.client.get(path=url)

            expected_response_data: dict[str, str] = {"detail": "Учетные данные не были предоставлены."}
            actual_response_data: dict[str, (str, int, dict[str, (str, int)])] = response.json()
            self.assertEqual(first=expected_response_data, second=actual_response_data, msg=error_msg)

            expected_response_status_code: int = 401
            actual_response_status_code: int = response.status_code
            self.assertEqual(first=expected_response_status_code, second=actual_response_status_code, msg=error_msg)
