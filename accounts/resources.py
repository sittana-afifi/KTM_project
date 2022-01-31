from import_export import resources
from django.contrib.auth.models import User
from import_export import  resources
    
class AccountResource(resources.ModelResource):

    def get_queryset(self):
        return User.objects.filter(username=self.username, first_name=self.first_name,last_name=self.last_name,date_joined=self.date_joined,email=self.email,is_superuser=self.is_superuser,is_active=self.is_active,is_staff=self.is_staff)
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name','date_joined', 'email','is_superuser', 'is_active', 'is_staff',)
        export_order = ('username', 'first_name', 'last_name', 'email','is_superuser', 'is_active', 'is_staff',)
        
        