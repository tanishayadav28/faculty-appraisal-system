from django.db import models
from django.contrib.auth.models import User


# ================= FACULTY PROFILE =================

class FacultyProfile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    full_name = models.CharField(max_length=100)

    employee_code = models.CharField(
        max_length=20,
        unique=True
    )

    department = models.CharField(max_length=100)

    designation = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    phone = models.CharField(
        max_length=15,
        blank=True,
        null=True
    )

    profile_photo = models.ImageField(
        upload_to='profile_photos/',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.full_name


# ================= PUBLICATIONS =================

class Publication(models.Model):

    faculty = models.ForeignKey(
        FacultyProfile,
        on_delete=models.CASCADE
    )

    title = models.CharField(max_length=200)

    journal_name = models.CharField(max_length=200)

    publication_date = models.DateField()

    def __str__(self):
        return self.title


# ================= SEMINARS / EVENTS =================

class SeminarEvent(models.Model):

    faculty = models.ForeignKey(
        FacultyProfile,
        on_delete=models.CASCADE
    )

    seminar_name = models.CharField(max_length=200)

    organized_by = models.CharField(max_length=200)

    seminar_date = models.DateField()

    def __str__(self):
        return self.seminar_name


# ================= PROJECTS =================

class Project(models.Model):

    faculty = models.ForeignKey(
        FacultyProfile,
        on_delete=models.CASCADE
    )

    project_title = models.CharField(max_length=200)

    project_description = models.TextField()

    def __str__(self):
        return self.project_title


# ================= LECTURES =================

class Lecture(models.Model):

    faculty = models.ForeignKey(
        FacultyProfile,
        on_delete=models.CASCADE
    )

    lecture_topic = models.CharField(max_length=200)

    lecture_date = models.DateField()

    def __str__(self):
        return self.lecture_topic


# ================= SELF APPRAISAL SUBMISSION =================
# ================= SELF APPRAISAL SUBMISSION =================

class SelfAppraisalSubmission(models.Model):

    STATUS_CHOICES = [

        ('Pending', 'Pending'),

        ('Approved', 'Approved'),

        ('Rejected', 'Rejected'),
    ]

    faculty = models.ForeignKey(
        FacultyProfile,
        on_delete=models.CASCADE
    )

    submission_date = models.DateTimeField(
        auto_now_add=True
    )

    status = models.CharField(

        max_length=20,

        choices=STATUS_CHOICES,

        default='Pending'
    )

    admin_remark = models.TextField(

        blank=True,

        null=True
    )

    def __str__(self):

        return f"{self.faculty.full_name} - {self.status}"