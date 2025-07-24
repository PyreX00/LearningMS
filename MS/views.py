from django.shortcuts import render
from .models import Category, Sponsor, Student, StudentCourse, Course, Instructor
from rest_framework.viewsets import ModelViewSet
from .serializer import CategorySerializer, CourseSerializer, StudentSerializer, StudentCourseSerializer,SponserSerializer, InstructorSerializer
from rest_framework.pagination import PageNumberPagination
from .pagination import CategoryPagination
from django_filters import rest_framework as filters
from .filters import CourseFilter

# Create your views here.
class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
    pagination_class = CategoryPagination
    
class SponsorViewSet(ModelViewSet):
    queryset = Sponsor.objects.all()
    serializer_class = SponserSerializer
    
    pagination_class = PageNumberPagination

class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    
    pagination_class = PageNumberPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = (CourseFilter)
    
class StudentViewSet(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    
    pagination_class = PageNumberPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('name','is_active')
    
    

class InstructorViewSet(ModelViewSet):
    queryset = Instructor.objects.all()
    serializer_class = InstructorSerializer
    
    pagination_class = PageNumberPagination
    
class StudentCourseViewSet(ModelViewSet):
    queryset = StudentCourse.objects.all()
    serializer_class = StudentCourseSerializer
    
    pagination_class = PageNumberPagination
    