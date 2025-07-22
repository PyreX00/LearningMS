from django.urls import path
from .views import home

urlpatterns = [
    path("api/v1", home )
    
]
