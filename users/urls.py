from django.urls import path, include
from .views import users
from rest_framework import routers

router = routers.SimpleRouter()
router.register('users', users.UserViewSet, basename='users')
router.register('account-management', users.ChangePasswordViewSet, basename='account')

urlpatterns = router.urls
