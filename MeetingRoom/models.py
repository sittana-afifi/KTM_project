from django.db import models
from django.db.models.fields import DateField
from django.urls.base import reverse

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
