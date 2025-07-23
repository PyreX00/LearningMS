from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.validators import ValidationError
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth import  authenticate

# Create your views here.
class LoginViewSet(APIView):
    def post(self,request):
        username = request.data.get("username")
        password = request.data.get("password")
        
        if username is None or password is None:
            raise ValidationError({
                "Details":"Username and password are required"
            })
        
        user = authenticate(username = username, password = password)
        
        if user:
            token = Token.objects.get_or_create(user=user)
            return Response({
                
                "username": username
                "token":token.key
            })
        
            