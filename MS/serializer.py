from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from django_filters import rest_framework as filters
from django.utils import timezone
from .models import Category, Instructor,Course,Student,Sponsor,StudentCourse

class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"
        
class InstructorSerializer(ModelSerializer):
    class Meta:
        model = Instructor
        fields = "__all__"

class StudentSerializer(ModelSerializer):
    sponsor = serializers.StringRelatedField()
    progress_status = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = ['id','name','age','gender','email','phone','address','sponsor','enrollment_date','is_active','progress_status'] 
    
    def get_progress_status(self, obj):
        first_enrollment = obj.enrollments.first()
        if first_enrollment and hasattr(first_enrollment, 'progress'):
            student_progress = first_enrollment.progress
            if student_progress:
                return student_progress.progress_status
        return '-'

        


class CourseSerializer(ModelSerializer):
    
    instructor = serializers.StringRelatedField()
    class Meta:
        model = Course
        fields = '__all__'
        
class SponserSerializer(ModelSerializer):
    class Meta:
        model = Sponsor 
        fields = "__all__"
        
class StudentCourseSerializer(ModelSerializer):
    class Meta:
        model = StudentCourse
        fields = '__all__'       
