from django.contrib import admin
from .models import *

admin.site.register(
    [
        Restaurant,
        Coupon,
        Award,
        CouponTransaction,
        OwnerRestaurant,
        AwardsCount,
        Transactions,
    ]
)