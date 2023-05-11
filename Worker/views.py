from django.shortcuts import render,redirect,get_object_or_404,HttpResponse
from django.contrib import messages
from django.db.models import Q
from Owner.models import Work
from Customer.models import Measurement,Customers
from authentication.decorators import group_required
from watson import search as watson
# Create your views here.
@group_required("Worker_grp",redirect_url='home')
def worker(request):
  username = request.user.username
  return HttpResponse(username)

@group_required("Worker_grp","Owner_grp",redirect_url='home')
def allComplited(request):
  works = Work.objects.filter(completed=True,delivered=False)
  return render(request,"worktable.html",{"works":works})
@group_required("Worker_grp","Owner_grp",redirect_url='home')
def customerinfo(request,pk):
  add_measurement = False
  customer = get_object_or_404(Customers, pk=pk)
  try:
    measurement = Measurement.objects.get(customers=customer)
  except:
    measurement = None
    add_measurement = True
  works = Work.objects.filter(customer=customer)
  context = {
    "customer":customer,
    "measurement":measurement,
    "works":works,
    "add_measurement":add_measurement
  }
  return render(request,"customerinfo.html",context)
@group_required("Worker_grp","Owner_grp",redirect_url='home')
def billinfo(request,pk):
  work = get_object_or_404(Work,pk=pk)
  customer = work.customer
  measurement = get_object_or_404(Measurement,customers=customer)
  context = {
    "work":work,
    "customer":customer,
    "measurement":measurement,
  }
  return render(request,"workinfo.html",context)
@group_required("Worker_grp","Owner_grp",redirect_url='home')
def work(request,fieldname):
    # Check if the specified field name is a valid field on the Work model
    valid_fields = [f.name for f in Work._meta.get_fields()]
    if fieldname not in valid_fields:
      messages.warning(request,f"{fieldname} is not a valid field on the Work model.")
      return redirect("home")

    # Filter the Work objects based on the specified field
    filter_kwargs = {f"{fieldname}": "Need", "completed": False}
    works = Work.objects.filter(**filter_kwargs)

    # Render the filtered works in a template or return them as a JSON response
    context = {
    "fieldname":fieldname,
    "works":works,
    }
    return render(request,"workstatus.html",context)
@group_required("Worker_grp","Owner_grp",redirect_url='home')
def workstatus(request, fieldname,pk):
    # Check if the specified field name is a valid field on the Work model
    valid_fields = [f.name for f in Work._meta.get_fields()]
    if fieldname not in valid_fields:
      messages.warning(request,f"{fieldname} is not a valid field on the Work model.")
      return redirect("home")

    # Filter the Work objects based on the specified field
    filter_kwargs = {f"{fieldname}": "Need", "completed": False,'id':pk}
    works = Work.objects.get(**filter_kwargs)
    setattr(works,fieldname,"Fulfilled")
    works.save()
    # Render the filtered works in a template or return them as a JSON response
    messages.success(request,f"Successfully Updated ")
    return redirect(f"/work/{fieldname}")

@group_required("Worker_grp","Owner_grp",redirect_url='home')
def completed(request):
  if request.method == "POST":
    id = request.POST.get("work")
    try:
      work = Work.objects.get(~(Q(astar__exact="Need") | Q(piku__exact="Need")),id=id)
    except:
      messages.warning(request,f"Something Went Wrong!")
      return redirect("completed")
    work.completed = True
    work.save()
    messages.success(request,f"Successfully completed ")
  works = Work.objects.filter( ~Q(astar__exact="Need"), ~Q(piku__exact="Need"),completed= False)
  context = {
    "works":works,
    }
  return render(request,"completed.html",context)

@group_required("Worker_grp","Owner_grp",redirect_url='home')
def search(request):
  if request.method == "GET":
    try:
      option = int(request.GET.get("option"))
    except:
      option=0
    query = request.GET.get("query")
    if query is None:
      messages.warning(request,"Something Went Wrong")
      return redirect("home")
    if option==0:
      customers = watson.filter(Customers,query).distinct()[:3]
      bill = watson.filter(Work,query).distinct()[:1]
      context = {
        "query":query,
        "option":option,
        "customers":customers,
        "works":bill,
        "more":True
      }
    elif option==1:
      customers = watson.filter(Customers,query).distinct()
      context = {
        "query":query,
        "option":option,
        "customers":customers,
        "more":False
      }
    elif option==2:
      print("enter")
      bill = watson.filter(Work,query)
      print("searched")
      context = {
        "query":query,
        "option":option,
        "works":bill,
        "more":False
      }
  else:
    messages.warning("Something Went Wrong")
    return redirect("home")
  return render(request,"search.html",context)