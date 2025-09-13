from django.shortcuts import render
from .data import RESUME
def resume_view(request):
    return render(request, 'resume.html', {"resume": RESUME})
# created a view for the resume page to render 
