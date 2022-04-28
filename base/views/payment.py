from django.shortcuts import render
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect
from django.urls import reverse
from ..models import Students,Teachers
from datetime import timedelta
from datetime import datetime
from ..models import Students,Teachers, CustomUser, Videos , Appointment
# authorize razorpay client with API Keys.
razorpay_client = razorpay.Client(
	auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))


def homepage(request):
    currency = 'INR'
    amount = 20000 # Rs. 200

    # Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                    currency=currency,
                                                    payment_capture='0'))

    # order id of newly created order.
    razorpay_order_id = razorpay_order['id']
    callback_url = 'paymenthandler/'

    # we need to pass these details to frontend.
    context = {}
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
    context['razorpay_amount'] = amount
    context['currency'] = currency
    context['callback_url'] = callback_url
    context['finished_free_trial'] = 0
    if request.user.finished_free_trial == True:
        context['finished_free_trial'] = 1   
    print(request.user.finished_free_trial)
    return render(request, 'base/paymentindex.html', context=context)


# we need to csrf_exempt this url as
# POST request will be made by Razorpay
# and it won't have the csrf token.
@csrf_exempt
def paymenthandler(request):

	# only accept POST request.
    if request.method == "POST":
        try:
            print("inside")
            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }

            # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(
                params_dict)
            if result is not None:
                print("inside result")
                amount = 20000 # Rs. 200
                try:

                    # capture the payemt
                    razorpay_client.payment.capture(payment_id, amount)
                    # render success page on successful caputre of payment
                    # return render(request, 'base/paymentsuccess.html')
                    student = Students.objects.filter(student_id = request.user).first()
                    
                    request.user.is_subscribed = True
                    request.user.save()
                    print(request.user.is_subscribed)
                    print(student.student_id.is_subscribed)
                    return redirect(reverse('home'))
                except Exception as e:
                    print(e)
                    # if there is an error while capturing payment
                    return render(request, 'base/paymentfail.html')
            else:
                print("signature")
                # if signature verification fails.
                return render(request, 'base/paymentfail.html')
        except:
            print("http bad")
            # if we don't find the required parameters in POST data
            return HttpResponseBadRequest()
    else:
        print("otohe")
    # if other than POST request is made.
        return HttpResponseBadRequest()

def freetrial(request):
    student = Students.objects.filter(student_id = request.user).first()
                    
    request.user.is_free_trial = True
    request.user.expiry_free_trial = datetime.now() + timedelta(days= 7)
    request.user.save()

    print(request.user.is_subscribed)
    return redirect(reverse('home'))

@csrf_exempt
def paymenthandler_contactus(request):


	# only accept POST request.
    if request.method == "POST":
        try:
            print('inside handler')
            print("inside")
            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }

            # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(
                params_dict)
            if result is not None:
                print("inside result")
                amount = 20000 # Rs. 200
                try:

                    # capture the payemt
                    razorpay_client.payment.capture(payment_id, amount)
                    # render success page on successful caputre of payment
                    # return render(request, 'base/paymentsuccess.html')
                    
                    print(time2)
                    print(ls[1])
                    print('Contact us successful')
                    print(asasa)
                    return redirect(reverse('home'))
                except Exception as e:
                    print(e)
                    # if there is an error while capturing payment
                    return render(request, 'base/paymentfail.html')
            else:
                print("signature")
                # if signature verification fails.
                return render(request, 'base/paymentfail.html')
        except:
            print("http bad")
            # if we don't find the required parameters in POST data
            return HttpResponseBadRequest()
    else:
        print("otohe")
    # if other than POST request is made.
        return HttpResponseBadRequest()
@csrf_exempt
def paymentcontactinitiate(request):

    currency = 'INR'
    amount = 20000 # Rs. 200

    # Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                    currency=currency,
                                                    payment_capture='0'))

    # order id of newly created order.
    razorpay_order_id = razorpay_order['id']
    callback_url = 'paymenthandler2/'
    print('insie initiate')
    # we need to pass these details to frontend.
    context = {}
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
    context['razorpay_amount'] = amount
    context['currency'] = currency
    context['callback_url'] = callback_url
    return render(request, 'base/gifted/paymentcontactinitiate.html', context=context)    
@csrf_exempt
def paymentredirect(request):
    print(Appointment.objects.all())
    return redirect(reverse('landing_page'))