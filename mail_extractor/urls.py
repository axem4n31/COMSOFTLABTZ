from django.urls import path

from mail_extractor.consumers import WSConsumer
from mail_extractor.views import (
    UserLoginView,
    MailListView,
    MailCreateView,
    MailDetailView,
    UserLogoutView,
    MailUpdateView,
)

app_name = "mail_extractor"

# http
urlpatterns = [
    path("", UserLoginView.as_view(), name="user_login_view"),
    path("logout/", UserLogoutView.as_view(), name="user_logout_view"),
    path("mail-list/", MailListView.as_view(), name="mail_list_view"),
    path("mail-create/", MailCreateView.as_view(), name="mail_create_view"),
    path("mail-detail/<int:pk>", MailDetailView.as_view(), name="mail_detail_view"),
    path("mail-update/<int:pk>", MailUpdateView.as_view(), name="mail_update_view"),
]

# websockets
ws_urlpatterns = [path("ws/message-processing/", WSConsumer.as_asgi())]
