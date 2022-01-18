from import_export import resources
from .models import Meeting, ReservationMeetingRoom
from import_export.widgets import ManyToManyWidget
from import_export.fields import Field
from TaskManagement.models import Employee, Project, Task, Taskmanagment
from import_export import resources,fields
from import_export.widgets import JSONWidget, ManyToManyWidget, ForeignKeyWidget

class MeetingResource(resources.ModelResource):

    def get_queryset(self):
        return Meeting.objects.filter(name=self.name, description=self.description)
    class Meta:
        model = Meeting
        fields = ('name', 'description',)
        export_order = ('name', 'description')

class ReservationMeetingRoomResource(resources.ModelResource):

    def get_queryset(self):
        return ReservationMeetingRoom.objects.filter(meeting_room=self.meeting_room, reservation_date=self.reservation_date,
        team =self.team,reservation_from_time = self.reservation_from_time, reservation_to_time=self.reservation_to_time,meeting_outcomes=self.meeting_outcomes,meeting_project_name=self.meeting_project_name,task_name=self.task_name )
    class Meta:
        model = ReservationMeetingRoom
        fields = ('meeting_room__name', 'reservation_date',  'reservation_from_time', 'reservation_to_time','team', 'meeting_outcomes','meeting_project_name__name','task_name__task_name',)
        export_order = ('meeting_room__name', 'reservation_date','reservation_from_time','reservation_to_time','team','meeting_outcomes','meeting_project_name__name','task_name__task_name')
        widget=ManyToManyWidget(model = Employee, field='username')