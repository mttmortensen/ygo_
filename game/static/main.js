document.getElementById('start-button').addEventListener('click', function() {
    fetch('/start_game', {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => updateGameState(data));
});

document.getElementById('summon-form').addEventListener('submit', function(event) {
    event.preventDefault();
    fetch('/summon', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            player: 0,  // The index of the player performing the action
            card: document.getElementById('card').value  // The index of the card to summon
        })
    })
    .then(response => response.json())
    .then(data => updateGameState(data));
});


function updateGameState() {
fetch('/game_state')
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            // If the server sent a message, display it on the page
            document.getElementById('message').textContent = data.message;
        } else {
            // Otherwise, update the game state as usual
            console.log(data);
            // Update your page elements here
        }
    });
}      

$('#update-button').on('click', function() {
    updateGameState();
});

setInterval(updateGameState, 1000);