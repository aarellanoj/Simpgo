from functools import wraps

from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.shortcuts import redirect

from django.utils.decorators import available_attrs


def worker_member_required(view_func):
    @wraps(view_func, assigned=available_attrs(view_func))
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated and not request.user.is_active:
            return redirect('user_login')
        if not request.user.profile.is_worker():
            raise PermissionDenied()
        return view_func(request, *args, **kwargs)

    return _wrapped_view

def superviser_member_required(view_func):
    @wraps(view_func, assigned=available_attrs(view_func))
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated and not request.user.is_active:
            return redirect('user_login')
        if not request.user.profile.is_superviser():
            raise PermissionDenied()
        return view_func(request, *args, **kwargs)

    return _wrapped_view