from django.contrib import admin
from .models import Meeting, ReservationMeetingRoom

# Register your models here.
admin.site.register(Meeting)
admin.site.register(ReservationMeetingRoom)