from rest_framework import routers
from .views.user_view import UserView
from .views.house_view import HouseView
from .views.housework_view import HouseworkView
from .views.house_user_view import HouseUserView


router = routers.DefaultRouter()

router.register('users', UserView)
router.register('houses', HouseView)
router.register('houseworks', HouseworkView)
router.register('house_users', HouseUserView)
