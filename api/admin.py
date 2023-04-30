from django.contrib import admin
from .models import Author, Book


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "first_name", "second_name", "date_of_birthday"]
    list_display_links = ["id", "user"]


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "author", "date_of_published"]
    list_display_links = ["id", "title"]
