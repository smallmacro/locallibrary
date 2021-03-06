from django.db import models
from django.urls import reverse
import uuid # Required for unique book instances

from django.contrib.auth.models import User

from datetime import date
# Create your models here.

class Genre(models.Model):
    
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name 

class Language(models.Model):
    name = models.CharField(max_length=150, help_text='Select a language for this book')

    def __str__(self):
        return self.name 

class Author(models.Model):
    """Model representing an author."""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    class Meta:
        ordering = [ 'first_name','last_name']

    def __str__(self):
        return f'{self.last_name}, {self.first_name}'

    def get_absolute_url(self):
        """Returns the url to access a particular author instance."""
        return reverse('author-detail', args=[str(self.id)])


class Book(models.Model):
    title = models.CharField(max_length=200,help_text='Enter the title')
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)
    
    written_language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True,help_text='Select a language for this book')
    summary = models.TextField(max_length=1000)
    ISBN = models.CharField('ISBN',unique=True, max_length=13, help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    category = models.ManyToManyField(Genre, help_text='Select a genre for this book')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        ordering = ['title', 'author']

    def get_absolute_url(self):
        return reverse('book-detail', kwargs={'pk':self.id})

    def display_genre(self):
        return ','.join(genre.name for genre in self.category.all()[:3])
    #customize the column???s title by adding a short_description attribute to the callable. like the verbose_name with a field
    display_genre.short_description = 'Genre'



class BookInstance(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular book across whole library') #a globally unique value for each instance
    
    book = models.ForeignKey(Book, on_delete=models.RESTRICT)
    due_back = models.DateField(null=True, blank=True)
    imprint = models.CharField(max_length=200)
    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )
    status = models.CharField(
        max_length=1, 
        choices=LOAN_STATUS, 
        default='m',
        help_text='Book availability',
        )
    borrower = models.ForeignKey(User,on_delete=models.SET_NULL, null=True,blank=True)

    class Meta:
        ordering = ['due_back']
        permissions = (("can_mark_returned", "Set book as returned"),)

    def __str__(self):
        return f'{self.id} ({self.book.title})'

    def get_absolute_url(self):
        return reverse('book-instance-detail', kwargs={'id':self.id})

    def dispaly_author(self):
        return f'{self.book.author}'
    dispaly_author.short_description = 'Author'

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False


class BookReview(models.Model):
    post_date = models.DateTimeField()
    content = models.TextField(max_length=1000)
    book_on = models.ForeignKey(Book,on_delete=models.CASCADE)
    reviewer = models.ForeignKey(User, on_delete=models.SET_NULL,null=True)
    ordering = '-post_date'

    def __str__(self):
        return self.content[:50]

    # def get_absolute_url(self):
    #     return reverse('bookreview-detail', kwargs={'id':self.id} )

    def display_reviewer(self):
        return f'{self.reviewer.username}'

    