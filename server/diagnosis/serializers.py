from .models import *
from .services import *

from rest_framework import serializers
from datetime import timedelta, datetime


class DoctorSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = Doctor
        fields = ['name', ]

    def get_name(self, obj):
        return str(obj)


class DiagnosisSerializer(serializers.ModelSerializer):
    date_service = DateService()
    model_service = ModelService()

    doctor_name = serializers.SerializerMethodField()
    patient_name = serializers.SerializerMethodField()
    desired_date = serializers.SerializerMethodField()
    expiration_date = serializers.SerializerMethodField()

    class Meta:
        model = Diagnosis
        fields = ['id', 'doctor', 'patient', 'patient_name', 'doctor_name', 'desired_date_time', 'desired_date', 'expiration_date']
        extra_kwargs = { 
            'doctor': {'write_only': True, },
            'patient': {'write_only': True, },
            'desired_date_time': {'write_only': True, },}

    def create(self, validated_data):
        request_date = datetime.now()
        # 일자(day)를 변경하길 희망하는 경우
        # request_date += timedelta(days=1)
        # 시간(hour)을 변경하길 희망하는 경우
        # request_date += timedelta(hours=1)
        # 분(min)을 변경하길 희망하는 경우
        # request_date += timedelta(minutes=1)
        diagnosis = self.model_service.create_instance(self.Meta, validated_data)
        opening_hour = diagnosis.doctor.opening_hours.get(day_of_week=request_date.strftime('%a').lower())

        expiration_time = self.date_service.calculate_expiration_time(request_date, opening_hour, diagnosis.doctor)
        
        diagnosis.expiration_time = expiration_time
        diagnosis.save()
        return diagnosis

    def get_doctor_name(self, obj):
        return str(obj.doctor)

    def get_patient_name(self, obj):
        return str(obj.patient)

    def get_desired_date(self, obj):
        desired_date = self.date_service.convert_datetime_to_format(obj.desired_date_time)
        return desired_date

    def get_expiration_date(self, obj):
        expiration_date = self.date_service.convert_datetime_to_format(obj.expiration_time)
        return expiration_date


class RequestDiagnosis(serializers.ModelSerializer):
    date_service = DateService()

    expiration_time = serializers.SerializerMethodField()
    patient = serializers.CharField(source='patient.name')
    desired_date_time = serializers.SerializerMethodField()

    class Meta:
        model = Diagnosis
        fields = ['id', 'patient', 'desired_date_time', 'expiration_time',]

    def get_desired_date_time(self, obj):
        desired_date_time = self.date_service.convert_datetime_to_format(obj.desired_date_time)
        return desired_date_time

    def get_expiration_time(self, obj):
        expiration_time = self.date_service.convert_datetime_to_format(obj.expiration_time)
        return expiration_time