from django.urls import path

from . import views

urlpatterns = [
    path("", views.portales_index, name="portales_index"),
    path("new_page/", views.new_page, name="new_page"),
    path("show_page/<int:page_id>/", views.show_page, name="show_page"),
    path("edit_page/<int:page_id>/", views.edit_page, name="edit_page"),
    path("delete_page/<int:page_id>/", views.delete_page, name="delete_page"),
    path("edit_design/", views.edit_design, name="edit_design"),

    # API Routes
    path('upload_changes/', views.upload_changes, name="upload_changes"),
]   