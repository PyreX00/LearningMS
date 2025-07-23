from django.contrib import admin
from django.shortcuts import render, get_object_or_404
from django.db.models import Count, Q, Sum, Avg, F
from django.urls import path
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Category, Sponsor, Student, Course, Instructor, StudentCourse
from django.contrib.auth.models import Group

def dashboard_view(request):
    """Custom dashboard view"""
    context = {
        **admin.site.each_context(request),
        'total_students': Student.objects.count(),
        'active_students': Student.objects.filter(is_active=True).count(),
        'inactive_students': Student.objects.filter(is_active=False).count(),
        'total_courses': Course.objects.count(),
        'active_courses': Course.objects.filter(is_active=True).count() if hasattr(Course, 'is_active') else Course.objects.count(),
        'total_enrollments': StudentCourse.objects.count(),
        'completed_enrollments': StudentCourse.objects.filter(is_completed=True).count(),
        'pending_enrollments': StudentCourse.objects.filter(is_completed=False).count(),
        'paid_enrollments': StudentCourse.objects.filter(payment_status='paid').count(),
        'unpaid_enrollments': StudentCourse.objects.filter(payment_status='pending').count(),
        
        # Recent enrollments
        'recent_enrollments': StudentCourse.objects.select_related('student', 'course').order_by('-enrollment_date')[:5],
        
        # Students by sponsor
        'students_by_sponsor': Student.objects.values('sponsor__name').annotate(count=Count('id')).order_by('-count')[:5],
    
        'popular_courses': Course.objects.annotate(
            enrollment_count=Count('enrollments')
        ).order_by('-enrollment_count')[:5],   
    }
    
    return render(request, 'admin/dashboard.html', context)

def sponsor_dashboard_list(request):
    """List all sponsors with summary metrics"""
    sponsors_data = []
    
    for sponsor in Sponsor.objects.all():
        # Get students sponsored by this sponsor
        sponsored_students = Student.objects.filter(sponsor=sponsor)
        
        # Get all enrollments for sponsored students
        enrollments = StudentCourse.objects.filter(student__sponsor=sponsor)
        
        # Calculate metrics
        total_students = sponsored_students.count()
        active_students = sponsored_students.filter(is_active=True).count()
        total_enrollments = enrollments.count()
        completed_enrollments = enrollments.filter(is_completed=True).count()
        
        # Fund utilization - total fees for enrolled courses
        total_funds_allocated = enrollments.aggregate(
            total=Sum('course__fee')
        )['total'] or 0
        
        paid_funds = enrollments.filter(payment_status='paid').aggregate(
            total=Sum('course__fee')
        )['total'] or 0
        
        # Success rate
        success_rate = (completed_enrollments / total_enrollments * 100) if total_enrollments > 0 else 0
        
        sponsors_data.append({
            'sponsor': sponsor,
            'total_students': total_students,
            'active_students': active_students,
            'total_enrollments': total_enrollments,
            'completed_enrollments': completed_enrollments,
            'success_rate': round(success_rate, 1),
            'total_funds_allocated': total_funds_allocated,
            'paid_funds': paid_funds,
            'utilization_rate': round((paid_funds / total_funds_allocated * 100) if total_funds_allocated > 0 else 0, 1)
        })
    
    context = {
        **admin.site.each_context(request),
        'sponsors_data': sponsors_data,
    }
    
    return render(request, 'admin/sponsor_dashboard_list.html', context)


original_get_urls = admin.site.get_urls

def get_custom_urls():
    custom_urls = [
        path('dashboard/', admin.site.admin_view(dashboard_view), name='dashboard'),
        path('sponsor-dashboard/', admin.site.admin_view(sponsor_dashboard_list), name='sponsor_dashboard_list'),
    ]
    return custom_urls + original_get_urls()


admin.site.get_urls = get_custom_urls
admin.site.site_header = "Management System Admin"
admin.site.site_title = "MS Admin Portal"
admin.site.index_title = "Welcome to Management System Administration"

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id','name']
    
admin.site.register(Category,CategoryAdmin)

class SponsorAdmin(admin.ModelAdmin):
    list_display = ['id','name','contact_person','email','phone','address']
    search_fields = ['name','contact_person']
    
    def changelist_view(self, request, extra_context=None):
        # Add link to sponsor dashboard in the changelist
        extra_context = extra_context or {}
        extra_context['sponsor_dashboard_url'] = '/admin/sponsor-dashboard/'
        return super().changelist_view(request, extra_context=extra_context)
    
admin.site.register(Sponsor, SponsorAdmin)

class StudentCourseInline(admin.TabularInline):
    model = StudentCourse
    extra = 1


class StudentAdmin(admin.ModelAdmin):
    list_display = ['id','name','age','gender','email','phone','address','sponsor','enrollment_date','is_active']
    list_filter = ['sponsor']
    search_fields = ['name']
    inlines = [StudentCourseInline]

admin.site.register(Student,StudentAdmin)
    


class CourseAdmin(admin.ModelAdmin):
    list_display = ['id','name','description','duration','instructor','category','fee','max_students','enrolled_students_count','available_spots','created_at','updated_at','is_active']
    inlines = [StudentCourseInline]
    
admin.site.register(Course,CourseAdmin)
    

class InstructorAdmin(admin.ModelAdmin):
    list_display = ['id','name','age','gender','email','phone','hire_date']
    
admin.site.register(Instructor,InstructorAdmin)
    

class StudentCourseAdmin(admin.ModelAdmin):
    list_display = ['id','student','course','enrollment_date','completion_date','grade','is_completed','payment_status','notes']
    list_filter = ['is_completed','payment_status']
    date_hierarchy = 'enrollment_date'
    list_editable = ['payment_status', 'is_completed','completion_date','notes']
    
    readonly_fields = ['enrollment_date']

admin.site.register(StudentCourse,StudentCourseAdmin)

