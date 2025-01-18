from game.turn import Turn
from game.player import Player

class Game:
    def __init__(self, players):
        self.players = players
        self.rounds = 1
        self.current_player = players[0]
        self.state = "inactive"

    def get_players(self):
        return self.players

    def get_rounds(self):
        return self.rounds

    def get_current_player(self):
        return self.current_player

    def get_state(self):
        return self.state

    def start_game(self):
        if self.state != "active":
            self.state = "active"
            self.current_player.start_turn()


    def play_turn(self):
        self.current_player.start_turn()
        self.current_player.play_turn()
        self.current_player.end_turn()

    def next_turn(self):
        current_index = self.players.index(self.current_player)
        if current_index == len(self.players) - 1:
            self.current_player = self.players[0]
            self.rounds += 1
        else:
            self.current_player = self.players[current_index + 1]

        if self.rounds > 13:
            winner, scores = self.end_game()
            return (winner, scores)
        return (None, None)

    def end_game(self):
        player_scores = []
        winner = None
        for player in self.players:
            player_scores.append(player.get_board().get_score())

        if player_scores[0] > player_scores[1]:
            winner = self.players[0]
        elif player_scores[0] < player_scores[1]:
            winner = self.players[1]

        self.state = "finished"
        return winner, player_scores







