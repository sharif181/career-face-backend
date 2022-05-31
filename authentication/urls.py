from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from authentication.views import RegisterView, ProfileView

urlpatterns = [
    path('token/', jwt_views.TokenObtainPairView.as_view(), name='token_create'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='register_view'),
    path('profile/', ProfileView.as_view(), name='profile_view')
]
