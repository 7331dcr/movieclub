from django.contrib import admin

# Register your models here.
from .models import List, List_item, Movie, Rating, Review, User

admin.site.register(List)
admin.site.register(List_item)
admin.site.register(Movie)
admin.site.register(Rating)
admin.site.register(Review)
admin.site.register(User)
