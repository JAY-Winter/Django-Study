from .models import *
from .services import *
from .serializers import *
from data.data import ResponseData

from rest_framework.response import Response
from rest_framework.decorators import api_view

from datetime import datetime


@api_view(['GET'])
def search(request,keyword=None, date=None):
    response_data = ResponseData()
    keyword = request.GET.get('keyword', None)
    date = request.GET.get('date', None)
    if keyword:
        search_doctors = DiagonsisService().get_search_list(keyword)
        if search_doctors:
            serializer = DoctorSerializer(search_doctors, many=True)
            data = [doctor['name'] for doctor in serializer.data]
            response_data.data = data
            message = '성공'
            status = 200
        else:
            response_data.data = ''
            message = '반환값 없음'
            status = 204

    elif date:
        day_of_week, request_time = DateService().parse_date_and_time(date)
        opening_hours = DiagonsisService().get_opening_hours(day_of_week, request_time)
        available_doctors = {opening.doctor for opening in opening_hours}

        if available_doctors:
            serializer = DoctorSerializer(available_doctors, many=True)
            data = [doctor['name'] for doctor in serializer.data]
            response_data.data = data
            message = '성공'
            status = 200
        else:
            data = ''
            message = '반환값 없음'
            status = 204
    else:
        message = '유효하지 않은 요청: keyword 또는 date 가 작성되어야함'
        status = 400

    response_data.data = data
    response_data.message = message
    return Response(response_data.builder(data, message), status=status)


@api_view(['POST'])
def request_diagnosis(request):
    doctor_id = request.data['doctor_id']
    patient_id = request.data['patient_id']
    desired_date_time_str = request.data['desired_date_time']
    desired_date_time = datetime.strptime(desired_date_time_str, '%Y 년 %m 월 %d 일 %H 시 %M 분')
    day_of_week = desired_date_time.strftime('%a').lower()

    opening_hours = DiagonsisService().get_opening_hours(day_of_week, desired_date_time)

    response_data = ResponseData()
    if opening_hours:
        doctor = Doctor.objects.get(id=doctor_id)
        patient = Patient.objects.get(id=patient_id)
        data = {'patient': patient.id, 'doctor': doctor.id, 'desired_date_time': desired_date_time}
        serializer = DiagnosisSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        data = serializer.data
        message = '성공'
        status = 200
    else:
        data = ''
        message = '의사의 영업시간이 아님'
        status = 204
    return Response(response_data.builder(data, message), status=status)


@api_view(['GET'])
def search_requested_diagonsis(request, doctor_id):
    request_diagnosises = DiagonsisService().get_request_diagnosises(doctor_id)

    response_data = ResponseData()
    if request_diagnosises:
        serializer = DiagnosisSerializer(request_diagnosises, many=True)
        data = serializer.data
        message = '성공'
        status = 200
    else:
        data = ''
        message = '해당 의사에 요청된 진료가 없음'
        status = 204
    return Response(response_data.builder(data, message), status=status)


@api_view(['POST'])
def accept_requested_diagonsis(request, request_id):
    response_data = ResponseData()
    
    try:
        diagnosis = DiagonsisService().get_diagnosis(request_id)
        DiagonsisService().accept_diagnosis(diagnosis)
        serializer = RequestDiagnosis(diagnosis)
        data = serializer.data
        message = '성공'
        status = 200
    except:
        data = ''
        message = '해당 진료 요청이 없음'
        status = 204
    return Response(response_data.builder(data, message), status=status)