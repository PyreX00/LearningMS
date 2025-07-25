from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from .models import StudentCourseProgress, StudentCourse
from django.utils import timezone
from datetime import timedelta
from background_task import background
import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender=StudentCourseProgress)
def send_sponsor_completion_report(sender, instance, created, **kwargs):

    if instance.progress_status == 'completed':
        try:
            student_course = instance.student_course
            student = student_course.student
            course = student_course.course
            sponsor = student.sponsor
            

            if not sponsor.email:
                logger.info(f"No sponsor email for student {student.name}, sponsor: {sponsor.name}")
                return
            
            context = {
                'student': student,
                'course': course,
                'instructor': course.instructor,
                'sponsor': sponsor,
                'student_course': student_course,
                'progress': instance,
                'completion_date': student_course.completion_date or instance.last_updated.date(),
                'enrollment_date': student_course.enrollment_date,
                'course_duration': instance.days_since_enrollment,
                'final_grade': instance.assignment_marks or 0,
                'assignment_marks': instance.assignment_marks or 'N/A',
                'attendance_rate': instance.attendance_percentage,
                'overall_progress': instance.overall_progress_percentage,
                'course_fee': course.fee,
                'payment_status': student_course.payment_status,
                'total_classes': instance.total_classes,
                'classes_attended': instance.classes_attended,
            }
            
            
            html_content = f"""
                <html>
                <body>
                    <h2>Course Completion Report</h2>
                    <p>Dear {sponsor.name},</p>
                    <p><strong>{student.name}</strong> has successfully completed the course: <strong>{course.name}</strong></p>
                    <p><strong>Performance Summary:</strong></p>
                    <ul>
                        <li>Overall Progress: {instance.overall_progress_percentage}%</li>
                        <li>Attendance Rate: {instance.attendance_percentage}%</li>
                        <li>Classes Attended: {instance.classes_attended}/{instance.total_classes}</li>
                        <li>Assignment Score: {instance.assignment_marks or 'N/A'}</li>
                    </ul>
                    <p><strong>Course Details:</strong></p>
                    <ul>
                        <li>Instructor: {course.instructor.name}</li>
                        <li>Duration: {instance.days_since_enrollment} days</li>
                        <li>Completion Date: {student_course.completion_date or instance.last_updated.date()}</li>
                    </ul>
                    <p>Best regards,<br>Learning Management System</p>
                </body>
                </html>
                """
            
            to_emails = [sponsor.email]
            cc_emails = []
            
            if course.instructor.email:
                cc_emails.append(course.instructor.email)
            
            email = EmailMessage(
                subject=f"Course Completion Report - {student.name} - {course.name}",
                body=html_content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=to_emails,
                cc=cc_emails if cc_emails else None,
            )
            email.content_subtype = 'html'
        
            result = email.send()
            
            if result == 1:
                logger.info(f"Sponsor completion report sent for {student.name} to {sponsor.email}")
            else:
                logger.warning(f"Email sending returned {result} for {student.name}")
                
        except Exception as e:
            logger.error(f"Failed to send sponsor completion report: {str(e)}")
            
            
@receiver(post_save, sender=StudentCourseProgress)
def send_student_completion_assessment(sender, instance, created, **kwargs):
 
    if instance.progress_status != 'completed':
        return

    try:
        student_course = instance.student_course
        student = student_course.student
        course = student_course.course
        instructor = course.instructor

        if not student.email:
            logger.info(f"No email for student {student.name}, skipping assessment email.")
            return

        context = {
            'student': student,
            'course': course,
            'instructor': instructor,
            'student_course': student_course,
            'progress': instance,
            'completion_date': student_course.completion_date or instance.last_updated.date(),
            'final_grade': instance.assignment_marks or 0,
            'assignment_marks': instance.assignment_marks or 'N/A',
            'attendance_rate': instance.attendance_percentage,
            'overall_progress': instance.overall_progress_percentage,
            'total_classes': instance.total_classes,
            'classes_attended': instance.classes_attended,
        }

      
        html_content = f"""
            <html><body>
                <h2>Course Assessment Result</h2>
                <p>Dear {student.name},</p>
                <p>Congratulations on completing {course.name}!</p>
                <ul>
                    <li>Final Grade: {instance.assignment_marks or 'N/A'}</li>
                    <li>Overall Progress: {instance.overall_progress_percentage}%</li>
                    <li>Attendance Rate: {instance.attendance_percentage}%</li>
                    <li>Classes Attended: {instance.classes_attended}/{instance.total_classes}</li>
                </ul>
                <p>We hope you found the course valuable.</p>
                <p>Best regards,<br>{instructor.name}</p>
            </body></html>
            """

        email = EmailMessage(
            subject=f"Assessment Result - {course.name}",
            body=html_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[student.email],
            cc=[instructor.email] if instructor.email else None
        )
        email.content_subtype = 'html'
        sent = email.send()

        if sent == 1:
            logger.info(f"Assessment result email sent to student {student.name} at {student.email}")
        else:
            logger.warning(f"Email.send() returned {sent} for student {student.name}")

    except Exception as exc:
        logger.error(f"Error sending assessment email: {exc}")