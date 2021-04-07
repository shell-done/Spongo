from PySide2.QtCore import QFile, QIODevice, QTextStream, Qt, Slot
from PySide2.QtGui import QPixmap
from PySide2.QtWidgets import QComboBox, QGridLayout, QHBoxLayout, QLabel, QMessageBox, QTextEdit, QWidget, QTabWidget, QVBoxLayout

class AboutMessageBox(QMessageBox):
    @staticmethod
    def show(parent: QWidget = None):
        about_dialog = AboutMessageBox(parent)
        about_dialog.exec_()

    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)

        self.setWindowTitle("A propos")
        self.setIconPixmap(QPixmap(":/img/spongo_logo.png").scaledToWidth(100, Qt.SmoothTransformation))

        title = QLabel("A propos de Spongo")
        title.setObjectName("about-title")
        self.layout().addWidget(title, 0, 2)

        tab_widget = QTabWidget(self)
        tab_widget.addTab(self._appTab(), "L'application")
        tab_widget.addTab(self._dependenciesTab(), "Dépendances")
        tab_widget.setFixedSize(600, 460)
        tab_font = tab_widget.tabBar().font()
        tab_font.setPointSize(12)
        tab_widget.tabBar().setFont(tab_font)

        self.layout().addWidget(tab_widget, 1, 2)


    def _appTab(self) -> QWidget:
        tab = QWidget(self)
        tab.setObjectName("about-tab")

        layout = QVBoxLayout(tab)
        layout.setAlignment(Qt.AlignTop)


        intro = (
            "Cette application a été réalisée par Margaux DOUDET et Alexandre THOMAS dans le cadre d'un projet en M1 à l'ISEN Yncréa Brest. "
            "Ce programme a été développé pour et en collaboration avec l'institut français de recherche et d'exploitation de la mer (Ifremer)."
        )

        context = (
            "L'objectif de cet outil est d'effectuer une analyse sur un dossier d'images de fonds marins. Durant l'analyse, le programme cherche "
            "à identifier les éponges marines visibles et les classifier selon 6 morphotypes : Ball, Vase, Corona, Crown, Red et Grey_white. Une "
            "fois l'analyse terminée, les données récoltées peuvent être exportées selon différents formats afin d'être exploitée pour des "
            "recherches scientifiques."
        )

        implementation = (
            "La détection et la classification des éponges est réalisée grâce au réseau de neurone Yolov4 entrainé sur environ 250 images "
            "de chaque morphotype. Ce réseau a ensuite été implémenté dans l'outil grâce à la library PyTorch. L'interface de l'application "
            "a quant à elle été réalisée avec le framework PySide2. Pour plus d'informations sur les autres dépendances, se référer à l'onglet "
            "\"Dépendances\"."
        )

        license = (
            "Ce projet est mis à disposition sous licence MIT. "
            "Pour plus d'informations, se référer au dépôt GitHub du projet : <a href='https://github.com/shell-done/Spongo_IHM'>https://github.com/shell-done/Spongo_IHM</a>."
        )

        title = QLabel("A propos")
        title.setAlignment(Qt.AlignJustify)
        title.setObjectName("tab-title")
        layout.addWidget(title)

        parts = [intro, context, implementation, license]
        for p in parts:
            label = QLabel(p)
            label.setAlignment(Qt.AlignJustify)
            label.setWordWrap(True)

            layout.addWidget(label)

        return tab

    def _dependenciesTab(self) -> QWidget:
        tab = QWidget(self)
        tab.setObjectName("about-tab")

        layout = QVBoxLayout(tab)
        layout.setAlignment(Qt.AlignTop)

        # add link and version
        dependencies = {
            "PySide2": {
                "version": "5.15.2",
                "author": "Qt for Python Team",
                "link": "https://www.pyside.org",
                "license": "LGPL v3",
                "license-file": "pyside2.txt"
            },
            "PyTorch": {
                "version": "1.8.1+cu102",
                "author": "PyTorch Team",
                "link": "https://pytorch.org/",
                "license": "BSD-3",
                "license-file": "pytorch.txt"
            },
            "OpenCV Python": {
                "version": "4.5.1.48",
                "author": "Olli-Pekka Heinisuo",
                "link": "https://github.com/skvark/opencv-python",
                "license": "MIT",
                "license-file": "opencv-python.txt"
            },
            "NumPy": {
                "version": "1.20.2",
                "author": "Travis E. Oliphant et al.",
                "link": "https://www.numpy.org",
                "license": "BSD-3",
                "license-file": "numpy.txt"
            },
            "YoloV4": {
                "version": "N/A",
                "author": "Alexey Bochkovskiy, Chien-Yao Wang, Hong-Yuan Mark Liao",
                "link": "https://github.com/AlexeyAB/darknet",
                "license": "Unlicense",
                "license-file": "yolov4.txt"
            },
            "Pytorch-YOLOv4": {
                "version": "N/A",
                "author": "Tianxiaomo, ersheng-ai",
                "link": "https://github.com/Tianxiaomo/pytorch-YOLOv4",
                "license": "Apache-2.0",
                "license-file": "pytorch-yolov4.txt"
            },
            "dict2xml": {
                "version": "1.7.0",
                "author": "Stephen Moore",
                "link": "http://github.com/delfick/python-dict2xml",
                "license": "MIT",
                "license-file": "dict2xml.txt"
            }
        }

        dependencies_title = QLabel("Dépendances :")
        dependencies_title.setObjectName("tab-title")

        self._dependencies_list = QComboBox(self)
        for name, data in dependencies.items():
            self._dependencies_list.addItem(name, data)
        self._dependencies_list.currentIndexChanged.connect(self._dependenciesComboBoxChanged)

        dependencies_list_layout = QVBoxLayout()
        dependencies_list_layout.addWidget(self._dependencies_list)
        dependencies_list_layout.setContentsMargins(5, 0, 5, 5)

        version_layout = QHBoxLayout()
        version_layout.setAlignment(Qt.AlignLeft)
        version_title = QLabel("Version :")
        version_title.setObjectName("dependency-info")
        self._version = QLabel()
        version_layout.addWidget(version_title)
        version_layout.addWidget(self._version, 1)

        license_layout = QHBoxLayout()
        license_layout.setAlignment(Qt.AlignLeft)
        license_title = QLabel("License :")
        license_title.setObjectName("dependency-info")
        self._license = QLabel()
        license_layout.addWidget(license_title)
        license_layout.addWidget(self._license, 1)

        author_layout = QHBoxLayout()
        author_title = QLabel("Auteur(s) :")
        author_title.setObjectName("dependency-info")
        self._author = QLabel()
        author_layout.addWidget(author_title)
        author_layout.addWidget(self._author, 1)

        link_layout = QHBoxLayout()
        link_layout.setAlignment(Qt.AlignLeft)
        link_title = QLabel("Lien :")
        link_title.setObjectName("dependency-info")
        self._link = QLabel()
        link_layout.addWidget(link_title)
        link_layout.addWidget(self._link, 1)

        dependency_info = QGridLayout()
        dependency_info.setVerticalSpacing(0)
        dependency_info.addLayout(version_layout, 0, 0)
        dependency_info.addLayout(license_layout, 0, 1)
        dependency_info.addLayout(author_layout, 1, 0, 1, 2)
        dependency_info.addLayout(link_layout, 2, 0, 1, 2)

        licenses_title = QLabel("Licence :")
        licenses_title.setObjectName("tab-title")

        self._license_area = QTextEdit(self)
        self._license_area.setReadOnly(True)
        self._license_area.setObjectName("license-file")
        license_area_layout = QVBoxLayout()
        license_area_layout.addWidget(self._license_area)
        license_area_layout.setContentsMargins(5, 0, 5, 5)

        layout.addWidget(dependencies_title)
        layout.addLayout(dependencies_list_layout)
        layout.addLayout(dependency_info)
        layout.addWidget(licenses_title)
        layout.addLayout(license_area_layout)

        self._dependenciesComboBoxChanged(0)

        return tab
    
    @Slot(int)
    def _dependenciesComboBoxChanged(self, idx: int):
        data = self._dependencies_list.currentData()
        self._version.setText(data["version"])
        self._license.setText(data["license"])
        self._author.setText(data["author"])
        self._link.setText("<a href='%s'>%s</a>" % (data["link"], data["link"]))

        license_file = QFile(":/documents/licenses/%s" % data["license-file"])
        text = ""
        if license_file.open(QIODevice.ReadOnly | QFile.Text):
            text = QTextStream(license_file).readAll()
            license_file.close()

        self._license_area.setText(text)