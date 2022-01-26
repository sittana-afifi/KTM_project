from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser , UserManager
<<<<<<< HEAD
import logging, logging.config
<<<<<<< HEAD

from django.db import  models # Logging view in Django.
=======
from django.db import models

>>>>>>> 9a9d0f3f14f4622ca7980b4362857200c32dca11
=======
from django.db import models
import os, logging, logging.config # Logging view in Django.
>>>>>>> c9fce7c (add email setting in the reservation request and assign task request)

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
<<<<<<< HEAD
    username = models.CharField('username',null = True , max_length= 20)
=======
    username = models.CharField('username', null=True, max_length=20)
>>>>>>> 9a9d0f3f14f4622ca7980b4362857200c32dca11
=======
    username = models.CharField('username',null = True,max_length = 20)
>>>>>>> c9fce7c (add email setting in the reservation request and assign task request)
    logger.info('enter Account model.')
    '''
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

<<<<<<< HEAD
=======
        return self.username
    '''
>>>>>>> c9fce7c (add email setting in the reservation request and assign task request)
