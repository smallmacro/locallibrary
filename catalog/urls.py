from django.urls import path,re_path

#funtion based view
from catalog.views import (
   index,
   book_list,
   book_detail,
   author_list,
   author_detail,
   renew_book_librarian,
   register
   
)

#class based view
from .views import (
   HomeListView,
   BookListView,
   BookDetailView,
   BookCreateView,
   BookUpdateView,
   BookDeleteView,
   AuthorListView,
   AuthorDetailView,
   AuthorCreateView,
   AuthorUpdateView,
   AuthorDeleteView,
   LoanedBookByUserListView,
   LoanedBookManagementListView,
   BookReviewCreateView,
   # BookReviewDetailView

   )

urlpatterns = [
   ####### Funtion based view
   # path('',index, name='index'),
   # path('book/', book_list, name='book-list'),
   # path('author/', author_list, name='author-list'),
   # path('author/<int:pk>/', author_detail, name='author-detail'),
   # path('book/<int:pk>/', book_detail, name='book-detail'),
   path('register/',register , name='register'),

   path('book/<uuid:pk>/renew/', renew_book_librarian, name='renew-book-librarian'),



   ###### Class based view
   path('',HomeListView.as_view(), name='index'),
   path('book/', BookListView.as_view(), name='book-list'),
   path('book/new/', BookCreateView.as_view(), name='book-create'),
   path('book/<int:pk>/update/', BookUpdateView.as_view(), name='book-update'),
   path('book/<int:pk>/delete/', BookDeleteView.as_view(), name='book-delete'),
   path('book/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
   path('book/<int:pk>/create', BookReviewCreateView.as_view(), name='bookreview-create'),
   # path('book/<int:bid>/review-<int:pk>/', BookReviewDetailView.as_view(), name='bookreview-detail'),

   path('author/', AuthorListView.as_view(), name='author-list'),
   path('author/new/', AuthorCreateView.as_view(), name='author-create'),
   path('author/<int:pk>/update/', AuthorUpdateView.as_view(), name='author-update'),
   path('author/<int:pk>/delete/', AuthorDeleteView.as_view(), name='author-delete'),
   path('author/<int:pk>/', AuthorDetailView.as_view(), name='author-detail'),
   path('mybook/', LoanedBookByUserListView.as_view(), name='my-borrowed-list'),
   path('borrowed/', LoanedBookManagementListView.as_view(), name='loaned-book-list'),

   # re_path(r'^book/(?P<year>[0-9]{4})', book_list, name='book-list-year')
   
]
