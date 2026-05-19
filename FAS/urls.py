from django.urls import path
from . import views


urlpatterns = [

    # ================= LOGIN =================

    path(
        '',
        views.login_view,
        name='login'
    ),

    # ================= REGISTER =================

    path(
        'register/',
        views.register_view,
        name='register'
    ),

    # ================= LOGOUT =================

    path(
        'logout/',
        views.logout_view,
        name='logout'
    ),

    # ================= FACULTY DASHBOARD =================

    path(
        'faculty-dashboard/',
        views.faculty_dashboard,
        name='faculty_dashboard'
    ),

    # ================= ADMIN DASHBOARD =================

    path(
        'admin-dashboard/',
        views.admin_dashboard,
        name='admin_dashboard'
    ),

    # ================= SELF APPRAISAL FORM =================

    path(
        'self-appraisal-form/',
        views.self_appraisal_form,
        name='self_appraisal_form'
    ),

    # ================= PROFILE =================

    path(
        'profile/',
        views.profile_view,
        name='profile'
    ),

    # ================= REPORTS =================

    path(
        'reports/',
        views.reports_view,
        name='reports'
    ),

    # ================= UPDATE SUBMISSION STATUS =================

    path(
        'update-submission-status/<int:submission_id>/',
        views.update_submission_status,
        name='update_submission_status'
    ),
    # ================= MY SUBMISSIONS =================

    path(
        'my-submissions/',
        views.my_submissions,
        name='my_submissions'
    ),
    # ================= DOWNLOAD PDF =================

    path(
    'download-pdf/<int:submission_id>/',
    views.download_pdf,
    name='download_pdf'
    ),
    # ================= EDIT PROFILE =================

    path(
        'edit-profile/',
        views.edit_profile,
        name='edit_profile'
    ),

]