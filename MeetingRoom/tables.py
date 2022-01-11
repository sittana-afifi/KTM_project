import django_tables2 as tables
from .models import ReservationMeetingRoom, Meeting
from django.urls import reverse_lazy

class ReservationMeetingRoomTable(tables.Table):
    T1     = '<button type="button" class="btn btn-success my-3" update-link="{{ record.get_absolute_url_update }}">update</button>'
    T2     = '<button type="button" class="btn btn-danger my-3" delete-link="{{ record.get_absolute_url_delete }}">delete</button>'
    Edit   = tables.TemplateColumn(T1)
    Delete = tables.TemplateColumn(T2)
    #meeting_room = '<a href="{{ reservationmeetingroom.get_absolute_url }}">{{ reservationmeetingroom.meeting_room}}</a>'
    class Meta:
      model = ReservationMeetingRoom
      template_name = "django_tables2/bootstrap.html"
      fields = ("meeting_room","reservation_date","reservation_from_time","reservation_to_time" )

