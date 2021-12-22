import os.path
import sys

from PyQt5 import QtWidgets

from interfaz.principal import IUPrincipal


def run():
    cwd = os.path.dirname(os.path.realpath(__file__))
    os.chdir(cwd)

    main = QtWidgets.QApplication(sys.argv)
    principal = IUPrincipal()

    principal.show()
    sys.exit(main.exec_())


if __name__ == "__main__":
    run()
