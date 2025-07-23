from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=70, unique=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Categories"

class Instructor(models.Model):
    MALE = "M"
    FEMALE = "F"
    
    GENDER_CHOICES = [
        (MALE, "Male"),
        (FEMALE, "Female"),
    ]
    
    name = models.CharField(max_length=70)
    age = models.PositiveIntegerField( validators=[MinValueValidator(18), MaxValueValidator(100)] )
    gender = models.CharField(
        max_length=1, 
        choices=GENDER_CHOICES, 
        default=MALE
    )
    email = models.EmailField(unique=True, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    hire_date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} ({self.gender})"
    
    class Meta:
        ordering = ['name']

class Course(models.Model):  # Singular name is better
    name = models.CharField(max_length=70, unique=True)
    description = models.TextField(blank=True, null=True)
    duration = models.PositiveIntegerField( verbose_name="Duration (Days)", validators=[MinValueValidator(1), MaxValueValidator(365)] )
    instructor = models.ForeignKey( Instructor,  on_delete=models.CASCADE, related_name='courses')
    category = models.ForeignKey( Category, on_delete=models.PROTECT, related_name='courses' )
    fee = models.PositiveIntegerField( validators = [MinValueValidator(0)] )
    max_students = models.PositiveIntegerField( default=30, validators=[MinValueValidator(1), MaxValueValidator(100)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.name} - {self.instructor.name}"
    
    @property
    def enrolled_students_count(self):
        return self.enrollments.count()
    
    @property
    def available_spots(self):
        return self.max_students - self.enrolled_students_count
    
    def is_full(self):
        return self.enrolled_students_count >= self.max_students
    
    class Meta:
        ordering = ['name']
        unique_together = ['name', 'instructor']  

class Sponsor(models.Model):
    name = models.CharField(max_length=70, unique=True)
    contact_person = models.CharField(max_length=70, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']

class Student(models.Model):
    MALE = "M"
    FEMALE = "F"
    
    GENDER_CHOICES = [
        (MALE, "Male"),
        (FEMALE, "Female"),
    ]
    
    name = models.CharField(max_length=70)
    age = models.PositiveIntegerField( validators=[MinValueValidator(16), MaxValueValidator(55)] )
    gender = models.CharField( max_length=1, choices=GENDER_CHOICES, default=MALE )
    email = models.EmailField(unique=True, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    sponsor = models.ForeignKey(Sponsor, on_delete=models.PROTECT, related_name='students' )
    enrollment_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.name} - {self.sponsor.name}"
    
    class Meta:
        ordering = ['name']

class StudentCourse(models.Model): 
    """
    Many-to-Many relationship between Students and Courses
    with additional enrollment information
    """
    student = models.ForeignKey( Student, on_delete=models.CASCADE, related_name='enrollments' )
    course = models.ForeignKey( Course, on_delete=models.CASCADE, related_name='enrollments')
    enrollment_date = models.DateField(auto_now_add=True)
    completion_date = models.DateField(blank=True, null=True)
    grade = models.CharField(
        max_length=2,
        choices=[
            ('A+', 'A+'), ('A', 'A'), ('A-', 'A-'),
            ('B+', 'B+'), ('B', 'B'), ('B-', 'B-'),
            ('C+', 'C+'), ('C', 'C'), ('C-', 'C-'),
            ('D', 'D'), ('F', 'F')
        ],
        blank=True, 
        null=True
    )
    is_completed = models.BooleanField(default=False)
    payment_status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('partial', 'Partial'),
            ('paid', 'Paid'),
            ('refunded', 'Refunded'),
        ],
        default='pending'
    )
    notes = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.student.name} - {self.course.name}"
    
    def save(self, *args, **kwargs):
        if self.completion_date and not self.is_completed:
            self.is_completed = True
        super().save(*args, **kwargs)
    
    class Meta:
        unique_together = ['student', 'course'] 
        ordering = ['-enrollment_date']
        verbose_name = "Student Enrollment"
        verbose_name_plural = "Student Enrollments"
