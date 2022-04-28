from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from ..decorators import teacher_required
from ..models import Teachers, Students, Assignments, Submissions, Videos
from ..forms import *     
from .. import email

from itertools import chain

@login_required(login_url='login')
@teacher_required('home')
def create_assignment(request,classroom_id):
    teacher_mapping = Teachers.objects.filter(teacher_id=request.user).select_related('classroom_id')
    student_mapping = Students.objects.filter(student_id=request.user).select_related('classroom_id')
    mappings = chain(teacher_mapping,student_mapping)

    if request.method == 'POST':
        form = CreateAssignmentForm(request.POST, request.FILES)
        print(1)
        print(form)
        if form.is_valid():
            print(2)
            assignment_name = form.cleaned_data.get('assignment_name')
            due_date = form.cleaned_data.get('due_date')
            due_time = form.cleaned_data.get('due_time')
            classroom_id = Classrooms.objects.get(pk=classroom_id)
            instructions = form.cleaned_data.get('instructions')
            total_marks = form.cleaned_data.get('total_marks')
            instruction_file = request.FILES['instruction_file']
            assignment = Assignments(assignment_name = assignment_name,due_date = due_date,instruction_file = instruction_file, due_time=due_time,instructions = instructions,total_marks = total_marks,classroom_id=classroom_id)
            assignment.save()
            email.assignment_post_mail(classroom_id,assignment.id)
            return redirect('render_class',id=classroom_id.id)
        else:
            print(3)
            return render(request,'base/create_assignment.html',{'form':form,'mappings':mappings})
    form = CreateAssignmentForm()
    return render(request,'base/create_assignment.html',{'form':form,'mappings':mappings})


@login_required(login_url='login')
@teacher_required('home')
def assignment_summary(request,assignment_id):
    assignment = Assignments.objects.filter(pk = assignment_id).first()
    submissions = Submissions.objects.filter(assignment_id = assignment_id)
    teachers = Teachers.objects.filter(classroom_id = assignment.classroom_id)
    teacher_mapping = Teachers.objects.filter(teacher_id=request.user).select_related('classroom_id')
    student_mapping = Students.objects.filter(student_id=request.user).select_related('classroom_id')
    no_of_students = Students.objects.filter(classroom_id=assignment.classroom_id)
    mappings = chain(teacher_mapping,student_mapping)
    return render(request,'base/assignment_summary.html',{'assignment':assignment,'submissions':submissions,'mappings':mappings,'no_of_students':no_of_students})

@login_required(login_url='login')
@teacher_required('home')
def delete_assignment(request,assignment_id):
    try:
        assignment = Assignments.objects.get(pk=assignment_id)
        classroom_id = assignment.classroom_id.id 
        Assignments.objects.get(pk=assignment_id).delete()
        return redirect('render_class', id=classroom_id)
    except Exception(e):
        return redirect('home')
        
@login_required(login_url='login')
@teacher_required('home')
def create_announcement(request,classroom_id):
    teacher_mapping = Teachers.objects.filter(teacher_id=request.user).select_related('classroom_id')
    student_mapping = Students.objects.filter(student_id=request.user).select_related('classroom_id')
    mappings = chain(teacher_mapping,student_mapping)

    if request.method == 'POST':
        form = CreateAnnouncementForm(request.POST, request.FILES)
        print(1)
        print(form)
        if form.is_valid():
            print(2)
            
            posted_date = form.cleaned_data.get('posted_date')
            
            classroom_id = Classrooms.objects.get(pk=classroom_id)
            instructions = form.cleaned_data.get('instructions')
            
            instruction_file = request.FILES['instruction_file']
            announcement = Announcements(posted_date = posted_date,instruction_file = instruction_file, instructions = instructions,classroom_id=classroom_id)
            announcement.save()
            # email.assignment_post_mail(classroom_id,assignment.id)
            return redirect('render_class',id=classroom_id.id)
        else:
            print(3)
            return render(request,'base/create_announcement.html',{'form':form,'mappings':mappings})
    form = CreateAnnouncementForm()
    return render(request,'base/create_announcement.html',{'form':form,'mappings':mappings})


@login_required(login_url='login')
@teacher_required('home')
def create_video(request,classroom_id):
    teacher_mapping = Teachers.objects.filter(teacher_id=request.user).select_related('classroom_id')
    student_mapping = Students.objects.filter(student_id=request.user).select_related('classroom_id')
    mappings = chain(teacher_mapping,student_mapping)

    if request.method == 'POST':
        form = VideosUploadForm(request.POST, request.FILES)
        print(1)
        print(form)
        if form.is_valid():
            print(2)
            
            # posted_date = form.cleaned_data.get('posted_date')
            
            classroom_id = Classrooms.objects.get(pk=classroom_id)
            description = form.cleaned_data.get('description')
            video_name = form.cleaned_data.get('video_name')
            video = request.FILES['video']
            video_obj = Videos(video = video, description = description,classroom_id=classroom_id, video_name= video_name)
            video_obj.save()
            # email.assignment_post_mail(classroom_id,assignment.id)
            return redirect('render_class',id=classroom_id.id)
        else:
            print(3)
            return render(request,'base/videos_upload.html',{'form':form,'mappings':mappings})
    form = VideosUploadForm()
    return render(request,'base/videos_upload.html',{'form':form,'mappings':mappings})