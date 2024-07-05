from rest_framework.routers import DefaultRouter
from .views import UserViewSet,TaskViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet,basename='user')
router.register(r'tasks', TaskViewSet,basename='task')