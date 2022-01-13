from django.contrib import admin
from import_export.admin import ImportExportMixin
from .models import Meeting, ReservationMeetingRoom

class MeetingAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['name', 'description']

class ReservationMeetingRoomAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['meeting_room', 'reservation_date', 'reservation_from_time', 'reservation_to_time', 'meeting_outcomes', 'meeting_project_name', 'task_name']

# Register your models here.
admin.site.register(Meeting, MeetingAdmin)
admin.site.register(ReservationMeetingRoom, ReservationMeetingRoomAdmin)