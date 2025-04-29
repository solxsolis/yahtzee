import argparse
from gui.yahtzee_gui import YahtzeeGUI

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument("--host", default = "127.0.0.1")
    p.add_argument("--port", type = int, default = 9999)
    p.add_argument("--id", type = int, choises = [0,1], required = True, help = "Your player ID: 0 or 1")
    args = p.parse_args()

    app = YahtzeeGUI(mode="join", host=args.host, port=args.port, player_id = args.id)
    app.mainloop()