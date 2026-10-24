from django.urls import path
from apps.api.api import v1

app_name = 'api'

urlpatterns = [
    path('v1/', v1.urls)
]