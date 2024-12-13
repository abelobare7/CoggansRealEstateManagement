from django.shortcuts import redirect
from django.contrib import messages

def is_landlord(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.user_type == 'landlord':
                return view_func(request, *args, **kwargs)
            elif request.user.user_type == 'tenant':
                messages.error(request, 'You do not have permission to access this page.', extra_tags='danger')
                return redirect('home')
            elif request.user.is_superuser:
                messages.error(request,"Login as admin to access this page", extra_tags='danger')
                return redirect('admin')
        else:
            messages.error(request, 'Please login to access this page.', extra_tags='danger')
            return redirect('home')
    return wrapper
