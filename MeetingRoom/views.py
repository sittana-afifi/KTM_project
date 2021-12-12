from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic
from .models import Meeting
from django.views.generic.edit import UpdateView , DeleteView , CreateView 

# Create your views here.
class MeetingListView(LoginRequiredMixin,generic.ListView):
    model = Meeting
    template_name = 'MeetingRoom/meeting_list.html'

class MeetingDetailView(LoginRequiredMixin,generic.DetailView):
    model = Meeting
    template_name = 'MeetingRoom/meeting_detail.html'

class MeetingCreate(LoginRequiredMixin,CreateView):
    model = Meeting
    fields = '__all__'

class MeetingUpdate(LoginRequiredMixin,UpdateView):
    model = Meeting
    fields = '__all__' # Not recommended (potential security issue if more fields added)

class MeetingDelete(LoginRequiredMixin,DeleteView):
    model = Meeting
    success_url = reverse_lazy('meetings')