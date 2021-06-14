from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    avatar = models.URLField(default="https://i.imgur.com/0P2wagS.png")


class Movie(models.Model):
    title = models.CharField(max_length=255, blank=False)
    year = models.IntegerField(blank=False)
    synopsis = models.TextField(blank=False)
    poster = models.URLField(default="https://i.imgur.com/Z7GSgGi.png")

    def __str__(self):
        return f" ID: {self.id} | Title: {self.title} | Year: {self.year}"

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "year": self.year,
            "synopsis": self.synopsis,
            "poster": self.poster
        }


class List(models.Model):
    name = models.CharField(max_length=255, blank=False)
    author = models.ForeignKey("User", on_delete=models.CASCADE, related_name="lists")

    def __str__(self):
        return f" ID: {self.id} | Author: {self.author}| Name: {self.name}"


class List_item(models.Model):
    list = models.ForeignKey("List", on_delete=models.CASCADE, related_name="list_items")
    movie = models.ForeignKey("Movie", on_delete=models.CASCADE, related_name="listed") #movie.revied.somedatafield <=tryit

    def __str__(self):
        return f" ID: {self.id} | List: {self.list} | Movie: {self.movie}"


class Rating(models.Model):
    movie = models.ForeignKey("Movie", on_delete=models.CASCADE, related_name="ratings", unique=True)
    rating = models.DecimalField(max_digits=4, decimal_places=2, blank=False)

    def __str__(self):
        return f" ID: {self.id} | Movie: {self.movie} | Rating: {self.rating}"


class Review(models.Model):
    title = models.CharField(max_length=255, blank=False)
    movie = models.ForeignKey("Movie", on_delete=models.CASCADE, related_name="reviewed") #movie.revied.somedatafield <=tryit
    author = models.ForeignKey("User", on_delete=models.CASCADE, related_name="reviews")
    review = models.TextField(blank=False)
    rating = models.IntegerField(blank=False)

    def __str__(self):
        return f" ID: {self.id} | Author: {self.author} | Title: {self.title} | Movie: {self.movie.title} | Rating: {self.rating}"

