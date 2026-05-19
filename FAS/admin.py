from django.contrib import admin

from .models import (
    FacultyProfile,
    Publication,
    SeminarEvent,
    Project,
    Lecture,
    SelfAppraisalSubmission
)


admin.site.register(FacultyProfile)
admin.site.register(Publication)
admin.site.register(SeminarEvent)
admin.site.register(Project)
admin.site.register(Lecture)
admin.site.register(SelfAppraisalSubmission)