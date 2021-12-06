from django.db import models
from django.contrib.auth.models import User






#create new model (employee) to extend user model and add one-to-one link between them.
class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Employee_id = models.CharField(max_length=4,  blank=True)
    Phone_number = models.CharField( max_length=10,  blank=True)
    date_joined = models.DateField(null=True, blank=True)
