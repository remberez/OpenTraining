from django.urls import path, include
from .views import users
from rest_framework import routers

router = routers.DefaultRouter()
router.register('users', users.UserRegistration, basename='users')
urlpatterns = [
]

urlpatterns += router.urls
