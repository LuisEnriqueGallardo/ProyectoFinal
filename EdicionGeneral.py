from PySide6.QtWidgets import (QApplication, QComboBox, QMainWindow, QGridLayout,QPushButton, 
                                QVBoxLayout, QWidget, QTreeWidget, QStatusBar, QTreeWidgetItem, QScrollArea, QMessageBox, QLabel)
from BasedeDatosBiblioteca import BasedeDatos as bdt


class EdicionDeDatosGenerales(QMainWindow):
    """
    Clase que muestra todos los datos de la biblioteca y permite editarlos en caso de ser necesario.

    Args:
        QMainWindow (class): Clase base de la ventana principal de la aplicación.
    """
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Edición de datos generales")
        self.setGeometry(100, 100, 800, 600)
        
        # Menu de la ventana
        self.combo = QComboBox()
        self.combo.addItem("Libros")
        self.combo.addItem("Autores")
        self.combo.addItem("Editoriales")
        self.combo.addItem("Categorías")
        self.combo.addItem("Usuarios")
        self.combo.currentIndexChanged.connect(self.cargarDatos)