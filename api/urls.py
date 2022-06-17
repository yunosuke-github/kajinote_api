from rest_framework import routers
from .views.user_view import UserView
from .views.house_view import HouseView


router = routers.DefaultRouter()

router.register('users', UserView)
router.register('houses', HouseView)
