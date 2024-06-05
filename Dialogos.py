from PySide6.QtWidgets import QDialog, QLabel, QPushButton, QLineEdit, QVBoxLayout, QComboBox, QTreeWidget, QListWidget, QStatusBar, QTreeWidgetItem, QMessageBox
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

class EditarUsuario(QDialog):
    def __init__(self, padre, usuario: Usuario):
        super().__init__(padre)
        self.parent = padre
        self.setModal(True)
        
        self.setFont("Segoe UI")
        self.setWindowTitle("Editar Usuario")
        self.setGeometry(200, 100, 600, 100)
        layout = QVBoxLayout()
        
        self.usuario = usuario
        self.entrada_usuario = QLineEdit()
        self.entrada_usuario.setText(usuario.nombreUsuario)
        self.entrada_usuario.setToolTip(usuario.nombreUsuario)
        
        self.entrada_nombre = QLineEdit()
        self.entrada_nombre.setText(usuario.nombre)
        self.entrada_nombre.setToolTip(usuario.nombre)
        
        self.entrada_apellido = QLineEdit()
        self.entrada_apellido.setText(usuario.apellido)
        self.entrada_apellido.setToolTip(usuario.apellido)
        
        self.entrada_correo = QLineEdit()
        self.entrada_correo.setText(usuario.correo)
        self.entrada_correo.setToolTip(usuario.correo)
        
        self.entrada_telefono = QLineEdit()
        self.entrada_telefono.setText(usuario.telefono)
        self.entrada_telefono.setToolTip(usuario.telefono)
        
        self.boton = QPushButton("Aceptar")
        self.boton.clicked.connect(self.aceptar)
        
        layout.addWidget(QLabel("Nombre:"))
        layout.addWidget(self.entrada_nombre)
        layout.addWidget(QLabel("Apellido:"))
        layout.addWidget(self.entrada_apellido)
        layout.addWidget(QLabel("Correo:"))
        layout.addWidget(self.entrada_correo)
        layout.addWidget(QLabel("Teléfono:"))
        layout.addWidget(self.entrada_telefono)
        layout.addWidget(self.boton)
        
        self.setLayout(layout)

    def aceptar(self):
        try:
            nombreUsuario = self.entrada_usuario.text()
            nombre = self.entrada_nombre.text()
            apellido = self.entrada_apellido.text()
            correo = self.entrada_correo.text()
            telefono = self.entrada_telefono.text()
            usuario = Usuario(nombreUsuario, nombre, apellido, correo, self.usuario.contrasena, telefono)
            bd.actualizarUsuario(self.usuario.nombreUsuario, usuario)
            self.accept()
            
        except Exception as e:
            print("Error: ", e)
            self.reject()

class MostrarLibro(QDialog):
    def __init__(self, padre, libro: Libro):
        super().__init__(padre)
        try:
            self.parent = padre
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
            
            reservar = QPushButton("Reservar")
            if libro.cantidad_disponible == 0:
                reservar.setEnabled(False)
            reservar.clicked.connect(self.reservar)
            
            layout.addWidget(self.etiqueta_titulo)
            layout.addWidget(self.etiqueta_editorial)
            layout.addWidget(self.etiqueta_anio_publicacion)
            layout.addWidget(self.etiqueta_isbn)
            layout.addWidget(self.etiqueta_genero)
            layout.addWidget(self.etiqueta_cantidad_disponible)
            layout.addWidget(reservar)
            
            self.setLayout(layout)
            self.setFont(QFont("Times New Roman", 14))
            self.setModal(True)
        except Exception as e:
            print(e, f"Linea {e.__traceback__.tb_lineno}")
    
    def reservar(self):
        try:
            bd.reservarLibro(self.libro, self.parent.sesion)
            self.parent.statusBar().showMessage("Libro reservado")
            self.parent.actualizarInterfaz(self.parent.menuPrincipal.currentText())
            self.accept()
        except Exception as e:
            print("Error: ", e)
            self.reject()

class MostrarUsuarios(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setModal(True)
        self.setMinimumSize(800, 600)
        
        self.setFont("Segoe UI")
        self.setWindowTitle("Usuarios")
        self.setGeometry(200, 100, 400, 100)
        layout = QVBoxLayout()
        
        self.etiqueta_usuarios = QLabel("Usuarios:")
        self.lista_usuarios = QTreeWidget()
        self.lista_usuarios.setHeaderLabels(["Usuario", "Nombre", "Apellido", "Correo", "Teléfono"])
        if bd.obtenerUsuarios():
            for usuario in bd.obtenerUsuarios():
                item = QTreeWidgetItem(self.lista_usuarios)
                item.setText(0, usuario[0])
                item.setText(1, usuario[1])
                item.setText(2, usuario[2])
                item.setText(3, usuario[3])
                item.setText(4, usuario[4])
                self.lista_usuarios.addTopLevelItem(item)
        
        layout.addWidget(self.etiqueta_usuarios)
        layout.addWidget(self.lista_usuarios)
        
        self.setLayout(layout)
        for i in range(5):
            self.lista_usuarios.resizeColumnToContents(i)
        self.lista_usuarios.header().setStyleSheet("QHeaderView::section { background-color: #c7fa9c }")
        self.lista_usuarios.itemDoubleClicked.connect(self.editarUsuario)
        
    def editarUsuario(self):
        try:
            usuario = self.lista_usuarios.currentItem()
            usuario = Usuario(usuario.text(0), usuario.text(1), usuario.text(2), usuario.text(3), usuario.text(4))
            usuario = bd.obtenerUsuario(usuario)
            usuario = Usuario(usuario[0], usuario[1], usuario[2], usuario[3], None, usuario[4])
            dialogo = EditarUsuario(self, usuario)
            dialogo.exec_()
            self.actualizar()
        except Exception as e:
            print(e, f"Linea {e.__traceback__.tb_lineno}")
    
    def actualizar(self):
        try:
            self.lista_usuarios.clear()
            if bd.obtenerUsuarios():
                for usuario in bd.obtenerUsuarios():
                    item = QTreeWidgetItem(self.lista_usuarios)
                    item.setText(0, usuario[0])
                    item.setText(1, usuario[1])
                    item.setText(2, usuario[2])
                    item.setText(3, usuario[3])
                    item.setText(4, usuario[4])
                    self.lista_usuarios.addTopLevelItem(item)
            for i in range(5):
                self.lista_usuarios.resizeColumnToContents(i)
            self.lista_usuarios.header().setStyleSheet("QHeaderView::section { background-color: #c7fa9c }")
        except Exception as e:
            print(e, f"Linea {e.__traceback__.tb_lineno}")
        
class MostrarUsuarioUnico(QDialog):
    def __init__(self, parent, usuario: Usuario):
        super().__init__(parent)
        self.parent = parent
        self.setModal(True)
        self.usuario = usuario
        
        self.setFont("Segoe UI")
        self.setWindowTitle("Información del usuario")
        self.setGeometry(200, 100, 400, 100)
        layout = QVBoxLayout()
        
        self.etiqueta_usuario = QLabel(f"Usuario: {usuario.nombreUsuario}")
        self.etiqueta_nombre = QLabel(f"Nombre: {usuario.nombre}")
        self.etiqueta_apellido = QLabel(f"Apellido: {usuario.apellido}")
        self.etiqueta_correo = QLabel(f"Correo: {usuario.correo}")
        self.etiqueta_telefono = QLabel(f"Teléfono: {usuario.telefono}")
        
        layout.addWidget(self.etiqueta_usuario)
        layout.addWidget(self.etiqueta_nombre)
        layout.addWidget(self.etiqueta_apellido)
        layout.addWidget(self.etiqueta_correo)
        layout.addWidget(self.etiqueta_telefono)
        
        self.setLayout(layout)
        self.setFont(QFont("Times New Roman", 14))
        self.setModal(True)
 
class MostrarEmpleados(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setModal(True)
        self.setMinimumSize(800, 600)
        
        self.setFont("Segoe UI")
        self.setWindowTitle("Empleados")
        self.setGeometry(200, 100, 400, 100)
        layout = QVBoxLayout()
        
        self.etiqueta_usuarios = QLabel("Empleados:")
        self.lista_usuarios = QTreeWidget()
        self.lista_usuarios.setHeaderLabels(["Numero Empleado", "Nombre", "Apellido", "Nombre de Usuario", "Administrador"])
        if bd.obtenerEmpleados():
            for usuario in bd.obtenerEmpleados():
                item = QTreeWidgetItem(self.lista_usuarios)
                item.setText(0, str(usuario[0]))
                item.setText(1, usuario[1])
                item.setText(2, usuario[2])
                item.setText(3, usuario[3])
                item.setText(4, str(usuario[4]))
                self.lista_usuarios.addTopLevelItem(item)
            self.lista_usuarios.itemClicked.connect(self.editarEmpleado)
        
        layout.addWidget(self.etiqueta_usuarios)
        layout.addWidget(self.lista_usuarios)
        
        self.setLayout(layout)
        for i in range(5):
            self.lista_usuarios.resizeColumnToContents(i)
        self.lista_usuarios.header().setStyleSheet("QHeaderView::section { background-color: #c7fa9c }")
        
    def editarEmpleado(self, item: QTreeWidgetItem):
        empleado = bd.obtenerEmpleado(Empleado(item.text(0), item.text(1), item.text(2), item.text(3), item.text(4)))
        empleado = empleado[0]
        empleado = Empleado(empleado[0], empleado[1], empleado[2], empleado[3], empleado[4])
        print(empleado)
        ventana = EditarEmpleado(self, empleado)
        ventana.exec_()
        
    def actualizar(self):
        self.lista_usuarios.clear()
        if bd.obtenerEmpleados():
            for usuario in bd.obtenerEmpleados():
                item = QTreeWidgetItem(self.lista_usuarios)
                item.setText(0, str(usuario[0]))
                item.setText(1, usuario[1])
                item.setText(2, usuario[2])
                item.setText(3, usuario[3])
                item.setText(4, str(usuario[4]))
                self.lista_usuarios.addTopLevelItem(item)
            self.lista_usuarios.itemClicked.connect(self.editarEmpleado)
            
        for i in range(5):
            self.lista_usuarios.resizeColumnToContents(i)
        self.lista_usuarios.header().setStyleSheet("QHeaderView::section { background-color: #c7fa9c }")

class EditarEmpleado(QDialog):
    def __init__(self, padre, empleado: Empleado):
        super().__init__(padre)
        self.parent = padre
        self.setModal(True)
        
        self.setFont("Segoe UI")
        self.setWindowTitle("Editar Empleado")
        self.setGeometry(200, 100, 600, 100)
        layout = QVBoxLayout()
        
        self.empleado = empleado
        self.numero_empleado = QLabel()
        self.numero_empleado.setText(str(empleado.numeroEmpleado))
        
        self.entrada_nombre = QLineEdit()
        self.entrada_nombre.setText(str(empleado.nombre))
        self.entrada_nombre.setToolTip(str(empleado.nombre))
        
        self.entrada_apellido = QLineEdit()
        self.entrada_apellido.setText(str(empleado.apellido))
        self.entrada_apellido.setToolTip(str(empleado.apellido))
        
        self.entrada_nombre_usuario = QLineEdit()
        self.entrada_nombre_usuario.setText(str(empleado.nombreUsuario))
        self.entrada_nombre_usuario.setToolTip(str(empleado.nombreUsuario))
        
        self.entrada_administrador = QComboBox()
        self.entrada_administrador.addItem("0")
        self.entrada_administrador.addItem("1")
        
        self.boton = QPushButton("Aceptar")
        self.boton.clicked.connect(self.aceptar)
        
        layout.addWidget(QLabel("Número de Empleado:"))
        layout.addWidget(self.numero_empleado)
        layout.addWidget(QLabel("Nombre:"))
        layout.addWidget(self.entrada_nombre)
        layout.addWidget(QLabel("Apellido:"))
        layout.addWidget(self.entrada_apellido)
        layout.addWidget(QLabel("Nombre de Usuario:"))
        layout.addWidget(self.entrada_nombre_usuario)
        layout.addWidget(QLabel("Administrador:"))
        layout.addWidget(self.entrada_administrador)
        layout.addWidget(self.boton)
        
        self.setLayout(layout)  

    def aceptar(self):
        try:
            nombre = self.entrada_nombre.text()
            apellido = self.entrada_apellido.text()
            nombreUsuario = self.entrada_nombre_usuario.text()
            administrador = int(self.entrada_administrador.currentText())
            empleado = Empleado(self.empleado.numeroEmpleado, nombre, apellido, nombreUsuario, administrador)
            bd.actualizarEmpleado(self.empleado.nombreUsuario, empleado)
            self.parent.actualizar()
            self.accept()
            
        except Exception as e:
            print("Error: ", e)

class MostrarReservaciones(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setModal(True)
        self.setMinimumSize(800, 600)
        
        self.setFont("Segoe UI")
        self.setWindowTitle("Reservaciones")
        self.setGeometry(200, 100, 400, 100)
        layout = QVBoxLayout()
        
        self.etiqueta_reservaciones = QLabel("Reservaciones:")
        self.lista_reservaciones = QTreeWidget()
        self.lista_reservaciones.setHeaderLabels(["No", "Usuario", "Libro", "Fecha de Reservación"])
        if bd.obtenerReservas():
            for reservacion in bd.obtenerReservas():
                item = QTreeWidgetItem(self.lista_reservaciones)
                item.setText(0, str(reservacion[0]))
                item.setText(1, str(reservacion[1]))
                item.setText(2, str(reservacion[2]))
                item.setText(3, str(reservacion[3]))
                self.lista_reservaciones.addTopLevelItem(item)
            self.lista_reservaciones.itemDoubleClicked.connect(self.borrarReservacion)
        
        layout.addWidget(self.etiqueta_reservaciones)
        layout.addWidget(self.lista_reservaciones)
        
        self.setLayout(layout)
        for i in range(3):
            self.lista_reservaciones.resizeColumnToContents(i)
        self.lista_reservaciones.header().setStyleSheet("QHeaderView::section { background-color: #c7fa9c }")
    
    def actualizar(self):
        try:
            self.lista_reservaciones.clear()
            try:
                self.lista_reservaciones.itemDoubleClicked.disconnect()
            except:
                pass
            if bd.obtenerReservas():
                for reservacion in bd.obtenerReservas():
                    item = QTreeWidgetItem(self.lista_reservaciones)
                    item.setText(0, str(reservacion[0]))
                    item.setText(1, str(reservacion[1]))
                    item.setText(2, str(reservacion[2]))
                    item.setText(3, str(reservacion[3]))
                    self.lista_reservaciones.addTopLevelItem(item)
                self.lista_reservaciones.itemDoubleClicked.connect(self.borrarReservacion)
                
            for i in range(3):
                self.lista_reservaciones.resizeColumnToContents(i)
            self.lista_reservaciones.header().setStyleSheet("QHeaderView::section { background-color: #c7fa9c }")
        except Exception as e:
            print(e, f"Linea {e.__traceback__.tb_lineno}")
    
    def borrarReservacion(self):
        QMessageBox.warning(self, "Eliminar", "¿Estás seguro de eliminar la reservación?", QMessageBox.Yes | QMessageBox.No)
        if QMessageBox.Yes:
            item = self.lista_reservaciones.currentItem()
            id_libro = bd.obtenerLibro(Libro("", item.text(2), "", "", "", "", ""))
            bd.eliminarReserva(item.text(0), Libro(id_libro[0], id_libro[1], id_libro[2], id_libro[3], id_libro[4], None, id_libro[5]))
            self.actualizar()
        else:
            pass