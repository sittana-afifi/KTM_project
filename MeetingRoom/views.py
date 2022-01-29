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
from .filters import ReservationMeetingRoomFilter, MeetingRoomFilter
from .tables import ReservationMeetingRoomTable
import datetime, _datetime
import xlwt, csv # use in export function
from .resources import MeetingResource, ReservationMeetingRoomResource
from tablib import Dataset
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import User

# Create a logger for this file or the name of the log level or Get an instance of a logger
logger = logging.getLogger(__name__) 
logger = logging.getLogger(__file__)

# Create your views here.
class MeetingListView(LoginRequiredMixin,generic.ListView):
    logger.info("Enter MeetingListView.")
    model = Meeting
    template_name = 'MeetingRoom/meeting_list.html'
    paginate_by = 5
    filter_class = MeetingRoomFilter

@login_required   
def MeetingFilter(request):
    """meeting View filter for meetings list and show filter options.

    Parameters
    ----------
    name : list
        a list of all meeting rooms
    returns : list, 
        a list of all meeting rooms with CRUD oprtions and detail view
    """
    
    meeting_list = Meeting.objects.all()
    meeting_filter = MeetingRoomFilter(request.GET, queryset= meeting_list)
    return render(request, 'MeetingRoom/meeting_list.html', {'filter': meeting_filter})

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
    success_url = reverse_lazy('meetings-filter')

# ReservationMeetingRoom CRUD View:
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
    success_url = reverse_lazy('reserve-filter')

@login_required
def ReservationFilter(request):
    """reservation meeting room requests View filter for meetings list and show filter options.

    Parameters
    ----------
    name : list
        a list of all reservation meeting room requests
    returns : list, 
        a list of all reservation meeting room requests with CRUD oprtions and detail view
    """
    
    reservation_list = ReservationMeetingRoom.objects.all()
    reservation_filter = ReservationMeetingRoomFilter(request.GET, queryset= reservation_list)
    return render(request, 'MeetingRoom/reservationmeetingroom_list.html', {'filter': reservation_filter})

# -----------------------------------------------------------
# Validation Reservation Meeting Room Requests Function:
# validate the reservation request in the database.
# created by : Mohammed Almoiz
# creation date : -Dec-2021
# update date : -Dec-2022
# -----------------------------------------------------------

@login_required
def validateReservationForm(form):
    """Function to check and make sure that there is no reservation for same meeting duplicated at same time
        and execlude the self pk.

    Parameters
    ----------
    input of reservation form and check cases

    meeting room : 
        forighn key from meeting model
    
    reservation date :
        datefield
    
    reservation_from_time ,reservation_to_time:
        timefield
        
    returns : 
        Boolean (true or false)

    """
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

"""
    A function used to reserve meetingroom request to the Team Form create view  for Metting Room.
    display the attributes of form and ask user to enter all requirements to reserve meetingroom.
    or a reservation Form and validate the reservation request in the database .
    to make sure that there is no reservation for same meeting duplicated at same time  
    ...

    Attributes
    ----------
    meeting room : 
        forighn key from meeting model
    
    team : 
        manytomany field from employee model
    
    task_managment :
        charfield forighn key from project model

    task_name :
        charfield forighn key form task model
    
    reservation date :
        datefield
    
    reservation_from_time ,reservation_to_time:
        timefield

    Methods
    -------
        user validation function and reserve form
    output 
    -------
    details of the reservation request and the staus if it success or failed.

    -------
    created by :
    -------
        Eman 

    creation date : 
    -------
        -Dec-2021

    update date :
    -------
        -Dec-2022
"""

@login_required
def reserve_view(request):
    """Function to send emails after reservationmeeting room model.

    Parameters
    ----------
    subject : 
        str

    meeting room : 
        forighn key from meeting model
    
    team : 
        manytomany field from employee model
    
    task_managment :
        charfield forighn key from project model

    task_name :
        charfield forighn key form task model
    
    reservation date :
        datefield
    
    reservation_from_time ,reservation_to_time:
        timefield
        
    returns : email, 
        send email address for the selected team email address.

    """
    
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
            Meeting_Room_Name = form.cleaned_data.get('meeting_room')
            Reservation_Date = form.cleaned_data.get('reservation_date')
            Reservation_From_Time = form.cleaned_data.get('reservation_from_time')
            Reservation_To_Time = form.cleaned_data.get('reservation_to_time')
            Task_Name = form.cleaned_data.get('task_name')
            Team_Members = form.cleaned_data.get('team')
            [print(member.user.email) for member in Team_Members.all()]
            subject = 'Team Meeting Details'
            message = f'Dear All:\n Have a good day this email due to meeting details. \n The meeting will be in {Meeting_Room_Name} at {Reservation_Date} from {Reservation_From_Time} to {Reservation_To_Time}.\n \n Best Regards'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [(member.user.email) for member in Team_Members.all() ]
            send_mail( subject, message, email_from, recipient_list )
            return HttpResponseRedirect(reverse('reserve-filter') )
    context = {
    'form' : form ,
    }
    return render(request, "MeetingRoom/reserve.html", context)


"""
    A function used to update reserve meetingroom request to the Team Form create view  for Metting Room.
    display the attributes of form and ask user to enter all requirements to reserve meetingroom.
    display the attributes of form.
     and ask user to enter all requirements to reserve meeting room.
    ...

    Attributes
    ----------
    meeting room : 
        forighn key from meeting model
    
    team : 
        manytomany field from employee model
    
    task_managment :
        charfield forighn key from project model

    task_name :
        charfield forighn key form task model
    
    reservation date :
        datefield
    
    reservation_from_time ,reservation_to_time:
        timefield

    Methods
    -------
        user validation function and reserve form
    output 
    -------
    details of the reservation request and the staus if it success or failed.
    add meeting outcomes  also execlude the self reservation request from validation.

    -------
    created by :
    -------
        Eman 

    creation date : 
    -------
        -Dec-2021

    update date :
    -------
        -Dec-2022
"""

@login_required
def update_reserve_view(request, pk):
    """ Function to send emails after update reservationmeeting room model.

    Parameters
    ----------
    subject : 
        str

    meeting room : 
        forighn key from meeting model
    
    team : 
        manytomany field from employee model
    
    task_managment :
        charfield forighn key from project model

    task_name :
        charfield forighn key form task model
    
    reservation date :
        datefield
    
    reservation_from_time ,reservation_to_time:
        timefield
        
    returns : email, 
        send email address for the selected team email address.

    """
    logger.info("Enter update_reserve_view.")
    reservation = ReservationMeetingRoom.objects.get(pk=pk)
    form = UpdateReservationForm(request.POST or None,instance=reservation)
    if request.method == "POST":
        logger.info("Enter request.method == POST")
        if form.is_valid():   
            logger.info("form is valid")
            form.save()
            messages.success(request, "You Successfully update reservation request for this meeting room at this time and date")
            Meeting_Room_Name = form.cleaned_data.get('meeting_room')
            Reservation_Date = form.cleaned_data.get('reservation_date')
            Reservation_From_Time = form.cleaned_data.get('reservation_from_time')
            Reservation_To_Time = form.cleaned_data.get('reservation_to_time')
            Task_Name = form.cleaned_data.get('task_name')
            Team_Members = form.cleaned_data.get('team')
            Meeting_Outcomes = form.cleaned_data.get('meeting_outcomes')
            [print(member.user.email) for member in Team_Members.all()]
            subject = 'Update Team Meeting Details'
            message = f'Dear All:\n Have a good day this email due to update meeting details.The meeting will be in {Meeting_Room_Name} at {Reservation_Date} from {Reservation_From_Time} to {Reservation_To_Time}. \n The meeting outcoumes points as below: \n\n {Meeting_Outcomes}..\n \nBest Regards'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [(member.user.email) for member in Team_Members.all() ]
            send_mail( subject, message, email_from, recipient_list )
            return HttpResponseRedirect(reverse('reserve-filter'))
    context = {
    'form' : form ,
    }
    return render(request, 'MeetingRoom/update_reserve_view.html', context)

today = _datetime.date.today()

"""
    A function used to export model information from database.
    ...

    Attributes
    ----------
    list : list
        the list of the meeting room
        first choose filter option from filter 
        function and then export file

    Methods
    -------
        import-export method in django

    output 
    -------
    file with different format (csv, excel ,yaml)

    -------
    created by :
    -------
        Eman 

    creation date : 
    -------
        15-Jan-2021

    update date :
    -------
        20-Jan-2022
"""

@login_required
def export_meetingrooms_xls(request):
    """ Export all meeting rooms list details view from database and allow filter option
        with different firmat(excel , json , yaml) .

        If there is no filter option choosed all meeting rooms in database will be export.

        Parameters
        ----------
        file format : (excel , json , yaml) 
            choose the file format from dropdown list

        Result
        ------
        export requested data with requested format.
        """

    logger.info("Export Function.")
    file_format = request.POST['file-format']
    meeting_filter = MeetingRoomFilter(request.GET, queryset=Meeting.objects.all())
    dataset = MeetingResource().export(meeting_filter.qs)

    if file_format == 'CSV':
        logger.info("Export csv file format.")
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment;filename={date}-MeetingRooms.csv'.format(date=today.strftime('%Y-%m-%d'),)    
        writer = csv.writer(response)
        writer.writerow(['Name', 'Description',])
        for std in dataset:
            writer.writerow(std)
        return response 
    
    elif  file_format == 'JSON':
        logger.info("Export json file format.")
        response = HttpResponse(dataset.json, content_type='application/json')
        response['Content-Disposition'] = 'attachment;filename={date}-MeetingRooms.json'.format(date=today.strftime('%Y-%m-%d'),)    
        return response

    elif file_format == 'YAML':
        logger.info("Export yaml file format.")
        response = HttpResponse(dataset.yaml,content_type='application/x-yaml')
        response['Content-Disposition'] = 'attachment;filename={date}-MeetingRooms.yaml'.format(date=today.strftime('%Y-%m-%d'),)    
        return response

    elif file_format == 'Excel':
        logger.info("Export excel file format.")
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment;filename={date}-MeetingRooms.xls'.format(date=today.strftime('%Y-%m-%d'),)    

        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Meetings')

        # Sheet header, first row
        row_num = 0

        font_style = xlwt.XFStyle()
        font_style.font.bold = True 

        columns = ['Name', 'Description',]

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

        # Sheet body, remaining rows
        font_style = xlwt.XFStyle()
    
        for row in dataset:
            row_num += 1
            for col_num in range(len(row)):
                ws.write(row_num, col_num, row[col_num], font_style)

        wb.save(response)
        return response

"""
    A function used to export model information from database.
    ...

    Attributes
    ----------
    list : list
        the list of the reservationmeetingroom
        first choose filter option from filter 
        function and then export file

    Methods
    -------
        import-export method in django

    output 
    -------
    file with different format (csv, excel ,yaml)

    -------
    created by :
    -------
        Eman 

    creation date : 
    -------
        15-Jan-2021

    update date :
    -------
        20-Jan-2022
"""

@login_required
def export_reservation_meeting_room_xls(request):
    """ Export all reservation meeting room requests list details view from database
         and allow filter option with different firmat(excel , json , yaml) .

        If there is no filter option choosed all reservation meeting room requests
        in database will be export.

        Parameters
        ----------
        file format : (excel , json , yaml) 
            choose the file format from dropdown list

        Result
        ------
        export requested data with requested format.
        """

    logger.info("Export Function.")
    file_format = request.POST['file-format']
    reservation_filter = ReservationMeetingRoomFilter(request.GET, queryset=ReservationMeetingRoom.objects.all())
    dataset = ReservationMeetingRoomResource().export(reservation_filter.qs)
    
    if file_format == 'CSV':
        logger.info("Export csv file format.")
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] ='attachment;filename={date}-Reservation_Meeting_Rooms.csv'.format(date=today.strftime('%Y-%m-%d'),)    
        writer = csv.writer(response)
        writer.writerow(['Meeting_Room', 'Reservation_Date','Reservation_From_Time', 'Reservation_To_Time','Team','Meeting_Outcomes','Meeting_Project_Name','Task_Name',])
        for std in dataset:
            writer.writerow(std)
        return response 

    elif  file_format == 'JSON':
        logger.info("Export json file format.")
        response = HttpResponse(dataset.json, content_type='application/json')
        response['Content-Disposition'] = 'attachment;filename={date}-Reservation_Meeting_Rooms.json'.format(date=today.strftime('%Y-%m-%d'),)    
        return response

    elif file_format == 'YAML':
        logger.info("Export yaml file format.")
        response = HttpResponse(dataset.yaml,content_type='application/x-yaml')
        response['Content-Disposition'] = 'attachment;filename={date}-Reservation_Meeting_Rooms.yaml'.format(date=today.strftime('%Y-%m-%d'),)    
        return response

    elif file_format == 'Excel':
        logger.info("Export excel file format.")
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment;filename={date}-Reservation_Meeting_Rooms.xls'.format(date=today.strftime('%Y-%m-%d'),)    

        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('ReservationMeetingRoomsRequest')

        # Sheet header, first row
        row_num = 0

        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        columns = ['Meeting_Room', 'Reservation_Date','Reservation_From_Time', 'Reservation_To_Time','Team','Meeting_Outcomes','Meeting_Project_Name','Task_Name',]

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

        # Sheet body, remaining rows
        font_style = xlwt.XFStyle()

        for row in dataset:
            row_num += 1
            for col_num in range(len(row)):                
                ws.write(row_num, col_num, row[col_num], font_style)

        wb.save(response)
        return response