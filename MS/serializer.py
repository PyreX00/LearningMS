from rest_framework.serializers import ModelSerializer
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
    class Meta:
        model = Student
        fields = '__all__'

class CourseSerializer(ModelSerializer):
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
