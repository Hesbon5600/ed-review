from django.urls import path

from . import views

app_name = 'course'
urlpatterns = [
    path('courses/', views.ListCreateCourse.as_view(), name='course_list'),
    path('courses/<int:pk>/', views.RetrieveUpdateDestroyCourse.as_view(),
         name='course_detail'),
    path('courses/<int:course_pk>/reviews', views.ListCreateReview.as_view(),
         name='review_list'),
    path('courses/<int:course_pk>/reviews/<int:pk>',
         views.RetrieveUpdateDestroyReview.as_view(), name='review_detail'),
]
