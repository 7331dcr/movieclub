# Movieclub - A movie review aggregator.

[Imgur](https://i.imgur.com/wNRpPIM.gif)

## Stack:

#### Front:
- HTML5 & CSS
- Javascript
- Django templates
#### Back:
- Python v. 3.8.6
- Django v. 3.1.5


## Instalation:

#### Setup:
Inside folder `/movieclub_project`, on your terminal of choice, execute the following:

- `python manage.py makemigrations` in order to generate the necessary files for the database setup;
- `python manage.py migrate` to execute the previous setup files created;
- `python manage.py runserver` to run the server.

As per default, the server adress is `http://127.0.0.1:8000/`.

#### Setup Django's deafult admin interface (optional):
In order to access the administrative interface via `/admin`, it is necessary to creat an administrative user.

To do that, inside `/movieclub_project` execute `python manage.py createsuperuser` and follow the instructions.


## Features:

### Page routes:

#### `/` (home page)

Allows movies to be searched by their title.

Utilizes javascript to dynamically show the queried search after 500 milliseconds of text being typed.

**Specific files for this page are:** _(this section title will be hidden for the features below)_
- `index.js`
- `index.html`

---------------
#### `/add_movie`

If user has `staff` status, allows movies to be added to database.

- `add_movie.html`

---------------
#### `/add_list`

Allows user to create a new list of movies.

- `add_list.html`

---------------
#### `/list/<id>`

Displays requested list page accordingly to the provided ID (integer) and allows user (if it's author) to delete it.

- `list.html`

---------------
#### `/movie/<id>`

Displays requested movie page accordingly to the provided ID (integer).

- `movie.html`

---------------
#### `/movie/<id>/reviews`

Displays a page with all the reviews for requested movie accordingly to the provided ID (integer).

- `movie_reviews.html`

---------------
#### `/profile/<username>`

Displays requested user profile page accordingly to the provided username (string).

- `profile.html`

---------------
#### `/profile/<username>/lists`

Displays a page with all the lists of the requested user accordingly to the provided username (string).

- `lists.html`

---------------
#### `/profile/<username>/reviews`

Displays a page with all the reviews of the requested user accordingly to the provided username (string).

- `user_reviews.html`

---------------
#### `/review/<id>`

Displays requested review page accordingly to the provided ID (integer) and allows user (if it's author) to delete or edit it.

- `review.html`
- `review.js`

---------------

### API Routes:

#### `/add_to_list`

Registers new movies to specified list via `POST` request.

---------------
#### `/add_review/<id>`

Registers to database new reviews via `POST` request.

---------------
#### `/edit_review/<id>`

Returns a JSON response with review data accordingly to the provided ID (integer) via `GET` request.

Receives JSON payload via `PUT` request with new data and saves it to provided review.

Deletes provided review via `POST` request.

- `review.js`

---------------
#### `/delete_list/<id>`

Deletes specified list via `POST` request accordingly to provided ID (integer).

---------------
#### `/get_movie`

Returns a JSON response with movie data accordingly to the provided ID via `GET` request, utilizing `"movie"` as `kwargs`.

---------------

### User Authentication:

#### `/login`

Displays a page for the login of registered users.

- `login.html`

---------------
#### `/logout`

Allows logged in users to log out.

---------------
#### `/register`

Allows the registration of new users. 

- `register.html`

---------------

&nbsp;

# CS50W Capstone project requirements:

&nbsp;

## Why you believe your project satisfies the distinctiveness and complexity requirements, mentioned above.

The project was made from scratch, based on an original idea, following the requirements and trying to implement all methods learned through the lectures and problem sets.

## What’s contained in each file you created.

  - `/movieclub_project/movieclub/static/movieclub` contains all javascript and css files.

  - `/movieclub_project/movieclub/templates/movieclub` contains all .html files.

All files created and used in the project are described in the [Features](#features) section, with the exception of the following, used more generally:

  - `image.js` used to frame images when reframing was needed.

  - `style.css` used to store all the css specifications.

  - `apology.html` used to return an apology page with specified error message when needed.

## How to run your application.

Described in [Instalation](#instalation) section.

## Any other additional information the staff should know about your project.
Some observations:
- The project allows (and requires, initially) manually adding each movie to it's database.
- `models.py` allows to implement an ___User.avatar___ and a ___Movie.poster___, providing the image url, but this feature is not enabled by default. To change it's default values, it is needed to access Django's admin interface via `/admin`.
