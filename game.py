from player import Player

class Game:
    def __init__(self, num_players):
        self.players = [Player(i) for i in range(num_players)]
        self.current_question = None
        self.current_answers = None

    def reset(self):
        for player in self.players:
            player.score = 0
        self.current_question = None
        self.current_answers = None

    def set_question(self, question, answers):
        self.current_question = question
        self.current_answers = answers

    def check_answers(self):
        for player in self.players:
            if player.answer == self.current_answers[0]:  # assuming the correct answer is always the first one
                player.update_score(1)
            else:
                player.update_score(-1)
