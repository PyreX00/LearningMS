from django.urls import path
from .views import CategoryViewSet, InstructorViewSet, StudentCourseViewSet, StudentViewSet, SponsorViewSet, CourseViewSet
from rest_framework import routers

router = routers.SimpleRouter()
router.register('category',CategoryViewSet,basename='category' )
router.register('instructor',InstructorViewSet, basename='instructor' )
router.register('course', CourseViewSet, basename='course')
router.register('student', StudentViewSet, basename='student')
router.register('sponsor', SponsorViewSet, basename='sponsor')
router.register('studentcourse', StudentCourseViewSet, basename='studentcourse')

urlpatterns = [
    
] + router.urls
