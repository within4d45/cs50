document.addEventListener('DOMContentLoaded', function() {

    const editButtons = document.getElementsByClassName("edit-button");

    for (var i = 0; i < editButtons.length; i++) {

        editButtons[i].addEventListener("click", function() {
            var postId = this.dataset.postId;
            edit_post(postId);
        });
    }


});

function edit_post(postId) {

    /* 
    Steps we need to go through:
    - Fetch content of the post through an API
    - Make the div of the post invisible
    - Make the div of the edit post visible
    - Prepoulate textarea with the content of the initial post
    - When submitting, POST the new content to the database being handled by an API
    - Make post visible again with the new content inside of it

    IDEAS:
    Two ways of making this possible: Either we have an invisible edit field for every
    post there is already and we just make it visible, when somebody is clicking the enter
    button - but this seems to be a waste of resources (?)

    Or we are just populating an empty div which's ID is #edit-post
    */
    var initialPost = document.querySelector(`#post-${postId}`);
    var editPost = document.querySelector(`#edit-post-${postId}`);

    initialPost.style.display = 'none';

    editPost.innerHTML =`
    <div class="mb-3">
        <textarea name="content" class="form-control" id="edit-post-content" cols="30" rows="5" required></textarea>
    </div>
    <input type="submit" class="btn btn-primary" value="Edit Post" id="edit-post">    `

    var editPost = document.querySelector('#edit-post');
    const textarea = document.querySelector('#edit-post-content');

    // Just for testing purposes, print the textarea value to the console
    editPost.addEventListener("click", () => {
        content = textarea.value
        console.log(content);
    });

}