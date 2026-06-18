from django.urls import path
from . import views

app_name = 'onlinecourse'

urlpatterns = [
    path(route='', view=views.popular_course_list, name='index'),
    path(route='enroll/<int:course_id>/', view=views.enroll, name='enroll'),
    path(route='course/<int:course_id>/', view=views.course_details, name='course_details'),
    path(route='registration/', view=views.registration_request, name='registration'),
    path(route='login/', view=views.login_request, name='login'),
    path(route='logout/', view=views.logout_request, name='logout'),
    # Exam submission and result paths
    path(
        route='course/<int:course_id>/submit/',
        view=views.submit,
        name='submit'
    ),
    path(
        route='course/<int:course_id>/submission/<int:submission_id>/result/',
        view=views.show_exam_result,
        name='show_exam_result'
    ),
]
