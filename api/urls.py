from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token, refresh_jwt_token

from api import views
from .views import *

app_name = 'api'


urlpatterns = [
    path('organization/<int:pk>'
         '/<int:year>/<int:month>/<int:day>'
         '/<str:sikdan_time>/', CafeteriaListView.as_view()),
    path('cafeteria/<int:pk>'
         '/<int:year>/<int:month>/<int:day>'
         '/<str:sikdan_time>/', CafeteriaDetailView.as_view()),
    path('review/create/', ReviewCreateView.as_view()),
    path('dish/<int:pk>/', DishDetailView.as_view()),
    path('user/update/<int:pk>/', UserUpdateView.as_view()),
    path('user/<int:pk>/', UserDetailView.as_view()),

    #jwt and social login
    path('api-jwt-auth/', obtain_jwt_token),
    path('api-jwt-auth/refresh/', refresh_jwt_token),
    path('api-jwt-auth/verify/', verify_jwt_token),

    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),

    path('rest-auth/kakao/', KakaoLogin.as_view(), name='kakao_login'),
    path('rest-auth/facebook/', FacebookLogin.as_view(), name='facebook_login'),
]


