from django.shortcuts import render,HttpResponse,redirect
from .decorators import group_required
# Create your views here.
# @group_required("Worker_grp",redirect_url='g')
def home(request):
  if request.user.groups.filter(name__in=("Owner_grp",)).exists():
    return redirect("homepage")
  elif request.user.groups.filter(name__in=("Worker_grp",)).exists():
    return redirect("homepage")
  else:
    return redirect('customer')
@group_required("Owner_grp",redirect_url='home')
def g(request):
  return HttpResponse("Hlo ownet ")