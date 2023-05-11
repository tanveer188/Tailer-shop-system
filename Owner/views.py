from django.shortcuts import render,redirect,get_object_or_404,HttpResponse
from django.forms.models import model_to_dict
from django.contrib import messages
from django.db.models import Q
from Customer.models import Measurement,Customers
from Owner.models import Work
from Owner.foams import WorkFoam,CustomerFoam,MeasurementFoam
from authentication.decorators import group_required
from django.contrib.auth.decorators import permission_required
import decimal,json

#decimal to sendsable json converter
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return str(o)
        return super(DecimalEncoder, self).default(o)

#homepage
@group_required("Owner_grp","Worker_grp",redirect_url='home')
def homepage(request):
  user = request.user
  username = request.user.username
  if user.has_perm("Owner.view_work"):
    works = Work.objects.filter(completed=False)
    # customer = work.customer.user.username
    # is_complited = work.is_complited
    # date = work.date
    context = {
      "works":works
    }
    return render(request,"Owner/index.html",context)
  return HttpResponse("Error")
#insert data into works
@group_required("Owner_grp",redirect_url='home')
def newbill(request):
  if request.method == "POST":
    submitedfoam = WorkFoam(request.POST)
    if submitedfoam.is_valid():
      submitedfoam.save()
      messages.success(request, "New Bill Added")
      return redirect("home")
    else:
      workfoam = submitedfoam
  else:
    workfoam = WorkFoam()
  context = {
    "workfoam":workfoam,
  }
  return render(request,"Owner/newbill.html",context)
#create a new customer
@group_required("Owner_grp",redirect_url='home')
def newcustomer(request):
  if request.method == "POST":
    submitedfoam =CustomerFoam(request.POST)
    if submitedfoam.is_valid():
      customer = submitedfoam.save()
      return redirect("newmeasurment/"+str(customer.id))
    else:
      customerfoam = submitedfoam
  else:
    customerfoam = CustomerFoam()
  context = {
    "customerfoam":customerfoam,
  }
  return render(request,"Owner/newcustomer.html",context)
#add measurment if it already not exist for customer
@group_required("Owner_grp",redirect_url='home')
def newmeasurment(request,pk):
  if pk:
    customer = get_object_or_404(Customers, pk=pk)
    try: 
      Measurement.objects.get(customers = customer)
      messages.warning(request,"Measurement is alredey taken of the customer : "+ customer.name)
      return redirect("home")
    except:
      if request.method == "POST":
        submitedfoam = MeasurementFoam(request.POST)
        if submitedfoam.is_valid():
          measurement = submitedfoam.save(commit=False)
          measurement.customers = customer
          measurement.save()
          messages.success(request, "Customer Added successfully")
          return redirect("home")
        else:
          measurementfoam = submitedfoam
      else:
        measurementfoam = MeasurementFoam()
      context = {
        "measurementfoam":measurementfoam,
      }
      return render(request,"Owner/newmeasurment.html",context)
  else:
    messages.warning(request,"Wrong Request")
    return redirect("home")
#if work is complete and all individual task are completed then owner can give it to customer
@group_required("Owner_grp",redirect_url='home')
def delivered(request):
  if request.method == "POST":
    id = request.POST.get("work")
    try:
      work = Work.objects.get(~(Q(astar__exact="Need") | Q(piku__exact="Need")),id=id,completed=True,delivered=False)
    except:
      messages.warning(request,f"Something Went Wrong!")
      return redirect("delivered")
    work.delivered = True
    work.save()
    messages.success(request,f"Successfully Delivered ")
  works = Work.objects.filter( ~Q(astar__exact="Need"), ~Q(piku__exact="Need"),completed= True,delivered=False)
  context = {
    "works":works,
    }
  return render(request,"Owner/delivered.html",context)
#editing updating views 
@group_required("Owner_grp",redirect_url='home')
def Edit(request,model_name,pk):
  if model_name == "Measurement":
    if request.method == "POST":
      instance = get_object_or_404(Measurement,pk=pk)
      foam = MeasurementFoam(request.POST or None, instance=instance)
      foam.save()
      messages.success(request,"updated Successfully")
      return redirect("/customerinfo/"+pk)
    instance = get_object_or_404(Measurement,pk=pk)
    foam = MeasurementFoam(instance=instance)
    context = {
      "foam":foam,
    }
  elif model_name == "Customers":
    if request.method == "POST":
      instance = get_object_or_404(Customers,pk=pk)
      foam = CustomerFoam(request.POST or None, instance=instance)
      foam.save()
      messages.success(request,"updated Successfully")
      return redirect("/customerinfo/"+pk)
    instance = get_object_or_404(Customers,pk=pk)
    foam = CustomerFoam(instance=instance)
    context = {
      "foam":foam,
    }
  elif model_name == "Work":
    if request.method == "POST":
      instance = get_object_or_404(Work,pk=pk)
      foam = WorkFoam(request.POST or None, instance=instance)
      foam.save()
      messages.success(request,"updated Successfully")
      return redirect("home")
    instance = get_object_or_404(Work,pk=pk)
    foam = WorkFoam(instance=instance)
    context = {
      "foam":foam,
    }
  return render(request,"foam.html",context)