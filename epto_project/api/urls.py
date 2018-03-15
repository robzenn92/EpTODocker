from . import views
from django.urls import path, include

urlpatterns = [

    path('v1/', include([
        # ---------------------
        # Debug routes
        # The below routes are for debug use only.

        path('hello', views.get_hello, name='index'),
        path('env', views.get_env, name='env'),
        path('ball', views.get_ball, name='ball'),

        # ---------------------
        # Production routes
        # The below routes are for production use.

        path('send-ball', views.receive_ball, name='send-ball'),
        path('broadcast', views.broadcast_event, name='broadcast')
    ])),
]
