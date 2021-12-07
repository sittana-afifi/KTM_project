from django.db import models
from django.contrib.auth.models import User






#create new model (employee) to extend user model and add one-to-one link between them.
class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Employee_id = models.CharField(max_length=4,  blank=True)
    Phone_number = models.CharField( max_length=10,  blank=True)
    date_joined = models.DateField(null=True, blank=True)


#######################################
# Create taskmanagment model :
class Taskmanagment(models.Model):
    assignee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=False, related_name='Taskmanagment')
    assigneedTo = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=False,related_name='teammamember')
    task_managment = models.ForeignKey('Task', on_delete=models.SET_NULL, null=True,blank=False)

    TASK_STATUS = (
        ('TD', 'To do'),
        ('IP', 'In Progress'),
        ('C', 'Completed'),
    )
    status = models.CharField(
        max_length=2,
        choices=TASK_STATUS,
        blank=True,
        default='C',
        help_text='Tasks Status',
    )
    TASK_PRIORITY = (
        ('H', 'High'),
        ('M', 'Meduim'),
        ('L', 'Low'),    
    )

    priority = models.CharField(
        max_length=1,
        choices=TASK_PRIORITY,
        blank=True,
        default='l',
        help_text='Tasks Priorities',
    )
    comment = models.CharField(max_length=200)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    @property
    def is_overdue(self):
        if self.end_date and date.today() > self.end_date:
            return True
        return False

    class Meta:
        ordering = ['end_date']
        permissions = (("can_mark_completed", "Set task as completed"),)

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.task_managment}'

    def get_absolute_url(self):
        """Returns the url to access a detail record for this task."""
        return reverse('taskmanagment-detail', args=[str(self.id)])