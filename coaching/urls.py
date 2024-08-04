from rest_framework.routers import DefaultRouter
from .views import games

router = DefaultRouter()
router.register('games', games.GameView, basename='game')

urlpatterns = [

]
urlpatterns += router.urls
