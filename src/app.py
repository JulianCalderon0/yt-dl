import json
import os.path
import sys

from PyQt5 import QtWidgets

from main import MainUi
from tools import create_settings, get_path


def run():
    cwd = os.path.dirname(os.path.realpath(__file__))
    os.chdir(cwd)

    app = QtWidgets.QApplication(sys.argv)
    ui = MainUi()
    ui.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    run()
