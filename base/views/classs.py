from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from ..utils import generate_class_code
from ..decorators import access_class,teacher_required,student_required
from ..models import Classrooms, Teachers, Students, Assignments, Announcements, Submissions

from itertools import chain

@login_required(login_url='login')
@student_required('home')
def unenroll_class(request,classroom_id):
    classroom = Classrooms.objects.get(pk=classroom_id)
    student_mapping = Students.objects.filter(student_id=request.user,classroom_id=classroom).delete()
    return redirect('home')

@login_required(login_url='login')
@teacher_required('home')
def delete_class(request,classroom_id):
    classroom = Classrooms.objects.get(pk=classroom_id)
    teacher_mapping = Teachers.objects.get(teacher_id=request.user,classroom_id=classroom)
    teacher_mapping.delete()
    classroom.delete()
    return redirect('home')

@login_required(login_url='login')
@access_class('home')
def render_class(request,id):
    print(id)
    print('abs')
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
        print(e)
        student = None
    print("student - ")

    print(student)
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


@login_required(login_url='login')
def create_class_request(request):
    if request.POST.get('action') == 'post':
        classrooms = Classrooms.objects.all()
        existing_codes=[]
        for classroom in classrooms:
            existing_codes.append(classroom.class_code)
        
        class_name = request.POST.get('class_name')
        section = request.POST.get('section')

        class_code = generate_class_code(6,existing_codes)
        classroom = Classrooms(classroom_name=class_name,section=section,class_code=class_code)
        classroom.save()
        teacher = Teachers(teacher_id=request.user,classroom_id=classroom)
        teacher.save()
        return JsonResponse({'status':'SUCCESS'})

@login_required(login_url='login')
def join_class_request(request):
    if request.POST.get('action') == 'post':
        code = request.POST.get('class_code')
        try:
            classroom = Classrooms.objects.get(class_code=code)
            student = Students.objects.filter(student_id = request.user, classroom_id = classroom)
            if (student.count()!=0):
                return redirect('home')
        except Exception as e:
            print(e)
            return JsonResponse({'status':'FAIL','message':str(e)})
        student = Students(student_id = request.user, classroom_id = classroom)
        student.save()
        return JsonResponse({'status':'SUCCESS'})

@login_required(login_url='login')
def videos(request):
    return render(request, 'base/videos.html')