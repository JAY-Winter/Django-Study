from django.contrib import admin
from .models import Patient, Doctor, Hospital, Specialty, CoverageItem, OpeningHours, Diagnosis

admin.site.register([Patient, Doctor, Hospital, Specialty, CoverageItem, OpeningHours, Diagnosis])