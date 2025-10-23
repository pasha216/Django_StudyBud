from django.urls import path
from . import views

urlpatterns = [
    # AUTH
    path("login/", views.login_page, name="login-page"),
    path("logout/", views.logout_page, name="logout-page"),
    path("register/", views.register_page, name="register-page"),

    # Pages
    path("", views.home, name="home"),
    path("room/<str:pk>", views.room, name="room"),
    path("profile/<str:pk>", views.profile, name="profile"),
    path("topics", views.topics, name="topics"),

    # Actions
    path("create-room/", views.create_room, name="create-room"),
    path("room/<str:pk>/update", views.update_room, name="update-room"),
    path("room/<str:pk>/delete", views.delete_room, name="delete-room"),
    path("profile/<str:pk>/update", views.update_profile, name="update-user"),
    path("profile/<str:pk>/update-password", views.update_password, name="update-password"),
    path("message/<str:pk>/delete", views.delete_message, name="delete-message"),
]
