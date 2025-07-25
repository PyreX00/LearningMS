from django_filters import rest_framework as filters
from .models import Course, Student

class CourseFilter(filters.FilterSet):
    
    class Meta:
        model = Course
        fields = {
            'name':['icontains'],
            'instructor__name':['icontains']
        }



class StudentFilter(filters.FilterSet):
    progress_report = filters.CharFilter(method='filter_progress_report')

    class Meta:
        model = Student
        fields = ['is_active', 'progress_report']

