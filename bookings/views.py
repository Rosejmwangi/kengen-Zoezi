from django.http import HttpResponse
import datetime

# ICS file download for reservation
def reservation_ics(request, reservation_id):
	reservation = get_object_or_404(Reservation, id=reservation_id)
	session = reservation.session
	start = session.start_time.strftime('%Y%m%dT%H%M%S')
	end = session.end_time.strftime('%Y%m%dT%H%M%S')
	summary = f"{session.gym_class.name} with {session.gym_class.instructor}"
	description = f"KenGen Zoezi Gym Session\nClass: {session.gym_class.name}\nInstructor: {session.gym_class.instructor}"
	location = "KenGen Staff Gym"
	ics_content = f"""
BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//KenGen Zoezi//EN
BEGIN:VEVENT
UID:{reservation.id}@kengenzoezi
DTSTAMP:{datetime.datetime.now().strftime('%Y%m%dT%H%M%S')}
DTSTART:{start}
DTEND:{end}
SUMMARY:{summary}
DESCRIPTION:{description}
LOCATION:{location}
END:VEVENT
END:VCALENDAR
"""
	response = HttpResponse(ics_content, content_type='text/calendar')
	response['Content-Disposition'] = f'attachment; filename=reservation_{reservation.id}.ics'
	return response
# For JSON response
from django.http import JsonResponse
# Calendar page view
def calendar_view(request):
	return render(request, 'bookings/calendar.html')

# API endpoint for sessions by date
def sessions_by_date(request):
	date_str = request.GET.get('date')
	from datetime import datetime
	import pytz
	nairobi_tz = pytz.timezone('Africa/Nairobi')
	sessions = []
	if date_str:
		try:
			date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
			from reservations.models import Session
			all_sessions = Session.objects.select_related('gym_class').all()
			for session in all_sessions:
				local_start = session.start_time.astimezone(nairobi_tz)
				if local_start.date() == date_obj:
					reserved_count = session.reservations.count()
					is_full = reserved_count >= session.capacity
					spots_left = max(session.capacity - reserved_count, 0)
					sessions.append({
						'id': session.id,
						'gym_class': session.gym_class.name,
						'instructor': session.gym_class.instructor,
						'start_time': local_start.strftime('%H:%M'),
						'end_time': session.end_time.strftime('%H:%M'),
						'capacity': session.capacity,
						'is_full': is_full,
						'spots_left': spots_left,
					})
		except Exception:
			pass
	return JsonResponse({'sessions': sessions})

from django.shortcuts import render


def homepage(request):
	return render(request, 'bookings/homepage.html')

# List all available sessions
from reservations.models import Session, Reservation
from django import forms
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse
# Cancel reservation view
def cancel_reservation(request, reservation_id):
	reservation = get_object_or_404(Reservation, id=reservation_id)
	session = reservation.session
	if request.method == 'POST':
		reservation.delete()
		return render(request, 'bookings/cancel_success.html', {'session': session})
	return render(request, 'bookings/cancel_confirm.html', {'reservation': reservation, 'session': session})
from django.core.mail import send_mail

# Reservation form
class ReservationForm(forms.ModelForm):
	class Meta:
		model = Reservation
		fields = ['name', 'email']

# Reservation view
def reserve_session(request, session_id):
	session = get_object_or_404(Session, id=session_id)
	is_full = session.reservations.count() >= session.capacity
	if is_full:
		return render(request, 'bookings/reserve_session.html', {'form': None, 'session': session, 'is_full': True})
	if request.method == 'POST':
		form = ReservationForm(request.POST)
		if form.is_valid():
			reservation = form.save(commit=False)
			reservation.session = session
			reservation.save()
			# Send email notification
			subject = f"Gym Reservation Confirmed: {session.gym_class.name}"
			start_time_str = session.start_time.strftime('%A, %d %B %Y at %H:%M')
			message = (
				f"Dear {reservation.name},\n\n"
				f"Your reservation for {session.gym_class.name} is confirmed.\n"
				f"Date & Time: {start_time_str} - {session.end_time.strftime('%H:%M')}\n"
				f"Instructor: {session.gym_class.instructor}\n\n"
				f"Thank you for booking with KenGen Staff Gym Booker!\n"
			)
			send_mail(
				subject,
				message,
				'noreply@kengen.co.ke',  # From email
				[reservation.email],
				fail_silently=True
			)
			return render(request, 'bookings/reservation_success.html', {'session': session, 'reservation': reservation})
	else:
		form = ReservationForm()
	return render(request, 'bookings/reserve_session.html', {'form': form, 'session': session, 'is_full': False})

from django.utils import timezone
from datetime import time

def session_list(request):
	# Nairobi is Africa/Nairobi, but Django uses USE_TZ=True, so times are in UTC in DB
	# We'll filter sessions whose start_time (converted to Nairobi) is between 4am and 9pm
	import pytz
	nairobi_tz = pytz.timezone('Africa/Nairobi')
	sessions = Session.objects.select_related('gym_class').all().order_by('start_time')
	filtered_sessions = []
	for session in sessions:
		local_start = session.start_time.astimezone(nairobi_tz)
		if time(4, 0) <= local_start.time() <= time(21, 0):
			filtered_sessions.append(session)
	return render(request, 'bookings/session_list.html', {'sessions': filtered_sessions})
