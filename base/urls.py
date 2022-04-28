from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from .views import home,auth,classs,assignments,submissions, payment

urlpatterns = [
    path('',home.landing_page,name='landing_page'),
    path('gifted/about_us/', home.about_us, name='about_us'),
    path('gifted/contact_us/', home.contact_us, name='contact_us'),
    path('gifted/courses/', home.courses, name='courses'),
    path('gifted/prices/', home.gifted_prices, name='prices'),
    path('gifted/videos/', home.gifted_videos, name='videos'),
    path('gifted/books/', home.gifted_books, name='books'),
    path('gifted/feedback_form/', home.feedback_form, name='feedback_form'),
    path('login/',auth.login_view,name='login'),
    path('register/',auth.register_view,name='register'),
    path('logout/', auth.logout_view,name='logout'),
    path('home/',home.home,name='home'),
    # path('videos/', classs.videos, name='videos'),
    path('payment/paymenthandler/', payment.paymenthandler, name='paymenthandler'),
    path('gifted/contact_us/paymenthandler/', payment.paymentcontactinitiate, name='paymenthandler_contactus'),
    path('gifted/contact_us/paymenthandler/paymenthandler2/', payment.paymentredirect, name='payment_redirect'),
    path('payment/', payment.homepage, name='paymenthome'),
    path('freetrial/', payment.freetrial, name='freetrial'),
    path('class/<int:id>',classs.render_class,name='render_class'),
    path('class/<int:id>/delete_assignment/<int:assignment_id>',submissions.delete_submission,name='del_sub'),
    path('create_assignment/<int:classroom_id>',assignments.create_assignment,name='create_assignment'),
    path('create_announcement/<int:classroom_id>',assignments.create_announcement,name='create_announcement'),
    path('videos_upload/<int:classroom_id>',assignments.create_video,name='create_video'),
    path('assignment_summary/<int:assignment_id>',assignments.assignment_summary,name='assignment_summary'),
    path('delete_assignment/<int:assignment_id>',assignments.delete_assignment,name='delete_assignment'),
    path('unenroll_class/<int:classroom_id>',classs.unenroll_class,name='unenroll_class'),
    path('delete_class/<int:classroom_id>',classs.delete_class,name='delete_class'),
    path('create_class_request/',classs.create_class_request,name='create_class_request'),
    path('join_class_request/',classs.join_class_request,name='join_class_request'),
    path('submit_assignment_request/<int:assignment_id>',submissions.submit_assignment_request,name='submit_assignment_request'),
    path('mark_submission_request/<int:submission_id>/<int:teacher_id>',submissions.mark_submission_request,name='mark_submission_request')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)