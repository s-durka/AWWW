from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # path('upload_file', views.upload_file, name='upload_file'),
    # path('delete_file', views.delete_file, name='delete_file'),
    # path('delete_directory', views.delete_directory, name='delete_directory'),
    # path('upload_directory', views.upload_folder, name='upload_directory'),

    path('ajax/upload_file', views.upload_file, name = 'upload_file'),
    path('ajax/upload_folder', views.upload_folder, name='upload_folder'),
    path('ajax/delete_folder', views.delete_folder, name='delete_folder'),
    path('ajax/delete_file', views.delete_file, name='delete_file'),
    path('ajax/run_frama', views.run_frama_ajax, name='run_frama_ajax'),
    path('ajax/render_forms', views.render_all_forms, name='render_all_forms'),
    path('ajax/open_file', views.open_file_ajax, name='open_file_ajax'),

    path('render_file_form', views.render_file_form, name='render_file_form'),
    path('render_folder_form', views.render_folder_form, name='render_folder_form'),
    path('render_delete_file_form', views.render_delete_file_form, name='render_delete_file_form'),
    path('render_delete_folder_form', views.render_delete_folder_form, name='render_delete_folder_form')
]