from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from ..models import Students,Teachers, CustomUser, Videos , Appointment
import razorpay
from django.conf import settings
from itertools import chain
from datetime import timedelta, datetime, time

from django.utils import timezone

# authorize razorpay client with API Keys.
razorpay_client = razorpay.Client(
	auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))



def landing_page(request):
    return render(request,'base/gifted/index.html')

def about_us(request):
    return render(request, 'base/gifted/about.html')  

def contact_us(request):

    
    teachers = Teachers.objects.all()
    start_date = datetime.now()
    # print(start_date)
    end_date = datetime.now() + timedelta(days=6)

    appointments = Appointment.objects.filter(date__range=[start_date,end_date])
    final_list = []
    temp = {}
    final_list2 = []
    # temp['date'] = start_date + timedelta(days=i)
    # temp['timeslot'] = '1:00'

    for i in range(7):
        single_day_list = []
        for j in range(3):
            temp = {}
            temp['date'] = start_date + timedelta(days=i)
            if j == 0:
                if Appointment.objects.filter(date = start_date + timedelta(days=i), timing=time(13,00,00)).first():
                    continue
                else:    
                    temp['timeslot'] = '1:00 pm'
            if j == 1:
                if Appointment.objects.filter(date = start_date + timedelta(days=i), timing=time(15,00,00)).first():
                    continue
                else:    
                    temp['timeslot'] = '3:00 pm'
            if j == 2:
                if Appointment.objects.filter(date = start_date + timedelta(days=i), timing=time(17,00,00)).first():
                    continue
                else:    
                    temp['timeslot'] = '5:00 pm' 
            single_day_list.append(temp)
            
            
        data = {}
        data[start_date + timedelta(days=i)] = single_day_list              
        final_list.append(single_day_list)

        final_list2.append(data)
 
    
    if request.method=='POST': 
        name = request.POST['name']
        phone = request.POST['phone']
        email = request.POST['email']
        date_time = request.POST['time']

        ls = date_time.split(';')
        print('date time split')
        print(ls[0])
        print(ls[1])
        
        teacher_name = request.POST['product']
        # teacher_name = 'varija'
        user1 = CustomUser.objects.get(username=teacher_name)
        teacher = Teachers.objects.get(teacher_id=user1)

        from django_zoom_meetings import ZoomMeetings
        # Creat a JWT app your account https://marketplace.zoom.us/ and use
        # the api_key, secret_key and your zoom email address to create a ZoomMeetings instance
        api_key='g4Jwbl4RQf6m4mlPVa7r7g'
        secret_key='JZZF8Ce3KXH1KvEocDVlsE08GgP0XJfvh1wR'
        zoom_email='aayush.halgekar@gmail.com'
        my_zoom = ZoomMeetings(api_key,secret_key,zoom_email)
        str_topic="test meetig"
        timenow = datetime.now()
        dates_ls = ls[1].split('-')
        # date1= datetime(2021,7,5,13,30)

        str_meeting_duration='30'
        str_meeting_password='12345'
        
        # required parameters are date,topic,duration and the password of the meeting. In return you will get all the meeting details including the join url
       

        if ls[0] == '1:00 pm':
            time2 = time(13,00,00)
            date1 = datetime(int(dates_ls[0]),int(dates_ls[1]),int(dates_ls[2]),13,00)
        if ls[0] == '3:00 pm':
            time2 = time(15,00,00)
            date1 = datetime(int(dates_ls[0]),int(dates_ls[1]),int(dates_ls[2]),15,00)
        if ls[0] == '5:00 pm':
            time2 = time(17,00,00)
            date1 = datetime(int(dates_ls[0]),int(dates_ls[1]),int(dates_ls[2]),17,00)

        create_meeting = my_zoom.CreateMeeting(date1,str_topic,str_meeting_duration,str_meeting_password) 
           

        Appointment.objects.create(timing = time2, date=ls[1],teacher_id=teacher,firstname=name,appointment_link = create_meeting['join_url'], zoom_id= create_meeting['id'],start_link=create_meeting['start_url'], zoom_password=create_meeting['password'])
       
        return redirect(reverse('paymenthandler_contactus'))
        # student = Students.objects.get(student_id = request.user)
        
    return render(request, 'base/gifted/contact.html', {'dates_list': final_list2,'teachers':teachers} )

def courses(request):
    return render(request, 'base/gifted/courses.html')    

def gifted_prices(request):
    return render(request, 'base/gifted/price.html')

def gifted_books(request):
    return render(request, 'base/gifted/books.html')    

def feedback_form(request):
    return render(request, 'base/gifted/sidebar-right.html')

def gifted_videos(request):
    student = Students.objects.filter(student_id = request.user)
    print(student)

    ls = {}
    for i in student:
        class_id = i.classroom_id.id

        videos = Videos.objects.filter(classroom_id = class_id)
        ls[i.classroom_id.classroom_name] = videos

    print(ls)
    # videos = Videos.objects.all()
    print(videos)
    return render(request, 'base/videos.html', {'videos':ls})    

@login_required(login_url='login')
def home(request):
    try :
        student = Students.objects.get(student_id = request.user)
        subscribed = student.student_id.is_subscribed
        freetrial = student.student_id.is_free_trial
        print(12345)
        present = timezone.now()
        if present < student.student_id.expiry_free_trial:
            request.user.is_free_trial = False
            request.user.finished_free_trial = True
            request.user.save()
            freetrial = False

        print(present < student.student_id.expiry_free_trial)
    except Exception as e:
        print(e)
        subscribed = True
        freetrial = False
    
    if (not subscribed and not freetrial):
        return redirect('paymenthome')
    else:    
        teacher_mapping = Teachers.objects.filter(teacher_id=request.user).select_related('classroom_id')
        student_mapping = Students.objects.filter(student_id=request.user).select_related('classroom_id')
        teachers_all = Teachers.objects.all()
        mappings = chain(teacher_mapping,student_mapping) 
        try:
            student = Students.objects.get(student_id = request.user)
        except Exception as e:
            student = None
        try:
            teacher = Teachers.objects.get(teacher_id = request.user)
        except Exception as e:
            teacher = None
        is_student = 0
        if teacher is None:
            is_student = 1
                            
        return render(request,'base/home.html',{'mappings':mappings,'teachers_all':teachers_all,'is_student':is_student}) 