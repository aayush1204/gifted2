from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from ..decorators import student_required
from ..models import Assignments, Students, Submissions
from ..forms import *     
from .. import email

from datetime import datetime

from django.http import HttpResponse
from itertools import chain

@csrf_exempt
@login_required(login_url='login')
@student_required('home')
def submit_assignment_request(request,assignment_id):
    assignment = Assignments.objects.get(pk=assignment_id)
    student_id = Students.objects.get(classroom_id=assignment.classroom_id,student_id=request.user.id)
    file_name = request.FILES.get('myfile')
    try:
        submission = Submissions.objects.get(assignment_id=assignment, student_id = student_id)
        submission.submission_file = file_name
        submission.save()
        return JsonResponse({'status':'SUCCESS'})

    except Exception as e:  
        print(str(e))  
        submission = Submissions(assignment_id = assignment,student_id= student_id,submission_file = file_name)
        dt1=datetime.now()
        dt2=datetime.combine(assignment.due_date,assignment.due_time)
        time = timesince(dt1, dt2)
        if time[0]=='0':
            submission.submitted_on_time=False
        submission.save()
        email.submission_done_mail(assignment_id,request.user,file_name)
        return JsonResponse({'status':'SUCCESS'})

def mark_submission_request(request,submission_id,teacher_id):
    if request.method == "POST":
        marks = request.POST['submission_marks']
        assignment_id = request.POST['assignmentid']
        submission_id2 = request.POST['submissionid'] 
        print(assignment_id)
        print(marks)
        print('marks submision')
        print(submission_id2)
        print(submission_id)
        submission = Submissions.objects.get(pk=submission_id2)
        submission.marks_alloted = marks
        submission.save()
        print("teacher id")
        teacher = Teachers.objects.filter(teacher_id=request.user).first()
        print(teacher.teacher_id)
        # print(teacher.teacher_id.teacher_id)
        print(teacher.teacher_id.username)
        teacher_name = teacher.teacher_id.username
        email.submission_marks_mail(submission_id,teacher_name,marks)
        # return JsonResponse({'status':'SUCCESS'})

        # zoom email
        from django_zoom_meetings import ZoomMeetings
        # Creat a JWT app your account https://marketplace.zoom.us/ and use
        # the api_key, secret_key and your zoom email address to create a ZoomMeetings instance
        api_key='g4Jwbl4RQf6m4mlPVa7r7g'
        secret_key='JZZF8Ce3KXH1KvEocDVlsE08GgP0XJfvh1wR'
        zoom_email='aayush.halgekar@gmail.com'
        my_zoom = ZoomMeetings(api_key,secret_key,zoom_email)
        str_topic="test meetig"
        timenow = datetime.now()
        date= datetime(2021,7,5,13,30)

        str_meeting_duration='30'
        str_meeting_password='12345'
        # required parameters are date,topic,duration and the password of the meeting. In return you will get all the meeting details including the join url
        create_meeting = my_zoom.CreateMeeting(date,str_topic,str_meeting_duration,str_meeting_password) 
        print(create_meeting)
        print(create_meeting['id'])
        print(create_meeting['start_url'])
        print(create_meeting['join_url'])
        print(create_meeting['password'])
        # return render HttpResponse('<h1>Dniee</h1>')
        # assignment_id = 1
        assignment = Assignments.objects.filter(pk = assignment_id).first()
        submissions = Submissions.objects.filter(assignment_id = assignment_id)
        teachers = Teachers.objects.filter(classroom_id = assignment.classroom_id)
        teacher_mapping = Teachers.objects.filter(teacher_id=request.user).select_related('classroom_id')
        student_mapping = Students.objects.filter(student_id=request.user).select_related('classroom_id')
        no_of_students = Students.objects.filter(classroom_id=assignment.classroom_id)
        mappings = chain(teacher_mapping,student_mapping)
        return render(request,'base/assignment_summary.html',{'assignment':assignment,'submissions':submissions,'mappings':mappings,'no_of_students':no_of_students})


def delete_submission(request,id,assignment_id):
    if request.method == "POST":
        student = Students.objects.filter(student_id=request.user)
        print(assignment_id)
        print(id)
        print(student)
        for i in student:
            try:
                Submissions.objects.get(student_id=i, assignment_id = assignment_id).delete()
            except Exception as e:
                continue
        print('inside delete')
       
        
        classroom = Classrooms.objects.get(pk=id)
        try: 
            assignments = Assignments.objects.filter(classroom_id = id)
        except Exception as e:
            assignments = None

        try:
            students = Students.objects.filter(classroom_id = id)
        except Exception as e:
            students = None
        
        try:
            announcements = Announcements.objects.filter(classroom_id = id)
        except Exception as e:
            announcements = None

        try :
            student = Students.objects.filter(student_id=request.user)
        except Exception as e:
            student = None


        if student.exists():
            try:
                submissions = Submissions.objects.filter(student_id=request.user)
            except Exception as e:
                submissions = None

            turned_in = []

            is_student = 1
            print(student)
            print("assngment-")
            flag = 0
            print(assignments)
            for i in assignments:
                # try:
                print(i.id)
                print('123')
                print(i)
                print(student)
                for j in student:
                    print(j)
                    submission = Submissions.objects.filter(student_id=j, assignment_id = i)
                    print(submission)
                    # except Exception as e:
                    #     submission = None
                    
                    if (submission.exists()):
                        turned_in.append((i, '1'))
                        flag = 1
                    else:
                        # turned_in.append((i, '0'))   
                        continue
                
                if flag == 0:
                    turned_in.append((i, '0')) 
                flag = 0


            print(turned_in)         
            print("aaaaa")    
            teachers = Teachers.objects.filter(classroom_id = id)
            teacher_mapping = Teachers.objects.filter(teacher_id=request.user).select_related('classroom_id')
            student_mapping = Students.objects.filter(student_id=request.user).select_related('classroom_id')
            mappings = chain(teacher_mapping,student_mapping) 
            return render(request,'base/class_page.html',{'announcements':announcements,'classroom':classroom,'assignments':turned_in ,'students':students,'teachers':teachers,"mappings":mappings,"is_student":is_student})

        else:
            teachers = Teachers.objects.filter(classroom_id = id)
            teacher_mapping = Teachers.objects.filter(teacher_id=request.user).select_related('classroom_id')
            student_mapping = Students.objects.filter(student_id=request.user).select_related('classroom_id')
            mappings = chain(teacher_mapping,student_mapping) 
            is_student = 0
            return render(request,'base/class_page.html',{'announcements':announcements,'classroom':classroom,'assignments':assignments ,'students':students,'teachers':teachers,"mappings":mappings,"is_student":is_student})

        # if student is not None:
        #     try:
        #         submissions = Submissions.objects.filter(student_id=request.user)
        #     except Exception as e:
        #         submissions = None

        #     turned_in = []

        #     is_student = 1
        #     # print(student)
        #     for i in assignments:
        #         # try:
        #         # print(i.id)
        #         # print('123')
        #         # print(i)
        #         # print(student)
        #         submission = Submissions.objects.filter(student_id=student, assignment_id = i)
        #         # print(submission)
        #         # except Exception as e:
        #         #     submission = None
                
        #         if (submission.exists()):
        #             turned_in.append((i, '1'))
        #         else:
        #             turned_in.append((i, '0'))   

        #     # print(turned_in)             
        #     teachers = Teachers.objects.filter(classroom_id = id)
        #     teacher_mapping = Teachers.objects.filter(teacher_id=request.user).select_related('classroom_id')
        #     student_mapping = Students.objects.filter(student_id=request.user).select_related('classroom_id')
        #     mappings = chain(teacher_mapping,student_mapping) 
        #     return render(request,'base/class_page.html',{'announcements':announcements,'classroom':classroom,'assignments':turned_in ,'students':students,'teachers':teachers,"mappings":mappings,"is_student":is_student})

        # else:
        #     teachers = Teachers.objects.filter(classroom_id = id)
        #     teacher_mapping = Teachers.objects.filter(teacher_id=request.user).select_related('classroom_id')
        #     student_mapping = Students.objects.filter(student_id=request.user).select_related('classroom_id')
        #     mappings = chain(teacher_mapping,student_mapping) 
        #     is_student = 0
        #     return render(request,'base/class_page.html',{'announcements':announcements,'classroom':classroom,'assignments':assignments ,'students':students,'teachers':teachers,"mappings":mappings,"is_student":is_student})
