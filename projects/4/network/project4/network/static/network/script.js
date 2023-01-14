document.addEventListener('DOMContentLoaded', function() {

    document.getElementById("follow-button").addEventListener("click", follow())

});

function follow(user_id) {
    fetch('/follow/' + user_id, {
        method: 'POST',
    })
    .then(response => response.json())
    .then(data => {
        console.log(data)
    })
    .catch(error => {
        console.error('Error:', error);
    });
}