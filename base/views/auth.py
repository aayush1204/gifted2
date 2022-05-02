from django.shortcuts import render, redirect
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required

from ..decorators import login_excluded
from ..forms import UserAuthenticationForm,UserRegisterationForm
from ..models import Students,Teachers, Classrooms, CustomUser
from itertools import chain

from ..utils import generate_class_code

@login_excluded('home')
def register_view(request):
    if request.method=="POST":
        form=UserRegisterationForm(request.POST,request.FILES)
        if form.is_valid():
            user=form.save()
            user_name=form.cleaned_data.get('username')
            classrooms = Classrooms.objects.all()
            existing_codes=[]
            for classroom in classrooms:
                existing_codes.append(classroom.class_code)
            class1 = Classrooms.objects.create(classroom_name="EVS - "+user_name,section="2nd year", class_code=generate_class_code(6,existing_codes))
            class1.save()
            class2 = Classrooms.objects.create(classroom_name="Maths - "+user_name,section="2nd year", class_code=generate_class_code(6,existing_codes))
            class1.save()
            class3 = Classrooms.objects.create(classroom_name="Physics - "+user_name,section="2nd year", class_code=generate_class_code(6,existing_codes))
            class1.save()
            # user1 = CustomUser.objects.get(username="varija")
            user1 = CustomUser.objects.filter(username="varija").first()
            user2 = CustomUser.objects.filter(username="teacher1").first()
            user3 = CustomUser.objects.filter(username="teacher10").first()
            Teachers.objects.create(teacher_id=user1, classroom_id=class1)
            Teachers.objects.create(teacher_id=user2, classroom_id=class2)
            Teachers.objects.create(teacher_id=user3, classroom_id=class3)
            Students.objects.create(student_id=user, classroom_id=class1)
            Students.objects.create(student_id=user, classroom_id=class2)
            Students.objects.create(student_id=user, classroom_id=class3)
            login(request,user)
            return redirect('paymenthome')
        else:
            return render(request,'base/register.html',{'form':form})
    form=UserRegisterationForm()
    return render(request,'base/register.html',{'form':form})

@login_excluded('home')  
def login_view(request):
    if request.method=="POST":
        form=UserAuthenticationForm(request=request,data=request.POST)
        print(form)
        print(form.is_valid())
        if form.is_valid():
            user_name=form.cleaned_data.get('username')
            password=form.cleaned_data.get('password')
            print(user_name)
            print(password)
            user=authenticate(username=user_name,password=password)
            print(user)
            if user!=None:
                login(request,user)
                try :
                    student = Students.objects.get(student_id = request.user)
                    subscribed = student.student_id.is_subscribed
                    freetrial = student.student_id.is_free_trial
                    
                    
                except Exception as e:
                    print(e)
                    subscribed = True
                    freetrial = False

                print(freetrial)
                print(subscribed)   
                if ((not subscribed) and (not freetrial)):
                    print("yes")
                    return redirect('paymenthome')
                else:    
                    return redirect('home')
        else:
            return render(request,'base/login.html',{'form':form})
    form=UserAuthenticationForm() 
    return render(request,'base/login.html',{'form':form}) 

@login_required(login_url='login')
def logout_view(request):
    logout(request)
    return redirect('login')