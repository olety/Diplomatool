from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from django.views.generic import TemplateView
from functools import wraps
from site_app.forms import ReviewUploadForm
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
        context['form'] = forms.StudentTopicProposalForm()
        return context

    def post(self, request):
        topic = models.Topic()
        topic.name = request.POST.get('name')
        topic.short_description = request.POST.get('description')
        supervisor_id = request.POST.get('supervisor')
        supervisor = models.User.objects.get(pk=supervisor_id)
        topic.supervisor = supervisor
        current_user = request.user
        topic.student = current_user
        topic.level = current_user.degree
        topic.save()

        self.object_list = self.get_queryset()
        context = self.get_context_data()
        return self.render_to_response(context)


@method_decorator(login_required, name='dispatch')
@method_decorator(check_group('Reviewer'), name='dispatch')
class ReviewListView(ListView):
    template_name = "reviewer/review_list.html"
    model = models.Review
    context_object_name = 'review_list'
    did_send = False
    object_list = None

    def get_queryset(self):
        return models.Review.objects.filter(author=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = forms.ReviewUploadForm
        return context

    def post(self, request):
        form = ReviewUploadForm(request.POST, request.FILES)
        if form.is_valid():
            review = models.Review.objects.get(id=request.POST.get('review_hidden_id'))
            review.file = form.cleaned_data.get('review_file')
            review.finished_date = timezone.now()
            review.save()

        print(review)
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        context['sent_review'] = True
        return self.render_to_response(context)
