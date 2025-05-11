from rest_framework import viewsets, status, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils import timezone
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from .models import Book, BorrowTransaction
from .serializers import (
    BookSerializer, 
    BorrowTransactionSerializer, 
    BorrowBookSerializer,
    ReturnBookSerializer,
    UserSerializer
)
from django.contrib.auth.models import User

# Keep DefaultRouter for Users only
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.filter(is_superuser=False)
    serializer_class = UserSerializer
    # Remove authentication requirement
    permission_classes = []

# Replace ViewSet with explicit class-based views for Books
class BookListCreate(ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = []
