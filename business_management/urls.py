from django.contrib import admin
from django.urls import path, include
from .views import *

app_name = 'business_management'

urlpatterns = [
     path('admin/', admin.site.urls),
    path('auth/register', RegisterUser.as_view()),
    path('auth/login', LoginView.as_view()),
    path('auth/user-information/<slug:query_type>', UserInformation.as_view()),
    path('auth/change-password', ChangePasswordView.as_view()),
    path('auth/update-user', UpdateUserView.as_view()),
    path('api/', include('restraurant_activities_management.urls'))
]