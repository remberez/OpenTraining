from rest_framework.routers import DefaultRouter
from .views import games, applications, coaching

router = DefaultRouter()
router.register('games', games.GameView, basename='game')
router.register('game-genres', games.GameGenreView, basename='game-genre')
router.register('coaching-applications', applications.ApplicationView, basename='coaching-applications')
router.register('application-statuses', applications.StatusView, basename='statuses')
router.register('application-management', applications.ApplicationManagementView, basename='application-management')
router.register('coaching', coaching.CoachingView, basename='coaching')
router.register('user-coaching', coaching.UserCoachingView, basename='user-coaching')

urlpatterns = [
]

urlpatterns += router.urls
