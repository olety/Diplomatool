from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login, logout
from . import views

urlpatterns = [
    url(r'^$', views.ProfileView.as_view(), name='profile'),
    url(r'^reviews', views.ReviewsView.as_view(), name='reviews'),
    url(r'^topic_list', views.TopicListView.as_view(), name='topic_list'),
    url(r'^login', login, {'template_name': 'login.html'}, name='login'),
    url(r'^logout', logout, name='logout'),
]
