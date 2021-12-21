from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.urls import reverse_lazy
from django.views import generic
from .models import Meeting, ReservationMeetingRoom
from django.views.generic.edit import UpdateView , DeleteView , CreateView 
from bootstrap_datepicker_plus.widgets import DatePickerInput, TimePickerInput, DateTimePickerInput, MonthPickerInput, YearPickerInput
from django.shortcuts import render 
from .forms import ReservationForm
from django.core.exceptions import ValidationError 
from django.forms import ValidationError
from .forms import ReservationForm
from flatpickr import DatePickerInput, TimePickerInput, DateTimePickerInput
from django.contrib import messages
from django.forms import ValidationError
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import get_object_or_404




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

######################################################
# ReservationMeetingRoom CRUD:
class ReservationMeetingRoomListView(LoginRequiredMixin,generic.ListView):
    model = ReservationMeetingRoom
    template_name = 'MeetingRoom/reservationmeetingroom_list.html'

class ReservationMeetingRoomDetailView(LoginRequiredMixin,generic.DetailView):
    model = ReservationMeetingRoom
    template_name = 'MeetingRoom/reservationmeetingroom_detail.html'

class ReservationMeetingRoomCreate(LoginRequiredMixin,CreateView):
    model = ReservationMeetingRoom
    fields = '__all__'

class ReservationMeetingRoomUpdate(LoginRequiredMixin,UpdateView):
    model = ReservationMeetingRoom
    fields = '__all__' # Not recommended (potential security issue if more fields added)

class ReservationMeetingRoomDelete(LoginRequiredMixin,DeleteView):
    model = ReservationMeetingRoom
    success_url = reverse_lazy('reservationmeetingrooms')

###############################################

# Reservation Form View:
@login_required
def reserve_view(request):
    form = ReservationForm(request.POST)
    if request.method == "POST":
        form = ReservationForm(request.POST)
        if form.is_valid():
            meeting_room = form.cleaned_data['meeting_room']
            reservation_date = form.cleaned_data['reservation_date']
            reservation_from_time = form.cleaned_data['reservation_from_time']
            reservation_to_time = form.cleaned_data['reservation_to_time']
            team = form.cleaned_data['team']
            form = form.save(commit=False)
            #if  form.meeting_room == form.meeting_room:
            case_1 = ReservationMeetingRoom.objects.filter(meeting_room=meeting_room,reservation_date=reservation_date, reservation_from_time__lte=reservation_from_time, reservation_to_time__gte=reservation_to_time).exists()
            # case 2: a room is booked before the requested check_out date and check_out date is after requested check_out date
            case_2 = ReservationMeetingRoom.objects.filter(meeting_room=meeting_room,reservation_date=reservation_date, reservation_from_time__lte=reservation_to_time, reservation_to_time__gte=reservation_to_time).exists()
            case_3 = ReservationMeetingRoom.objects.filter(meeting_room=meeting_room,reservation_date=reservation_date, reservation_from_time__gte=reservation_from_time, reservation_to_time__lte=reservation_to_time).exists()
            # if either of these is true, abort and render the error
            if case_1 or case_2 or case_3:                    
                #raise ValidationError(('Selected Meeting room already reserved at this date and time'))
                return render (request, "MeetingRoom/reserveerrorl.html")
            form.save()
            return HttpResponseRedirect(reverse('reservationmeetingrooms') )
        else:
            print('Error please correct your information and then submit')
    context = {
        'form' : form ,
    }
    return render(request, "MeetingRoom/reserve.html", context)






###########################################
# Reservation Update View :
@login_required
def update_reserve_view(request, pk):
        form = ReservationForm(request.POST)
        form= get_object_or_404(ReservationMeetingRoom, pk=pk)
        form = ReservationForm(request.POST or None, instance= form)
        context= {'form': form}
        if request.method == "POST":
            form = ReservationForm(request.POST)
            if form.is_valid():
                meeting_room = form.cleaned_data['meeting_room']
                reservation_date = form.cleaned_data['reservation_date']
                reservation_from_time = form.cleaned_data['reservation_from_time']
                reservation_to_time = form.cleaned_data['reservation_to_time']
                team = form.cleaned_data['team']
                form= form.save(commit= False)
                case_1 = ReservationMeetingRoom.objects.filter(meeting_room=meeting_room,reservation_date=reservation_date, reservation_from_time__lte=reservation_from_time, reservation_to_time__gte=reservation_to_time).exists()
            # case 2: a room is booked before the requested check_out date and check_out date is after requested check_out date
                case_2 = ReservationMeetingRoom.objects.filter(meeting_room=meeting_room,reservation_date=reservation_date, reservation_from_time__lte=reservation_to_time, reservation_to_time__gte=reservation_to_time).exists()
                case_3 = ReservationMeetingRoom.objects.filter(meeting_room=meeting_room,reservation_date=reservation_date, reservation_from_time__gte=reservation_from_time, reservation_to_time__lte=reservation_to_time).exists()
            # if either of these is true, abort and render the error
                if case_1 or case_2 or case_3:
                    return render (request, "MeetingRoom/reserveerrorl.html")
                    raise ValidationError(('Selected Meeting room already reserved at this date and time'))
                form.save()
                messages.success(request, "You successfully updated the post")
                context= {'form': form}
                return HttpResponseRedirect(reverse('reservationmeetingrooms') )
        else:
            context= {'form': form,}
                  #'error': 'The form was not updated successfully. Please enter in a title and content'}
            return render(request,'MeetingRoom/update_reserve_view.html' , context)


