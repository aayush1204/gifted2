from django.shortcuts import render

# Create your views here.

# from base.models import Appointment


def appointment_book(request):

    if request.method == "POST":
        time = request.POST['timing']
        date = request.POST['date']
        doctor = request.POST['doctor']

        name = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        
        # Appointment.objects.create()
        print(time)
        print(date)
        print(doctor)
        
        # Appointment.objects.create(student_id = student, teacher_id = teacher)
    return render(request,'student_book_appointment.html')
