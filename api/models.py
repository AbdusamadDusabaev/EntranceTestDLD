from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    user = models.OneToOneField(User, related_name="author", on_delete=models.PROTECT, verbose_name="Пользователь")
    first_name = models.CharField(max_length=50, null=True, verbose_name="Имя")
    second_name = models.CharField(max_length=50, null=True, verbose_name="Фамилия")
    date_of_birthday = models.DateField(null=True, verbose_name="Дата рождения")
    api_token = models.CharField(max_length=300, null=True, verbose_name="Токен API")

    def verbose_date_of_birthday(self) -> str:
        return str(self.date_of_birthday)

    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"
        ordering = ["-id"]

    def __str__(self) -> str:
        return f"{self.first_name} {self.second_name}"


class Book(models.Model):
    title = models.CharField(max_length=300, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    author = models.ForeignKey(Author, on_delete=models.PROTECT, related_name="books", verbose_name="Автор")
    date_of_published = models.DateField(auto_now_add=True, verbose_name="Дата публикации")

    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"
        ordering = ["-id"]

    def __str__(self) -> str:
        return f"{self.title}"
