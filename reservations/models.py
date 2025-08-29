
from django.db import models

class GymClass(models.Model):
	name = models.CharField(max_length=100)
	description = models.TextField(blank=True)
	def __str__(self):
		return self.name


class Session(models.Model):
	gym_class = models.ForeignKey(GymClass, on_delete=models.CASCADE, related_name='sessions')
	start_time = models.DateTimeField()
	end_time = models.TimeField()
	capacity = models.PositiveIntegerField(default=10)
	def __str__(self):
		return f"{self.gym_class.name} ({self.start_time:%Y-%m-%d %H:%M} - {self.end_time})"

class Reservation(models.Model):
	session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='reservations')
	name = models.CharField(max_length=100)
	email = models.EmailField()
	reserved_at = models.DateTimeField(auto_now_add=True)
	def __str__(self):
		return f"{self.name} - {self.session}"
