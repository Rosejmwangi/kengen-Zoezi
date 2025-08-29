from django.contrib import admin



from .models import GymClass, Session, Reservation

class ReservationAdmin(admin.ModelAdmin):
	list_display = ("name", "email", "session", "reserved_at")
	list_filter = ("reserved_at",)
	search_fields = ("name", "email", "session__gym_class__name")

admin.site.register(GymClass)
admin.site.register(Session)
admin.site.register(Reservation, ReservationAdmin)
