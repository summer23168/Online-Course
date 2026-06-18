# Online Course Django Application

A full-featured online course application built with Django, featuring course management, enrollment, and exam functionality.

## Features
- Course listing and enrollment
- Lesson management
- Exam/Quiz system with multiple choice questions
- Exam submission and result evaluation
- Admin interface for content management
- Bootstrap-styled responsive UI

## Tech Stack
- Python 3.x
- Django 4.x
- Bootstrap 5
- SQLite (development)

## Setup Instructions

```bash
# Clone the repository
git clone https://github.com/summer23168/e-learning.git
cd e-learning

# Install dependencies
pip install django pillow

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run the server
python manage.py runserver
```

## Project Structure
```
onlinecourse/
├── models.py       # Course, Lesson, Question, Choice, Submission models
├── views.py        # Views including submit and show_exam_result
├── admin.py        # Admin configuration with inline classes
├── urls.py         # URL patterns including exam routes
└── templates/
    └── onlinecourse/
        ├── course_details_bootstrap.html
        └── exam_result_bootstrap.html
```
