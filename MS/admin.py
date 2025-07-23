from django.contrib import admin
from .models import Category, Sponsor, Student, Course, Instructor, StudentCourse

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id','name']
    
admin.site.register(Category,CategoryAdmin)

class SponsorAdmin(admin.ModelAdmin):
    list_display = ['id','name','contact_person','email','phone','address']
    search_fields = ['name','contact_person']
    
admin.site.register(Sponsor, SponsorAdmin)

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['id','name','age','gender','email','phone','address','sponsor','enrollment_date','is_active']
    list_filter = ['sponsor']
    search_fields = ['name']

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['id','name','description','duration','instructor','category','fee','max_students','created_at','updated_at','is_active']
    
@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ['id','name','age','gender','email','phone','hire_date']
    
@admin.register(StudentCourse)
class StudentCourseAdmin(admin.ModelAdmin):
    list_display = ['id','student','course','enrollment_date','completion_date','grade','is_completed','payment_status','notes']
    list_filter = ['is_completed','payment_status']