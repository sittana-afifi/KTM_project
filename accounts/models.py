from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractBaseUser , UserManager
from django.urls import reverse



# create new model to deal with user ,
# this model is dynamics, we could extend it in demand.
class Account (AbstractBaseUser,BaseUserManager):


    #def get_absolute_url(self):
     #   return reverse('user-detail',args= [str(self.id)]) 

    def __str__(self):
        return self.username
    


