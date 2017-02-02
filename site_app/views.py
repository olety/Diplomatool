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
    """
    View class responsible for displaying review list. Presents the Topic model.
    """

    template_name = "student/topic_list.html"
    model = models.Topic
    context_object_name = 'topic_list'

    def get_queryset(self):
        """
        Gets the queryset of a Topic model presented by this view

        :return: List of available topics
        :rtype: QuerySet
        """

        return models.Topic.objects.filter(available=True)

    def get_context_data(self, **kwargs):
        """
        Gets context data of the topic list view to pass to the template.

        :param kwargs: Keyword arguments
        :return: The context of the topic list view
        :rtype: MultipleObjectMixin
        """

        context = super(TopicListView, self).get_context_data()
        context['form'] = forms.StudentTopicProposalForm()
        return context

    def post(self, request):
        """
        Handler the post request of sending the propose topic form

        :param request: (HttpRequest) The request performed by user
        :return: The response containing content of the topic list page
        :rtype TemplateResponse

        """
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
    """
    View class responsible for displaying review list. Presents the Review model. Only reviewers and administrators will be able to access this
    view.
    """

    template_name = "reviewer/review_list.html"
    model = models.Review
    context_object_name = 'review_list'
    did_send = False
    object_list = None

    def get_queryset(self):
        """
        Gets the queryset of a Review model presented by this view

        :return: List of reviews made by current user
        :rtype: QuerySet
        """

        return models.Review.objects.filter(author=self.request.user)

    def get_context_data(self, **kwargs):
        """
        Gets context data of the review list view to pass to the template.

        :param kwargs: Keyword arguments
        :return: The context of the review list view
        :rtype: MultipleObjectMixin
        """

        context = super().get_context_data(**kwargs)
        context['form'] = forms.ReviewUploadForm
        return context

    def post(self, request):
        """
        Handles the post request of sending the review file form

        :param request: (HttpRequest) The request performed by user
        :return: The response containing content of the review list page
        :rtype TemplateResponse

        """

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
