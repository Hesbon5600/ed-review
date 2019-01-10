from rest_framework import routers
from django.urls import path, include

from . import views
app_name = 'course'

router = routers.SimpleRouter()
router.register('courses', views.CourseViewset)
router.register('reviews', views.ReviewViewset)

urlpatterns = [
    path('users/', views.UserRetrieveUpdateAPIView.as_view()),
    path('auth/signup', views.SignupAPIView.as_view()),
    path('auth/login', views.LoginAPIView.as_view()),
    path('', include(router.urls)),
]
