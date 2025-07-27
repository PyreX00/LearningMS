from django.contrib import admin
from django.shortcuts import render
from django.db.models import Count, Sum
from django.urls import path
from .models import Category, Sponsor, Student, Course, Instructor, StudentCourse,StudentCourseProgress
from rest_framework.pagination import PageNumberPagination

def dashboard_view(request):
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
        
    
        'recent_enrollments': StudentCourse.objects.select_related('student', 'course').order_by('-enrollment_date')[:5],
        
       
        'students_by_sponsor': Student.objects.values('sponsor__name').annotate(count=Count('id')).order_by('-count')[:5],
    
        'popular_courses': Course.objects.annotate(
            enrollment_count=Count('enrollments')
        ).order_by('-enrollment_count')[:5],   
    }
    
    return render(request, 'admin/dashboard.html', context)

def sponsor_dashboard_list(request):

    sponsors_data = []

    total_students = 0
    total_active_students = 0
    total_enrollments = 0
    total_completed = 0
    total_allocated = 0
    total_paid = 0
    success_rates = []
    utilization_rates = []
    
    for sponsor in Sponsor.objects.all():
        sponsored_students = Student.objects.filter(sponsor=sponsor)
        enrollments = StudentCourse.objects.filter(student__sponsor=sponsor)
        
        sponsor_total_students = sponsored_students.count()
        sponsor_active_students = sponsored_students.filter(is_active=True).count()
        sponsor_total_enrollments = enrollments.count()
        sponsor_completed_enrollments = enrollments.filter(is_completed=True).count()
        
        # Fund utilization - total fees for enrolled courses
        sponsor_total_funds_allocated = enrollments.aggregate(
            total=Sum('course__fee')
        )['total'] or 0
        
        sponsor_paid_funds = enrollments.filter(payment_status='paid').aggregate(
            total=Sum('course__fee')
        )['total'] or 0
        
        # Success rate
        sponsor_success_rate = (sponsor_completed_enrollments / sponsor_total_enrollments * 100) if sponsor_total_enrollments > 0 else 0
        sponsor_utilization_rate = (sponsor_paid_funds / sponsor_total_funds_allocated * 100) if sponsor_total_funds_allocated > 0 else 0
        
        sponsors_data.append({
            'sponsor': sponsor,
            'total_students': sponsor_total_students,
            'active_students': sponsor_active_students,
            'total_enrollments': sponsor_total_enrollments,
            'completed_enrollments': sponsor_completed_enrollments,
            'success_rate': round(sponsor_success_rate, 1),
            'total_funds_allocated': sponsor_total_funds_allocated,
            'paid_funds': sponsor_paid_funds,
            'utilization_rate': round(sponsor_utilization_rate, 1)
        })
        

        total_students += sponsor_total_students
        total_active_students += sponsor_active_students
        total_enrollments += sponsor_total_enrollments
        total_completed += sponsor_completed_enrollments
        total_allocated += sponsor_total_funds_allocated
        total_paid += sponsor_paid_funds
        
        if sponsor_success_rate > 0:
            success_rates.append(sponsor_success_rate)
        if sponsor_utilization_rate > 0:
            utilization_rates.append(sponsor_utilization_rate)
    

    summary_stats = {
        'total_sponsors': len(sponsors_data),
        'total_students': total_students,
        'total_active_students': total_active_students,
        'total_enrollments': total_enrollments,
        'total_completed': total_completed,
        'avg_success_rate': round(sum(success_rates) / len(success_rates), 1) if success_rates else 0,
        'total_allocated': total_allocated,
        'total_paid': total_paid,
        'avg_utilization': round(sum(utilization_rates) / len(utilization_rates), 1) if utilization_rates else 0
    }
    
    context = {
        **admin.site.each_context(request),
        'sponsors_data': sponsors_data,
        'summary_stats': summary_stats,
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
    list_display = ['id','name','age','gender','email','phone','address','sponsor','enrollment_date','is_active','progress_report']
    list_filter = ['sponsor']
    search_fields = ['name']
    inlines = [StudentCourseInline]




    @admin.display(description='Progress Status')
    def progress_report(self, obj):
        first_enrollment = obj.enrollments.first()
        if first_enrollment and hasattr(first_enrollment, 'progress'):
            student_progress = first_enrollment.progress  # No .first()!
            if student_progress:
                return student_progress.progress_status
        return '-'
    
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
    list_per_page = 10
    search_fields = ['student__name']
    
    readonly_fields = ['enrollment_date']

admin.site.register(StudentCourse,StudentCourseAdmin)

class StudentCourseProgressAdmin(admin.ModelAdmin):
    list_display = [
        'student_name', 'course_name', 'progress_status', 
        'overall_progress_percentage', 'attendance_percentage',
        'assignment_marks', 'is_assignment_overdue','assignment_due_date'
    ]
    list_filter = ['progress_status', 'student_course__course']
    search_fields = ['student_course__student__name', 'student_course__course__name']
    list_editable = ['progress_status','assignment_due_date']
    list_per_page = 20
    fieldsets = (
        ('Student & Course', {
            'fields': ('student_course', 'progress_status', 'overall_progress_percentage')
        }),
        ('Assignment', {
            'fields': ('assignment_title', 'assignment_date', 'assignment_due_date', 
                      'assignment_submission_date', 'assignment_marks')
        }),
        ('Attendance', {
            'fields': ('total_classes', 'classes_attended')
        }),
        ('Notes', {
            # 'classes':["collapse"], just to collapse the fields
            'fields': ('instructor_notes', 'last_updated')
        })
    )
    
    readonly_fields = ['overall_progress_percentage', 'last_updated']
    
    def student_name(self, obj):
        return obj.student_course.student.name
    
    def course_name(self, obj):
        return obj.student_course.course.name
    
    def attendance_percentage(self, obj):
        return f"{obj.attendance_percentage}%"
    
    def is_assignment_overdue(self, obj):
        return obj.is_assignment_overdue
    is_assignment_overdue.boolean = True

admin.site.register(StudentCourseProgress, StudentCourseProgressAdmin)

