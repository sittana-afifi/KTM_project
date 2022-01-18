from import_export import resources
from .models import Meeting, ReservationMeetingRoom
from import_export.widgets import ManyToManyWidget
from import_export.fields import Field
from TaskManagement.models import Employee, Project, Task, Taskmanagment
from import_export import resources,fields
from import_export.widgets import JSONWidget, ManyToManyWidget, ForeignKeyWidget
from import_export.widgets import ForeignKeyWidget, ManyToManyWidget,DateWidget

class CustomManyToManyWidget(ManyToManyWidget):
    def __init__(self, model, separator=None, field=None, *args, **kwargs):
        self.lookup_field = kwargs.get('lookup_field', None)
        super(CustomManyToManyWidget, self).__init__(model)
        self.field=field

    def clean(self, value, row=None, *args, **kwargs):
        if not value:
            return self.model.objects.none()
        if isinstance(value, (float, int)):
            ids = [int(value)]
        else:
            ids = value.split(self.separator)
            ids = filter(None, [i.strip() for i in ids])

        return self.model.objects.filter(**{"{}__{}__in".format(self.field,self.lookup_field):ids})
        
class MeetingResource(resources.ModelResource):

    def get_queryset(self):
        return Meeting.objects.filter(name=self.name, description=self.description)
    class Meta:
        model = Meeting
        fields = ('name', 'description',)
        export_order = ('name', 'description')

class ReservationMeetingRoomResource(resources.ModelResource):
    team = fields.Field( attribute='team', widget=CustomManyToManyWidget(model=Employee,field='user',lookup_field='user'))

    def get_queryset(self):
        return ReservationMeetingRoom.objects.filter(meeting_room=self.meeting_room, reservation_date=self.reservation_date,
        team =self.team,reservation_from_time = self.reservation_from_time, reservation_to_time=self.reservation_to_time,meeting_outcomes=self.meeting_outcomes,meeting_project_name=self.meeting_project_name,task_name=self.task_name )
    class Meta:
        model = ReservationMeetingRoom
        fields = ('meeting_room__name', 'reservation_date',  'reservation_from_time', 'reservation_to_time','team', 'meeting_outcomes','meeting_project_name__name','task_name__task_name',)
        export_order = ('meeting_room__name', 'reservation_date','reservation_from_time','reservation_to_time','team','meeting_outcomes','meeting_project_name__name','task_name__task_name')
        widget=ManyToManyWidget(model = Employee, field='username')