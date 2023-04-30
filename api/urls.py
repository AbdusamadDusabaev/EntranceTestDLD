from django.urls import path
from .views import (
    RegistrationView, UpdateProfileView, ProfileView, CustomLoginView, CustomLogoutView,
    BooksAPIView, BookDetailAPIView,
    DocumentationView
)


app_name = "api"


urlpatterns = [
    path("registration/", RegistrationView.as_view(), name="registration"),
    path("update-profile/", UpdateProfileView.as_view(), name="update-profile"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    path("books/", BooksAPIView.as_view(), name="books"),
    path("books/<int:pk>/", BookDetailAPIView.as_view(), name="book-detail"),
    path("documentation/", DocumentationView.as_view(), name="documentation"),
]
