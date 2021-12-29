from django.db import models
from django.db.models.fields import DateField
from django.urls.base import reverse
from django.core.exceptions import ValidationError
from TaskManagement.models import Employee, Project, Task, Taskmanagment
from parler.models import TranslatableModel, TranslatedFields

# Create your models here.
class Meeting(models.Model):
    """Model representing a Meeting."""
    name = models.CharField(max_length=200, help_text='Enter a Meeting name (e.g. Meeting Room App)')
    description = models.TextField(max_length=1000, help_text='Enter a brief location of the meeting')
    #privacy
    def __str__(self):
        """String for representing the Model object."""
        return self.name
    def get_absolute_url(self):
        """Returns the url to access a detail record for this project."""
        return reverse('meeting-detail', args=[str(self.id)])



# ReservationMeetingRoom Model:
class ReservationMeetingRoom(models.Model):
    """Model representing a project."""
    meeting_room = models.ForeignKey(Meeting, on_delete=models.SET_NULL, null=True, blank=False)
    reservation_date = models.DateField(null=False, blank=False)
    reservation_from_time = models.TimeField(auto_now=False, auto_now_add=False)
    reservation_to_time = models.TimeField(auto_now=False, auto_now_add=False)
    team = models.ManyToManyField(Employee,blank=True,related_name='+')
    meeting_outcomes = models.TextField(max_length=1000, help_text='Enter the meeting outcomes')
    meeting_project_name = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True)
    task_name = models.ForeignKey(Task, on_delete=models.SET_NULL, null=True, blank=True)
    def clean_reservation_date(self):
        date = self.cleaned_date['reservation_date']
        # Check if a date is not in the past.
        if date < datetime.date.today():
            raise ValidationError(_('Invalid date - Date cannot be in the past'))
        return date
    def clean(self, *args, **kwargs):
        cleaned_data = super().clean(*args, **kwargs)
        if self.pk:
            case_1 = ReservationMeetingRoom.objects.exclude(pk = self.pk).filter(meeting_room=self.meeting_room,reservation_date=self.reservation_date, reservation_from_time__lte=self.reservation_from_time, reservation_to_time__gte=self.reservation_to_time).exists()
            case_2 = ReservationMeetingRoom.objects.exclude(pk = self.pk).filter(meeting_room=self.meeting_room,reservation_date=self.reservation_date, reservation_from_time__lte=self.reservation_to_time, reservation_to_time__gte=self.reservation_to_time).exists()
            case_3 = ReservationMeetingRoom.objects.exclude(pk = self.pk).filter(meeting_room=self.meeting_room,reservation_date=self.reservation_date, reservation_from_time__gte=self.reservation_from_time, reservation_to_time__gte=self.reservation_to_time).exists()                # if either of these is true, abort and render the error
            if case_1 or case_2 or case_3:
                #messages.error(request, "Selected Meeting room already reserved at this date and time ,please correct your information and then submit")
                raise ValidationError(('Selected Meeting room already reserved at this date and time ,please correct your information and then submit'))
        return cleaned_data
    
    def __str__(self):
        """String for representing the Model object."""
        return f'{self.meeting_room}'
        return f'{self.team.first_name}'
    def get_absolute_url(self):
        """Returns the url to access a detail record for this project."""
        return reverse('reservationmeetingroom-detail', args=[str(self.id)])
