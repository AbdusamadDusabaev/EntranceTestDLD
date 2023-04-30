from django.views.generic import CreateView, TemplateView
from django.views import View

from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login

from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest
from django.forms import Form

from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.serializers import Serializer
from rest_framework import status
from rest_framework import mixins

from .models import Book, Author
from .serializers import BookSerializer
from .validators import validate_registration_data, validate_create_book_data


class DocumentationView(TemplateView):
    template_name = "api/documentation.html"


class CustomLoginView(LoginView):
    template_name: str = "api/login.html"
    next_page: str = reverse_lazy("api:profile")


class CustomLogoutView(LogoutView):
    next_page: str = reverse_lazy("api:login")


class ProfileView(LoginRequiredMixin, View):
    @staticmethod
    def get(request: HttpRequest) -> HttpResponse:
        author: Author = Author.objects.get(user=request.user)
        if author.first_name is not None:
            return render(request=request, template_name="api/profile.html")
        return redirect("api:update-profile")


class RegistrationView(CreateView):
    form_class = UserCreationForm
    template_name = "api/registration.html"

    def form_valid(self, form: Form) -> HttpResponse:
        if form.is_valid():
            username: str = form.cleaned_data["username"]
            password: str = form.cleaned_data["password1"]
            user: User = User.objects.create_user(username=username, password=password)
            api_token: Token = Token.objects.create(user=user)
            author: Author = Author(user=user, api_token=api_token)
            author.save()
            login(request=self.request, user=user)
            return redirect(reverse("api:update-profile"))
        return HttpResponse(form.errors, status=HttpResponseBadRequest)


class UpdateProfileView(LoginRequiredMixin, View):
    @staticmethod
    def get(request: HttpRequest, error_messages: list[str] = None) -> HttpResponse:
        context: dict[str, (list[str], None)] = {
            "error_messages": error_messages
        }
        return render(request=request, template_name="api/update-profile.html", context=context)

    def post(self, request: HttpRequest) -> HttpResponse:
        registration_data_is_valid: tuple[bool, (list[str], None)] = validate_registration_data(request=request)
        if registration_data_is_valid[0]:
            author: Author = Author.objects.get(user=request.user)
            author.first_name = request.POST["first_name"]
            author.second_name = request.POST["second_name"]
            author.date_of_birthday = request.POST["date_of_birthday"]
            author.save()
            return redirect("api:profile")
        return self.get(request=request, error_messages=registration_data_is_valid[1])


class BooksAPIView(mixins.ListModelMixin, mixins.CreateModelMixin, GenericAPIView):
    authentication_classes: list = [TokenAuthentication]
    permission_classes: list = [IsAuthenticated]
    queryset: list = Book.objects.all()
    serializer_class: Serializer = BookSerializer

    def get(self, request: HttpRequest, *args, **kwargs) -> Response:
        return self.list(request=request, *args, **kwargs)

    def post(self, request: HttpRequest) -> Response:
        data_is_valid: tuple[bool, (list[str], None)] = validate_create_book_data(request=request)
        if data_is_valid[0]:
            book: Book = Book(
                title=request.data["title"],
                description=request.data["description"],
                author=request.user.author,
            )
            book.save()

            response_data: dict[str, str] = {
                "id": book.pk,
                "title": book.title,
                "description": book.description,
                "author": {
                    "id": book.author.id,
                    "first_name": book.author.first_name,
                    "second_name": book.author.second_name,
                    "date_of_birthday": str(book.author.date_of_birthday)
                },
                "date_of_published": book.date_of_published
            }
            return Response(response_data, status=status.HTTP_201_CREATED)

        error_messages: list[str] = data_is_valid[1]
        return Response(error_messages, status=status.HTTP_400_BAD_REQUEST)


class BookDetailAPIView(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, GenericAPIView):
    authentication_classes: list = [TokenAuthentication]
    permission_classes: list = [IsAuthenticated]
    queryset: list = Book.objects.all()
    serializer_class: Serializer = BookSerializer

    def get(self, request: HttpRequest, *args, **kwargs) -> Response:
        return self.retrieve(request, *args, **kwargs)

    def put(self, request: HttpRequest, *args, **kwargs) -> Response:
        return self.update(request, *args, **kwargs)

    def delete(self, request: HttpRequest, *args, **kwargs) -> Response:
        return self.destroy(request, *args, **kwargs)
