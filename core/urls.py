from django.urls import path
from .views import LoginViewSet

urlpatterns = [
    path('login/', LoginViewSet)
    
]
