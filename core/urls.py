from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.login_view, name='login_view'),
    url(r'^logout/$', views.logout_view, name='logout_view'),
    url(r'^create_capsule/$', views.create_capsule_view, name='create_capsule_view'),
    url(r'^capsules/$', views.display_capsules_view, name='display_capsules_view'),
    url(r'^classify/$', views.display_classify_view, name='display_classify_view'),

]
