from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Book, BorrowTransaction

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name','is_superuser']

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'isbn', 'copies_available', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

    def validate_isbn(self, value):
       
        if not value.isdigit() or not (len(value) == 10 or len(value) == 13):
            raise serializers.ValidationError("ISBN must be 10 or 13 digits")
        return value

class BorrowTransactionSerializer(serializers.ModelSerializer):
    user_name = serializers.ReadOnlyField(source='user.username')
    book_title = serializers.ReadOnlyField(source='book.title')
    
    class Meta:
        model = BorrowTransaction
        fields = ['id', 'user', 'user_name', 'book', 'book_title', 'borrow_date', 'return_date', 'status']
        read_only_fields = ['borrow_date', 'return_date', 'status']

class BorrowBookSerializer(serializers.Serializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    book = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all())
    
    def validate_book(self, value):
        if value.copies_available <= 0:
            raise serializers.ValidationError("No copies available for borrowing")
        return value

class ReturnBookSerializer(serializers.Serializer):
    transaction_id = serializers.PrimaryKeyRelatedField(
        queryset=BorrowTransaction.objects.filter(status='borrowed'),
        source='id'
    )