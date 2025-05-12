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

class BookRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = []
    
    def update(self, request, *args, **kwargs):
        book = self.get_object()
        # Check if there are any active borrow records
        if BorrowTransaction.objects.filter(book=book, status='borrowed').exists():
            return Response(
                {"error": "Cannot update book with active borrow records. All copies must be returned first."},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        book = self.get_object()
        # Check if there are any active borrow records
        if BorrowTransaction.objects.filter(book=book, status='borrowed').exists():
            return Response(
                {"error": "Cannot delete book with active borrow records"},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().destroy(request, *args, **kwargs)
    
# Replace ViewSet with class-based view for Transactions
class TransactionList(APIView):
    permission_classes = []
    
    def get(self, request):
        transactions = BorrowTransaction.objects.all().order_by('-borrow_date')
        serializer = BorrowTransactionSerializer(transactions, many=True)
        return Response(serializer.data)

# Replace decorated functions with class-based views
class BorrowBookView(APIView):
    permission_classes = []
    
    def post(self, request):
        serializer = BorrowBookSerializer(data=request.data)
        if serializer.is_valid():
            with transaction.atomic():
                user = serializer.validated_data['user']
                book = serializer.validated_data['book']
                
                # Check again if book is available (for race conditions)
                if book.copies_available <= 0:
                    return Response(
                        {"error": "No copies available for borrowing"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                # Create borrow transaction
                borrow_transaction = BorrowTransaction.objects.create(
                    user=user,
                    book=book,
                    status='borrowed'
                )
                
                # Update book copies
                book.copies_available -= 1
                book.save()
                
                return Response(
                    BorrowTransactionSerializer(borrow_transaction).data,
                    status=status.HTTP_201_CREATED
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ReturnBookView(APIView):
    permission_classes = []
    
    def post(self, request):
        serializer = ReturnBookSerializer(data=request.data)
        if serializer.is_valid():
            with transaction.atomic():
                borrow_transaction = serializer.validated_data['id']
                
                # Update transaction
                borrow_transaction.status = 'returned'
                borrow_transaction.return_date = timezone.now()
                borrow_transaction.save()
                
                # Update book copies
                book = borrow_transaction.book
                book.copies_available += 1
                book.save()
                
                return Response(
                    BorrowTransactionSerializer(borrow_transaction).data,
                    status=status.HTTP_200_OK
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
