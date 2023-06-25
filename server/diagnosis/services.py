from .models import *

from django.db.models import Q

import re
from dataclasses import dataclass
from datetime import datetime, time, timedelta

from django.core.cache import cache

@dataclass
class DateService():

    days_of_week = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']

    def parse_date_and_time(self, date: str):
        """문자열로된 날짜를 받아 날짜, 요일, 시간을 반환합니다."""
        pattern = r'(오전|오후)'
        date_parts = re.split(pattern, date)
        meridiem = date_parts[1]
        hour = int(date_parts[2].split('시')[0])
        if meridiem == '오후' and hour != 12:
            hour += 12
        day = date_parts[0]
        date = datetime.strptime(day[:-1], '%Y 년 %m 월 %d 일').date()
        day_of_week = date.strftime('%a').lower()
        request_time = time(hour, 0)
        return day_of_week, request_time

    def add_minutes_to_time(self, input_date, input_time, minutes):
        """datetime.time 객체에 N분을 더합니다."""
        return datetime.combine(input_date, input_time) + timedelta(minutes=minutes)

    def get_available_day(self, request_date: datetime, doctor: Doctor):
        """해당 의사의 가능한 진료일 중 가장 가까운 날짜를 얻습니다."""
        current_day_index = self.days_of_week.index(request_date.strftime('%a').lower()) 
        week = 7
        for i in range(current_day_index + 1, current_day_index + week):
            next_day_index = i % week
            diff_day = next_day_index - current_day_index
            if diff_day > 0:
                next_day = request_date + timedelta(days=(next_day_index - current_day_index))
            else:
                next_day = request_date + timedelta(days=(next_day_index - current_day_index)+week)
            opening_hour = doctor.opening_hours.filter(day_of_week=self.days_of_week[next_day_index])
            
            if opening_hour.exists() and not opening_hour.first().is_closed:
                return next_day
    
    def calculate_expiration_time(self, request_date, opening_hour, doctor):
        """해당 요청에 대한 만료 시간을 구합니다."""
        available_day = self.get_available_day(request_date, doctor)

        is_close = opening_hour.is_closed
        open_time = opening_hour.open_time
        close_time = opening_hour.close_time
        lunch_start_time = opening_hour.lunch_start_time
        lunch_end_time = opening_hour.lunch_end_time

        # 요청 시간이 업무 시간 외인 경우
        if is_close or not(open_time <= request_date.time() <= close_time):
            day_of_week = available_day.strftime('%a').lower()
            open_time = doctor.opening_hours.filter(day_of_week=day_of_week).first().open_time
            expiration_time = datetime.combine(available_day, open_time) + timedelta(minutes=15)
        # 요청 시간이 점심 시간인 경우
        elif lunch_start_time <= request_date.time() <= lunch_end_time:
            lunch_end_datetime = datetime.combine(datetime.today(), lunch_end_time)
            expiration_time = lunch_end_datetime + timedelta(minutes=15)
        # 요청 시간이 업무 시간인 경우
        else:
            expiration_time = request_date + timedelta(minutes=20)
        return expiration_time
    
    def convert_datetime_to_format(self, datetime: datetime):
        """datetime을 주어진 형식에 맞춰서 변환합니다."""
        return datetime.fromisoformat(str(datetime)).strftime('%Y 년 %m 월 %d 일 %H 시 %M 분')


class ModelService():

    def create_instance(self, Meta, validated_data):
        ModelClass = Meta.model
        return ModelClass._default_manager.create(**validated_data)


class DiagonsisService():

    def get_search_list(self, words):
        """키워드를 입력받아 의사 중 해당 키워드 조건에 맞는 의사 리스트를 반환합니다."""
        doctor_names = Doctor.objects.values_list('name', flat=True)
        hospital_names = Hospital.objects.values_list('name', flat=True)
        specialty_names = Specialty.objects.values_list('name', flat=True)
        coverage_item_names = CoverageItem.objects.values_list('name', flat=True) 
        
        query = Q()
        words = words.split()
        for word in words:
            if word in doctor_names:
                query &= Q(name__icontains=word)
            elif word in hospital_names:
                query &= Q(hospital__name__icontains=word)
            elif word in specialty_names:
                query &= Q(specialty__name__icontains=word)
            elif word in coverage_item_names:
                query &= Q(coverage_item__name__icontains=word)
        return Doctor.objects.filter(query).distinct()
    
    def get_search_list2(self, words):
        """
        키워드를 입력받아 의사 중 해당 키워드 조건에 맞는 의사 리스트를 반환합니다.
        - 캐시 적용
        - 다만, 해당 메서드 미호출
        """
        cache_key = f"search:{words}"
        cached_result = cache.get(cache_key)
        if cached_result is not None:
            return cached_result

        # 캐시에 결과가 없다면 검색을 수행합니다.
        doctor_names = Doctor.objects.values_list('name', flat=True)
        hospital_names = Hospital.objects.values_list('name', flat=True)
        specialty_names = Specialty.objects.values_list('name', flat=True)
        coverage_item_names = CoverageItem.objects.values_list('name', flat=True)

        query = Q()
        words = words.split()
        for word in words:
            if word in doctor_names:
                query &= Q(name__icontains=word)
            elif word in hospital_names:
                query &= Q(hospital__name__icontains=word)
            elif word in specialty_names:
                query &= Q(specialty__name__icontains=word)
            elif word in coverage_item_names:
                query &= Q(coverage_item__name__icontains=word)

        # 검색 결과를 캐시에 저장합니다.
        result = list(Doctor.objects.filter(query).distinct())
        # 캐시 유효 시간은 5분으로
        cache.set(cache_key, result, 300)
        return Doctor.objects.filter(query).distinct()

    def get_opening_hours(self, day_of_week, request_time):
        """영업시간 중 요청시간이 포함된 객체를 반환합니다."""
        query = (
            Q(is_closed=False) &
            Q(day_of_week=day_of_week) &
            Q(open_time__lte=request_time) & 
            Q(close_time__gte=request_time) &
            ~(
                Q(lunch_start_time__lte=request_time) &
                Q(lunch_end_time__gte=request_time)
            )
        )
        return OpeningHours.objects.filter(query)

    def get_request_diagnosises(self, doctor_id):
        """의사별 진료요청 리스트를 반환합니다."""
        doctor = Doctor.objects.get(id=doctor_id)
        request_diagnosises = doctor.diagnosis.all().filter(is_accepted=False)
        return request_diagnosises
    
    def get_diagnosis(self, request_id):
        """특정 진료요청 객체를 반환합니다."""
        diagnosis = Diagnosis.objects.get(id=request_id)
        return diagnosis
    
    def accept_diagnosis(self, diagnosis):
        """특정 진료 요청을 수락합니다."""
        diagnosis.is_accepted = True
        diagnosis.save()