from django.urls import path, include
from .views import users
from rest_framework import routers

router = routers.DefaultRouter()
router.register('users', users.UserView, basename='users')
router.register('teachers', users.TeacherView, basename='teachers')
urlpatterns = [

]

urlpatterns += router.urls
