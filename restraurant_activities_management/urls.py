from django.urls import path
from .views import *

app_name = 'restraurant_activities_management'

urlpatterns = [
    path('/api/restaurant', RestaurantView.as_view()),
    path('/api/coupon', CouponView.as_view()),
    path('/api/awards', AwardView.as_view()),
    path('/api/owner-restaurant', OwnerRestaurantView.as_view()),
    path('/api/use_points', CouponTransactionView.as_view()),
]