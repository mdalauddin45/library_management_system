
from django.urls import path
from .views import UserRegistrationView, UserLoginView,ProfileView
from book.views import ReturnView
 
urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile' ),
    path('return/<int:pk>', ReturnView.as_view(), name='return_book'),
]