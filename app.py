from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, join_room, leave_room, emit
from game import Game
from questions import QuestionFetcher
import json
import random

app = Flask(__name__)
app.debug = True
socketio = SocketIO(app)

game = Game(0)
fetcher = QuestionFetcher()

players = {}
scores = {}
questions = []
answers = {}

@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        num_players = int(request.form['num_players'])
        game.__init__(num_players)  # reset the game with the new number of players
        return redirect(url_for('question'))
    return render_template('main.html', num_players=range(1, 9))

@app.route('/question', methods=['GET', 'POST'])
def question():
    if request.method == 'POST':
        for player in game.players:
            player.set_answer(request.form[f'player{player.id}_answer'])
        game.check_answers()
    game.set_question(*fetcher.fetch_question())
    return render_template('question.html', game=game)

@app.route('/reset')
def reset():
    game.reset()
    return redirect(url_for('main'))

@app.route('/player/<int:player_id>')
def player(player_id):
    return render_template('player.html', player_id=player_id)

@socketio.on('join')
def on_join(data):
    player_id = data['player_id']
    join_room(player_id)
    players[player_id] = request.sid
    scores[player_id] = 0

@socketio.on('leave')
def on_leave(data):
    player_id = data['player_id']
    leave_room(player_id)
    del players[player_id]
    del scores[player_id]

@socketio.on('start game')
def start_game(data):
    # Load questions from JSON file
    with open('questions.json', 'r') as f:
        questions = json.load(f)
    # Shuffle questions
    random.shuffle(questions)
    # Emit first question
    emit('new question', questions[0], broadcast=True)

@socketio.on('answer')
def handle_answer(data):
    player_id = data['player_id']
    answer = data['answer']
    answers[player_id] = answer
    # Check if all players have answered
    if len(answers) == len(players):
        # Check answers and update scores
        for player_id, answer in answers.items():
            if answer == questions[0]['correct']:
                scores[player_id] += 1
            else:
                scores[player_id] -= 1
        # Emit updated scores
        emit('score update', scores, broadcast=True)
        # Emit correct answer
        emit('correct answer', questions[0]['correct'], broadcast=True)
        # Fetch new question
        questions.pop(0)
        if questions:
            emit('new question', questions[0], broadcast=True)
        answers = {}

@socketio.on('reset')
def reset():
    global players, scores, questions, answers
    players = {}
    scores = {}
    questions = []
    answers = {}
    emit('reset', broadcast=True)

if __name__ == '__main__':
    socketio.run(app)
