from django.urls import path
from image_api import views

urlpatterns = [
    path('', views.ImageList.as_view(), name='image-list'),
    path('<int:pk>/', views.ImageDetail.as_view(), name='image-detail'),
    path('<int:pk>/original/', views.ImageOriginal.as_view(), name='image-original'),
    path('<int:pk>/thumbnail/<int:height>', views.image_thumbnail, name='image-thumbnail'),
    path('<int:pk>/<str:expiring_link>', views.image_detail_expiring, name='image-detail-expiring')
]