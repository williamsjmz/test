from django.urls import path

from . import views
import geco

urlpatterns = [
    path("", views.geco_index, name="geco_index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
]