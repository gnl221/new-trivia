class Player:
    def __init__(self, id):
        self.id = id
        self.score = 0
        self.answer = None

    def update_score(self, points):
        self.score += points

    def set_answer(self, answer):
        self.answer = answer
