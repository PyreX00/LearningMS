from django.shortcuts import render
from .models import Category, Sponsor, Student, StudentCourse, Course, Instructor
from rest_framework.viewsets import ModelViewSet
from .serializer import CategorySerializer, CourseSerializer, StudentSerializer, StudentCourseSerializer,SponserSerializer, InstructorSerializer

# Create your views here.
class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
class SponsorViewSet(ModelViewSet):
    queryset = Sponsor.objects.all()
    serializer_class = SponserSerializer

class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    
class StudentViewSet(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class InstructorViewSet(ModelViewSet):
    queryset = Instructor.objects.all()
    serializer_class = InstructorSerializer
    
class StudentCourseViewSet(ModelViewSet):
    queryset = StudentCourse.objects.all()
    serializer_class = StudentCourseSerializer
    