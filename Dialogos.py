from PySide6.QtWidgets import QDialog, QLabel, QPushButton, QLineEdit, QVBoxLayout, QComboBox, QListView, QListWidget, QStatusBar
from PySide6.QtGui import QFont
from BasedeDatosBiblioteca import BasedeDatos as bdt
from Objetosparabases import *

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

class AutorNuevo(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFont("Segoe UI")
        self.setWindowTitle("Añadir Autoes")
        self.setGeometry(200, 100, 600, 100)
        layout = QVBoxLayout()
        
        etiqueta = QLabel("Verifica que el autor por añadir no se encuentre en registrado. \nAutores:")
        self.muestraAutores = QListWidget()
        if bd.obtenerAutores():
            for autor in bd.obtenerAutores():
                self.muestraAutores.addItem(autor[0])
        
        self.entrada = QLineEdit()
        self.entrada.setToolTip("Ingrese el nombre del autor")
        self.boton = QPushButton("Aceptar")
        self.boton.clicked.connect(self.aceptar)

        self.boton2 = QPushButton("Cancelar")
        self.boton2.clicked.connect(self.cancelar)
        
        layout.addWidget(etiqueta)
        layout.addWidget(self.muestraAutores)
        layout.addWidget(QLabel("Nombre del autor:"))
        layout.addWidget(self.entrada)
        layout.addWidget(self.boton)
        layout.addWidget(self.boton2)
        
        self.setLayout(layout)

    def aceptar(self):
        try:
            nombre = self.entrada.text()
            autor = Autor(nombre)
            bd.registrarAutor(autor)
            self.autorAgregado = autor
            self.accept()
        except Exception as e:
            print("Error: ", e)
            self.reject()

    def cancelar(self):
        self.reject()
        
class EditorialNuevo(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFont("Segoe UI")
        self.setWindowTitle("Añadir Editorial")
        self.setGeometry(200, 100, 600, 100)
        layout = QVBoxLayout()
        
        etiqueta = QLabel("Verifica que la editorial por añadir no se encuentre en registrado. \nEditoriales:")
        self.muestraEditoriales = QListWidget()
        if bd.obtenerEditoriales():
            for editorial in bd.obtenerEditoriales():
                self.muestraEditoriales.addItem(editorial[0])
        
        self.entrada = QLineEdit()
        self.entrada.setToolTip("Ingrese el nombre de la editorial")
        self.boton = QPushButton("Aceptar")
        self.boton.clicked.connect(self.aceptar)

        self.boton2 = QPushButton("Cancelar")
        self.boton2.clicked.connect(self.cancelar)
        
        layout.addWidget(etiqueta)
        layout.addWidget(self.muestraEditoriales)
        layout.addWidget(QLabel("Nombre de la editorial:"))
        layout.addWidget(self.entrada)
        layout.addWidget(self.boton)
        layout.addWidget(self.boton2)
        
        self.setLayout(layout)

    def aceptar(self):
        try:
            nombre = self.entrada.text()
            bd.registrarEditorial(nombre)
            self.editorialAgregada = nombre
            self.accept()
        except Exception as e:
            print("Error: ", e)
            self.reject()

    def cancelar(self):
        self.reject()
        
class GeneroNuevo(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFont("Segoe UI")
        self.setWindowTitle("Añadir Género")
        self.setGeometry(200, 100, 600, 100)
        layout = QVBoxLayout()
        
        etiqueta = QLabel("Verifica que el género por añadir no se encuentre en registrado. \nGéneros:")
        self.muestraGeneros = QListWidget()
        if bd.consultarGeneros():
            for genero in bd.consultarGeneros():
                self.muestraGeneros.addItem(genero[0])
        
        self.entrada = QLineEdit()
        self.entrada.setToolTip("Ingrese el nombre del género")
        self.boton = QPushButton("Aceptar")
        self.boton.clicked.connect(self.aceptar)

        self.boton2 = QPushButton("Cancelar")
        self.boton2.clicked.connect(self.cancelar)
        
        layout.addWidget(etiqueta)
        layout.addWidget(self.muestraGeneros)
        layout.addWidget(QLabel("Nombre del género:"))
        layout.addWidget(self.entrada)
        layout.addWidget(self.boton)
        layout.addWidget(self.boton2)
        
        self.setLayout(layout)

    def aceptar(self):
        try:
            nombre = self.entrada.text()
            bd.registrarGenero(nombre)
            self.generoAgregado = nombre
            self.accept()
        except Exception as e:
            print("Error: ", e)
            self.reject()

    def cancelar(self):
        self.reject()

class EditarAutor(QDialog):
    def __init__(self, padre, autor: Autor):
        super().__init__(padre)
        self.parent = padre
        self.setModal(True)
        
        self.setFont("Segoe UI")
        self.setWindowTitle("Editar Autor")
        self.setGeometry(200, 100, 600, 100)
        layout = QVBoxLayout()
        
        self.autor = autor
        self.entrada = QLineEdit()
        self.entrada.setText(autor.nombre)
        self.entrada.setToolTip(self.autor.nombre)
        self.boton = QPushButton("Aceptar")
        self.boton.clicked.connect(self.aceptar)
        
        layout.addWidget(QLabel("Nombre del autor:"))
        layout.addWidget(self.entrada)
        layout.addWidget(self.boton)
        
        self.setLayout(layout)

    def aceptar(self):
        try:
            nombre = self.entrada.text()
            self.autor.nombre = nombre
            bd.actualizarAutor(self.autor.nombre, nombre)
            self.parent.statusBar().showMessage("Autor actualizado")
            self.accept()
            
        except Exception as e:
            print("Error: ", e)
            self.reject()
            
class EditarEditorial(QDialog):
    def __init__(self, padre, editorial: str):
        super().__init__(padre)
        self.parent = padre
        self.setModal(True)
        
        self.setFont("Segoe UI")
        self.setWindowTitle("Editar Editorial")
        self.setGeometry(200, 100, 600, 100)
        layout = QVBoxLayout()
        
        self.editorial = editorial
        self.entrada = QLineEdit()
        self.entrada.setText(editorial)
        self.entrada.setToolTip(self.editorial)
        self.boton = QPushButton("Aceptar")
        self.boton.clicked.connect(self.aceptar)

        layout.addWidget(QLabel("Nombre de la editorial:"))
        layout.addWidget(self.entrada)
        layout.addWidget(self.boton)
        
        self.setLayout(layout)

    def aceptar(self):
        try:
            nombre = self.entrada.text()
            bd.actualizarEditorial(self.editorial, nombre)
            self.parent.statusBar().showMessage("Editorial actualizada")
            self.accept()
        except Exception as e:
            print("Error: ", e)
            self.reject() 

class EditarGenero(QDialog):
    def __init__(self, padre, genero: str):
        super().__init__(padre)
        self.parent = padre
        self.setModal(True)
        
        self.setFont("Segoe UI")
        self.setWindowTitle("Editar Género")
        self.setGeometry(200, 100, 600, 100)
        layout = QVBoxLayout()
        
        self.genero = genero
        self.entrada = QLineEdit()
        self.entrada.setText(genero)
        self.entrada.setToolTip(self.genero)
        self.boton = QPushButton("Aceptar")
        self.boton.clicked.connect(self.aceptar)
        
        layout.addWidget(QLabel("Nombre del género:"))
        layout.addWidget(self.entrada)
        layout.addWidget(self.boton)
        
        self.setLayout(layout)

    def aceptar(self):
        try:
            nombre = self.entrada.text()
            bd.actualizarGenero(self.genero, nombre)
            self.parent.statusBar().showMessage("Género actualizado")
            self.accept()
            
        except Exception as e:
            print("Error: ", e)
            self.reject()

class MostrarLibro(QDialog):
    def __init__(self, parent, libro: Libro):
        super().__init__(parent)
        self.parent = parent
        self.setModal(True)
        self.libro = libro
        
        self.setFont("Segoe UI")
        self.setWindowTitle("Información del libro")
        self.setGeometry(200, 100, 400, 100)
        layout = QVBoxLayout()
        
        self.etiqueta_titulo = QLabel(f"Título: {libro.nombre}")
        self.etiqueta_editorial = QLabel(f"Editorial: {libro.editorial}")
        self.etiqueta_anio_publicacion = QLabel(f"Año de Publicación: {libro.anio_publicacion}")
        self.etiqueta_isbn = QLabel(f"ISBN: {libro.ISBN}")
        self.etiqueta_genero = QLabel(f"Género: {bd.consultarGeneroPorLibro(libro)}")
        self.etiqueta_cantidad_disponible = QLabel(f"Cantidad Disponible: {libro.cantidad_disponible}")
        
        layout.addWidget(self.etiqueta_titulo)
        layout.addWidget(self.etiqueta_editorial)
        layout.addWidget(self.etiqueta_anio_publicacion)
        layout.addWidget(self.etiqueta_isbn)
        layout.addWidget(self.etiqueta_genero)
        layout.addWidget(self.etiqueta_cantidad_disponible)
        
        self.setLayout(layout)
        self.setFont(QFont("Times New Roman", 14))
        self.setModal(True)