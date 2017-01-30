from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from functools import wraps


def check_group(group_name):
    def _check_group(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if request.user.groups.filter(name=group_name).exists() or request.user.is_admin:
                return view_func(request, *args, **kwargs)
            return redirect('/')
        return wrapper
    return _check_group


@method_decorator(login_required, name='dispatch')
class ProfileView(TemplateView):
    template_name = "profile.html"


@method_decorator(login_required, name='dispatch')
@method_decorator(check_group('Reviewer'), name='dispatch')
class ReviewsView(TemplateView):
    template_name = "reviewer/review_list.html"

