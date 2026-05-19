from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.db.models import Q

from reportlab.pdfgen import canvas

from .models import (
    FacultyProfile,
    Publication,
    SeminarEvent,
    Project,
    Lecture,
    SelfAppraisalSubmission
)


# ================= LOGIN =================

def login_view(request):

    if request.method == "POST":

        role = request.POST.get("role")

        username = request.POST.get("username")

        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            # ADMIN CHECK
            if role == "admin" and not user.is_staff:

                messages.error(
                    request,
                    "This account is not registered as Admin."
                )

                return redirect('login')

            # FACULTY CHECK
            if role == "faculty" and user.is_staff:

                messages.error(
                    request,
                    "This account is not registered as Faculty."
                )

                return redirect('login')

            login(request, user)

            messages.success(
                request,
                "Login successful."
            )

            # REDIRECT
            if role == "admin":

                return redirect('admin_dashboard')

            return redirect('faculty_dashboard')

        else:

            messages.error(
                request,
                "Invalid username or password."
            )

            return redirect('login')

    return render(request, 'login.html')


# ================= REGISTER =================

def register_view(request):

    if request.method == "POST":

        full_name = request.POST.get("full_name")

        username = request.POST.get("username")

        email = request.POST.get("email")

        employee_code = request.POST.get("employee_code")

        department = request.POST.get("department")

        password = request.POST.get("password")

        confirm_password = request.POST.get("confirm_password")

        # PASSWORD CHECK
        if password != confirm_password:

            messages.error(
                request,
                "Passwords do not match."
            )

            return redirect('register')

        # USERNAME CHECK
        if User.objects.filter(username=username).exists():

            messages.error(
                request,
                "Username already exists."
            )

            return redirect('register')

        # EMPLOYEE CODE CHECK
        if FacultyProfile.objects.filter(
            employee_code=employee_code
        ).exists():

            messages.error(
                request,
                "Employee code already exists."
            )

            return redirect('register')

        # CREATE USER
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        # CREATE FACULTY PROFILE
        FacultyProfile.objects.create(
            user=user,
            full_name=full_name,
            employee_code=employee_code,
            department=department
        )

        messages.success(
            request,
            "Registration successful. Please login."
        )

        return redirect('login')

    return render(request, 'register.html')


# ================= LOGOUT =================

def logout_view(request):

    logout(request)

    messages.success(
        request,
        "Logged out successfully."
    )

    return redirect('login')


# ================= FACULTY DASHBOARD =================

@login_required
def faculty_dashboard(request):

    # ADMIN CANNOT ACCESS
    if request.user.is_staff:

        return redirect('admin_dashboard')

    faculty = FacultyProfile.objects.filter(
        user=request.user
    ).first()

    if not faculty:

        messages.error(
            request,
            "Faculty profile not found."
        )

        return redirect('login')

    # COUNTS

    total_publications = Publication.objects.filter(
        faculty=faculty
    ).count()

    total_seminars = SeminarEvent.objects.filter(
        faculty=faculty
    ).count()

    total_projects = Project.objects.filter(
        faculty=faculty
    ).count()

    total_lectures = Lecture.objects.filter(
        faculty=faculty
    ).count()

    total_submissions = SelfAppraisalSubmission.objects.filter(
        faculty=faculty
    ).count()

    context = {

        'faculty': faculty,

        'total_publications': total_publications,

        'total_seminars': total_seminars,

        'total_projects': total_projects,

        'total_lectures': total_lectures,

        'total_submissions': total_submissions,
    }

    return render(
        request,
        'dashboard.html',
        context
    )


# ================= ADMIN DASHBOARD =================

@login_required
def admin_dashboard(request):

    if not request.user.is_staff:

        return redirect('faculty_dashboard')

    # COUNTS

    total_faculty = FacultyProfile.objects.count()

    total_publications = Publication.objects.count()

    total_projects = Project.objects.count()

    total_submissions = SelfAppraisalSubmission.objects.count()

    approved_submissions = SelfAppraisalSubmission.objects.filter(
        status='Approved'
    ).count()

    pending_submissions = SelfAppraisalSubmission.objects.filter(
        status='Pending'
    ).count()

    rejected_submissions = SelfAppraisalSubmission.objects.filter(
        status='Rejected'
    ).count()

    # SEARCH

    search_query = request.GET.get(
        'search',
        ''
    )

    # SORT

    sort_by = request.GET.get(
        'sort',
        '-submission_date'
    )

    # FETCH

    submissions = SelfAppraisalSubmission.objects.select_related(
        'faculty'
    )

    # SEARCH FILTER

    if search_query:

        submissions = submissions.filter(

            Q(faculty__full_name__icontains=search_query) |

            Q(faculty__employee_code__icontains=search_query)

        )

    # SORTING

    if sort_by == 'name':

        submissions = submissions.order_by(
            'faculty__full_name'
        )

    elif sort_by == 'employee_code':

        submissions = submissions.order_by(
            'faculty__employee_code'
        )

    elif sort_by == 'approved':

        submissions = submissions.filter(
            status='Approved'
        )

    elif sort_by == 'pending':

        submissions = submissions.filter(
            status='Pending'
        )

    elif sort_by == 'rejected':

        submissions = submissions.filter(
            status='Rejected'
        )

    else:

        submissions = submissions.order_by(
            '-submission_date'
        )

    context = {

        'total_faculty': total_faculty,

        'total_publications': total_publications,

        'total_projects': total_projects,

        'total_submissions': total_submissions,

        'approved_submissions': approved_submissions,

        'pending_submissions': pending_submissions,

        'rejected_submissions': rejected_submissions,

        'submissions': submissions,

        'search_query': search_query,

        'sort_by': sort_by,
    }

    return render(
        request,
        'admin_dashboard.html',
        context
    )


# ================= SELF APPRAISAL FORM =================

@login_required
def self_appraisal_form(request):

    if request.user.is_staff:

        return redirect('admin_dashboard')

    faculty = FacultyProfile.objects.filter(
        user=request.user
    ).first()

    if not faculty:

        messages.error(
            request,
            "Faculty profile not found."
        )

        return redirect('faculty_dashboard')

    if request.method == "POST":
        # CHECK EXISTING SUBMISSION

        existing_submission = SelfAppraisalSubmission.objects.filter(
            faculty=faculty,
            status='Pending'
        ).exists()

        if existing_submission:

            messages.warning(
                request,
                'You already have a pending submission.'
            )

            return redirect('self_appraisal_form')

        # PUBLICATION

        publication_title = request.POST.get(
            "publication_title"
        )

        journal_name = request.POST.get(
            "journal_name"
        )

        publication_date = request.POST.get(
            "publication_date"
        )

        if publication_title:

            Publication.objects.create(
                faculty=faculty,
                title=publication_title,
                journal_name=journal_name,
                publication_date=publication_date
            )

        # SEMINAR

        seminar_name = request.POST.get(
            "seminar_name"
        )

        organized_by = request.POST.get(
            "organized_by"
        )

        seminar_date = request.POST.get(
            "seminar_date"
        )

        if seminar_name:

            SeminarEvent.objects.create(
                faculty=faculty,
                seminar_name=seminar_name,
                organized_by=organized_by,
                seminar_date=seminar_date
            )

        # PROJECT

        project_title = request.POST.get(
            "project_title"
        )

        project_description = request.POST.get(
            "project_description"
        )

        if project_title:

            Project.objects.create(
                faculty=faculty,
                project_title=project_title,
                project_description=project_description
            )

        # LECTURE

        lecture_topic = request.POST.get(
            "lecture_topic"
        )

        lecture_date = request.POST.get(
            "lecture_date"
        )

        if lecture_topic:

            Lecture.objects.create(
                faculty=faculty,
                lecture_topic=lecture_topic,
                lecture_date=lecture_date
            )

        # SUBMISSION

        SelfAppraisalSubmission.objects.create(
            faculty=faculty,
            status='Pending'
        )

        messages.success(
            request,
            "Self appraisal submitted successfully."
        )

        return redirect('self_appraisal_form')

    return render(
        request,
        'self_appraisal_form.html'
    )


# ================= PROFILE =================

@login_required
def profile_view(request):

    if request.user.is_staff:

        return redirect('admin_dashboard')

    faculty = FacultyProfile.objects.filter(
        user=request.user
    ).first()

    context = {

        'faculty': faculty
    }

    return render(
        request,
        'profile.html',
        context
    )


# ================= UPDATE STATUS =================

@login_required
def update_submission_status(request, submission_id):

    if not request.user.is_staff:

        return redirect('faculty_dashboard')

    submission = SelfAppraisalSubmission.objects.get(
        id=submission_id
    )

    if request.method == "POST":

        submission.status = request.POST.get(
            'status'
        )

        submission.admin_remark = request.POST.get(
            'remark'
        )

        submission.save()

        messages.success(
            request,
            "Submission status updated successfully."
        )

    return redirect('admin_dashboard')


# ================= MY SUBMISSIONS =================

@login_required
def my_submissions(request):

    if request.user.is_staff:

        return redirect('admin_dashboard')

    faculty = FacultyProfile.objects.filter(
        user=request.user
    ).first()

    submissions = SelfAppraisalSubmission.objects.filter(
        faculty=faculty
    ).order_by('-submission_date')

    context = {

        'submissions': submissions
    }

    return render(
        request,
        'my_submissions.html',
        context
    )


# ================= REPORTS =================

@login_required
def reports_view(request):

    # ADMIN CANNOT ACCESS
    if request.user.is_staff:

        return redirect('admin_dashboard')

    faculty = FacultyProfile.objects.get(
        user=request.user
    )

    # FETCH DATA

    submissions = SelfAppraisalSubmission.objects.filter(
        faculty=faculty
    ).order_by('-submission_date')

    publications = Publication.objects.filter(
        faculty=faculty
    )

    seminars = SeminarEvent.objects.filter(
        faculty=faculty
    )

    projects = Project.objects.filter(
        faculty=faculty
    )

    lectures = Lecture.objects.filter(
        faculty=faculty
    )

    context = {

        'faculty': faculty,

        'submissions': submissions,

        'publications': publications,

        'seminars': seminars,

        'projects': projects,

        'lectures': lectures,
    }

    return render(
        request,
        'reports.html',
        context
    )

# ================= DOWNLOAD PDF =================

@login_required
def download_pdf(request, submission_id):

    # ================= ONLY ADMIN =================

    if not request.user.is_staff:

        return redirect('faculty_dashboard')

    # ================= GET SUBMISSION =================

    submission = SelfAppraisalSubmission.objects.get(
        id=submission_id
    )

    faculty = submission.faculty

    # ================= RESPONSE =================

    response = HttpResponse(
        content_type='application/pdf'
    )

    response[
        'Content-Disposition'
    ] = f'attachment; filename="Faculty_Report_{faculty.employee_code}.pdf"'

    # ================= PDF =================

    p = canvas.Canvas(response)

    # ================= TITLE =================

    p.setFont("Helvetica-Bold", 18)

    p.drawString(
        170,
        800,
        "Faculty Appraisal Report"
    )

    # ================= FACULTY DETAILS =================

    p.setFont("Helvetica", 12)

    y = 750

    details = [

        f"Faculty Name: {faculty.full_name}",

        f"Employee Code: {faculty.employee_code}",

        f"Department: {faculty.department}",

        f"Designation: {faculty.designation}",

        f"Phone: {faculty.phone}",

        f"Status: {submission.status}",

        f"Submission Date: {submission.submission_date}",

        f"Admin Remark: {submission.admin_remark}",
    ]

    for detail in details:

        p.drawString(
            70,
            y,
            detail
        )

        y -= 30

    # ================= PUBLICATIONS =================

    publications = Publication.objects.filter(
        faculty=faculty
    )

    p.setFont("Helvetica-Bold", 14)

    p.drawString(
        70,
        y - 10,
        "Research Publications"
    )

    y -= 40

    p.setFont("Helvetica", 12)

    if publications:

        for pub in publications:

            p.drawString(
                90,
                y,
                f"- {pub.title}"
            )

            y -= 25

    else:

        p.drawString(
            90,
            y,
            "No Publications"
        )

        y -= 25

    # ================= SEMINARS =================

    seminars = SeminarEvent.objects.filter(
        faculty=faculty
    )

    p.setFont("Helvetica-Bold", 14)

    p.drawString(
        70,
        y - 10,
        "Seminars / Events"
    )

    y -= 40

    p.setFont("Helvetica", 12)

    if seminars:

        for seminar in seminars:

            p.drawString(
                90,
                y,
                f"- {seminar.seminar_name}"
            )

            y -= 25

    else:

        p.drawString(
            90,
            y,
            "No Seminars"
        )

        y -= 25

    # ================= PROJECTS =================

    projects = Project.objects.filter(
        faculty=faculty
    )

    p.setFont("Helvetica-Bold", 14)

    p.drawString(
        70,
        y - 10,
        "Projects"
    )

    y -= 40

    p.setFont("Helvetica", 12)

    if projects:

        for project in projects:

            p.drawString(
                90,
                y,
                f"- {project.project_title}"
            )

            y -= 25

    else:

        p.drawString(
            90,
            y,
            "No Projects"
        )

        y -= 25

    # ================= LECTURES =================

    lectures = Lecture.objects.filter(
        faculty=faculty
    )

    p.setFont("Helvetica-Bold", 14)

    p.drawString(
        70,
        y - 10,
        "Lectures"
    )

    y -= 40

    p.setFont("Helvetica", 12)

    if lectures:

        for lecture in lectures:

            p.drawString(
                90,
                y,
                f"- {lecture.lecture_topic}"
            )

            y -= 25

    else:

        p.drawString(
            90,
            y,
            "No Lectures"
        )

        y -= 25

    # ================= SAVE PDF =================

    p.showPage()

    p.save()

    return response


# ================= EDIT PROFILE =================

@login_required
def edit_profile(request):

    if request.user.is_staff:

        return redirect('admin_dashboard')

    faculty = FacultyProfile.objects.filter(
        user=request.user
    ).first()

    if request.method == "POST":

        faculty.full_name = request.POST.get(
            'full_name'
        )

        faculty.department = request.POST.get(
            'department'
        )

        faculty.designation = request.POST.get(
            'designation'
        )

        faculty.phone = request.POST.get(
            'phone'
        )

        if request.FILES.get('profile_photo'):

            faculty.profile_photo = request.FILES.get(
                'profile_photo'
            )

        faculty.save()

        messages.success(
            request,
            "Profile updated successfully."
        )

        return redirect('profile')

    context = {

        'faculty': faculty
    }

    return render(
        request,
        'edit_profile.html',
        context
    )