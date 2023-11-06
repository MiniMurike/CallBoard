from django.urls import path, include
from .views import Signup, send_emails


urlpatterns = [
    path('signup/', Signup.as_view(), name='signup'),
    path('send_emails/', send_emails, name='send_emails'),
]
