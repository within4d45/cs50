document.addEventListener('DOMContentLoaded', function() {

    user_id = document.getElementById("follow-button").dataset.userId;
    
    document.getElementById("follow-button").addEventListener("click", () => {
        follow(user_id);
    });

});

function follow(user_id) {
    fetch('/follow/' + user_id + '/', {
        method: 'POST',
    })
    .then(response => response.json())
    .then(data => {
        console.log(data)
    });
}