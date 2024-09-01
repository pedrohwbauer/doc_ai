from django.urls import path
from .views import (
    index,
    create_user_message,
)

urlpatterns = [
    path('', index, name="index"),
    path('create-user-message', create_user_message, name="create-user-message"),
]