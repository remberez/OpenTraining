from rest_framework.routers import DefaultRouter
from .views import games, applications

router = DefaultRouter()
router.register('games', games.GameView, basename='game')
router.register('game-genres', games.GameGenreView, basename='game-genre')
router.register('coaching-applications', applications.ApplicationView, basename='coaching-applications')

urlpatterns = [

]

urlpatterns += router.urls
