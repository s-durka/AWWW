from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('upload_file', views.upload_file, name='upload_file'),
    path('delete_file', views.delete_file, name='delete_file'),
    path('delete_directory', views.delete_directory, name='delete_directory'),
    path('upload_directory', views.upload_folder, name='upload_directory')
]