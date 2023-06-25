from .views import search, request_diagnosis, search_requested_diagonsis, accept_requested_diagonsis

from django.urls import path


urlpatterns = [
    path('doctors', search),
    path('diagnosis', request_diagnosis), 
    path('doctors/<int:doctor_id>/requests', search_requested_diagonsis),
    path('request/<int:request_id>/accept', accept_requested_diagonsis),
]
