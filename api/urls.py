from rest_framework import routers
from .views.login_view import LoginView
from .views.user_view import UserView
from .views.house_view import HouseView
from .views.housework_view import HouseworkView
from .views.housework_history_view import HouseworkHistoryView
from .views.house_user_view import HouseUserView


router = routers.DefaultRouter()

router.register('login', LoginView)
router.register('users', UserView)
router.register('houses', HouseView)
router.register('houseworks', HouseworkView)
router.register('housework_histories', HouseworkHistoryView)
router.register('house_users', HouseUserView)
