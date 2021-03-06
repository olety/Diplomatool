from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login, logout
from . import views, forms

urlpatterns = [
    url(r'^$', views.ProfileView.as_view(), name='profile'),
    url(r'^reviews', views.ReviewListView.as_view(), name='reviews'),
    url(r'^topic_list', views.TopicListView.as_view(), name='topic_list'),
    url(r'^login', login, {'authentication_form': forms.LoginForm, 'template_name': 'login.html'}, name='login'),
    url(r'^logout', logout, name='logout'),
]
