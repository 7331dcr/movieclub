document.addEventListener('DOMContentLoaded', function() {
    let timeout = null;
    document.querySelector('#search-form').addEventListener('submit', preventSubmit);
    const search = document.querySelector('#search-input');
    /* https://schier.co/blog/wait-for-user-to-stop-typing-using-javascript */
    search.addEventListener('keyup', function(e) {
        clearTimeout(timeout);
        timeout = setTimeout(function () {
            search_movie(search.value)
        }, 200);
    })
});


function preventSubmit(form) {
    form.preventDefault(); 
}


function delay(fn, ms) {
    let timer = 0
    return function(...args) {
        clearTimeout(timer)
        timer = setTimeout(fn.bind(this, ...args), ms || 0)
    }
}


function search_movie(title) {
    fetch(`/get_movie?` + new URLSearchParams ({
        movie: title,
    }))
    .then(response => response.json())
    .then(data => {
        document.querySelector('#display').innerHTML = ''
        if (data.movies !== null) {
            load_movies(data);
        }
    })
}


function load_movies(list) {
    const display = document.querySelector('#display');
    display.innerHTML = ''
    list.forEach(element => {
        display.innerHTML = display.innerHTML + `
        <div class="display-item">
                <div class="display-image" onclick="openMovie(${element.id})">
                    <img id=img${element.id} src="${element.poster}" alt="${element.title} poster">
                </div>
                <div class="display-info">
                    <span class="display-title"><strong>${element.title}</strong></span>
                    <span class="display-year">(${element.year})</span>
                </div>
        </div>
        `;
        document.querySelector(`#img${element.id}`).addEventListener('load', () => resizeImage(document.querySelector(`#img${element.id}`)));
    });
}


function resizeImage(image) {
    const aspectRatio = image.naturalWidth / image.naturalHeight;

    // If landscape
    if (aspectRatio > 1) {
        image.style.minWidth = 'unset';
        image.style.maxHeight = '100%';
    };
}


function openMovie(id) {
    let url = window.location.origin
    window.location.href = (`${url}/movie/${id}`);
}


