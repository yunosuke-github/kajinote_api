from rest_framework import routers
from .views.user_view import UserView


router = routers.DefaultRouter()

# user_view = UserView()
# user_view.request = None
# user_view.basename = router.get_default_basename(UserView)
# user_view.reverse_action(user_view.get.url_name, args=[])


router.register('users', UserView)
