from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.utils import timezone
from .models import Post, Borrow, Biblio


def home (request):
    content = {'posts': Post.objects.all()}
    return render(request, 'library/home.html', content)

class PostListView(ListView):
    model = Post
    template_name = 'library/home.html' #<app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']

class PostDetailView(DetailView):
    model = Post

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object
        if self.request.user == post.author:
            return True
        return False
        #return super().test_func()

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post

    #def test_func(self):
        #post = self.get_object()
        #return self.request.user == post.author


        #if self.request.user == post.author:
            #return True
        #return False

    

def about(request):
    return render(request, 'library/about.html', {'title': 'About'})

def book_list(request):
    books = Biblio.objects.all()
    return render(request, 'library/books.html', {'books': books})

def book_detail(request, id):
    book = get_object_or_404(Biblio, pk=id)  # Get the book by its ID
    return render(request, 'library/book_detail.html', {'book': book})

def borrowed_books(request):
    borrowed = Borrow.objects.filter(user=request.user)
    return render(request, 'library/borrowed_books.html', {'borrowed': borrowed})

@login_required
def borrow_book(request, book_id):
    book = get_object_or_404(Biblio, pk=book_id)

    if not book.available:
        messages.error(request, 'This book is currently unavailable.')
        return redirect('book-detail', id=book.id)

    # Create a borrow record
    Borrow.objects.create(user=request.user, book=book)

    # Mark the book as unavailable
    book.available = False
    book.save()

    messages.success(request, f'You have successfully borrowed "{book.title}".')
    return redirect('book-detail', id=book.id)

@login_required
def return_book(request, borrow_id):
    borrow = get_object_or_404(Borrow, id=borrow_id, user=request.user)

    if not borrow.return_date:  # Only allow return if not already returned
        borrow.return_date = timezone.now().date()
        borrow.save()

        # Optional: Mark book as available again
        borrow.book.available = True
        borrow.book.save()

    return redirect('borrowed-list')  # Update to your actual borrowed list view name