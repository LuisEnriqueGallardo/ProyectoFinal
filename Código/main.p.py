from functools import partial
import sys
from PySide6.QtWidgets import (QApplication, QComboBox, QMainWindow, QGridLayout,QPushButton, 
                                QVBoxLayout, QWidget, QTreeWidget, QStatusBar, QTreeWidgetItem, QScrollArea, QMessageBox, QLabel)
from PySide6.QtCore import Qt
from PySide6.QtGui import QShortcut, QKeySequence, QFont
from Objetosparabases import *
from BasedeDatosBiblioteca import BasedeDatos as bdt
from Login import LoginWindow
from IngresarLibros import IngresarLibroDialog
from Dialogos import *

bd = bdt()
global sesionIniciada
sesionIniciada = False
fuente = QFont("Arial", 12)
        
class VentanaPrincipal(QMainWindow):
    def __init__(self):
        """Constructor de la clase VentanaPrincipal
        Inicializa la ventana principal de la aplicación
        """
        super().__init__()
        self.setWindowTitle("Biblioteca")
        self.setMinimumSize(1280, 720)
        self.arbol = QTreeWidget()
        self.sesion = None
        
        widgetPrincipal = QWidget()
        
        self.contenedorPrincipal = QGridLayout()
        
        login = QShortcut(QKeySequence("F1"), self)
        login.activated.connect(self.login)
        
        self.AtajoEditar = QShortcut(QKeySequence("F2"), self)
        
        self.menuSuperior = self.menuBar()
        self.menuArchivo = self.menuSuperior.addMenu("Insertar")
        self.menuEditar = self.menuSuperior.addMenu("Editar")
        
        self.borrar = QShortcut(QKeySequence(Qt.Key_Delete), self)
                
        self.menuPrincipal = QComboBox()
        elementosMenu = ["Libros", "Editorial", "Generos", "Autores"]
        
        for elemento in elementosMenu:
            self.menuPrincipal.addItem(elemento)
        
        self.contenedorCentral = QVBoxLayout()
        self.contenedorLateral = QVBoxLayout()
        
        self.scrollArea = QScrollArea()
        self.scrollArea.setFixedSize(400, 700)
        self.scrollArea.setWidgetResizable(True)
        
        # Creamos un widget contenedor para los botones
        self.buttonWidget = QWidget()
        self.buttonLayout = QVBoxLayout(self.buttonWidget)
        
        self.scrollArea.setWidget(self.buttonWidget)  # Agregamos el widget contenedor al QScrollArea
                
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)
        self.statusbar.showMessage("Bienvenido a la biblioteca")

        self.menuPrincipal.currentTextChanged.connect(lambda: self.actualizarInterfaz(self.menuPrincipal.currentText()))
        
        self.etiquetaPrincipal = QLabel()

        self.contenedorPrincipal.addWidget(self.menuPrincipal, 0, 0)
        self.contenedorPrincipal.addWidget(self.etiquetaPrincipal, 0, 1, 1, 3)
        # self.contenedorPrincipal.addWidget(botonLogin, 0, 3)
        self.contenedorPrincipal.addWidget(self.scrollArea, 1, 0)  # Agregamos el QScrollArea en lugar del QVBoxLayout
        self.contenedorPrincipal.addLayout(self.contenedorCentral, 1, 1, 1, 3)
        widgetPrincipal.setLayout(self.contenedorPrincipal)
        self.setCentralWidget(widgetPrincipal)
        
        self.actualizarInterfaz("Libros")
        self.ultimoIndex = None

    def actualizarInterfaz(self, current):
        """
        Actualiza la interfaz de la ventana principal

        Args:
            current: str - El índice del menú principal
        """
        index = current.lower()
        self.arbol.clear()
        try:
            self.arbol.itemDoubleClicked.disconnect()
        except Exception as e:
            pass
        
        if index == "libros":
            self.arbol.setHeaderLabels(["Titulo", "Editorial", "Año Publicación", "ISBN", "Genero", "Stock"])
            self.etiquetaPrincipal.setText("Libros")
            libros = bd.obtenerLibros()
            self.vaciarLayout(self.buttonLayout)
            
            for libro in libros:
                button = QPushButton(libro[1])
                self.buttonLayout.addWidget(button)
                libro = Libro(libro[0], libro[1], libro[2], libro[3], libro[4], None, libro[5])
                button.clicked.connect(partial(self.seleccionarLibro, libro=libro))
        
        elif index in ("autores", "editorial", "generos"):
            self.arbol.setHeaderLabels(["Nombre", "Libros"])
            if index == "autores":
                self.etiquetaPrincipal.setText("Autores")
                autores = bd.obtenerAutores()
                if autores:
                    self.vaciarLayout(self.buttonLayout)
                    
                    for autor in autores:
                        item = QPushButton(autor[0])
                        self.buttonLayout.addWidget(item)
                        item.clicked.connect(partial(self.seleccionarAutor, autor=autor))
            if index == "editorial":
                self.etiquetaPrincipal.setText("Editoriales")
                editoriales = bd.obtenerEditoriales()
                if editoriales:
                    self.vaciarLayout(self.buttonLayout)
                    
                    for editorial in editoriales:
                        item = QPushButton(editorial[0])
                        self.buttonLayout.addWidget(item)
                        item.clicked.connect(partial(self.seleccionarEditorial, editorial=editorial))
            if index == "generos":
                self.etiquetaPrincipal.setText("Generos")
                generos = bd.consultarGeneros()
                if generos:
                    self.vaciarLayout(self.buttonLayout)
                    
                    for genero in generos:
                        item = QPushButton(genero[0])
                        self.buttonLayout.addWidget(item)
                        item.clicked.connect(partial(self.seleccionarGenero, genero=genero[0]))
                return

    def login(self):
        """
        Muestra la ventana de inicio de sesión
        """
        try:
            global sesionIniciada
            
            if sesionIniciada:
                QMessageBox.information(self, "Sesión iniciada", "Ya has iniciado sesión. Reinicia el programa para iniciar sesión con otra cuenta.")
                return
            
            self.loginW = LoginWindow(self)
            if self.loginW.exec():
                self.statusbar.showMessage(f"Bienvenido {bd.usuarioLogueado[1]} {bd.usuarioLogueado[2]}")
            
            if (bd.usuarioLogueado == 1 or bd.usuarioLogueado == 2) and not sesionIniciada:
                sesionIniciada = True

                self.borrar.activated.connect(self.eliminar_libro)
                self.menuArchivo.addAction("Ingresar libro").triggered.connect(self.ingresarLibro)
                self.editarBoton = self.menuEditar.addAction("Editar")
                
                staff = self.menuSuperior.addMenu("Staff")                
                staff.addAction("Usuarios").triggered.connect(lambda: self.mostrarUsuarios())
                staff.addAction("Reservas").triggered.connect(lambda: self.mostrarReservas())
                staff.addAction("Prestamos").triggered.connect(lambda: self.mostrarPrestamos())
                staff.addAction("Multas").triggered.connect(lambda: self.mostrarMultas())

                self.editarActual()
                if bd.usuarioLogueado == 2:
                    administracion = self.menuSuperior.addMenu("Administración")
                    
                    empleados = administracion.addAction("Empleados")
                    empleados.triggered.connect(lambda: self.mostrarEmpleados())
                    
                    self.editarActual()
        except Exception as e:
            print(e, f"Linea {e.__traceback__.tb_lineno}")

    def mostrarMultas(self):
        """
        Muestra la ventana de multas
        """
        try:
            ventanaMultas = MostrarMultas(self)
            ventanaMultas.exec()
        except Exception as e:
            print(e, f"Linea {e.__traceback__.tb_lineno}")

    def mostrarPrestamos(self):
        """
        Muestra la ventana de prestamos
        """
        try:
            ventanaPrestamos = MostrarLibrosPrestados(self)
            ventanaPrestamos.exec()
        except Exception as e:
            print(e, f"Linea {e.__traceback__.tb_lineno}")

    def mostrarReservas(self):
        """
        Muestra la ventana de reservas
        """
        try:
            ventanaReservas = MostrarReservaciones(self)
            ventanaReservas.exec()
        except Exception as e:
            print(e, f"Linea {e.__traceback__.tb_lineno}")
            
    def mostrarEmpleados(self):
        """
        Muestra la ventana de administración de empleados
        """
        try:
            ventanaEmpleados = MostrarEmpleados(self)
            ventanaEmpleados.exec()
        except Exception as e:
            print(e, f"Linea {e.__traceback__.tb_lineno}")
            
    def mostrarUsuarios(self):
        """
        Muestra la ventana de administración de usuarios
        """
        try:
            ventanaUsuarios = MostrarUsuarios(self)
            ventanaUsuarios.exec()
        except Exception as e:
            print(e, f"Linea {e.__traceback__.tb_lineno}")
        
    def ingresarLibro(self):
        """
        Muestra la ventana para ingresar un libro
        """
        try:
            self.ingresarLibroDialog = IngresarLibroDialog(self)
            self.ingresarLibroDialog.exec()
            self.actualizarInterfaz("Libros")
        except Exception as e:
            print(e, f"Linea {e.__traceback__.tb_lineno}")
        
    def editarActual(self):
        """
        Conecta el atajo de teclado para editar el objeto que esté elegido
        """
        try:
            self.desconectarSlots()
            if self.menuPrincipal.currentText() == "Libros":
                self.editarBoton.triggered.connect(self.editar_libro)
                self.AtajoEditar.activated.connect(self.editar_libro)
            elif self.menuPrincipal.currentText() == "Autores":
                self.editarBoton.triggered.connect(self.editar_autor)
                self.AtajoEditar.activated.connect(self.editar_autor)
            elif self.menuPrincipal.currentText() == "Editorial":
                self.editarBoton.triggered.connect(self.editar_editorial)
                self.AtajoEditar.activated.connect(self.editar_editorial)
            elif self.menuPrincipal.currentText() == "Generos":
                self.editarBoton.triggered.connect(self.editar_genero)
                self.AtajoEditar.activated.connect(self.editar_genero)
        except Exception as e:
            print(e, f"Linea {e.__traceback__.tb_lineno}")
        
    def desconectarSlots(self):
        try:
            self.editarBoton.triggered.disconnect(self.editar_autor)
            self.AtajoEditar.activated.disconnect(self.editar_autor)
        except (TypeError, RuntimeError):
            pass
        try:
            self.editarBoton.triggered.disconnect(self.editar_libro)
            self.AtajoEditar.activated.disconnect(self.editar_libro)
        except (TypeError, RuntimeError):
            pass
        try:
            self.editarBoton.triggered.disconnect(self.editar_editorial)
            self.AtajoEditar.activated.disconnect(self.editar_editorial)
        except (TypeError, RuntimeError):
            pass
        try:
            self.editarBoton.triggered.disconnect(self.editar_genero)
            self.AtajoEditar.activated.disconnect(self.editar_genero)
        except (TypeError, RuntimeError):
            pass
        
    def ajustarColumnas(self):
        try:
            for i in range(self.arbol.columnCount()):
                self.arbol.resizeColumnToContents(i)
            self.arbol.header().setStyleSheet("QHeaderView::section { background-color: #9bfbe0 }")
        except Exception as e:
            print(e, f"Linea {e.__traceback__.tb_lineno}")
    
    def enDobleClic(self, item: QTreeWidgetItem):
        try:
            libro = bd.conseguirLibro(Libro(None, item.text(0), None, None, None, None, None))
            self.seleccionActual = Libro(libro[0], libro[1], libro[2], libro[3], libro[4], None, libro[5])
            if self.sesion:
                if bd.usuarioLogueado == 1 or bd.usuarioLogueado == 2:
                    self.editar_libro()
                else:
                    mostrarLibroDialog = MostrarLibro(self, self.seleccionActual)
                    mostrarLibroDialog.exec()
        except Exception as e:
            print(e, f"Linea {e.__traceback__.tb_lineno}")
            
    def seleccionarLibro(self, libro: Libro):
        """
        Muestra la información de un libro seleccionado

        Args:
            libro (Libro): El libro seleccionado 
        """
        try:
            self.seleccionActual = libro
            if bd.usuarioLogueado == 1 or bd.usuarioLogueado == 2:
                self.editarActual()
            
            self.arbol.clear()
            self.arbol.setHeaderLabels(["Titulo", "Editorial", "Año Publicación", "ISBN", "Genero", "Stock"])
            self.contenedorCentral.addWidget(self.arbol)
            self.statusBar().showMessage(f"Libro seleccionado: {libro.nombre}")
            self.etiquetaPrincipal.setText(f"Libro: {libro.nombre}")

            item = QTreeWidgetItem(self.arbol)
            libro.genero = bd.consultarGeneroPorLibro(libro)
            self.seleccionActual = libro
            
            item.setText(0, str(libro.nombre))
            item.setText(1, str(libro.editorial))
            item.setText(2, str(libro.anio_publicacion))
            item.setText(3, str(libro.ISBN))
            item.setText(4, str(libro.genero))
            item.setText(5, str(libro.cantidad_disponible))
            self.ajustarColumnas()
            self.arbol.itemDoubleClicked.connect(self.enDobleClic)
        except Exception as e:
            print(e, f"Linea {e.__traceback__.tb_lineno}")
        
    def seleccionarAutor(self, autor):
        """
        Muestra la información de un autor seleccionado

        Args:
            autor (Autor): El autor seleccionado
        """
        try:
            self.autor_seleccionado = Autor(autor[0])
            if bd.usuarioLogueado == 1 or bd.usuarioLogueado == 2:
                self.editarActual()
                
            self.contenedorCentral.removeWidget(self.arbol)
            self.arbol = QTreeWidget()
            self.arbol.setHeaderLabels(["Libros"])
            self.contenedorCentral.addWidget(self.arbol)
            self.statusBar().showMessage(f"Autor seleccionado: {autor[0]}")
            libros = bd.obtenerLibrosPorAutor(autor[0])
            for libro in libros:
                libroArmado = Libro(libro[0], libro[1], libro[2], libro[3], libro[4], None, libro[5])
                genero = bd.consultarGeneroPorLibro(libroArmado)
                libroArmado.genero = genero
                item = QTreeWidgetItem(self.arbol)
                self.etiquetaPrincipal.setText(autor[0])
                item.setText(0, libroArmado.nombre)
                # self.arbol.itemClicked.connect(lambda: self.seleccionarLibro(libroArmado))
            self.ajustarColumnas()
            self.arbol.itemDoubleClicked.connect(self.enDobleClic)
        except Exception as e:
            print(e, f"Linea {e.__traceback__.tb_lineno}")
            
    def seleccionarGenero(self, genero):
        """
        Muestra la información de un género seleccionado

        Args:
            genero (str): El género seleccionado
        """
        try:
            self.genero_seleccionado = genero
            if bd.usuarioLogueado == 1 or bd.usuarioLogueado == 2:
                self.editarActual()
                
            self.contenedorCentral.removeWidget(self.arbol)
            self.arbol = QTreeWidget()
            self.arbol.setHeaderLabels(["Libros"])
            self.contenedorCentral.addWidget(self.arbol)
            self.statusBar().showMessage(f"Genero seleccionado: {genero}")
            libros = bd.obtenerLibrosPorGenero(genero)
            self.etiquetaPrincipal.setText(f"Genero: {genero}")
            for libro in libros:
                item = QTreeWidgetItem(self.arbol)
                item.setText(0, libro[0])
            self.ajustarColumnas()
            self.arbol.itemDoubleClicked.connect(self.enDobleClic)
        except Exception as e:
            print(e, f"Linea {e.__traceback__.tb_lineno}")
    
    def seleccionarEditorial(self, editorial: str):
        """
        Muestra la información de una editorial seleccionada

        Args:
            editorial (Editorial): La editorial seleccionada
        """
        try:
            self.editorial_seleccionada = editorial[0]
            if bd.usuarioLogueado == 1 or bd.usuarioLogueado == 2:
                self.editarActual()
                
            self.contenedorCentral.removeWidget(self.arbol)
            self.arbol = QTreeWidget()
            self.arbol.setHeaderLabels(["Libros"])
            self.contenedorCentral.addWidget(self.arbol)
            self.statusBar().showMessage(f"Editorial seleccionada: {editorial[0]}")
            libros = bd.obtenerLibrosPorEditorial(editorial[0])
            self.etiquetaPrincipal.setText(f"Editorial: {editorial[0]}")
            for libro in libros:
                item = QTreeWidgetItem(self.arbol)
                item.setText(0, libro[0])
            self.ajustarColumnas()
            self.arbol.itemDoubleClicked.connect(self.enDobleClic)
        except Exception as e:
            print(e, f"Linea {e.__traceback__.tb_lineno}")
    
    def vaciarLayout(self, layout):
        """
        Vacía un layout seleccioado

        Args:
            layout (QWidget): El layout a vaciar
        """
        try:            
            while layout.count():
                child = layout.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()
        except Exception as e:
            print(e, f"Linea {e.__traceback__.tb_lineno}")
                
    def editar_libro(self):
        """
        Muestra la ventana para editar un libro seleccionado
        """
        try:            
            self.editarLibroDialog = EditarLibroDialog(self, self.seleccionActual)
            self.editarLibroDialog.exec()
            if self.editarLibroDialog.result() == 1:
                self.actualizarInterfaz("Libros")
                self.seleccionarLibro(self.seleccionActual)
            else:
                self.statusBar().showMessage("No se ha editado ningún libro.")
        except Exception as e:
            print(e, f"Linea {e.__traceback__.tb_lineno}")

    def eliminar_libro(self):
        """
        Elimina un libro seleccionado
        """
        try:
            if not self.seleccionActual:
                self.statusBar().showMessage("No se ha seleccionado ningún libro.")
                return

            respuesta = QMessageBox.question(self, "Confirmación", f"¿Estás seguro de que quieres eliminar el libro '{self.seleccionActual}'?", QMessageBox.Yes | QMessageBox.No)
            if respuesta == QMessageBox.Yes:
                if bd.eliminarLibro(self.seleccionActual):
                    QMessageBox.information(self, "Éxito", f"El libro '{self.seleccionActual.nombre}' ha sido eliminado correctamente.")
                    # Actualizar la interfaz después de eliminar el libro
                    self.actualizarInterfaz("Libros")
                else:
                    QMessageBox.warning(self, "Error", "No se pudo eliminar el libro.")
        except Exception as e:
            print(e, f"Linea {e.__traceback__.tb_lineno}")

    def editar_autor(self):
        """
        Muestra la ventana para editar un autor seleccionado
        """
        try:
            self.editarAutor = EditarAutor(self, self.autor_seleccionado)
            self.editarAutor.exec()
            self.actualizarInterfaz("Autores")
        except Exception as e:
            print(e, f"Linea {e.__traceback__.tb_lineno}")
        
    def editar_editorial(self):
        """
        Muestra la ventana para editar una editorial seleccionada
        """
        try:
            self.editarEditorial = EditarEditorial(self, self.editorial_seleccionada)
            self.editarEditorial.exec()
            self.actualizarInterfaz("Editorial")
        except Exception as e:
            print(e, f"Linea {e.__traceback__.tb_lineno}")
        
    def editar_genero(self):
        """
        Muestra la ventana para editar un género seleccionado
        """
        try:
            self.editarGenero = EditarGenero(self, self.genero_seleccionado)
            self.editarGenero.exec()
            self.actualizarInterfaz("Generos")
        except Exception as e:
            print(e, f"Linea {e.__traceback__.tb_lineno}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setFont(fuente)
    window = VentanaPrincipal()
    window.show()
    sys.exit(app.exec())
