from django.shortcuts import render
from .models import Category, Sponsor, Student, StudentCourse, Course, Instructor, StudentCourseProgress
from rest_framework.viewsets import ModelViewSet
from .serializer import CategorySerializer, CourseSerializer, StudentSerializer, StudentCourseSerializer,SponserSerializer, InstructorSerializer, StudentCourseProgressSerializer
from rest_framework.pagination import PageNumberPagination
from .pagination import CategoryPagination
from django_filters import rest_framework as filters
from rest_framework import filters as fa
from .filters import CourseFilter
from .persmission import IsAdminOrReadOnly, StudentAccess,StudentCourseAccess, StudentCourseProgressAccess

# Create your views here.
class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
    pagination_class = CategoryPagination
    permission_classes = [IsAdminOrReadOnly]

class SponsorViewSet(ModelViewSet):
    queryset = Sponsor.objects.all()
    serializer_class = SponserSerializer
    
    
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = PageNumberPagination

class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = PageNumberPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = (CourseFilter)
    
class StudentViewSet(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    
    permission_classes = [StudentAccess]
    pagination_class = PageNumberPagination
    filter_backends = (filters.DjangoFilterBackend, fa.SearchFilter)
    filterset_fields = ['is_active']
    

class InstructorViewSet(ModelViewSet):
    queryset = Instructor.objects.all()
    serializer_class = InstructorSerializer
    
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = PageNumberPagination
    
class StudentCourseViewSet(ModelViewSet):
    queryset = StudentCourse.objects.all()
    serializer_class = StudentCourseSerializer
    
    pagination_class = PageNumberPagination
    permission_classes = [StudentCourseAccess]

class StudentCourseProgressViewSet(ModelViewSet):
    queryset = StudentCourseProgress.objects.all()
    serializer_class = StudentCourseProgressSerializer
    
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ['progress_status']
    pagination_class = PageNumberPagination
    permission_classes = [StudentCourseProgressAccess]
    