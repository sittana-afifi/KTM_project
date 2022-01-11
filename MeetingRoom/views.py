from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.urls import reverse_lazy, reverse
from django.views import generic
from .models import Meeting, ReservationMeetingRoom
from django.views.generic.edit import UpdateView , DeleteView , CreateView 
from bootstrap_datepicker_plus.widgets import DatePickerInput, TimePickerInput, DateTimePickerInput, MonthPickerInput, YearPickerInput
from .forms import ReservationForm, UpdateReservationForm
from django.core.exceptions import ValidationError 
from django.forms import ValidationError
from flatpickr import DatePickerInput, TimePickerInput, DateTimePickerInput
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
import os, logging, logging.config # Logging view in Django
from .filters import ReservationMeetingRoomFilter
from .tables import ReservationMeetingRoomTable

# Create a logger for this file or the name of the log level or Get an instance of a logger
logger = logging.getLogger(__name__) 
logger = logging.getLogger(__file__)

# Create your views here.
class MeetingListView(LoginRequiredMixin,generic.ListView):
    logger.info("Enter MeetingListView.")
    model = Meeting
    template_name = 'MeetingRoom/meeting_list.html'
    paginate_by = 5

class MeetingDetailView(LoginRequiredMixin,generic.DetailView):
    logger.info("Enter MeetingDetailView.")
    model = Meeting
    template_name = 'MeetingRoom/meeting_detail.html'

class MeetingCreate(LoginRequiredMixin,CreateView):
    logger.info("Enter MeetingCreate.")
    model = Meeting
    fields = '__all__'

class MeetingUpdate(LoginRequiredMixin,UpdateView):
    logger.info("Enter MeetingUpdate.")
    model = Meeting
    fields = '__all__' # Not recommended (potential security issue if more fields added)

class MeetingDelete(LoginRequiredMixin,DeleteView):
    logger.info("Enter MeetingDelete.")
    model = Meeting
    success_url = reverse_lazy('meetings')

# ReservationMeetingRoom CRUD:
def search(request):
    reservation_list = ReservationMeetingRoom.objects.all()
    reservation_filter = ReservationMeetingRoomFilter(request.GET, queryset= reservation_list)
    return render(request, 'MeetingRoom/reservationmeetingroom_list.html', {'filter': reservation_filter})

class ReservationMeetingRoomListView(LoginRequiredMixin,generic.ListView):
    logger.info("Enter ReservationMeetingRoomListView.")
    model = ReservationMeetingRoom
    template_name = 'MeetingRoom/reservationmeetingroom_list.html'
    paginate_by = 5
    table_class  = ReservationMeetingRoomTable
    filter_class = ReservationMeetingRoomFilter

class ReservationMeetingRoomDetailView(LoginRequiredMixin,generic.DetailView):
    logger.info("Enter ReservationMeetingRoomDetailView.")
    model = ReservationMeetingRoom
    template_name = 'MeetingRoom/reservationmeetingroom_detail.html'

class ReservationMeetingRoomCreate(LoginRequiredMixin,CreateView):
    logger.info("Enter ReservationMeetingRoomCreate.")
    model = ReservationMeetingRoom
    fields = '__all__'

class ReservationMeetingRoomUpdate(LoginRequiredMixin,UpdateView):
    logger.info("Enter ReservationMeetingRoomUpdate.")
    model = ReservationMeetingRoom
    fields = '__all__' # Not recommended (potential security issue if more fields added)

class ReservationMeetingRoomDelete(LoginRequiredMixin,DeleteView):
    logger.info("Enter ReservationMeetingRoomDelete.")
    model = ReservationMeetingRoom
    success_url = reverse_lazy('reservationmeetingrooms')

# Validation Reservation Meeting Room Requests Function:
def validateReservationForm(form):
    logger.info("Enter validateReservationForm.")
    if form.is_valid():
            logger.info("Enter form.is_valid.")
            meeting_room = form.cleaned_data['meeting_room']
            reservation_date = form.cleaned_data['reservation_date']
            reservation_from_time = form.cleaned_data['reservation_from_time']
            reservation_to_time = form.cleaned_data['reservation_to_time']
            team = form.cleaned_data['team']
            form = form.save(commit=False)
            case_1 = ReservationMeetingRoom.objects.filter(meeting_room=meeting_room, reservation_date=reservation_date, reservation_from_time__gte=reservation_from_time, reservation_to_time=reservation_to_time).exists()
            case_2 = ReservationMeetingRoom.objects.filter(meeting_room=meeting_room, reservation_date=reservation_date, reservation_from_time__lte=reservation_from_time, reservation_to_time__gte=reservation_to_time).exists()
            case_3 = ReservationMeetingRoom.objects.filter(meeting_room=meeting_room, reservation_date=reservation_date, reservation_from_time__gte=reservation_from_time, reservation_to_time__lte=reservation_to_time).exists()
            case_4 = ReservationMeetingRoom.objects.filter(meeting_room=meeting_room, reservation_date=reservation_date, reservation_from_time__lte=reservation_from_time, reservation_to_time=reservation_to_time).exists()
            case_5 = ReservationMeetingRoom.objects.filter(meeting_room=meeting_room, reservation_date=reservation_date, reservation_from_time__gt=(reservation_from_time and reservation_to_time), reservation_to_time__lt=(reservation_to_time and reservation_from_time)).exists()
            case_6 = ReservationMeetingRoom.objects.filter(meeting_room=meeting_room, reservation_date=reservation_date, reservation_from_time__lt=(reservation_from_time and reservation_to_time), reservation_to_time__gt=(reservation_to_time and reservation_from_time)).exists()
            # if either of these is true, abort and render the error
            return case_1 or case_2 or case_3 or case_4 or case_6

# Reservation Form Create View:
@login_required
def reserve_view(request):
    logger.info("Enter reserve_view.")
    form = ReservationForm()
    if request.method == "POST":
        form = ReservationForm(request.POST)
        notvalidform =  validateReservationForm(form)
        if notvalidform:  
            messages.error(request, "Selected Meeting room already reserved at this date and time ,please correct your information and then submit")
        elif form.is_valid():
            form.save()
            messages.success(request, "You successfully reserve this meeting room at this time and date")
            return HttpResponseRedirect(reverse('reservationmeetingrooms') )
    context = {
    'form' : form ,
    }
    return render(request, "MeetingRoom/reserve.html", context)

# Reservation Form Update View :
@login_required
def update_reserve_view(request, pk):
    logger.info("Enter update_reserve_view.")
    reservation = ReservationMeetingRoom.objects.get(pk=pk)
    form = UpdateReservationForm(request.POST or None,instance=reservation)
    if request.method == "POST":
        logger.info("Enter request.method == POST")
        if form.is_valid():   
            logger.info("form is valid")
            form.save()
            messages.success(request, "You Successfully update reservation request for this meeting room at this time and date")
            return HttpResponseRedirect(reverse('reservationmeetingrooms'))
    context = {
    'form' : form ,
    }
    return render(request, 'MeetingRoom/update_reserve_view.html', context)