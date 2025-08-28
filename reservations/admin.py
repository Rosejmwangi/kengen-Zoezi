from django.contrib import admin


from .models import GymClass, Session, Reservation

admin.site.register(GymClass)
admin.site.register(Session)
admin.site.register(Reservation)
