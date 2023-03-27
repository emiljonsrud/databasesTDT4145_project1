#/usr/bin/python3
from Application import App

def main() -> None:
    app = App("norwegian_rail.db", erase=True)
    app.run()

if __name__=="__main__":
    main()
