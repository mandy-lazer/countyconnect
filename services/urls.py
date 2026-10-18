from django.urls import path

from . import views

app_name = 'services'

urlpatterns = [
    path('submit/',                   views.submit_request,  name='submit'),
    path('mine/',                     views.my_requests,     name='my_requests'),
    path('track/',                    views.track,           name='track'),
    path('manage/',                   views.manage_requests, name='manage'),
    path('r/<str:reference>/',        views.detail,          name='detail'),
    path('r/<str:reference>/status/', views.update_status,   name='update_status'),
]
