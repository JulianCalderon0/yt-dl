import html
import json
from urllib.request import urlopen

from PyQt5 import QtCore, QtGui, QtWidgets
import helpers
from helpers import get_path

import settings


class MainUi(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # Icon Setup
        self.icon = QtGui.QIcon()
        self.icon.addPixmap(
            QtGui.QPixmap(helpers.get_path("resources/imgs/youtube.png")),
        )

        # Font Setup
        font = QtGui.QFont()
        font.setPointSize(10)

        # Main Config
        self.setObjectName("MainWindow")
        self.resize(641, 220)
        self.setWindowIcon(self.icon)

        # Central Widget
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")

        # Layout 1
        self.layout_widget_1 = QtWidgets.QWidget(self.centralwidget)
        self.layout_widget_1.setGeometry(QtCore.QRect(10, 10, 621, 31))
        self.layout_widget_1.setObjectName("layout_widget_1")
        self.layout_1 = QtWidgets.QHBoxLayout(self.layout_widget_1)
        self.layout_1.setContentsMargins(0, 0, 0, 0)
        self.layout_1.setObjectName("layout_1")

        self.input = QtWidgets.QLineEdit(self.layout_widget_1)
        self.input.setMinimumSize(QtCore.QSize(0, 21))
        self.input.setFont(font)
        self.input.setPlaceholderText("Busqueda")
        self.input.setObjectName("input")
        self.configuration = QtWidgets.QPushButton(self.layout_widget_1)
        self.configuration.setMinimumSize(QtCore.QSize(90, 0))
        self.configuration.setFont(font)
        self.configuration.setObjectName("configuration")
        self.search = QtWidgets.QPushButton(self.layout_widget_1)
        self.search.setMinimumSize(QtCore.QSize(90, 0))
        self.search.setFont(font)
        self.search.setObjectName("search")

        self.layout_1.addWidget(self.input)
        self.layout_1.addWidget(self.search)
        self.layout_1.addWidget(self.configuration)

        # Layout 2
        self.layout_widget_2 = QtWidgets.QWidget(self.centralwidget)
        self.layout_widget_2.setGeometry(QtCore.QRect(10, 50, 621, 161))
        self.layout_widget_2.setObjectName("layout_widget_2")
        self.layout_2 = QtWidgets.QHBoxLayout(self.layout_widget_2)
        self.layout_2.setContentsMargins(0, 0, 0, 0)
        self.layout_2.setObjectName("layout_2")

        self.list = QtWidgets.QListWidget(self.layout_widget_2)
        self.list.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.list.setFont(font)
        self.list.setObjectName("list")

        self.download_box_widget = QtWidgets.QWidget(self.layout_widget_2)
        self.download_box_widget.setGeometry(QtCore.QRect(10, 50, 621, 161))
        self.download_box_widget.setObjectName("download_box_widget")
        self.download_box = QtWidgets.QVBoxLayout(self.download_box_widget)
        self.download_box.setContentsMargins(0, 0, 0, 0)
        self.download_box.setObjectName("layoudownload_box")

        self.download = QtWidgets.QPushButton(self.download_box_widget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        self.download.setSizePolicy(sizePolicy)
        self.download.setMinimumSize(QtCore.QSize(90, 0))
        self.download.setFont(font)
        self.download.setObjectName("download")

        self.audio = QtWidgets.QPushButton(self.download_box_widget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        self.audio.setSizePolicy(sizePolicy)
        self.audio.setMinimumSize(QtCore.QSize(90, 0))
        self.audio.setFont(font)
        self.audio.setObjectName("audio")

        self.download_box.addWidget(self.download)
        self.download_box.addWidget(self.audio)

        self.layout_2.addWidget(self.list)
        self.layout_2.addWidget(self.download_box_widget)

        # Layout 3
        self.layout_widget_3 = QtWidgets.QWidget(self.centralwidget)
        self.layout_widget_3.setGeometry(QtCore.QRect(10, 230, 621, 191))
        self.layout_widget_3.setObjectName("layout_widget_3")
        self.layout_3 = QtWidgets.QHBoxLayout(self.layout_widget_3)
        self.layout_3.setContentsMargins(0, 0, 0, 0)
        self.layout_3.setObjectName("layout_3")

        self.thumbnail = QtWidgets.QLabel(self.layout_widget_3)
        self.thumbnail.setMaximumSize(QtCore.QSize(240, 180))
        self.thumbnail.setText("")
        self.thumbnail.setPixmap(QtGui.QPixmap(get_path("resources/imgs/default.jpg")))
        self.thumbnail.setScaledContents(True)
        self.thumbnail.setObjectName("thumbnail")
        self.description = QtWidgets.QTextBrowser(self.layout_widget_3)
        self.description.setObjectName("description")

        self.layout_3.addWidget(self.thumbnail)
        self.layout_3.addWidget(self.description)

        # End Config
        self.setCentralWidget(self.centralwidget)
        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

        # Functions
        self.input.setFocus()

        self.search.clicked.connect(self.search_button)
        self.download.clicked.connect(self.download_button)
        self.audio.clicked.connect(self.audio_button)
        self.configuration.clicked.connect(self.config_button)
        self.list.itemSelectionChanged.connect(self.selection_changed)

    def retranslateUi(self):
        # Sets GUI Text
        self.setWindowTitle("YouTube")
        self.configuration.setText("Configuracion")
        self.search.setText("Buscar")
        self.download.setText("Descargar")
        self.audio.setText("Audio")

    def search_button(self):
        # Retrieves API Key
        with open(get_path("resources/settings.json"), "r") as f:
            key = json.load(f)["key"]

        # Retrieves API Data
        q = str(self.input.text())
        if q:
            self.data = helpers.search(q, key)
            if self.data == "error":
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle("Error")
                msg.setText("Error con la clave")
                msg.setIcon(QtWidgets.QMessageBox.Critical)
                msg.setWindowIcon(self.icon)
                msg.exec_()
                return

            # Adds data to list
            self.list.clear()
            new_data = {}
            for title in self.data.keys():
                new_title = html.unescape(title)

                new_data[new_title] = self.data[title]
                self.list.addItem(new_title)
            self.data = new_data

    def download_button(self):
        if self.list.selectedItems():
            # Retrieves selected video
            with open(get_path("resources/settings.json"), "r") as f:
                download_folder = json.load(f)["folder"]

            title = self.list.selectedItems()[0].text()
            id = self.data[title]["id"]

            # Downloads video

            self.setWindowTitle("Descargando")

            helpers.download(id, download_folder)

            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle("Descarga")
            msg.setText("Descarga Completada")
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setWindowIcon(self.icon)
            msg.exec_()

            self.setWindowTitle("YouTube")

    def audio_button(self):
        if self.list.selectedItems():
            # Retrieves selected video
            with open(get_path("resources/settings.json"), "r") as f:
                download_folder = json.load(f)["folder"]

            title = self.list.selectedItems()[0].text()
            id = self.data[title]["id"]

            # Downloads video

            self.setWindowTitle("Descargando")

            helpers.download_audio(id, download_folder)

            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle("Descarga")
            msg.setText("Descarga Completada")
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setWindowIcon(self.icon)
            msg.exec_()

            self.setWindowTitle("YouTube")

    def selection_changed(self):
        if self.list.selectedItems():
            self.resize(641, 431)

            # Retrieves data
            title = self.list.selectedItems()[0].text()
            author = self.data[title]["channel"]
            date = self.data[title]["date"].replace("T", " ").replace("Z", " ")
            description = self.data[title]["description"]

            # Sets thumbnail
            url = self.data[title]["thumbnail"]["url"]
            img = urlopen(url).read()
            pixmap = QtGui.QPixmap()
            pixmap.loadFromData(img)
            self.thumbnail.setPixmap(pixmap)

            # Sets description
            with open(get_path("resources/static/description.html"), "r") as f:
                self.description.setHtml(
                    f.read().format(
                        title=title, author=author, date=date, description=description
                    )
                )
        else:
            # Resets thumbnail and description when deselect
            self.resize(641, 220)
            self.thumbnail.setPixmap(
                QtGui.QPixmap(get_path("resources/imgs/default.jpg"))
            )
            self.description.setHtml("")

    def config_button(self):
        # Open settings
        self.ui_settings = settings.SettingsUi()
        self.ui_settings.show()
