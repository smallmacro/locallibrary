from django.urls import path

#funtion based view
from catalog.views import (
   index,
   book_list,
   book_detail
   
)

#class based view
from .views import (
   HomeListView,
   BookListView,
   BookDetailView

   )

urlpatterns = [
   ####### Funtion based view
   # path('',index, name='index'),
   # path('book/', book_list, name='book-list'),
   path('book/<int:pk>/', book_detail, name='book-detail'),



   ###### Class based view
   path('',HomeListView.as_view(), name='index'),
   path('book/', BookListView.as_view(), name='book-list'),
   # path('book/<int:pk>/', BookDetailView.as_view(), name='book-detail'),

   
]
