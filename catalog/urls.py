from django.urls import path,re_path

#funtion based view
from catalog.views import (
   index,
   book_list,
   book_detail,
   author_list,
   author_detail
   
)

#class based view
from .views import (
   HomeListView,
   BookListView,
   BookDetailView,
   AuthorListView,
   AuthorDetailView

   )

urlpatterns = [
   ####### Funtion based view
   # path('',index, name='index'),
   # path('book/', book_list, name='book-list'),
   # path('author/', author_list, name='author-list'),
   # path('author/<int:pk>/', author_detail, name='author-detail'),
   # path('book/<int:pk>/', book_detail, name='book-detail'),



   ###### Class based view
   path('',HomeListView.as_view(), name='index'),
   path('book/', BookListView.as_view(), name='book-list'),
   path('book/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
   path('author/', AuthorListView.as_view(), name='author-list'),
   path('author/<int:pk>/', AuthorDetailView.as_view(), name='author-detail'),
   # re_path(r'^book/(?P<year>[0-9]{4})', book_list, name='book-list-year')
   
]
