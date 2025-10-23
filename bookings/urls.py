from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('calendar/', views.calendar_view, name='calendar'),
    path('sessions/', views.session_list, name='session_list'),
    path('sessions/by-date/', views.sessions_by_date, name='sessions_by_date'),
    path('sessions/<int:session_id>/reserve/', views.reserve_session, name='reserve_session'),
    path('reservations/<int:reservation_id>/cancel/', views.cancel_reservation, name='cancel_reservation'),
    path('reservations/<int:reservation_id>/ics/', views.reservation_ics, name='reservation_ics'),
    # auth
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='bookings/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/members/'), name='logout'),
    path('members/', views.members_home, name='members_home'),
]
