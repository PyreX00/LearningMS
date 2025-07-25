from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from django_filters import rest_framework as filters
from django.utils import timezone
from .models import Category, Instructor,Course,Student,Sponsor,StudentCourse, StudentCourseProgress

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
    student = serializers.StringRelatedField()
    course = serializers.StringRelatedField()
    sponsor = serializers.SerializerMethodField()
    instructor = serializers.SerializerMethodField()
    
    class Meta:
        model = StudentCourse
        fields = ['id',
        'student',
        'course',
        'sponsor',
        'instructor',
        'enrollment_date',
        'completion_date',
        'grade',
        'is_completed',
        'payment_status',
        'notes']       
    
    def get_sponsor(self,obj):
        return obj.student.sponsor.name
    
    def get_instructor(self,obj):
        return obj.course.instructor.name
    
class StudentCourseProgressSerializer(ModelSerializer):
    student = serializers.SerializerMethodField()
    course = serializers.SerializerMethodField()
    sponsor = serializers.SerializerMethodField()
    instructor = serializers.SerializerMethodField()
    class Meta:
        model = StudentCourseProgress
        fields = ['id',
                  'student',
                  'course',
                  'instructor',
                  'sponsor',
                  'assignment_title',
                  'assignment_date',
                  'assignment_due_date',
                  'assignment_submission_date',
                  'assignment_marks',
                  'total_classes',
                  'classes_attended',
                  'overall_progress_percentage',
                  'progress_status',
                  'instructor_notes',
                  'last_updated']
        
    def get_student(self,obj):
        return obj.student_course.student.name
    
    def get_course(self,obj):
        return obj.student_course.course.name
    
    def get_sponsor(self,obj):
        return obj.student_course.student.sponsor.name
    
    def get_instructor(self,obj):
        return obj.student_course.course.instructor.name