from django.http import HttpResponse
from django.shortcuts import redirect

# Simple decorator to ensure the user is authenticated. If they are they should not
# be able to access the login or register pages this is used on.
def authenticatedUser(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('accounts:home')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func

# Simple decorator to ensure the user has the permissions to view a page.
def allowedUsers(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):

            denied = False

            for roles in allowed_roles:
                if request.user.groups.filter(name = roles).exists():
                    return view_func(request, *args, **kwargs)
                else:
                    denied = True
           
            if denied == True:
                return redirect('accounts:home')

        return wrapper_func
    return decorator
