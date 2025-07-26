

# Learning Management System (LMS)

A comprehensive Learning Management System built with Django and Django REST Framework, featuring multiple user roles including Admin, Instructor, Student, and Sponsor.

## 🚀 Features

### User Roles
- **Admin**: Oversee platform operations and analytics
- **Instructor**: Manage courses, create assessments, and track student progress
- **Student**: Enroll in courses, complete assessments, and track learning progress
- **Sponsor**: Fund students and monitor their educational journey

### Core Functionality
- **Course Management**: Complete CRUD operations for courses, lessons, and assessments
- **User Authentication**: Role-based authentication using Django Groups
- **Search & Filtering**: Advanced search capabilities for courses and student filtering
- **Pagination**: Efficient data pagination for all major entities
- **Analytics Dashboard**: Comprehensive metrics and reporting
- **Email Notifications**: Automated notifications for deadlines and progress updates
- **Sponsorship System**: Complete sponsor-student relationship management

## 🛠 Technology Stack

- **Backend**: Django 4.2+, Django REST Framework
- **Database**: PostgreSQL
- **Authentication**: Django built-in authentication with Groups
- **API Documentation**: DRF Spectacular (Swagger/OpenAPI)
- **Email**: Django Email Backend

## 📋 Prerequisites

- Python 3.8+
- PostgreSQL (optional, SQLite works for development)
- pip (Python package manager)
- Virtual environment (recommended)

## 🔧 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/PyreX00/LearningMS
cd LearningMS
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv lms_env

# Activate virtual environment
# On Windows
lms_env\Scripts\activate

# On macOS/Linux
source lms_env/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Configuration

Create a `.env` file in the project root:

```env


# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Email Configuration
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Media and Static Files
MEDIA_URL=/media/
STATIC_URL=/static/
```

### 5. Database Setup

```bash
# Create database migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser (Admin)
python manage.py createsuperuser

# Load initial data (optional)
python manage.py loaddata fixtures/initial_data.json
```

### 6. Create User Groups

```bash
# Run custom management command to create user groups
python manage.py setup_groups
```

### 7. Collect Static Files

```bash
python manage.py collectstatic
```

### 8. Run Development Server

```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`

## 🎯 Usage Guide

### Admin Dashboard
- Access: `http://127.0.0.1:8000/admin/`
- Features: User management, course oversight, platform analytics

### API Endpoints
- Base URL: `http://127.0.0.1:8000/api/v1/`
- Documentation: `http://127.0.0.1:8000/api/docs/` (Swagger UI)
- Schema: `http://127.0.0.1:8000/api/schema/`


### Core Workflows

#### For Students:
1. Register and verify email
2. Browse available courses with search/filter
3. Enroll in courses
4. Complete lessons and assessments
5. Track progress on dashboard

#### For Instructors:
1. Create and manage courses
2. Add lessons and assessments
3. Monitor student progress
4. Send notifications and updates

#### For Sponsors:
1. Browse and sponsor students
2. Track sponsored students' progress
3. Receive progress reports
4. Manage funding allocations

## 📚 API Documentation

### Interactive Documentation
Visit `http://127.0.0.1:8000/api/docs/` for comprehensive interactive API documentation powered by DRF Spectacular.

### Key API Endpoints

#### Authentication
```
POST /api/v1/auth/login/
POST /api/v1/auth/logout/
POST /api/v1/auth/register/student/
POST /api/v1/auth/register/instructor/
POST /api/v1/auth/register/sponsor/
```

#### Courses
```
GET    /api/v1/courses/              # List courses with search/filter
POST   /api/v1/courses/              # Create course (Instructor only)
GET    /api/v1/courses/{id}/         # Course details
PUT    /api/v1/courses/{id}/         # Update course
DELETE /api/v1/courses/{id}/         # Delete course
POST   /api/v1/courses/{id}/enroll/  # Enroll in course
```

#### Students
```
GET    /api/v1/student/             # List students (with filtering)
GET    /api/v1/student/{id}/        # Student profile
PUT    /api/v1/student/{id}/        # Update profile
GET    /api/v1/student/{id}/progress/ # Student progress
```

#### Sponsorships
```
GET    /api/v1/sponsor/         # List sponsorships
POST   /api/v1/sponsor/         # Create sponsorship
GET    /api/v1/sponsor/{id}/    # Sponsorship details
PUT    /api/v1/sponsor/{id}/    # Update sponsorship
```

#### Analytics
```
GET    /admin/dashboard/      # Admin dashboard data
GET    /admin/sponsor_dashboard    # Sponsor dashboard data
```

### Query Parameters

#### Course Search & Filtering
```
GET /api/v1/courses/?search=python&instructor=john&difficulty=beginner&page=1
```

#### Student Filtering
```
GET /api/v1/students/?status=active&progress_min=50&sponsor=123&page=1
```

### Authentication Headers
```
Authorization: Token your-auth-token-here
```

### Response Format
All API responses follow this structure:
```json
{
    "success": true,
    "data": {
        // Response data
    },
    "message": "Success message",
    "errors": null
}
```

### Error Handling
```json
{
    "success": false,
    "data": null,
    "message": "Error message",
    "errors": {
        "field": ["Error details"]
    }
}
```

## 🗄 Database Schema

### Core Models
- **User**: Extended Django user with role-based permissions
- **Course**: Course information and metadata
- **Lesson**: Individual lessons within courses
- **Assessment**: Quizzes and assignments
- **Enrollment**: Student-course relationships
- **Sponsorship**: Sponsor-student funding relationships
- **Progress**: Student progress tracking


## 🔍 Search & Filtering

### Course Search
- Search by course name, description, or instructor name
- Filter by difficulty level, category, or price range
- Sort by popularity, rating, or creation date

### Student Filtering (for Sponsors)
- Filter by enrollment status, progress percentage
- Search by name or email
- Sort by progress or enrollment date

## 📊 Analytics Features

### Admin Dashboard
- Total users by role
- Active courses and enrollments
- Revenue and sponsorship metrics
- User activity trends

### Sponsor Dashboard
- Sponsored students progress
- Fund utilization tracking
- ROI on educational investments
- Completion rates

## 📧 Email Notifications

### Automated Emails
- Assignment deadline reminders
- Progress milestone notifications

### Email Templates
Located in `templates/emails/` directory, customizable for branding.


**Happy Learning! 🎓**