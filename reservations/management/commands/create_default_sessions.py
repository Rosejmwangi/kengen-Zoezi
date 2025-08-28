from django.core.management.base import BaseCommand
from reservations.models import GymClass, Session
from django.utils import timezone
from datetime import datetime, time, timedelta
import pytz

CLASS_SCHEDULE = [
    {"name": "Spinning", "start": time(5, 30), "end": time(7, 30), "instructor": "Coach Spin"},
    {"name": "Yoga", "start": time(8, 0), "end": time(10, 0), "instructor": "Coach Yoga"},
    {"name": "Zumba", "start": time(10, 0), "end": time(12, 0), "instructor": "Coach Zumba"},
    {"name": "Cardio", "start": time(12, 0), "end": time(14, 0), "instructor": "Coach Cardio"},
    {"name": "Lifting", "start": time(14, 0), "end": time(16, 0), "instructor": "Coach Lift"},
    {"name": "Dance", "start": time(16, 30), "end": time(20, 0), "instructor": "Coach Dance"},
]

class Command(BaseCommand):
    help = 'Create default gym sessions for a given day (or today by default)'

    def add_arguments(self, parser):
        parser.add_argument('--days', type=int, default=365, help='Number of days to create sessions for, starting today (default: 365)')
        parser.add_argument('--start-date', type=str, help='Start date (YYYY-MM-DD), default is today')

    def handle(self, *args, **options):
        nairobi_tz = pytz.timezone('Africa/Nairobi')
        days = options.get('days', 365)
        start_date_str = options.get('start_date')
        if start_date_str:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        else:
            start_date = timezone.now().astimezone(nairobi_tz).date()

        for day_offset in range(days):
            session_date = start_date + timedelta(days=day_offset)
            for class_info in CLASS_SCHEDULE:
                gym_class, _ = GymClass.objects.get_or_create(
                    name=class_info["name"],
                    defaults={"description": f"{class_info['name']} class", "instructor": class_info["instructor"]}
                )
                start_dt = datetime.combine(session_date, class_info["start"])
                start_dt = nairobi_tz.localize(start_dt)
                # Only create if not already exists for this class and start time
                if not Session.objects.filter(gym_class=gym_class, start_time=start_dt).exists():
                    Session.objects.create(
                        gym_class=gym_class,
                        start_time=start_dt,
                        end_time=class_info["end"],
                        capacity=10
                    )
            self.stdout.write(self.style.SUCCESS(f"Default sessions created for {session_date}"))
