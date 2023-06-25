from django.db import models
from django.core.exceptions import ValidationError


class Patient(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self) -> str:
        return self.name


class Doctor(models.Model):
    name = models.CharField(max_length=255)
    specialty = models.ManyToManyField('Specialty')
    coverage_item = models.ManyToManyField('CoverageItem', blank=True)
    hospital = models.ForeignKey('Hospital', on_delete=models.CASCADE, related_name='doctors')

    def __str__(self) -> str:
        return self.name + '의사'


class Hospital(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self) -> str:
        return self.name + '병원'


class Specialty(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name


class CoverageItem(models.Model):
    name = models.CharField(max_length=255)
    is_coverage = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.name


class OpeningHours(models.Model):
    DAYS_OF_WEEK = (
        ('mon', '월요일'),
        ('tue', '화요일'),
        ('wed', '수요일'),
        ('thu', '목요일'),
        ('fri', '금요일'),
        ('sat', '토요일'),
        ('sun', '일요일'),
    )
    open_time = models.TimeField(null=True, blank=True)
    close_time = models.TimeField(null=True, blank=True)
    is_closed = models.BooleanField(default=False)
    lunch_end_time = models.TimeField(null=True, blank=True)
    lunch_start_time = models.TimeField(null=True, blank=True)
    day_of_week = models.CharField(max_length=3, choices=DAYS_OF_WEEK, null=True, blank=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='opening_hours')

    def clean(self):
        if self.is_closed:
            fields = [self.open_time, self.close_time, self.lunch_end_time, self.lunch_start_time]
            if any(fields):
                raise ValidationError("휴무일일 때 다른 필드들은 비어있어야 합니다.")
        else:
            if not all([self.open_time, self.close_time, self.day_of_week]):
                raise ValidationError("휴무일이 아닐 때 open_time, close_time, day_of_week 필드들은 비어있지 않아야 합니다.")


class Diagnosis(models.Model):
    expiration_time = models.DateTimeField(null=True)
    desired_date_time = models.DateTimeField()
    is_accepted = models.BooleanField(default=False)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='diagnosis')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='diagnosis')