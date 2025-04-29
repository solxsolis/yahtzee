import socket, threading, json
from game.categories import Category

class NetworkClient:
    def __init__(self, host, port, on_state):
        self.on_state = on_state
        self.sock = socket.create_connection((host, port))
        threading.Thread(target=self._recv_loop, daemon=True).start()

    def _recv_loop(self):
        buf = ""

        while True:
            data = self.sock.recv(4096).decode()
            if not data:
                break
            buf += data
            while "\n" in buf:
                line, buf = buf.split("\n", 1)
                msg = json.loads(line)
                self.on_state(msg)

    def send(self, msg: dict):
        self.sock.sendall((json.dumps(msg)+"\n").encode())


class GameServer:
    def __init__(self, host, port, GameFactory):
        self.sock = socket.socket()
        self.sock.bind((host, port))
        self.sock.listen(2)

        self.game = GameFactory()
        self.game.start_game()

        self.handlers = []
        threading.Thread(target=self._accept_and_serve, daemon=True).start()
        print(f"Game server started on {host}:{port}")

    def _accept_and_serve(self):
        conn1, _ = self.sock.accept()
        conn2, _ = self.sock.accept()
        self.handlers = [(conn1, 0), (conn2, 1)]
        self._serve()

    def _serve(self):
        def broadcast_state():
            player = self.game.get_current_player()
            turn = player.get_current_turn()

            state = {
                "type": "state",
                "current_player": self.game.cuurent_player_idx,
                "dice": turn.get_dice_values(),
                "rolls_left": turn.get_rolls(),
            }

            data = json.dumps(state) + "\n"
            for conn, _ in self.handlers:
                conn.sendall(data.encode())

        buffers = ["", ""]
        broadcast_state()

        while True:
            for idx, (conn, pid) in enumerate(self.handlers):
                data = conn.recv(4096).decode()
                if not data:
                    return
                buffers[idx] += data
                while "\n" in buffers[idx]:
                    line, buffers[idx] = buffers[idx].split("\n", 1)
                    cmd = json.loads(line)

                    if self.game.current_player_idx == pid:
                        self._apply_command(cmd)
                    broadcast_state()

                    if self.game.get_state() == "finished":
                        end = {
                            "type": "game_over",
                            "winner": self.game.get_winner(),
                            "scores": self.game.get_scores()
                        }

                        for c, _ in self.handlers:
                            c.sendall((json.dumps(end) + "\n").encode())
                        return

    def _apply_command(self, cmd):
        turn = self.game.get_current_player().get_current_turn()
        t = cmd.get("type")
        if t == "roll":
            turn.roll()
        elif t == "hold":
            keep = cmd.get("indices", [])
            for i, die in enumerate(turn.get_dice()):
                want = (i in keep)
                if die.get_active != want:
                    die.toggle()
        elif t == "score":
            cat = getattr(Category, cmd.get("category"))
            pts = turn.get_score(cat)
            self.game.get_current_player().set_score(cat, pts)
            self.game.next_turn()