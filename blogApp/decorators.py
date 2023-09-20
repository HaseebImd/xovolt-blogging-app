from functools import wraps
from django.shortcuts import redirect

def api_login_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Check if "user_id" is in the session
        if "user_id" in request.session:
            # User is logged in, proceed with the view
            return view_func(request, *args, **kwargs)
        else:
            # User is not logged in, redirect to the login page
            return redirect("login")  # Adjust the URL name as needed

    return _wrapped_view
