import json
import os.path
import sys

from PyQt5 import QtWidgets

from tools.tools import get_path
from ui.main import MainUi


def create_settings():
    # Create empty settings.json
    with open(get_path("resources/settings.json"), "w") as f:
        data = {"key": "", "folder": ""}
        json.dump(data, f)


def run():
    # Create settings.json if missing
    path = get_path("resources/settings.json")
    if os.path.exists(path):
        with open(path, "r") as f:
            data = json.load(f)
            if list(data.keys()) != ["key", "folder"]:
                create_settings()
    else:
        create_settings()

    # Starts MainUI
    app = QtWidgets.QApplication(sys.argv)
    ui = MainUi()
    ui.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    run()