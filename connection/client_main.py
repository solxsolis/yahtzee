import argparse
from gui.yahtzee_gui import YahtzeeGUI

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument("--host", default = "127.0.0.1")
    p.add_argument("--port", type = int, default = 9999)
    args = p.parse_args()

    app = YahtzeeGUI(mode="network", host=args.host, port=args.port)
    app.mainloop()