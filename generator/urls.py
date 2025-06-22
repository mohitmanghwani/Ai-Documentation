from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/upload-project/', views.upload_project, name='upload_project'),
    path('api/generate-from-path/', views.generate_from_path, name='generate_from_path'),
    path('api/download/<str:request_id>/', views.download_files, name='download_files'),
    path('api/status/<str:request_id>/', views.get_status, name='get_status'),
] 