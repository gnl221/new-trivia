document.addEventListener('DOMContentLoaded', () => {
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    document.querySelector('#start').onclick = () => {
        socket.emit('start game');
    };

    socket.on('new question', data => {
        document.querySelector('#question').innerHTML = data['question'];
    });
});

if (window.location.pathname.startsWith('/player')) {
    var player_id = parseInt(window.location.pathname.split('/')[2]);

    socket.emit('join', {player_id: player_id});

    document.querySelectorAll('button').forEach((button, index) => {
        button.onclick = () => {
            socket.emit('answer', {player_id: player_id, answer: index});
        };
    });

    window.onbeforeunload = () => {
        socket.emit('leave', {player_id: player_id});
    };
}

// Add event listener for reset button
document.querySelector('#reset').onclick = () => {
    socket.emit('reset');
};

// Add event listener for reset event
socket.on('reset', () => {
    document.querySelector('#question').innerHTML = '';
});

// Add event listener for correct answer event
socket.on('correct answer', data => {
    // Highlight correct answer
});

document.querySelector('form').onsubmit = () => {
    var num_players = document.querySelector('select').value;
    socket.emit('start game', {num_players: num_players});
    return false;  // prevent the form from being submitted normally
};
