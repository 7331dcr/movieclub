import json
from decimal import Decimal
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.db.models import Avg
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .models import List, List_item, Movie, Rating, Review, User


def index(request):
    return render(request, "movieclub/index.html")


def add_movie(request):

    # Checks if current user is staff
    if not request.user.is_staff:
        messages.error(request, f"Forbidden.")
        return render(request, "movieclub/apology.html", status=403)

    if request.method == "POST":
        title = request.POST["title"]
        year = request.POST["year"]
        synopsis = request.POST["synopsis"]

        # Attempt to save new movie entry
        try:
            movie = Movie(title=title, year=year, synopsis=synopsis)
            movie.save()
            messages.success(request, "Successfully added movie do the database.")
        except ValueError:
            messages.error(request, "Failed to add movie to database.")
            return render(request, "movieclub/add_movie.html", status=500)

        return render(request, "movieclub/add_movie.html")

    return render(request, "movieclub/add_movie.html")


def add_list(request):
    if request.method == "GET":
        if not request.user.username:
            messages.error(request, f"You must be logged in to access this page.")
            return render(request, "movieclub/apology.html", status=403)

        return render(request, "movieclub/add_list.html")

    if request.method == "POST":
        author = request.user
        name = request.POST['name']

        if not author.username:
            messages.error(request, f"Failed to create list. You must be logged in to create a list.")
            return render(request, "movieclub/apology.html", status=403)

        if not name:
            messages.error(request, f"Failed to create list. Your list must have a name.")
            return render(request, "movieclub/apology.html", status=500)

        # Attempts to save new list
        try:
            new_list = List(author=author, name=name)
            new_list.save()
            messages.success(request, "Successfully added review to database.")
        except Exception:
            messages.error(request, f"Failed to create new list.")
            return render(request, "movieclub/apology.html", status=500)

        return HttpResponseRedirect(reverse("list", args=(new_list.id,)))


def add_to_list(request):
    if request.method == "POST":

        # Checks if user is logged in
        if not request.user.is_authenticated:
            messages.error(request, f"You must be logged in do this action.")
            return render(request, "movieclub/apology.html", status=403)

        # Attemps to find provied list and movie
        try:
            list = List.objects.get(pk=request.POST['list'])
            movie = Movie.objects.get(pk=request.POST['movie'])
        except List.DoesNotExist or movie.DoesNotExist:
            messages.error(request, f"Request failed. Invalid movie or list")
            return render(request, "movieclub/apology.html", status=500)

        # Ensures movie isn't already on the list
        if movie.listed.filter(list=list):
            messages.error(request, f"Movie is already on the list")
            return render(request, "movieclub/apology.html", status=500)

        # Attempts to save new list entry
        try:
            new_list_item = List_item(list=list, movie=movie)
            new_list_item.save()
            messages.success(request, "Successfully added movie to selected list.")
        except Exception:
            messages.error(request, f"Failed to add movie to selected list.")
            return render(request, "movieclub/apology.html", status=500)

        return HttpResponseRedirect(reverse("list", args=(list.id,)))


def add_review(request, movie_id):
    if request.method == "POST":
        author = request.user
        if not author.is_authenticated:
            messages.error(request, f"You must be logged in do this action.")
            return render(request, "movieclub/apology.html", status=403)

        # Attempt to find movie
        try:
            movie = Movie.objects.get(pk=movie_id)
        except Movie.DoesNotExist:
            messages.error(request, f'Movie not found.')
            return render(request, "movieclub/apology.html", status=500)

        rating = request.POST['rating']
        review = request.POST['review']
        title = request.POST['title']

        if int(rating) < 0 or int(rating) > 10:
            messages.error(request, f"Rating has to be an integer between 0 and 10.")
            return render(request, "movieclub/apology.html", status=500)

        # Ensures movie isn't already reviewd
        check_reviewed = movie.reviewed.filter(movie=movie, author=author)
        if check_reviewed:
            messages.error(request, f"You have already reviewed this movie")
            return HttpResponseRedirect(reverse("review", args=(check_reviewed[0].id,)))

        # Attempts to add new review entry to database
        try:
            new_review = Review(author=author, movie=movie, rating=rating, review=review, title=title)
            new_review.save()
        except Exception:
            messages.error(request, f"Failed to add review to database.")
            return render(request, "movieclub/apology.html", status=500)

        # Calculates new movie rating
        average_review_ratings = movie.reviewed.all().aggregate(Avg('rating'))
        movie_rating = round(average_review_ratings['rating__avg'], 2)

        # Attempts to update movie rating
        try:
            new_rating = Rating.objects.get(movie=movie)
            new_rating.rating = Decimal(movie_rating)
            new_rating.save()
        except Rating.DoesNotExist:
            new_rating = Rating(movie=movie, rating=movie_rating)
            new_rating.save()
        except Exception:
            messages.error(request, f"Failed to add rating to database.")
            return render(request, "movieclub/apology.html", status=500)

        messages.success(request, "Successfully added review do the database.")
        return HttpResponseRedirect(reverse("movie", args=(movie.id,)))


@csrf_exempt
def edit_review(request, review_id):

    # Attempts to query requested post
    try:
        review = Review.objects.get(pk=review_id)
    except Review.DoesNotExist:
        return JsonResponse({"error": "Review not found."}, status=404)

    movie = review.movie

    # Ensures edit is made by the post's owner
    if not request.user.id == review.author.id:
        return JsonResponse({"error": "Forbidden action."}, status=403)

    # Handles edit button request
    if request.method == "GET":
        return JsonResponse({
            "title": review.title,
            "rating": review.rating,
            "review": review.review
        })
    
    # Handles confirm button request
    if request.method == "PUT":
        data = json.loads(request.body)
        review.title = data['title']
        review.rating = data['rating']
        if int(data['rating']) < 0 or int(data['rating']) > 10:
            return JsonResponse({"error": "Rating has to be an integer between 0 and 10."}, status=500)
        review.review = data['review']
        review.save()

        # Calculates new movie rating
        average_review_ratings = movie.reviewed.all().aggregate(Avg('rating'))
        movie_rating = round(average_review_ratings['rating__avg'], 2)

        # Updates movie rating
        new_rating = Rating.objects.get(movie=movie)
        new_rating.rating = Decimal(movie_rating)
        new_rating.save()

    # Handles delete button request
    if request.method == "POST":
        review.delete()
        reviews = movie.reviewed.all()
        new_rating = Rating.objects.get(movie=movie)
        
        if not reviews:
            new_rating.delete()
        else:
            average_review_ratings = reviews.aggregate(Avg('rating'))
            movie_rating = round(average_review_ratings['rating__avg'], 2)
            new_rating.rating = Decimal(movie_rating)
            new_rating.save()

        messages.success(request, f'Review "{review.title}" successfully deleted.')
        return HttpResponseRedirect(reverse('movie', args=(review.movie.id,)))

    return HttpResponse(status=204)


def delete_list(request, list_id):
    if request.method == "POST":

        # Attempts to find list
        try:
            requested_list = List.objects.get(pk=list_id)
        except List.DoesNotExist:
            messages.error(request, f'List not found.')
            return render(request, "movieclub/apology.html", status=500)

        # Ensures request is made by the list's owner
        if not request.user.id == requested_list.author.id:
            messages.error(request, f'Forbidden action.')
            return render(request, "movieclub/apology.html", status=403)

        # Deletes entry from database
        requested_list.delete()
        messages.success(request, f'List "{requested_list.name}" successfully deleted.')
        return HttpResponseRedirect(reverse('lists', args=(request.user.username,)))
    else:
        messages.error(request, f'Forbidden request.')
        return render(request, "movieclub/apology.html", status=403)


def get_movie(request):

    # Handles kwargs request from index page search
    query = str(request.GET.get('movie', ''))
    if not query:
        return JsonResponse({'movies': None})

    # # Selects all movies
    # if query == "'":
    #     movies = Movie.objects.all().order_by('title')
    #     return JsonResponse([movie.serialize() for movie in movies], safe=False)

    movies = Movie.objects.filter(title__contains=query).order_by('title')

    # ### same thing as the in-line for loop below
    # movies = []
    # for movie in movies:
    #     movies.append(movie.serialize())
    # return JsonResponse(movies, safe=False)

    return JsonResponse([movie.serialize() for movie in movies], safe=False)


def list(request, list_id):
    if request.method == "GET":
        
        # Attempt to find list
        try:
            requested_list = List.objects.get(pk=list_id)
        except List.DoesNotExist:
            messages.error(request, f'List not found.')
            return render(request, "movieclub/apology.html", status=500)

        # Gets requested_list items
        list_items = List_item.objects.filter(list=requested_list)

        return render(request, "movieclub/list.html", {
            "list": requested_list,
            "list_items": list_items
        })


def lists(request, username):
    if request.method == "GET":

        # Attempt to find user
        try:
            requested_user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, f'User "{username}" not found')
            return render(request, "movieclub/apology.html", status=500)

        # Gets all requested_user lists in reverse chronological order
        requested_user_lists = List.objects.filter(author=requested_user).order_by('-id') 
        ### same thing as requested_user.lists.all()

        return render(request, "movieclub/lists.html", {
            "requested_user": requested_user,
            "lists": requested_user_lists,
            "movies_qnt": len(requested_user_lists)
        })


def movie(request, movie_id):
    if request.method == "GET":

        # Attempts to find movie
        try:
            movie = Movie.objects.get(pk=movie_id)
        except Movie.DoesNotExist:
            messages.error(request, f'Movie not found.')
            return HttpResponseRedirect(reverse('index'))
    
        # Attempts to get movie's rating
        try:
            rating = Rating.objects.get(movie=movie)
        except Rating.DoesNotExist:
            rating = None

        # Gets latest 3 reviews
        reviews = Review.objects.filter(movie=movie).order_by("-id")[:3]

        # Gets all current user lists
        lists = None
        if request.user.is_authenticated:
            lists = List.objects.filter(author=request.user).order_by("-id")

        return render(request, "movieclub/movie.html", {
            "movie": movie,
            "rating": rating,
            "reviews": reviews,
            "lists": lists
        })


def movie_reviews(request, movie_id):
    if request.method == "GET":

        # Attempts to find movie
        try:
            movie = Movie.objects.get(pk=movie_id)
        except Movie.DoesNotExist:
            messages.error(request, f'Movie not found.')
            return render(request, "movieclub/apology.html", status=500)

        # Gets all movie reivews
        movie_reviews = Review.objects.filter(movie=movie).order_by('-id')

        return render(request, "movieclub/movie_reviews.html", {
            "movie": movie,
            "reviews": movie_reviews
        })


def profile(request, username):
    if request.method == "GET":

        # Attempts to find user
        try:
            requested_user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, f'User "{username}" not found')
            return render(request, "movieclub/apology.html", status=500)

        # Gets latest 3 requested_user lists in reverse chronological order
        requested_user_lists = List.objects.filter(author=requested_user).order_by("-id")

        # Gets latest 3 requested_user reviews in reverse chronological order
        requested_user_reviews = Review.objects.filter(author=requested_user).order_by("-id")

        return render(request, "movieclub/profile.html", {
            "requested_user": requested_user,
            "lists": requested_user_lists[:3],
            "reviews": requested_user_reviews[:3],
            "reviews_num": len(requested_user_reviews),
            "lists_num": len(requested_user_lists)
        })

        return render(request, "movieclub/profile.html")


def review(request, review_id):
    if request.method == "GET":

        # Attempts to find movie
        try:
            review = Review.objects.get(pk=review_id)
        except Review.DoesNotExist:
            messages.error(request, f'Review not found.')
            return render(request, "movieclub/apology.html", status=500)

        return render(request, "movieclub/review.html", {
            "review": review
        })


def user_reviews(request, username):
    if request.method == "GET":

        # Attempt to find user
        try:
            requested_user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, f'Username "{username}" not found')
            return render(request, "movieclub/apology.html", status=500)

        # Gets all reviews from requested_user
        user_reviews = Review.objects.filter(author=requested_user).order_by('-id')

        return render(request, "movieclub/user_reviews.html", {
            "requested_user": requested_user,
            "reviews": user_reviews
        })


# User Authentication
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "movieclub/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        if request.user.is_authenticated:
            messages.error(request, f"You are already logged in.")
            return render(request, "movieclub/apology.html", status=403)
        return render(request, "movieclub/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "movieclub/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "movieclub/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        if request.user.is_authenticated:
            messages.error(request, f"You are already logged in.")
            return render(request, "movieclub/apology.html", status=403)
        return render(request, "movieclub/register.html")