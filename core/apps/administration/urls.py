from apps.administration import views
from django.urls import path

app_name = "apps.administration"

urlpatterns = [
    path("", views.DashboardView.as_view(), name="index"),
    path("privacy-policy", views.PrivacyPolicyView.as_view(), name="privacy-policy"),
    path("about", views.AboutView.as_view(), name="about"),
    path("contact", views.ContactView.as_view(), name="contact"),
    path('users', views.UserListView.as_view(), name='user-list'),
    path('users/create', views.UserCreateView.as_view(), name='user-create'),
    path('users/<int:pk>/delete', views.UserDeleteView.as_view(), name='user-delete'),
    path('auth/login', views.LoginView.as_view(), name='auth-login'),
    path("auth/logout", views.LogoutView.as_view(), name="auth-logout"),
    path("auth/password-change", views.PasswordChangeView.as_view(),
         name="auth-password-change"),
    path('auth/profile', views.ProfileView.as_view(), name='auth-profile'),
]
