from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser , UserManager
import logging, logging.config
<<<<<<< HEAD

from django.db import  models # Logging view in Django.
=======
from django.db import models

>>>>>>> 9a9d0f3f14f4622ca7980b4362857200c32dca11

# Create a logger for this file or the name of the log level or Get an instance of a logger
logger = logging.getLogger(__name__)
logger = logging.getLogger(__file__)

"""
    A class used to represent an Account, this model is dynamics, we could extend it in demand
    ...

    Attributes
    ----------
    username : CharField
        the name of the user

    Methods
    -------
    def __str__(self)
        tells Django what to print when it needs to print out an instance of Account model

    created by :
    -------
        Sittana 

    creation date : 
    -------
        01-Dec-2021

    update date :
    -------
         21-Jan-2022
"""

class Account (AbstractBaseUser):
<<<<<<< HEAD
    username = models.CharField('username',null = True , max_length= 20)
=======
    username = models.CharField('username', null=True, max_length=20)
>>>>>>> 9a9d0f3f14f4622ca7980b4362857200c32dca11
    logger.info('enter Account model.')
    class ReadonlyMeta:
        readonly = ['username']

    def __str__(self):
        """print out username as an instance of Account model.

        Parameters
        ----------
        self :
            self.instance is your current user

        return:
        ----------
            username as an instance of Account model
        """
        return self.username
#user1=Account.objects.get(id='1')
#print(Account.objects.all())

