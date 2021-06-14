function edit_review(id) {
    document.querySelector(`.edit-btn_${id}`).style.display = 'none';
    document.querySelector(`.delete-btn_${id}`).style.display = 'none';

    fetch(`/edit_review/${id}`)
    .then(response => response.json())
    .then(data => {
        const review = document.querySelector(`#review_${id}`);
        review.innerHTML = `
            <div class="edit_review_title bottom-marg">
                <input type="text" id="edited_title" name="edit_title" autocomplete="off" placeholder="Review title" value="${data.title}"><br>
            </div>

            <div class="edit_review_rating bottom-marg">
                <input type="number" id="edited_rating" name="edit_rating" min="0" max="10" autocomplete="off" placeholder="Rating (0-10)" value="${data.rating}"><br>
            </div>

            <div class="edit_review_title bottom-marg">
                <textarea  id="edited_review" class="txt_container" name="edit_post" placeholder="Review" rows="6" cols="60">${data.review}</textarea>
            </div>
            
            <div style="margin-left: -4px;">
                <input class="button" type="button" onclick="cancel(${id})" value="Cancel">
                <input class="button" type="button" onclick="confirm(${id})" value="Confirm">
            </div>
        `
    });
}


// Handles edit_review() Cancel button
function cancel(id) {
    const review = document.querySelector(`#review_${id}`);
    fetch(`/edit_review/${id}`)
    .then(response => response.json())
    .then(data => {
        review.innerHTML = `
            Rating: <strong>${data.rating}</strong>
            <br>
            <br>
            ${data.review}
            <br>
            <br>
        `;
    });
    document.querySelector(`.edit-btn_${id}`).style.display = 'inline-block';
    document.querySelector(`.delete-btn_${id}`).style.display = 'inline-block';
}


// Handles edit_review() Confirm button
function confirm(id) {
    let new_title = (document.getElementById('edited_title').value);
    let new_rating = (document.getElementById('edited_rating').value);
    let new_review = (document.getElementById('edited_review').value);
    fetch(`/edit_review/${id}`, {
        method: 'PUT',
        body: JSON.stringify({
            title: new_title,
            rating: new_rating,
            review: new_review,
        })
    })
    .then(function() {
        fetch(`/edit_review/${id}`)
        .then(response => response.json())
        .then(data => {
            const review = document.querySelector(`#review_${id}`);
            review.innerHTML = `
                Rating: <strong>${data.rating}</strong>
                <br>
                <br>
                ${data.review}
                <br>
                <br>
            `;
            document.querySelector('#review_title').innerHTML = `Review: ${data.title}.`
            document.querySelector(`.edit-btn_${id}`).style.display = 'inline-block';
            document.querySelector(`.delete-btn_${id}`).style.display = 'inline-block';
        });
    });
}