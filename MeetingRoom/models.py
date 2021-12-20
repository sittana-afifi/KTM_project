from django.db import models
from django.db.models.fields import DateField
from django.urls.base import reverse
from django.core.exceptions import ValidationError
from TaskManagement.models import Employee
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



# Ceate Reservation Meeting Room Model:
class ReservationMeetingRoom(models.Model):
    """Model representing a project."""
    meeting_room = models.ForeignKey(Meeting, on_delete=models.SET_NULL, null=True, blank=False)
    reservation_date = models.DateField(null=True, blank=False)
    reservation_from_time = models.TimeField(auto_now=False, auto_now_add=False)
    reservation_to_time = models.TimeField(auto_now=False, auto_now_add=False)
    team = models.ManyToManyField(Employee,blank=True,related_name='+') 
    #models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=False)
    def clean_reservation_date(self):
        date = self.cleaned_date['reservation_date']
        # Check if a date is not in the past.
        if date < datetime.date.today():
            raise ValidationError(_('Invalid date - Date cannot be in the past'))
        return date

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.meeting_room}'
    def get_absolute_url(self):
        """Returns the url to access a detail record for this project."""
        return reverse('reservationmeetingroom-detail', args=[str(self.id)])
