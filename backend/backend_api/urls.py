from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register(r'users', views.UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # Explicit URL patterns for other endpoints
    path('books/', views.BookListCreate.as_view(), name='book-list'),
    path('books/<int:pk>/', views.BookRetrieveUpdateDestroy.as_view(), name='book-detail'),
]
