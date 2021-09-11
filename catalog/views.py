from django.shortcuts import render, get_object_or_404
from .models import (Book, BookInstance, Author,Genre)
from django.views.generic import (
    ListView,
    DetailView
    )

# Create your views here.
def index(request):
    num_books = Book.objects.count()
    num_instances = BookInstance.objects.count()
    num_instance_available = BookInstance.objects.filter(status__exact='a').count
    num_authors = Author.objects.count()
    num_genres = Genre.objects.count()
    num_contains_you = Book.objects.filter(title__icontains='You').count()
    context = {
        'num_books':num_books,
        'num_instances':num_instances,
        'num_instance_available':num_instance_available,
        'num_authors':num_authors,
        'num_genres':num_genres,
        'num_contains_you':num_contains_you
    }

    return render(request, 'catalog/index.html', context=context)



def book_list(request):
    book_list = Book.objects.all()
    context = {
        'book_list':book_list
    }
    
    return render(request, 'catalog/book_list.html', context)


def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    context = {
        'book' : book
    }
    return render(request, 'catalog/book_detail.html', context)

def author_list(request):
    author_list = Author.objects.all()
    context = {
        'author_list': author_list
    }
    return render(request, 'catalog/author_list.html' , context)

def author_detail(request, pk):
    author = get_object_or_404(Author, pk=pk)
    context = {
        'author' : author
    }
    return render(request, 'catalog/author_detail.html', context)



class HomeListView(ListView):
    template_name = 'catalog/index.html'
    model = BookInstance
    context_object_name = 'instance_list'
    
    def get_context_data(self, **kwargs):
        #Call the base implementation first to get the context
        context = super(HomeListView, self).get_context_data(**kwargs)
        context['num_books'] = Book.objects.count()
        context['author_list'] = Book.objects.all()
        context['num_instances'] = BookInstance.objects.count()
        context['num_instance_available'] = BookInstance.objects.filter(status__exact='a').count()
        context['num_authors'] = Author.objects.count()
        context['num_genres'] = Genre.objects.count()
        context['num_contains_you'] = Book.objects.filter(title__icontains='You').count()

        return context



class BookListView(ListView):
    model = Book
    template_name = 'catalog/book_list.html'    
    context_object_name = 'book_list'
    paginate_by = 2
    # filter queryset outcome here
    # def get_queryset(self):
    #     pass


class BookDetailView(DetailView):
    template_name = 'catalog/book_detail.html'
    model = Book
    context_object_name = 'book'

    # def get_context_data(self, **kwargs):
    #     context = super(BookDetailView, self).get_context_data(**kwargs)
    #     context['copies'] = 

class AuthorListView(ListView):
    model = Author
    template_name = 'catalog/author_list.html'    
    context_object_name = 'author_list'


class AuthorDetailView(DetailView):
    template_name = 'catalog/author_detail.html'
    model = Author
    context_object_name = 'author'



