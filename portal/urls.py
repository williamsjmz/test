from django.urls import path

from . import views

urlpatterns = [
    path("<str:portal_url>/", views.portal_index, name="portal_index"),
    path("portal_show_page/<str:portal_url>/<int:page_id>/", views.portal_show_page, name="portal_show_page")
]   