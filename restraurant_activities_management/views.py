from rest_framework.response import Response
from .models import *
from .serializer import *
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated



class RestaurantView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request):
        data = request.data
        serialized = RestaurantPostSerializer(data=data)
        if serialized.is_valid():
            serialized.save()
            restaurant_added = Restaurant.objects.get(reg_no=serialized['reg_no'].value)
            all_users = User.objects.all()
            for user in all_users:
                user_rt_serialized = OwnerRestaurantPostSerializer(data={
                    "user": user.id,
                    "restaurant": restaurant_added.id,
                })
                if user_rt_serialized.is_valid():
                    user_rt_serialized.save()
            return Response({"save": True})
        return Response({"save": False, "error": serialized.errors})

    @staticmethod
    def get(request):
        querytype = request.GET.get("querytype")
        if querytype == "all":
            queryset = Restaurant.objects.all()
            serialized = RestaurantGetSerializer(instance=queryset, many=True)
            return Response(serialized.data)
        elif querytype == "single":
            userId = request.GET.get("userId")
            queryset = Restaurant.objects.filter(user=userId)
            serialized = RestaurantGetSerializer(instance=queryset, many=True)
            return Response(serialized.data)
        else:
            return Response({"message": "Specify the querying type"})


class CouponView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated] 

    @staticmethod
    def post(request):
        data = request.data
        serialized = CouponPostSerializer(data=data)
        if serialized.is_valid():
            serialized.save()
            return Response({"save": True})
        return Response({"save": False, "error": serialized.errors})

    @staticmethod
    def get(request):
        querytype = request.GET.get("querytype")
        if querytype == "all":
            queryset = Coupon.objects.all()
            serialized = CouponGetSerializer(instance=queryset, many=True)
            return Response(serialized.data)
        if querytype == "single":
            couponId = request.GET.get("coupon")
            queryset = Coupon.objects.get(id=couponId)
            serialized = CouponGetSerializer(instance=queryset)
            return Response(serialized.data)
        else:
            return Response({"message": "Specify the querying type"})


class AwardView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request):
        data = request.data
        reward_threshold = int(data.get("threshold"))
        reward_ratio = 0.5
        reward_value = int(data.get("reward_value"))
        numbers_of_points = (reward_threshold * reward_ratio) / reward_value
        award_data = {
            "restaurant": data.get("restaurant"),
            "pic": data.get("pic"),
            "product": data.get("product"),
            "points": int(numbers_of_points)
        }
        serialized = AwardPostSerializer(data=award_data)
        if serialized.is_valid():
            serialized.save()
            return Response({"save": True})
        return Response({"save": False, "error": serialized.errors})

    @staticmethod
    def get(request):
        restaurantId = request.GET.get("restaurantId")
        queryset = Award.objects.filter(restaurant=restaurantId)
        serialized = AwardGetSerializer(instance=queryset, many=True)
        return Response(serialized.data)


class CouponTransactionView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request):
        data = request.data
        print(data)
        points_used = int(data.get("point_used"))
        trans_data = {
            "user": data.get("user"),
            "award": data.get("award"),
            "point_used": points_used
        }
        print(data.get("restaurant_id"))
        serialized = CouponTransactionPostSerializer(data=trans_data)
        user_restaurant = OwnerRestaurant.objects.get(user=data.get("user"), restaurant=data.get("restaurant_id"))
        user = User.objects.get(id=data.get("user"))
        user.total_points_made -= points_used
        user_restaurant.total_points -= points_used
        user_restaurant.save()
        user.save()
        if serialized.is_valid():
            serialized.save()
            return Response({"save": True})
        return Response({"save": False, "error": serialized.errors})

    @staticmethod
    def get(request):
        userId = request.GET.get("userId")
        queryset = CouponTransaction.objects.filter(user=userId)
        serialized = CouponTransactionGetSerializer(instance=queryset, many=True)
        return Response(serialized.data)


class OwnerRestaurantView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request):
        data = request.data
        user_id = data.get('user')
        restaurant_id = data.get('restaurant')
        total_points = data.get('total_points')
        try:
            user_restaurant = OwnerRestaurant.objects.get(user=user_id, restaurant=restaurant_id)
            transactioned = TransactionPostSerializer(data={
                "user": user_id,
                "coupon": data.get('coupon'),
                "points_made": total_points
            })
            if transactioned.is_valid():
                transactioned.save()
            print(user_restaurant)
            user_restaurant.total_points += total_points
            user_restaurant.total_lifetime_points += total_points
            user = User.objects.get(id=user_id)
            user.total_points_made += total_points
            user.total_lifetime_points += total_points
            user.save()
            user_restaurant.save()
        except OwnerRestaurant.DoesNotExist:
            serialized = OwnerRestaurantPostSerializer(data=data)
            if serialized.is_valid():
                serialized.save()
                return Response({"save": True})

        return Response({"save": True, "msg": "The Points added to the user"})

    @staticmethod
    def get(request):
        userId = request.GET.get("userId")
        queryset = OwnerRestaurant.objects.filter(user=userId)
        serialized = OwnerRestaurantGetSerializer(instance=queryset, many=True)
        return Response(serialized.data)
