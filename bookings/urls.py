from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('calendar/', views.calendar_view, name='calendar'),
    path('sessions/', views.session_list, name='session_list'),
    path('sessions/by-date/', views.sessions_by_date, name='sessions_by_date'),
    path('sessions/<int:session_id>/reserve/', views.reserve_session, name='reserve_session'),
    path('reservations/<int:reservation_id>/cancel/', views.cancel_reservation, name='cancel_reservation'),
    path('reservations/<int:reservation_id>/ics/', views.reservation_ics, name='reservation_ics'),
]
