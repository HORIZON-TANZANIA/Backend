from django.urls import path
from .views import *

app_name = 'business_management'

urlpatterns = [
    path('api/register', RegisterUser.as_view()),
    path('api/login', LoginView.as_view()),
    path('api/user-information/<slug:query_type>', UserInformation.as_view()),
    path('api/change-password', ChangePasswordView.as_view()),
    path('api/update-user', UpdateUserView.as_view()),
]