from django.urls import path
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView
from . import views

urlpatterns = [
    path('', PostListView.as_view(), name='library-home'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('about/', views.about, name='library-about'),
    path('books/', views.book_list, name='book-list'),
    path('borrowed/', views.borrowed_books, name='borrowed-list'),
    path('book/<int:book_id>/borrow/', views.borrow_book, name='borrow-book'),
    path('books/<int:id>/', views.book_detail, name='book-detail'),
]