"""
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
# Use include() to add paths from the account application
from django.urls import include
#Add URL maps to redirect the base URL to our application
from django.views.generic import RedirectView
# Use static() to add url mapping to serve static files during development (only)
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns # For localization and translation settings
from django.utils.translation import gettext_lazy as _
from accounts import views
from TaskManagement import views
from MeetingRoom import views
from django.contrib import admin
from django.urls import path
from django.views.generic import RedirectView, TemplateView
from accounts import views

urlpatterns = i18n_patterns(

    path('', views.index, name='index'),
    path('admin/', admin.site.urls),    
    path('accounts/', include('accounts.urls' )),
    path('accounts/', include('django.contrib.auth.urls')),
    path('TaskManagement/', include('TaskManagement.urls')),
    path('MeetingRoom/', include('MeetingRoom.urls')),
    path('rosetta/', include('rosetta.urls')),  
    path('bootstrap/',TemplateView.as_view(template_name='bootstrap/')),

 ) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)