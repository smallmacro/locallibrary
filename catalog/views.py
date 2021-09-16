from django.shortcuts import render, get_object_or_404, reverse,redirect
from .models import (Book, BookInstance, Author,Genre, BookReview)
from django.contrib import messages
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
    )
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin ,PermissionRequiredMixin

from .forms import RenewBookForm, RenewBookModelForm, UerRegisterForm
from django.http import HttpResponseRedirect
import datetime

from django.urls import reverse_lazy

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

# User register
def register(request):

    if request.method == 'POST':
        form = UerRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You can log in now. {username}!')
            form = UerRegisterForm()
            return redirect('login')
    else:
        form = UerRegisterForm()
    return render(request, 'registration/register.html', {'form':form})

@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
def book_list(request):
    book_list = Book.objects.all()
    context = {
        'book_list':book_list
    }
    
    return render(request, 'catalog/book_list.html', context)

@login_required
def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    context = {
        'book' : book
    }
    return render(request, 'catalog/book_detail.html', context)

@login_required
def author_list(request):
    author_list = Author.objects.all()
    context = {
        'author_list': author_list
    }
    return render(request, 'catalog/author_list.html' , context)

@login_required
def author_detail(request, pk):
    author = get_object_or_404(Author, pk=pk)
    context = {
        'author' : author
    }
    return render(request, 'catalog/author_detail.html', context)

#Only Librarians can renew the due date.
@login_required
@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)
    if request.method == 'POST':
        form = RenewBookModelForm(request.POST)

        if form.is_valid():
            book_instance.due_back = form.cleaned_data['due_back']
            book_instance.save()
            return HttpResponseRedirect(reverse('loaned-book-list') )
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookModelForm(initial={'due_back':proposed_renewal_date})

    context = {
        'form': form,
        'book_instance':book_instance
    }

    return render(request, 'catalog/renewal_book.html', context)


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



class BookListView(LoginRequiredMixin,ListView):
    model = Book
    template_name = 'catalog/book_list.html'    
    context_object_name = 'book_list'
    paginate_by = 2
    # filter queryset outcome here
    # def get_queryset(self):
    #     pass



class BookDetailView(LoginRequiredMixin,DetailView):
    template_name = 'catalog/book_detail.html'
    model = Book
    context_object_name = 'book'

    # Add the Bookreview
    def get_context_data(self, **kwargs):
        context = super(BookDetailView, self).get_context_data(**kwargs)
        context['bookreview'] = BookReview.objects.filter(book_on=self.object).order_by('-post_date')
        return context

class BookReviewCreateView(LoginRequiredMixin,CreateView):
    model = BookReview
    template_name = 'catalog/bookreview_form.html'
    fields = ['post_date','content']

    def get_context_data(self,**kwargs):
        context = super(BookReviewCreateView, self).get_context_data(**kwargs)
        
        context['book'] = get_object_or_404(Book, pk=self.kwargs.get('pk'))

        return context

    def form_valid(self,form):
        form.instance.reviewer = self.request.user
        form.instance.book_on = get_object_or_404(Book, pk=self.kwargs.get('pk'))

        return super().form_valid(form)

    def get_success_url(self):
        # print(self.kwargs.get('pk'))
        return reverse_lazy('book-detail',kwargs={'pk':self.kwargs.get('pk')})

# class BookReviewDetailView(DetailView):
#     model = BookReview
#     template_name = 'catalog/bookreview_detail.html'

    # def get_queryset(self,**kwargs):
    #     print()
    #     self.object = BookReview.objects.filter(book_on=get_object_or_404(Book,pk=self.kwargs.get('bid')))


class BookCreateView(LoginRequiredMixin,PermissionRequiredMixin,CreateView):
    model = Book
    fields = ['title', 'author' ,'written_language','ISBN','summary','category']
    permission_required = 'catalog.can_mark_returned'

class BookUpdateView(LoginRequiredMixin,PermissionRequiredMixin,UpdateView):
    model = Book
    fields = ['title', 'author' ,'written_language','ISBN','summary','category']
    permission_required = 'catalog.can_mark_returned'

    # success_url = reverse_lazy('author-detail')

class BookDeleteView(LoginRequiredMixin,PermissionRequiredMixin,DeleteView):
    model = Book
    # fields = ['first_name', 'last_name' ,'date_of_birth','date_of_death']
    permission_required = 'catalog.can_mark_returned'
    
    success_url = reverse_lazy('book-list')






class AuthorListView(LoginRequiredMixin,ListView):
    model = Author
    template_name = 'catalog/author_list.html'    
    context_object_name = 'author_list'


class AuthorDetailView(LoginRequiredMixin,DetailView):
    template_name = 'catalog/author_detail.html'
    model = Author
    context_object_name = 'author'

class AuthorCreateView(LoginRequiredMixin,PermissionRequiredMixin,CreateView):
    model = Author
    fields = ['first_name', 'last_name' ,'date_of_birth','date_of_death']
    permission_required = 'catalog.can_mark_returned'

class AuthorUpdateView(LoginRequiredMixin,PermissionRequiredMixin,UpdateView):
    model = Author
    fields = ['first_name', 'last_name' ,'date_of_birth','date_of_death']
    permission_required = 'catalog.can_mark_returned'

    # success_url = reverse_lazy('author-detail')

class AuthorDeleteView(LoginRequiredMixin,PermissionRequiredMixin,DeleteView):
    model = Author
    # fields = ['first_name', 'last_name' ,'date_of_birth','date_of_death']
    permission_required = 'catalog.can_mark_returned'

    success_url = reverse_lazy('author-list')



class LoanedBookByUserListView(LoginRequiredMixin,ListView):
    template_name = 'catalog/BookInstance_list_view.html'
    model = BookInstance
    # context_object_name = 'copy_list'

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')


#Only librarians can see all the books borrowed.
class LoanedBookManagementListView(LoginRequiredMixin,PermissionRequiredMixin,ListView):
    template_name = 'catalog/loaned_book_list.html'
    model = BookInstance
    permission_required = 'catalog.can_mark_returned'

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')

