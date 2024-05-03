from django.http import HttpResponseRedirect
from django.urls import reverse


def check_post_method(view_func):
    def wrapper(request, *args, **kwargs):
        
        if request.method == 'POST':
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse("index"))
        
    return wrapper
    
