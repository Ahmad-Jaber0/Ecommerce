from django.urls import path
from . import views

urlpatterns = [
    path('<int:pk>/reviews/', views.create_or_update_review, name='create_review'),
    path('<int:pk>/reviews/delete/', views.delete_review, name='delete_review'),
]
