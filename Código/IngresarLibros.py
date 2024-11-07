from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QLineEdit, QComboBox, QGridLayout
from BasedeDatosBiblioteca import BasedeDatos as bdt
from Objetosparabases import *
from Dialogos import *

bd = bdt()
class IngresarLibroDialog(QDialog):
    """
    Clase para la ventana de ingreso de libros a la biblioteca
    Args:
        QDialog (QWidget): Clase base para las ventanas de diálogo de la aplicación
    """
    def __init__(self, padre):
        super().__init__()
        self.parent = padre
        
        self.setWindowTitle("Ingresar Libro")
        self.setMaximumSize(800, 600)

        self.contenedorMain = QGridLayout()

        self.etiqueta_titulo = QLabel("Título:")
        self.entrada_titulo = QLineEdit()

        self.etiqueta_editorial = QLabel("Editorial:")
        self.entrada_editorial = QComboBox()
        if bd.obtenerEditoriales():
            for editorial in bd.obtenerEditoriales():
                self.entrada_editorial.addItem(editorial[0])
        
        botonEditorialNuevo = QPushButton("+")
        botonEditorialNuevo.setFixedSize(30, 30)
        botonEditorialNuevo.clicked.connect(self.ingresarEditorial)

        self.etiqueta_anio_publicacion = QLabel("Año de Publicación:")
        self.entrada_anio_publicacion = QLineEdit()

        self.etiqueta_isbn = QLabel("ISBN:")
        self.entrada_isbn = QLineEdit()
        self.entrada_isbn.setMaxLength(14)
        self.entrada_isbn.textChanged.connect(lambda: self.formatoISBN(self.entrada_isbn.text()))
        
        self.etiqueta_genero = QLabel("Género:")
        self.entrada_genero = QComboBox()
        if bd.consultarGeneros:
            for genero in bd.consultarGeneros():
                self.entrada_genero.addItem(genero[0])
                
        botonGeneroNuevo = QPushButton("+")
        botonGeneroNuevo.setFixedSize(30, 30)
        botonGeneroNuevo.clicked.connect(self.ingresarGenero)
        
        self.otrosAutores = QLabel("Autores:")
        self.autoresActuales = QComboBox()
        if bd.obtenerAutores():
            for autor in bd.obtenerAutores():
                self.autoresActuales.addItem(autor[0])
        
        botonAutorNuevo = QPushButton("+")
        botonAutorNuevo.setFixedSize(30, 30)
        botonAutorNuevo.clicked.connect(self.ingresarAutor)
        
        self.cantidad_disponible = QLabel("Cantidad Disponible:")
        self.entrada_cantidad_disponible = QLineEdit()

        self.boton_guardar = QPushButton("Guardar")
        self.boton_guardar.clicked.connect(self.guardar)

        self.contenedorMain.addWidget(self.etiqueta_titulo, 0, 0, 1, 1)
        self.contenedorMain.addWidget(self.entrada_titulo, 0, 1, 1, 1)
        self.contenedorMain.addWidget(self.etiqueta_editorial, 1, 0, 1, 1)
        self.contenedorMain.addWidget(self.entrada_editorial, 1, 1, 1, 1)
        self.contenedorMain.addWidget(botonEditorialNuevo, 1, 2, 1, 1)
        self.contenedorMain.addWidget(self.etiqueta_anio_publicacion, 2, 0, 1, 1)
        self.contenedorMain.addWidget(self.entrada_anio_publicacion, 2, 1, 1, 1)
        self.contenedorMain.addWidget(self.etiqueta_isbn, 3, 0, 1, 1)
        self.contenedorMain.addWidget(self.entrada_isbn, 3, 1, 1, 1)
        self.contenedorMain.addWidget(self.etiqueta_genero, 4, 0, 1, 1)
        self.contenedorMain.addWidget(self.entrada_genero, 4, 1, 1, 1)
        self.contenedorMain.addWidget(botonGeneroNuevo, 4, 2, 1, 1)
        self.contenedorMain.addWidget(self.otrosAutores, 5, 0, 1, 1)
        self.contenedorMain.addWidget(self.autoresActuales, 5, 1, 1, 1)
        self.contenedorMain.addWidget(botonAutorNuevo, 5, 2, 1, 1)
        self.contenedorMain.addWidget(self.cantidad_disponible, 6, 0, 1, 1)
        self.contenedorMain.addWidget(self.entrada_cantidad_disponible, 6, 1, 1, 1)
        self.contenedorMain.addWidget(self.boton_guardar, 7, 0, 1, 2)

        self.setLayout(self.contenedorMain)
        self.setModal(True)
        
    def formatoISBN(self, isbn):
        """
        Dar formato al ISBN

        Returns:
            str: ISBN formateado
        """
        if len(self.entrada_isbn.text()) == 14:
            self.entrada_isbn.setText(f"{isbn[:3]}-{isbn[4:]}")
        
    def ingresarAutor(self):
        """
        Función para ingresar un autor a la base de datos
        """
        dialogoAutor = AutorNuevo(self)
        if dialogoAutor.exec_() == 1:
            if bd.obtenerAutores():
                self.autoresActuales.clear()
                autores = bd.obtenerAutores()
                for i in range(len(autores)):
                    self.autoresActuales.insertItem(0, autores[i][0])
            self.autoresActuales.setCurrentIndex(0)
        
    def verificarCampos(self):
        """
        Verficar que los campos no estén vacíos o tengan datos erroneos

        Returns:
            Bool: Regresa verdadero si los campos están correctos, falso si no lo están
        """
        if self.entrada_titulo.text() == "" or self.entrada_anio_publicacion.text() == "" or self.entrada_isbn.text() == "" or self.entrada_genero.currentText() == "" or self.entrada_cantidad_disponible.text() == "":
            return False
        if self.cantidad_disponible.text() == "" or not self.entrada_cantidad_disponible.text().isdigit():
            return False
        return True

    def guardar(self):
        """
        Función para guardar un libro en la base de datos
        """
        if not self.verificarCampos():
            print("Campos vacíos o incorrectos.")
            return
        titulo = self.entrada_titulo.text()
        editorial = self.entrada_editorial.currentText()
        anio_publicacion = self.entrada_anio_publicacion.text()
        isbn = self.entrada_isbn.text()
        autor = Autor(nombre=self.autoresActuales.currentText())
        genero = self.entrada_genero.currentText()
        cantidad_disponible = self.entrada_cantidad_disponible.text()
        libro = Libro(None, titulo, editorial, anio_publicacion, isbn, genero, cantidad_disponible)
        if bd.insertarLibro(libro, autor):
            self.close()
            self.parent.statusBar().showMessage("Libro ingresado con éxito.")
        else:
            self.parent.statusBar().showMessage("Error al ingresar libro. Verifica los datos.")
            self.close()
            print("Error al ingresar libro.")
            return
        
    def ingresarEditorial(self):
        """
        Función para ingresar una editorial a la base de datos
        """
        dialogoEditorial = EditorialNuevo(self)
        if dialogoEditorial.exec_() == 1:
            if bd.obtenerEditoriales():
                self.entrada_editorial.clear()
                editoriales = bd.obtenerEditoriales()
                for i in range(len(editoriales)):
                    self.entrada_editorial.insertItem(0, editoriales[i][0])
            self.entrada_editorial.setCurrentIndex(0)
    
    def ingresarGenero(self):
        """
        Función para ingresar un género a la base de datos
        """
        dialogoGenero = GeneroNuevo(self)
        if dialogoGenero.exec_() == 1:
            if bd.consultarGeneros():
                self.entrada_genero.clear()
                generos = bd.consultarGeneros()
                for i in range(len(generos)):
                    self.entrada_genero.insertItem(0, generos[i][0])
            self.entrada_genero.setCurrentIndex(0)	