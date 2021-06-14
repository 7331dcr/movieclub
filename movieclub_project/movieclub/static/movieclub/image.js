document.addEventListener('DOMContentLoaded', function() {

    const images = document.querySelectorAll('img');

    images.forEach(image => {
        image.addEventListener('load', () => resizeImage(image));
    })

})


function resizeImage(image) {
    const aspectRatio = image.naturalWidth / image.naturalHeight;

    // If landscape
    if (aspectRatio > 1) {
        image.style.minWidth = 'auto';
        image.style.maxHeight = '100%';
    }
}