from PySide6.QtWidgets import QApplication, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QGridLayout

class IngresarLibroDialog:
    def __init__(self):
        self.dialog = QDialog()
        self.dialog.setWindowTitle("Ingresar Libro")
        self.dialog.setMaximumSize(800, 600)

        self.layout_ingresar_libro = QVBoxLayout()

        self.etiqueta_titulo = QLabel("Título:")
        self.entrada_titulo = QLineEdit()

        self.etiqueta_editorial = QLabel("Editorial:")
        self.entrada_editorial = QLineEdit()

        self.etiqueta_anio_publicacion = QLabel("Año de Publicación:")
        self.entrada_anio_publicacion = QLineEdit()

        self.etiqueta_isbn = QLabel("ISBN:")
        self.entrada_isbn = QLineEdit()

        self.etiqueta_genero = QLabel("Género:")
        self.entrada_genero = QLineEdit()

        self.etiqueta_autores = QLabel("Autores:")
        self.entrada_autores = QLineEdit()

        self.boton_agregar_autor = QPushButton("Agregar Autor")
        self.boton_agregar_autor.clicked.connect(self.agregar_autor)

        self.boton_guardar = QPushButton("Guardar")
        self.boton_guardar.clicked.connect(self.guardar)

        self.layout_ingresar_libro.addWidget(self.etiqueta_titulo)
        self.layout_ingresar_libro.addWidget(self.entrada_titulo)
        self.layout_ingresar_libro.addWidget(self.etiqueta_editorial)
        self.layout_ingresar_libro.addWidget(self.entrada_editorial)
        self.layout_ingresar_libro.addWidget(self.etiqueta_anio_publicacion)
        self.layout_ingresar_libro.addWidget(self.entrada_anio_publicacion)
        self.layout_ingresar_libro.addWidget(self.etiqueta_isbn)
        self.layout_ingresar_libro.addWidget(self.entrada_isbn)
        self.layout_ingresar_libro.addWidget(self.etiqueta_genero)
        self.layout_ingresar_libro.addWidget(self.entrada_genero)

        # Creamos un QHBoxLayout para alinear horizontalmente el campo de autor y el botón "Agregar Autor"
        layout_autor = QHBoxLayout()
        layout_autor.addWidget(self.etiqueta_autores)
        layout_autor.addWidget(self.entrada_autores)
        layout_autor.addWidget(self.boton_agregar_autor)

        self.layout_ingresar_libro.addLayout(layout_autor)
        self.layout_ingresar_libro.addWidget(self.boton_guardar)

        self.dialog.setLayout(self.layout_ingresar_libro)
        self.dialog.setModal(True)
    
    def agregar_autor(self):
        autor = self.entrada_autores.text()
        # Aquí puedes agregar la lógica para guardar el autor en una lista o en la base de datos

    def guardar(self):
        titulo = self.entrada_titulo.text()
        editorial = self.entrada_editorial.text()
        anio_publicacion = self.entrada_anio_publicacion.text()
        isbn = self.entrada_isbn.text()
        genero = self.entrada_genero.text()
        autores = self.entrada_autores.text()
        # Aquí puedes agregar la lógica para guardar el libro en la base de datos


if __name__ == "__main__":
    app = QApplication([])
    dialog = IngresarLibroDialog()
    dialog.dialog.show()
    app.exec_()