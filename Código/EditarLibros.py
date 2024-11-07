from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QStatusBar
from Objetosparabases import *
from BasedeDatosBiblioteca import BasedeDatos as bdt

bd = bdt()
class EditarLibroDialog(QDialog):
    """
    Clase para la ventana de edición de libros de la biblioteca

    Args:
        QDialog (_type_): _description_
    """
    def __init__(self, padre, libro: Libro):
        super().__init__()
        self.setWindowTitle("Editar Libro")
        self.setMaximumSize(800, 600)
        self.libro = libro
        self.parent = padre


        self.layout_editar_libro = QVBoxLayout()

        self.etiqueta_titulo = QLabel("Título:")
        self.entrada_titulo = QLineEdit()
        self.entrada_titulo.setText(str(libro.nombre))

        self.etiqueta_editorial = QLabel("Editorial:")
        self.entrada_editorial = QLineEdit()
        self.entrada_editorial.setText(str(libro.editorial))

        self.etiqueta_anio_publicacion = QLabel("Año de Publicación:")
        self.entrada_anio_publicacion = QLineEdit()
        self.entrada_anio_publicacion.setText(str(libro.anio_publicacion))

        self.etiqueta_isbn = QLabel("ISBN:")
        self.entrada_isbn = QLineEdit()
        self.entrada_isbn.setText(str(libro.ISBN))

        self.etiqueta_genero = QLabel("Género:")
        self.entrada_genero = QComboBox()
        if bd.consultarGeneros:
            for genero in bd.consultarGeneros():
                self.entrada_genero.addItem(genero[0])

        self.etiqueta_cantidad_disponible = QLabel("Cantidad Disponible:")
        self.entrada_cantidad_disponible = QLineEdit()
        self.entrada_cantidad_disponible.setText(str(libro.cantidad_disponible))
        
        self.statusbar = QStatusBar()
        self.statusbar.showMessage("Editar libro")

        self.boton_guardar = QPushButton("Guardar")
        self.boton_guardar.clicked.connect(self.guardar)

        self.layout_editar_libro.addWidget(self.etiqueta_titulo)
        self.layout_editar_libro.addWidget(self.entrada_titulo)
        self.layout_editar_libro.addWidget(self.etiqueta_editorial)
        self.layout_editar_libro.addWidget(self.entrada_editorial)
        self.layout_editar_libro.addWidget(self.etiqueta_anio_publicacion)
        self.layout_editar_libro.addWidget(self.entrada_anio_publicacion)
        self.layout_editar_libro.addWidget(self.etiqueta_isbn)
        self.layout_editar_libro.addWidget(self.entrada_isbn)
        self.layout_editar_libro.addWidget(self.etiqueta_genero)
        self.layout_editar_libro.addWidget(self.entrada_genero)
        self.layout_editar_libro.addWidget(self.etiqueta_cantidad_disponible)
        self.layout_editar_libro.addWidget(self.entrada_cantidad_disponible)
        self.layout_editar_libro.addWidget(self.boton_guardar)
        self.layout_editar_libro.addWidget(self.statusbar)

        self.setLayout(self.layout_editar_libro)
        self.setModal(True)

    def verificarCampos(self):
        """
        Función para verificar que los campos estén llenos

        Returns:
            Bool: Regresa verdadero si los campos están llenos, falso si no
        """
        if self.entrada_titulo.text() and self.entrada_editorial.text() and self.entrada_anio_publicacion.text() and self.entrada_isbn.text() and self.entrada_genero.currentText() and self.entrada_cantidad_disponible.text() and self.entrada_cantidad_disponible > 0:
            return True
        return False

    def guardar(self):
        """
        Función para guardar los cambios en la base de datos
        """
        if self.verificarCampos:
            id_libro = self.libro.id_libro
            titulo = self.entrada_titulo.text()
            editorial = self.entrada_editorial.text()
            anio_publicacion = int(self.entrada_anio_publicacion.text())
            isbn = self.entrada_isbn.text()
            genero = self.entrada_genero.currentText()
            cantidad_disponible = int(self.entrada_cantidad_disponible.text())
            
            libro = Libro(id_libro, titulo, editorial, anio_publicacion, isbn, genero, cantidad_disponible)
            bd.editarLibro(libro)
            self.accept()
        else:
            self.statusbar.showMessage("Por favor, llene todos los campos correctamente o verifique sus datos.")