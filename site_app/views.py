from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from django.views.generic import TemplateView
from functools import wraps
from . import models
from . import forms


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
@method_decorator(check_group('Student'), name='dispatch')
class TopicListView(ListView):
    template_name = "student/topic_list.html"
    model = models.Topic
    context_object_name = 'topic_list'

    def get_queryset(self):
        return models.Topic.objects.filter(available=True)

    def get_context_data(self, **kwargs):
        context = super(TopicListView, self).get_context_data()
        context['supervisors'] = models.User.objects.filter(groups__name='Supervisor')
        return context

    def post(self, request):
        print(request.POST)
        print(request)

        self.object_list = self.get_queryset()
        context = self.get_context_data()
        return self.render_to_response(context)


@method_decorator(login_required, name='dispatch')
@method_decorator(check_group('Reviewer'), name='dispatch')
class ReviewListView(ListView):
    template_name = "reviewer/review_list.html"
    model = models.Review
    context_object_name = 'review_list'
    show_completed = True

    def get_queryset(self):
        if self.show_completed:
            return models.Review.objects.filter(author=self.request.user)
        else:
            return models.Review.objects.filter(author=self.request.user, finished=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['show_completed'] = self.show_completed
        return context

    def post(self, request):
        self.show_completed = True if request.POST['show_completed'] == 'True' else False
        self.object_list = self.get_queryset()
        allow_empty = self.get_allow_empty()
        if not allow_empty:
            if self.get_paginate_by(self.object_list) is not None and hasattr(self.object_list, 'exists'):
                is_empty = not self.object_list.exists()
            else:
                is_empty = len(self.object_list) == 0
            if is_empty:
                raise Http404('Empty list and \'%(class_name)s.allow_empty\' is False.' % {
                    'class_name': self.__class__.__name__,
                })
        context = self.get_context_data()
        return self.render_to_response(context)
