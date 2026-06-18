from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import Course, Enrollment, Question, Choice, Submission


def popular_course_list(request):
    context = {}
    if request.user.is_authenticated:
        courses = Course.objects.order_by('-total_enrollment')[:10]
        for course in courses:
            if request.user in course.users.all():
                course.is_enrolled = True
        context['course_list'] = courses
    else:
        context['course_list'] = Course.objects.order_by('-total_enrollment')[:10]
    return render(request, 'onlinecourse/course_list_bootstrap.html', context)


def enroll(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    user = request.user
    is_enrolled = Enrollment.objects.filter(user=user, course=course).exists()
    if not is_enrolled and user.is_authenticated:
        Enrollment.objects.create(user=user, course=course, mode='honor')
        course.total_enrollment += 1
        course.save()
    return HttpResponseRedirect(
        reverse(viewname='onlinecourse:course_details', args=(course.id,))
    )


@login_required
def course_details(request, course_id):
    context = {}
    course = get_object_or_404(Course, pk=course_id)
    context['course'] = course
    return render(request, 'onlinecourse/course_details_bootstrap.html', context)


def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'onlinecourse/user_registration_bootstrap.html', context)
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        from django.contrib.auth.models import User
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except User.DoesNotExist:
            pass
        if not user_exist:
            user = User.objects.create_user(
                username=username, first_name=first_name,
                last_name=last_name, password=password
            )
            login(request, user)
            return HttpResponseRedirect(reverse(viewname='onlinecourse:index'))
        else:
            context['message'] = "User already exists."
            return render(request, 'onlinecourse/user_registration_bootstrap.html', context)


def login_request(request):
    context = {}
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse(viewname='onlinecourse:index'))
        else:
            context['message'] = "Invalid username or password."
    return render(request, 'onlinecourse/user_login_bootstrap.html', context)


def logout_request(request):
    logout(request)
    return HttpResponseRedirect(reverse(viewname='onlinecourse:index'))


@login_required
def submit(request, course_id):
    """
    Handle exam submission:
    1. Get the enrolled user for this course
    2. Create a Submission object
    3. Collect selected choices from POST data and add to submission
    4. Redirect to show_exam_result
    """
    user = request.user
    course = get_object_or_404(Course, pk=course_id)
    enrollment = get_object_or_404(Enrollment, user=user, course=course)

    submission = Submission.objects.create(enrollment=enrollment)

    submitted_answers = []
    for key, value in request.POST.items():
        if key.startswith('choice'):
            choice_id = int(value)
            submitted_answers.append(choice_id)

    selected_choices = Choice.objects.filter(id__in=submitted_answers)
    submission.choices.set(selected_choices)
    submission.save()

    return HttpResponseRedirect(
        reverse(
            viewname='onlinecourse:show_exam_result',
            args=(course_id, submission.id)
        )
    )


@login_required
def show_exam_result(request, course_id, submission_id):
    """
    Show exam result:
    1. Retrieve course and submission
    2. Calculate total score from correct answers
    3. Pass results to template
    """
    context = {}
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(Submission, pk=submission_id)

    selected_ids = submission.choices.values_list('id', flat=True)

    total_score = 0
    for question in course.question_set.all():
        if question.is_get_score(selected_ids):
            total_score += question.grade

    context['course'] = course
    context['submission'] = submission
    context['selected_ids'] = selected_ids
    context['total_score'] = total_score

    return render(request, 'onlinecourse/exam_result_bootstrap.html', context)
