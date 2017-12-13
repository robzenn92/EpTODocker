from . import views
from django.urls import path

urlpatterns = [

    # ---------------------
    # Debug routes
    # The below routes are for debug use only.

    path('hello', views.get_hello, name='index'),
    path('env', views.get_env, name='env'),

    # ---------------------
    # Production routes
    # The below routes are for production use.

    path('receive-ball', views.receive_ball, name='receive-ball')
]
