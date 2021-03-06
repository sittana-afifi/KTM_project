from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields import DateField
from django.urls.base import reverse
import logging, logging.config # Logging view in Django.
# Create a logger for this file or the name of the log level or Get an instance of a logger
logger = logging.getLogger(__name__)
logger = logging.getLogger(__file__)

"""
    create new model (employee) to extend user model and add one-to-one link between them.
    ...

    Attributes
    ----------
    user : OneToOneField
        user model with one_to_one mmap
    Employee_id : CharField
        Id for the employee
    Phone_number : CharField
        phone number for employee
    date_joined : DateField
        the joined date for employee

    Methods
    -------
    def __str__(self)
        tells Django what to print when it needs to print out an instance of Employee model

    created by :
    -------
        Sittana Afifi

    creation date : 
    -------
        06-Dec-2021

    update date :
    -------
         21-Jan-2022
"""
class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Employee_id = models.CharField(max_length=4,  blank=True)
    Phone_number = models.CharField( max_length=10,  blank=True)
    date_joined = models.DateField(null=True, blank=True,)

    def __str__(self):
        """
            Parameters
            ----------
            self : 
                 self.instance is your current user

            return:
            ----------
                String for representing the Model object.
            
            """
        logger.info("Enter Employee model.")
        return f'{self.user}'
        
# Create a project model :
class Project(models.Model):
    """Model representing a project."""
    name = models.CharField(max_length=200, help_text='Enter a project name (e.g. Task Managment Project)')
    description = models.TextField(max_length=1000, help_text='Enter a brief description of the project')
    #privacy
    def __str__(self):
        """String for representing the Model object."""
        return self.name

    def get_absolute_url(self):
        """Returns the url to access a detail record for this project."""
        return reverse('project-detail', args=[str(self.id)])

# Create Task model :
class Task(models.Model):
    """Model representing a specific task in a project."""
    project = models.ForeignKey('Project', on_delete=models.SET_NULL, null=True, blank=True)
    task_name = models.CharField(max_length=200, help_text='Enter a task name (e.g. Design)')
    task_description = models.TextField(max_length=1000, help_text='Enter a brief description of the task')
    def __str__(self):
        """String for representing the Model object."""
        return self.task_name

    def get_absolute_url(self):
        """Returns the url to access a detail record for this project."""
        return reverse('task-detail', args=[str(self.id)])

"""
    A class used to represent Taskmanagment.
    ...

    Attributes
    ----------
    assignee : ForeignKey from Employee Model which is ForeignKey from User model
    assigneedTo : ForeignKey as ManyToManyField from Employee Model
    task_managment : ForeignKey from Task Model
    status : CharField
    priority : CharField
    comment : CharField
    start_date : DateField
    end_date : DateField

    Methods
    -------
    def __str__(self)
        tells Django what to print when it needs to print out an instance of Taskmanagment model

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
class Taskmanagment(models.Model):
    """Model representing assign task process as Taskmanagment ."""
    assignee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=False, related_name='taskmanagments')
    assigneedTo = models.ManyToManyField(Employee)
    task_managment = models.ForeignKey('Task', on_delete=models.SET_NULL, null=True,blank=False)
    TASK_STATUS = (
        ('TD', 'To do'),
        ('IP', 'In Progress'),
        ('C', 'Completed'),
    )
    status = models.CharField(
        max_length=2,
        choices=TASK_STATUS,
        blank=False,
        default='TD',
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
        blank=False,
        default='l',
        help_text='Tasks Priorities',
    )
    comment = models.CharField(max_length=200,null=True,blank=True)
    start_date = models.DateField(null=True, blank=False)
    end_date = models.DateField(null=True, blank=False)
    
    def get_assigneedTo_values(self):
        ret = ''
        print(self.assigneedTo.all())
        # use models.ManyToMany field's all() method to return all the assigneedTo objects that this employee belongs to.
        for assigneedTo in self.assigneedTo.all():
            ret = ret + assigneedTo.user.username + ','
        # remove the last ',' and return the value.
        return ret[:-1]

    def get_assigneedTo_emails(self):
        ret = ''
        print(self.assigneedTo .all())
        # use models.ManyToMany field's all() method to return all the Team objects that this employee belongs to.
        for assigneedTo  in self.assigneedTo .all():
            ret = ret + assigneedTo .user.email + ','
        # remove the last ',' and return the value.
        return ret[:-1]

    @property
    def is_overdue(self):
        if self.end_date and DateField.today() > self.end_date:
            return True
        return False

    class Meta:
        ordering = ['end_date']
        permissions = (("can_mark_completed", "Set task as completed"),)

    def get_absolute_url(self):
        """Returns the url to access a detail record for this task."""
        return reverse('taskmanagment-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.task_managment}'