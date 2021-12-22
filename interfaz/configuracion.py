from PyQt5 import QtCore, QtGui, QtWidgets

import json


class IUConfiguracion(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.icon = QtGui.QIcon()
        self.icon.addPixmap(
            QtGui.QPixmap("recursos/imagenes/engranaje.png"),
        )

        self.setObjectName("settings")
        self.resize(471, 111)
        self.setWindowIcon(self.icon)

        # LAYOUT 1

        self.layout_widget1 = QtWidgets.QWidget(self)
        self.layout_widget1.setGeometry(QtCore.QRect(10, 0, 451, 71))
        self.layout_widget1.setObjectName("layout_widget1")
        self.layout1 = QtWidgets.QFormLayout(self.layout_widget1)
        self.layout1.setFormAlignment(QtCore.Qt.AlignCenter)
        self.layout1.setContentsMargins(0, 0, 0, 0)
        self.layout1.setHorizontalSpacing(10)
        self.layout1.setVerticalSpacing(15)
        self.layout1.setObjectName("layout1")

        self.key_label = QtWidgets.QLabel(self.layout_widget1)
        self.key_label.setObjectName("key_label")

        self.key_input = QtWidgets.QLineEdit(self.layout_widget1)
        self.key_input.setMinimumSize(QtCore.QSize(0, 21))
        self.key_input.setObjectName("key_input")

        self.folder_label = QtWidgets.QLabel(self.layout_widget1)
        self.folder_label.setObjectName("folder_label")

        self.folder_layout = QtWidgets.QHBoxLayout()
        self.folder_layout.setSpacing(6)
        self.folder_layout.setObjectName("folder_layout")

        self.folder_input = QtWidgets.QLineEdit(self.layout_widget1)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed
        )
        self.folder_input.setSizePolicy(sizePolicy)
        self.folder_input.setMinimumSize(QtCore.QSize(0, 21))
        self.folder_input.setText("")
        self.folder_input.setObjectName("folder_input")

        self.browse = QtWidgets.QPushButton(self.layout_widget1)
        self.browse.setMinimumSize(QtCore.QSize(0, 20))
        self.browse.setObjectName("browse")

        self.folder_layout.addWidget(self.folder_input)
        self.folder_layout.addWidget(self.browse)

        self.layout1.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.key_label)
        self.layout1.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.key_input)
        self.layout1.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.folder_label)
        self.layout1.setLayout(1, QtWidgets.QFormLayout.FieldRole, self.folder_layout)

        # LAYOUT 2

        self.layout_widget2 = QtWidgets.QWidget(self)
        self.layout_widget2.setGeometry(QtCore.QRect(10, 80, 451, 25))
        self.layout_widget2.setObjectName("layout_widget2")
        self.layout2 = QtWidgets.QHBoxLayout(self.layout_widget2)
        self.layout2.setContentsMargins(0, 0, 0, 0)
        self.layout2.setObjectName("layout2")

        spacerItem = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.save = QtWidgets.QPushButton(self.layout_widget2)
        self.save.setObjectName("save")

        self.layout2.addItem(spacerItem)
        self.layout2.addWidget(self.save)

        self.nombrar(self)
        QtCore.QMetaObject.connectSlotsByName(self)

        self.save.clicked.connect(self.guardar)
        self.browse.clicked.connect(self.navegar)

    def nombrar(self, Form):
        Form.setWindowTitle("Configuracion")
        self.save.setText("Guardar")
        self.key_label.setText("Clave del API:")
        self.folder_label.setText("Carpeta de Descarga:")
        self.browse.setText("...")

        with open("recursos/configuracion.json", "r") as f:
            data = json.load(f)

        key = data["clave"]
        download_folder = data["carpeta"]

        self.key_input.setText(key)
        self.folder_input.setText(download_folder)

    def guardar(self):
        # Saves data to settings.json
        data = {"clave": self.key_input.text(), "carpeta": self.folder_input.text()}
        with open("recursos/configuracion.json", "w") as f:
            json.dump(data, f)

        self.close()

    def navegar(self):
        # Selects download folder
        download_folder = QtWidgets.QFileDialog.getExistingDirectory(
            None,
            "Abrir carpeta de descarga",
            "",
            QtWidgets.QFileDialog.ShowDirsOnly,
        )
        self.folder_input.setText(download_folder)
