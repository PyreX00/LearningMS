from django.contrib import admin
from django.shortcuts import render 
from django.db.models import Count, Q
from django.urls import path
from .models import Category, Sponsor, Student, Course, Instructor, StudentCourse

# Register your models here.
# Custom admin site to override index
class CustomAdminSite(admin.AdminSite):
    site_header = "Management System Admin"
    site_title = "MS Admin Portal"
    index_title = "Welcome to Management System Administration"
    
    def get_urls(self):
        custom_urls = [
            path('dashboard/', self.admin_view(self.dashboard_view), name='dashboard'),
        ]
        default_urls = super().get_urls()
        return custom_urls + default_urls

    
    def has_permission(self, request):
        return  True

    
    def dashboard_view(self, request):
        
        context = {
            **self.each_context(request),
            'total_students': Student.objects.count(),
            'active_students': Student.objects.filter(is_active=True).count(),
            'inactive_students': Student.objects.filter(is_active=False).count(),
            'total_courses': Course.objects.count(),
            'active_courses': Course.objects.filter(is_active=True).count() if hasattr(Course, 'is_active') else Course.objects.count(),
            'total_enrollments': StudentCourse.objects.count(),
            'completed_enrollments': StudentCourse.objects.filter(is_completed=True).count(),
            'pending_enrollments': StudentCourse.objects.filter(is_completed=False).count(),
            'paid_enrollments': StudentCourse.objects.filter(payment_status='paid').count(),
            'unpaid_enrollments': StudentCourse.objects.filter(payment_status='unpaid').count(),
            
            # Recent enrollments
            'recent_enrollments': StudentCourse.objects.select_related('student', 'course').order_by('-enrollment_date')[:5],
            
            # Students by sponsor
            'students_by_sponsor': Student.objects.values('sponsor__name').annotate(count=Count('id')).order_by('-count')[:5],
        
            'popular_courses': Course.objects.annotate(
                enrollment_count=Count('enrollments')
            ).order_by('-enrollment_count')[:5],   
        }
        
        return render(request, 'admin/dashboard.html', context)


# Create custom admin site instance
admin_site = CustomAdminSite(name='custom_admin')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id','name']
    
admin_site.register(Category,CategoryAdmin)

class SponsorAdmin(admin.ModelAdmin):
    list_display = ['id','name','contact_person','email','phone','address']
    search_fields = ['name','contact_person']
    
admin_site.register(Sponsor, SponsorAdmin)

class StudentCourseInline(admin.TabularInline):
    model = StudentCourse
    extra = 1


class StudentAdmin(admin.ModelAdmin):
    list_display = ['id','name','age','gender','email','phone','address','sponsor','enrollment_date','is_active']
    list_filter = ['sponsor']
    search_fields = ['name']
    inlines = [StudentCourseInline]

admin_site.register(Student,StudentAdmin)
    


class CourseAdmin(admin.ModelAdmin):
    list_display = ['id','name','description','duration','instructor','category','fee','max_students','enrolled_students_count','available_spots','created_at','updated_at','is_active']
    inlines = [StudentCourseInline]
    
admin_site.register(Course,CourseAdmin)
    

class InstructorAdmin(admin.ModelAdmin):
    list_display = ['id','name','age','gender','email','phone','hire_date']
    
admin_site.register(Instructor,InstructorAdmin)
    

class StudentCourseAdmin(admin.ModelAdmin):
    list_display = ['id','student','course','enrollment_date','completion_date','grade','is_completed','payment_status','notes']
    list_filter = ['is_completed','payment_status']
    date_hierarchy = 'enrollment_date'
    list_editable = ['payment_status', 'is_completed','completion_date','notes']
    
    readonly_fields = ['enrollment_date']

    

admin_site.register(StudentCourse,StudentCourseAdmin)

  