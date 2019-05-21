from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
# create things for your pages (function/classes written in Python)

def home_view(request, *args, **kwargs):
    #https://www.geeksforgeeks.org/args-kwargs-python/
    #args: pass a variable number of arguments
    #kwargs??

    print(request.user)
    #return HttpResponse('<h1>Hello World</h1>') #string of html code

    return render(request, 'home.html', {}) #html template
    
def contact_view(request, *args, **kwargs):
    return HttpResponse('<h1>Contact Page</h1>')

def social_view():
    pass
def about_view():
    pass

#Django templates