from django.shortcuts import render,redirect,get_object_or_404,HttpResponse
from django.forms.models import model_to_dict
from django.contrib.auth.models import User,Group
from django.contrib import messages
from django.db.models import Q
from Customer.models import Measurement,Customers
from Owner.models import Work,Member,Types
from Owner.foams import WorkFoam,CustomerFoam,MeasurementFoam,OrganizationFoam,TypeFoam
from authentication.decorators import group_required
from django.contrib.auth.decorators import permission_required
import decimal,json
import convertapi
import os
from django.conf import settings

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
  organization = request.user.member.organization
  username = request.user.username
  if user.has_perm("Owner.view_work"):
    works = Work.objects.filter(completed=False,organization=organization)
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
    organization = request.user.member.organization

    if request.method == "POST":
        submitedfoam = WorkFoam(organization=organization, data=request.POST)

        if submitedfoam.is_valid():
            instance = submitedfoam.save(commit=False)
            #customer_id = submitedfoam.cleaned_data.get('customer').id  # Retrieve the selected customer ID
            #customer = Customers.objects.get(id=customer_id)  # Fetch the corresponding Customer object
            #instance.customer=customer
            instance.organization = organization
            instance.save()

            messages.success(request, "New Bill Added")
            return redirect("home")
        else:
            workfoam = submitedfoam
    else:
        workfoam = WorkFoam(organization=organization)

    context = {
        "workfoam": workfoam,
    }
    return render(request, "Owner/newbill.html", context)

#create a new customer
@group_required("Owner_grp",redirect_url='home')
def newcustomer(request):
  organization = request.user.member.organization
  if request.method == "POST":
    submitedfoam =CustomerFoam(request.POST)
    if submitedfoam.is_valid():
      customer = submitedfoam.save(commit=False)
      customer.organization = organization
      customer.save()
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
  organization = request.user.member.organization
  if request.method == "POST":
    id = request.POST.get("work")
    try:
      work = Work.objects.get(~(Q(astar__exact="Need") | Q(piku__exact="Need")),id=id,completed=True,delivered=False,organization=organization)
    except:
      messages.warning(request,f"Something Went Wrong!")
      return redirect("delivered")
    if work.organization == organization:
      work.delivered = True
      work.save()
      messages.success(request,f"Successfully Delivered ")
    else:
      messages.warning(request,f"Something Went Wrong!")
      return redirect("delivered")
  works = Work.objects.filter( ~Q(astar__exact="Need"), ~Q(piku__exact="Need"),completed= True,delivered=False,organization=organization)
  context = {
    "works":works,
    }
  return render(request,"Owner/delivered.html",context)
#editing updating views 
@group_required("Owner_grp",redirect_url='home')
def Edit(request,model_name,pk):
  organization = request.user.member.organization
  if model_name == "Measurement":
    if request.method == "POST":
      instance = get_object_or_404(Measurement,pk=pk)
      foam = MeasurementFoam(request.POST or None, instance=instance)
      if foam.is_valid():
        measurement = foam.save()
        messages.success(request,"updated Successfully")
        return redirect("/customerinfo/"+str(measurement.customers.id))
      else:
        context= {"foam":foam}
        return render(request,"foam.html",context)
    instance = get_object_or_404(Measurement,pk=pk)
    foam = MeasurementFoam(instance=instance)
    context = {
      "foam":foam,
    }
  elif model_name == "Customers":
    if request.method == "POST":
      instance = get_object_or_404(Customers,pk=pk,organization=organization)
      foam = CustomerFoam(request.POST or None, instance=instance)
      if foam.is_valid():
        foam.save()
        messages.success(request,"updated Successfully")
        return redirect("/customerinfo/"+pk)
      else:
        context= {"foam":foam}
        return render(request,"foam.html",context)
    instance = get_object_or_404(Customers,pk=pk,organization=organization)
    foam = CustomerFoam(instance=instance)
    context = {
      "foam":foam,
    }
  elif model_name == "Work":
    if request.method == "POST":
      instance = get_object_or_404(Work,pk=pk,organization=organization)
      foam = WorkFoam(data=request.POST or None, instance=instance,organization=organization)
      if foam.is_valid():
        foam.save()
        messages.success(request,"updated Successfully")
        return redirect("home")
      else:
        context= {"foam":foam}
        return render(request,"foam.html",context)
    instance = get_object_or_404(Work,pk=pk,organization=organization)
    foam = WorkFoam(instance=instance,organization=organization)
    context = {
      "foam":foam,
    }
  elif model_name=="organization":
    if request.method == "POST":
      foam = OrganizationFoam(request.POST,instance=organization)
      if foam.is_valid():
        foam.save()
        messages.success(request,"updated Successfully")
        return redirect("home")
      else:
        context= {"foam":foam}
        return render(request,"foam.html",context)
    foam = OrganizationFoam(instance=organization)
    context = {
      "foam":foam,
    }
  elif model_name=="Types":
    type = Types.objects.get(id=pk,organization=organization)
    if request.method == "POST":
      foam = TypeFoam(request.POST,instance=type)
      if foam.is_valid():
        foam.save()
        messages.success(request,"updated Successfully")
        return redirect("typepage")
      else:
        context= {"foam":foam}
        return render(request,"foam.html",context)
    foam = TypeFoam(instance=type)
    context = {
      "foam":foam,
    }
  return render(request,"foam.html",context)
@group_required("Owner_grp",redirect_url='home')
def newmember(request):
  if request.method == "POST":
    organization = request.user.member.organization
    delete = request.POST.get("delete")
    user_id = request.POST.get("user_id")
    role = bool(int(request.POST.get("role")))
    #deleting the member
    print(type(delete))
    if delete is not None:
      user = User.objects.get(id=user_id)
      member = Member.objects.get(user=user)
      member.delete()
      user.is_staff=False
      if role:
        group = Group.objects.get(name="Owner_grp")
      else:
        group = Group.objects.get(name="Worker_grp")
      user.groups.remove(group)
      user.save()
      messages.success(request,"Successfully Removed")
    else:
      user = User.objects.get(id=user_id,groups__isnull=True)
      if role:
        group = Group.objects.get(name="Owner_grp")
        member = Member.objects.create(user=user,organization=organization,is_owner=True)
      else:
        group = Group.objects.get(name="Worker_grp")
        member = Member.objects.create(user=user,organization=organization,is_owner=False)
      user.is_staff=True
      user.groups.add(group)
      user.save()
      messages.success(request,"Successfully Added")
    return redirect("organization")
  users = User.objects.filter(groups__isnull=True)
  context = {
    "users":users
  }
  return render(request,"Owner/newmember.html",context)
  
@group_required("Owner_grp",redirect_url='home')
def delete(request,model_name):
  if request.method=="POST":
    organization = request.user.member.organization
    if model_name=="Work":
      work_id = request.POST.get("work_id")
      work = get_object_or_404(Work,pk=work_id,organization=organization)
      work.delete()
    if model_name=="Types":
      type_id = request.POST.get("type_id")
      type = get_object_or_404(Types,pk=type_id,organization=organization)
      type.delete()
      return redirect("typepage")

def bill_maker(request,pk):
  organization = request.user.member.organization
  work = Work.objects.get(id=pk,organization=organization)
  customer = work.customer
  context = {
    "organization":organization,
    "customer":customer,
    "work":work,
  }
  response = str(render(request,"Owner/bill_template.html",context).content.decode('utf-8'))
  upload_folder = os.path.join(settings.MEDIA_ROOT, 'upload')
  os.makedirs(upload_folder, exist_ok=True)
  uploaded_file_path = os.path.join(upload_folder, f'index{work.id}.html')

  with open(uploaded_file_path, 'w') as file:
          file.write(response)

  convertapi.api_secret = '7bBdd7b66JI1xvI8'
  result = convertapi.convert('pdf', {'File': uploaded_file_path})
  converted_folder = os.path.join(settings.MEDIA_ROOT, 'converted')

  os.makedirs(converted_folder, exist_ok=True)
  converted_file_name = f'abc{work.id}.pdf'
  converted_file_path = os.path.join(converted_folder, converted_file_name)
  result.file.save(converted_file_path)
  work.bill_pdf = "converted/"+converted_file_name
  work.save()
  context = {
    "work":work
  }
  return render(request,"Customer/bill.html",context)
@group_required("Owner_grp",redirect_url='home')
def typepage(request):
  organization = request.user.member.organization
  types = Types.objects.filter(organization=organization)
  context = {
    "types":types
  }
  return render(request,"types.html",context)
@group_required("Owner_grp",redirect_url='home')
def newtype(request):
    organization = request.user.member.organization

    if request.method == "POST":
        submitedfoam = TypeFoam(data=request.POST)

        if submitedfoam.is_valid():
            instance = submitedfoam.save(commit=False)
            instance.organization = organization
            instance.save()

            messages.success(request, "New Type Added")
            return redirect("typepage")
        else:
            foam = submitedfoam
    else:
        foam = TypeFoam()

    context = {
        "foam": foam,
    }
    return render(request, "foam.html", context)