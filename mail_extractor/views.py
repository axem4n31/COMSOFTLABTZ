from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from mail_extractor.forms import MailForm
from mail_extractor.models import Mail


class UserLoginView(LoginView):
    """Обработка логина пользователей."""

    template_name = "login.html"
    success_url = reverse_lazy("mail_extractor:mail_list_view")


class UserLogoutView(LoginRequiredMixin, LogoutView):
    """Обработка выхода пользователей."""

    template_name = "logout.html"
    next_page = reverse_lazy("mail_extractor:user_login_view")


class MailListView(LoginRequiredMixin, ListView):
    """Отображение списка почтовых ящиков."""

    model = Mail
    template_name = "mail-list.html"
    context_object_name = "mails"


class MailCreateView(LoginRequiredMixin, CreateView):
    """Создание нового почтового ящика."""

    model = Mail
    template_name = "mail-create.html"
    form_class = MailForm
    success_url = reverse_lazy("mail_extractor:mail_list_view")


class MailUpdateView(LoginRequiredMixin, UpdateView):
    """Обновление существующего почтового ящика."""

    model = Mail
    form_class = MailForm
    template_name = "mail-update.html"
    success_url = reverse_lazy("mail_extractor:mail_list_view")


class MailDetailView(LoginRequiredMixin, DetailView):
    """Отображение деталей конкретного почтового ящика."""

    model = Mail
    template_name = "mail-detail.html"
    context_object_name = "mail"
