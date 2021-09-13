from django.contrib import admin
from .models import Genre,Author,Language, Book,BookInstance



# Register your models here.
# admin.site.register(Genre)
# admin.site.register(Author)
# admin.site.register(Language)
# admin.site.register(Book)
# admin.site.register(BookInstance)

admin.site.register(Genre)
admin.site.register(Language)

class BookInline(admin.TabularInline):
    model = Book
    extra = 0

class AuthorAdmin(admin.ModelAdmin):
    #Set list_display to control which fields are displayed on the change list page of the admin.
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')

    #Fields are displayed vertically by default, but will display horizontally if you further group them in a tuple (as shown in the "date" fields above).
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]
    inlines = [BookInline]

admin.site.register(Author,AuthorAdmin)


class BookInstanceInline(admin.TabularInline):
    model = BookInstance
    extra = 0


#This does the same with     admin.site.register(Book,AuthorAdmin)
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    inlines = [BookInstanceInline]



#This does the same with    admin.site.register(BookInstance,,AuthorAdmin)
@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('id','book','dispaly_author','due_back','status')
    list_filter = ('status', 'due_back')


    #add "sections" to group related model information within the detail form,and change the order of displaying 
    fieldsets = fieldsets = (
        ("Book Info", {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back','borrower')
        }),
    )