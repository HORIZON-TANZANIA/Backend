from django.urls import path
from .views import *

app_name = 'restraurant_activities_management'

urlpatterns = [
    path('restaurant/', RestaurantView.as_view()),
    path('coupon/', CouponView.as_view()),
    path('awards/', AwardView.as_view()),
    path('owner-restaurant/', OwnerRestaurantView.as_view()),
    path('transactions/', CouponTransactionView.as_view())
]