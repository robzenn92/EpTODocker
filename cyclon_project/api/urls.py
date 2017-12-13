from . import views
from django.urls import path

urlpatterns = [

    # ---------------------
    # Debug routes
    # The below routes are for debug use only.

    path('hello', views.get_hello, name='index'),
    path('who-am-i', views.get_who_am_i, name='who-am-i'),
    path('env', views.get_env, name='env'),
    path('view', views.get_view, name='view'),

    # ---------------------
    # Production routes
    # The below routes are for production use.

    path('k-view', views.get_k_view, name='k-view'),
    path('exchange-view', views.exchange_view, name='exchange-view')
]
