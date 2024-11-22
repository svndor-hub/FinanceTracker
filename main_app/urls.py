from django.urls import path
from .views import RegistrationView, UserLoginView, UserProfileView

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
]