from django.shortcuts import render,HttpResponse
from authentication.decorators import group_required
from .models import Customers,Measurement
from Owner.models import Work
# Create your views here.
def customer(request):
  if request.method == "POST":
    mobileno = request.POST.get("mobileno")
    billno = request.POST.get("billno")
    # try:
    customer = Customers.objects.get(mobileno=mobileno)
    work = Work.objects.filter(customer=customer.id,billno=billno)
    measurement = Measurement.objects.get(customers=customer)
    # except:
    #   return HttpResponse("wrong ")
    context = {
      "customer":customer,
      "works":work,
      "measurement":measurement,
    }
    return render(request,"customerinfo.html",context)
  return render(request,"Customer/customerlogin.html")