from django.contrib.auth.views import login, logout
from django.conf.urls.defaults import *
from views import *

urlpatterns = patterns('',
    url(r'logout/$', logout, name="logout"),
    url(r'login/$', login, {}, name='login'),
    url(r'register/$', register, name="register"),
    url(r'activate/$', activate, name="activate"),
)