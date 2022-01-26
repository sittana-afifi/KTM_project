from django.db import models
from django.db.models.fields import DateField
from django.urls.base import reverse
from django.core.exceptions import ValidationError
from TaskManagement.models import Employee, Project, Task, Taskmanagment
from parler.models import TranslatableModel, TranslatedFields

# Create your models here.
class Meeting(models.Model):
    """Model representing a Meeting."""
    name = models.CharField(max_length=200, help_text='Enter a Meeting name (e.g. Meeting Room )')
    description = models.TextField(max_length=1000, help_text='Enter a brief location of the meeting')

    def __str__(self):
        """String for representing the Model object."""
        return self.name
    def get_absolute_url(self):
        """Returns the url to access a detail record for this project."""
        return reverse('meeting-detail', args=[str(self.id)])

"""
    A class used to represent Reservation meeting room request.
    ...

    Attributes
    ----------
    meeting_room : ForeignKey from MeetingModel is CharField
    reservation_date : DateField
    reservation_from_time : TimeField
    reservation_to_time : TimeField
    team : ForeignKey as ManyToManyField from Employee Model
    meeting_outcomes : TextField
    meeting_project_name : ForeignKey from Project model
    task_name : ForeignKey from Task Model


    Methods
    -------
    def __str__(self)
        tells Django what to print when it needs to print out an instance of Reservation meeting room request model

    created by :
    -------
        Eman 

    creation date : 
    -------
        -Dec-2021

    update date :
    -------
         -Jan-2022
"""

class ReservationMeetingRoom(models.Model):
    """Model representing a reservation meeting room."""
    meeting_room = models.ForeignKey(Meeting, on_delete=models.SET_NULL, null=True, blank=False)
    reservation_date = models.DateField(null=False, blank=False)
    reservation_from_time = models.TimeField(auto_now=False, auto_now_add=False)
    reservation_to_time = models.TimeField(auto_now=False, auto_now_add=False)
    team = models.ManyToManyField(Employee,blank=True,related_name='+')
    meeting_outcomes = models.TextField(null = True ,max_length=1000, help_text='Enter the meeting outcomes')
    meeting_project_name = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True)
    task_name = models.ForeignKey(Task, on_delete=models.SET_NULL, null=True, blank=True)

    def clean_reservation_date(self):
        date = self.cleaned_date['reservation_date']
        # Check if a date is not in the past.
        if date < datetime.date.today():
            raise ValidationError(_('Invalid date - Date cannot be in the past'))
        return date

    def get_team_values(self):
        ret = ''
        print(self.team.all())
    # use models.ManyToMany field's all() method to return all the Team objects that this employee belongs to.
        for team in self.team.all():
            ret = ret + team.user.username + ','
    # remove the last ',' and return the value.
        return ret[:-1]
        
    def get_team_emails(self):
        ret = ''
        print(self.team.all())
    # use models.ManyToMany field's all() method to return all the Team objects that this employee belongs to.
        for team in self.team.all():
            ret = ret + team.user.email + ','
    # remove the last ',' and return the value.
        return ret[:-1]

    def clean(self, *args, **kwargs):
        cleaned_data = super().clean(*args, **kwargs)
        if self.pk:
            case_1 = ReservationMeetingRoom.objects.exclude(pk = self.pk).filter(meeting_room=self.meeting_room,reservation_date=self.reservation_date, reservation_from_time__gte= self.reservation_from_time, reservation_to_time= self.reservation_to_time).exists()
            case_2 = ReservationMeetingRoom.objects.exclude(pk = self.pk).filter(meeting_room=self.meeting_room,reservation_date=self.reservation_date, reservation_from_time__lte= self.reservation_from_time, reservation_to_time__gte= self.reservation_to_time).exists()
            case_3 = ReservationMeetingRoom.objects.exclude(pk = self.pk).filter(meeting_room=self.meeting_room,reservation_date=self.reservation_date, reservation_from_time__gte= self.reservation_from_time, reservation_to_time__lte=self.reservation_to_time).exists()
            case_4 = ReservationMeetingRoom.objects.exclude(pk = self.pk).filter(meeting_room=self.meeting_room,reservation_date=self.reservation_date, reservation_from_time__lte= self.reservation_from_time, reservation_to_time=self.reservation_to_time).exists()
            case_5 = ReservationMeetingRoom.objects.exclude(pk = self.pk).filter(meeting_room=self.meeting_room,reservation_date=self.reservation_date, reservation_from_time__gt=(self.reservation_from_time and self.reservation_to_time), reservation_to_time__lt=(self.reservation_to_time and self.reservation_from_time)).exists()
            case_6 = ReservationMeetingRoom.objects.exclude(pk = self.pk).filter(meeting_room=self.meeting_room,reservation_date=self.reservation_date, reservation_from_time__lt=(self.reservation_from_time and self.reservation_to_time), reservation_to_time__gt=(self.reservation_to_time and self.reservation_from_time)).exists()
            # if either of these is true, abort and render the error
            if case_1 or case_2 or case_3 or case_4 or case_5 or case_6 :
                raise ValidationError(('Selected Meeting room already reserved at this date and time ,please correct your information and then submit'))
        return cleaned_data
        
    def get_absolute_url(self):
        """Returns the url to access a detail record for this ReservationMeetingRoom Request Model."""
        return reverse('reservationmeetingroom-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.meeting_room}'