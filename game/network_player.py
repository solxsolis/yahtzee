from game.player import Player

class NetworkPlayer(Player):
    def __init__(self, player_id, client):
        super().__init__(f"Player {player_id+1}")
        self.player_id = player_id
        self.client = client

    def play_turn(self):
        pass

    def roll(self):
        self.client.send({"type":"roll"})

    def hold(self, indices):
        self.client.send({"type":"hold", "indices":indices})

    def score(self, category):
        self.client.send({"type":"score", "category":category})

