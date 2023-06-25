from django.test import TestCase

from diagnosis.models import Specialty, Hospital, Doctor

from factory.django import DjangoModelFactory
from factory import Faker, SubFactory, post_generation


class SpecialtyFactory(DjangoModelFactory):
    class Meta:
        model = Specialty

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        specialty = Specialty.objects.get(name='일반의')
        return specialty
    

class HospitalFactory(DjangoModelFactory):
    class Meta:
        model = Hospital

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        hospital = Hospital.objects.get(name='메라키병원')
        return hospital


class DoctorFactory(DjangoModelFactory):
    class Meta:
        model = Doctor

    name = Faker('name')
    hospital = SubFactory(HospitalFactory)

    @post_generation
    def specialty(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for specialty in extracted:
                self.specialty.add(specialty)
        else:
            self.specialty.add(SpecialtyFactory.create())

    @post_generation
    def coverage_item(self, create, extracted, **kwargs):
        # CoverageItem이 null이어야 하므로 아무 것도 하지 않음
        pass

case = 1000000

for _ in range(case):
    DoctorFactory.create()
