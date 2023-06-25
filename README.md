# 프로젝트 세팅

## 가상환경 세팅

```bash
python3 -m venv venv

source venv/bin/activate

pip install -r requirements.txt
```

## 서버 구동 및 데이터 로드

```python
python manage.py migrate

python manage.py loaddata dump.json

python manage.py runserver
```

# API 메뉴얼

## 1. 의사 검색

### 문자열 검색

1. API 기본 정보

   | 메서드 | 요청 URL                                     | 출력 포맷 |
   | ------ | -------------------------------------------- | --------- |
   | GET    | localhost:8000/api/doctors?keyword=<keyword> | JSON      |

   - `keyword`: str = 검색 키워드

2. 입력값 및 출력값 예제

   1. **일반의**

   ```json
   {
       "message": "성공",
       "data": [
           "손웅래의사",
           "선재원의사"
       ]
   }
   ```

   1. **메라키**

   ```json
   {
       "message": "성공",
       "data": [
           "손웅래의사",
           "선재원의사"
       ]
   }
   ```

   1. **메라키 손웅래**

   ```json
   {
       "message": "성공",
       "data": [
           "손웅래의사"
       ]
   }
   ```

   1. **한의학과 선재원**

   ```json
   {
       "message": "성공",
       "data": [
           "선재원의사"
       ]
   }
   ```

   1. **다이어트약 선재원**

   ```json
   {
       "message": "성공",
       "data": [
           "선재원의사"
       ]
   }
   ```

   1. **다이어트약 손웅래**

   ```json
   {
       "message": "반환값 없음",
       "data": ""
   }
   ```

### 특정 날짜와 시간 입력하여 해당 시간에 영업중인 의사 반환

1. API 기본 정보

   | 메서드 | 요청 URL                               | 출력 포맷 |
   | ------ | -------------------------------------- | --------- |
   | GET    | localhost:8000/api/doctors?date=<date> | JSON      |

   - `date`: str = 검색 날짜

2. 입력값 및 출력값 예제

   2-0. 기본 값

   - 명세상 주어진 입력값 참고했음(스페이스바 주의)
   - OOOO 년 O 월 O 일 OO 시 OO 분
     - 7월 → 7 월
     - 12월 → 12 월
     - 7시 → 7 시
     - 12시 → 12 시

   2-1. 예제

   1. **2023 년 5 월 24 일 오전 11 시**

      - 손웅래 의사 점심시간

      ```json
      {
          "message": "성공",
          "data": [
              "선재원의사"
          ]
      }
      ```

   2. **2023 년 5 월 24 일 오후 12 시**

      - 모든 의사 점심시간

      ```json
      {
          "message": "반환값 없음",
          "data": null
      }
      ```

   3. **2023 년 5 월 25 일 오전 7 시**

      - 모든 의사 운영 외 시간

      ```json
      {
          "message": "반환값 없음",
          "data": null
      }
      ```

   4. **2023 년 5 월 24 일 오후 5 시**

      ```json
      {
          "message": "성공",
          "data": [
              "손웅래의사",
              "선재원의사"
          ]
      }
      ```

   5. **2023 년 5 월 24 일 오후 7 시**

      ```json
      {
          "message": "성공",
          "data": [
              "손웅래의사"
          ]
      }
      ```

## 2. 진료 요청

1. API 기본 정보

   | 메서드 | 요청 URL                     | 출력 포맷 |
   | ------ | ---------------------------- | --------- |
   | POST   | localhost:8000/api/diagnosis | JSON      |

2. 입력값

   | KEY               | VALUE                      | DESCRIPTION  |
   | ----------------- | -------------------------- | ------------ |
   | desired_date_time | 입력값 및 출력값 예제 참고 | 희망진료시간 |
   | patient_id        | 입력값 및 출력값 예제 참고 | 환자 id      |
   | doctor_id         | 입력값 및 출력값 예제 참고 | 의사 id      |

3. 입력값 및 출력값 예제

   ​	해당 API 의 “진료요청 만료 날짜시간”은 API 를 요청한 시간에 맞춰서 값이 설정됩니다. 따라서, 여러가지 경우(업무 시간 내, 점심 시간 내, 업무 시간 외, 업무 시간 외 다음 날 휴무)를 테스트 하길 희망하신 다면 아래와 같이 테스트 하시면 됩니다.

   1. diagnosis/serializers.py

   2. DiagnosisSerializer - create(self,validated_data) 주석 참고하여 진료요청시간을 수정하여 테스트 하시면 됩니다.

   - 기본 값
     - 명세상 주어진 입력값 참고했음(스페이스바 주의)
     - OOOO 년 O 월 O 일 OO 시 OO 분
       - 7월 → 7 월
       - 12월 → 12 월
       - 7시 → 7 시
       - 12시 → 12 시

   1. **업무 시간 내 요청**

      - 요청 시간 : 2023 년 5 월 25 일 10 시 00 분

      - 희망진료 시간 : 2023 년 5 월 25 일 10 시 00 분

        - 요청일 : 목요일
        - 희망일 : 목요일

      - 입력값

        | KEY               | VALUE                          |
        | ----------------- | ------------------------------ |
        | desired_date_time | 2023 년 5 월 25 일 10 시 00 분 |
        | patient_id        | 2                              |
        | doctor_id         | 2                              |

      - 출력값

        ```json
        {
            "message": "성공",
            "data": {
                "id": 76,
                "patient_name": "이환자",
                "doctor_name": "선재원의사",
                "desired_date_time": "2023 년 05 월 25 일 10 시 00 분",
                "expiration_time": "2023 년 05 월 25 일 10 시 20 분"
            }
        }
        ```

   2. **업무 시간 외 요청(1)**

      - 요청 시간 : 2023 년 5 월 25 일 22 시 00 분

      - 희망진료 시간 : 2023 년 5 월 26 일 10 시 00 분

        - 요청일 : 목요일
        - 희망일 : 금요일

      - 입력값

        | KEY               | VALUE                          |
        | ----------------- | ------------------------------ |
        | desired_date_time | 2023 년 5 월 26 일 10 시 00 분 |
        | patient_id        | 2                              |
        | doctor_id         | 2                              |

      - 출력값

        ```json
        {
            "message": "성공",
            "data": {
                "id": 78,
                "patient_name": "이환자",
                "doctor_name": "선재원의사",
                "desired_date_time": "2023 년 05 월 26 일 10 시 00 분",
                "expiration_time": "2023 년 05 월 26 일 09 시 15 분"
            }
        }
        ```

   3. **업무 시간 외 요청(2)**

   - 요청 시간 : 2023 년 5 월 27 일 22 시 00 분

   - 희망진료 시간 : 2023 년 5 월 29 일 10 시 00 분

     - 요청일 : 토요일
     - 희망일 : 월요일

   - 입력값

     | KEY               | VALUE                          |
     | ----------------- | ------------------------------ |
     | desired_date_time | 2023 년 5 월 29 일 10 시 00 분 |
     | patient_id        | 2                              |
     | doctor_id         | 2                              |

   - 출력값

     ```json
     {
         "message": "성공",
         "data": {
             "id": 80,
             "patient_name": "이환자",
             "doctor_name": "선재원의사",
             "desired_date_time": "2023 년 05 월 29 일 10 시 00 분",
             "expiration_time": "2023 년 05 월 29 일 09 시 15 분"
         }
     }
     ```

   1. **점심 시간 내 요청**

   - 요청 시간 : 2023 년 5 월 25 일 12 시 00 분

   - 희망진료 시간 : 2023 년 5 월 25 일 16 시 00 분

   - 해당의사 점심시간 : 12:00 ~ 13:00

     - 요청일 : 목요일
     - 희망일 : 목요일

   - 입력값

     | KEY               | VALUE                          |
     | ----------------- | ------------------------------ |
     | desired_date_time | 2023 년 5 월 25 일 16 시 00 분 |
     | patient_id        | 2                              |
     | doctor_id         | 2                              |

   - 출력값

   ```json
   {
       "message": "성공",
       "data": {
           "id": 82,
           "patient_name": "이환자",
           "doctor_name": "선재원의사",
           "desired_date_time": "2023 년 05 월 25 일 16 시 00 분",
           "expiration_time": "2023 년 05 월 25 일 13 시 15 분"
       }
   }
   ```

## 3. 진료 요청 검색

1. API 기본 정보

   | 메서드 | 요청 URL                                        | 출력 포맷 |
   | ------ | ----------------------------------------------- | --------- |
   | POST   | localhost:8000/api/doctors/<doctor_id>/requests | JSON      |

2. 입력값

   | KEY       | VALUE                      | DESCRIPTION |
   | --------- | -------------------------- | ----------- |
   | doctor_id | 입력값 및 출력값 예제 참고 | 의사 id     |

3. 입력값 및 출력값 예제

   **1. `doctor_id` = 2 (선재원의사)**

   - id : 168, 169 → 이미 수락된 진료 요청

   ```json
   [
   	"message": "성공",
   	"data": [
       {
           "id": 167,
           "patient_name": "이환자",
           "doctor_name": "선재원의사",
           "desired_date": "2023 년 05 월 25 일 01 시 00 분",
           "expiration_date": "2023 년 05 월 30 일 00 시 15 분"
       },
       {
           "id": 170,
           "patient_name": "이환자",
           "doctor_name": "선재원의사",
           "desired_date": "2023 년 05 월 25 일 01 시 00 분",
           "expiration_date": "2023 년 05 월 30 일 00 시 15 분"
       }
   	]
   ]
   ```

## 4. 진료 요청 수락

1. API 기본 정보

   | 메서드 | 요청 URL                                       | 출력 포맷 |
   | ------ | ---------------------------------------------- | --------- |
   | POST   | localhost:8000/api/request/<request_id>/accept | JSON      |

2. 입력값

   | KEY        | VALUE       |
   | ---------- | ----------- |
   | request_id | 진료요청 id |

3. 입력값 및 출력값 예제

   **1. `diagonsis_id` = 169**

   ```json
   {
   	"message": "성공",
   	"data": [
       "id": 169,
       "patient": "이환자",
       "desired_date_time": "2023 년 05 월 25 일 01 시 00 분",
       "expiration_time": "2023 년 05 월 30 일 00 시 15 분"
   	]
   }
   ```

------

# 진행하며 들었던 생각

개발적으로는 아래와 같은 부분을 경험하게 되어서 좋았습니다.

### 1. Overiding Serializer

- Django 로 프로젝트를 진행하며 이미 경험해보았던 부분이었지만 디테일한 부분 예를 들어,

  “진료 요청 만료시간을 구하는 과정”이 흥미로웠습니다.

- 진료 요청이 들어온 시간이 영업 내, 점심 시간 내, 진료 시간 내, 영업 외(평일, 주말)인지 여러 경우에 따라

  다른 값을 반환해야 했습니다.

- 따라서, 진료 레코드를 생성하는 과정에서 이러한 경우를 따져야했기에  `ModelSerializer` 의 `create` 메서드를

  오버라이딩해 이를 해결했습니다.

- Django 프레임워크를 사용하며 무의식적으로 Serializer 를 다루는 경우가 많았는데, 좀 더 이에 대해 공부하는 계기가 되어서

  개인적으로 좋았던 시간이었습니다.

### 2. 누군가에게 보여줘야하는 코드

- 나혼자만이 진행하는 프로젝트가 아닌, 다른 사람이 내 코드를 봤을 때 직관적으로 이해할 수 있도록 코드를 작성하는 부분에 노력했습니다.

------

# 개선을 시도한 과정

## 상황

- Doctor Table 레코드 개수가 1,000,000 개라고 가정을 하고 해당 Table 과 관련된 쿼리 작업이 일어날 때, 어떤 결과가 나오고

  이를 어떻게 개선해볼 것 인가?

### Cache

```python
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}
```

- Cache 를 다루는 여러가지 툴(redis 등) 이 있지만, 원활한 테스트를 위해 로컬에서 작동하는 `LocMemCache` 채택했습니다.

## Case 1

```python
localhost:8000/api/doctors?keyword=메라키
```

- 의사 1,000,000 건
  - 소속 병원 : “메라키”

1. 기존 코드 및 응답 결과

```python
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
```

- 요청에 대한 결과

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/e7d26a82-7006-461f-ad5a-b97b4f1948a4/Untitled.png)

1. 검색 결과 값에 대한 캐시 적용

```python
def get_search_list(self, words):
        """키워드를 입력받아 의사 중 해당 키워드 조건에 맞는 의사 리스트를 반환합니다."""
        cache_key = f"search:{words}"
        cached_result = cache.get(cache_key)
        if cached_result is not None:
            return cached_result

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

        result = list(Doctor.objects.filter(query).distinct())
        cache.set(cache_key, result, 300)
        return Doctor.objects.filter(query).distinct()
```

- 최초 실행

  ![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/5a22e370-1e63-4f4c-ab05-ef135f739bde/Untitled.png)

- 최초 실행 이후 동일한 요청에 대한 결과

  ![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/b296ffda-20e9-4236-bdb0-3ca1d97e9b77/Untitled.png)

## Case 2

```bash
localhost:8000/api/doctors?keyword=한의학과 선재원
```

- cache 적용 이전

  ![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/75e1df2d-d437-4edc-b6f8-9828c6a61583/Untitled.png)

- cache 적용 이후

  1. 최초 실행

  ![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/561ad351-8fcf-443e-817e-cc9466beab4b/Untitled.png)

  1. 최초 실행 이후

  ![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/888ac2c5-d81b-4bd5-8f6f-f9e666a4b3f1/Untitled.png)

# 의문점

## 캐싱

- 각 검색 결과를 캐싱하여 저장했습니다.

- API Case 2 경우, 유의미한 데이터 값이 도출됐습니다.

  기존 결과에 비해 확연히 응답 시간이 줄어든 모습을 확인할 수 있습니다.

- API Case 1 경우가 문제입니다.

  기존 응답 시간에 비해서 다른 점이 아예 없습니다.

- 다른 점이라고 찾아보면 캐시가 적용되고 최초 검색 요청이 들어왔을 때, 이를 캐싱하여 캐시 메모리에 할당하여

  소요되는 시간이 기존 시간 대비 약 2.5 배 정도 증가했습니다.

- 최초 검색 요청에 대해서 기존 시간이 소요될 수 있음은 충분히 인지하고 있었으나, 최초 요청 이후에 대한 소요된 시간이

  캐시를 적용하기 전과 다른 점이 없다는 것입니다…

# 따라서

- 솔직히 말하자면, 1,000,000 개의 데이터를 빠른 속도로 응답하는 부분을 어떻게 처리해야할 지 모르겠습니다.

  더 정확히는 캐싱된 “일반의” 의사 데이터가 1,000,000 개가 있을 때 응답 소요시간을 어떤 식으로 줄여야 하는 것 입니다.

- 인덱싱을 고려할 수도 있겠으나, 이미 캐시 메모리에 저장되어 있는 데이터를 호출하는 시간 자체가 너무 길기에 인덱싱은

  캐시 이전에 고려해봐야하는 문제라고 생각합니다.
