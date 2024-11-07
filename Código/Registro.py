from PySide6.QtWidgets import (QDialog, QHBoxLayout, QLabel, QLineEdit, QPushButton, QVBoxLayout, QStatusBar, QMessageBox)
from Objetosparabases import *
from BasedeDatosBiblioteca import BasedeDatos as bdt

bd = bdt()
class RegistroDialog(QDialog):
    """
    Clase para la ventana de registro de la aplicación

    Args:
        QDialog (QWIdget): Clase base para las ventanas de diálogo de la aplicación
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Registro")
        self.setMaximumSize(800, 600)
        self.statusbar = QStatusBar()

        
        self.layout_registro = QVBoxLayout()
        
        self.etiqueta_usuario = QLabel("Nombre de usuario:")
        self.entrada_usuario = QLineEdit()
                
        self.etiqueta_nombre = QLabel("Nombre:")
        self.entrada_nombre = QLineEdit()
        
        self.etiqueta_apellido = QLabel("Apellido:")
        self.entrada_apellido = QLineEdit()
        
        self.etiqueta_correo = QLabel("Correo electrónico:")
        self.entrada_correo = QLineEdit()
        
        self.etiqueta_contrasena = QLabel("Contraseña:")
        self.entrada_contrasena = QLineEdit()
        self.entrada_contrasena.setEchoMode(QLineEdit.Password)
        
        self.etiqueta_confirmar_contrasena = QLabel("Confirmar contraseña:")
        self.entrada_confirmar_contrasena = QLineEdit()
        self.entrada_confirmar_contrasena.setEchoMode(QLineEdit.Password)
        self.entrada_confirmar_contrasena.textChanged.connect(self.confirmarContrasena)
        
        self.usuarioNuevo = Usuario(self.entrada_usuario.text(), self.entrada_nombre.text(), self.entrada_apellido.text(), self.entrada_correo.text(), self.entrada_contrasena.text(), "")
        
        self.campobotones = QHBoxLayout()
        self.boton_registrar = QPushButton("Registrar")
        self.boton_registrar.clicked.connect(self.registrar)
        self.boton_registrar.setEnabled(False)
        
        self.boton_cancelar = QPushButton("Cancelar")
        self.boton_cancelar.clicked.connect(lambda: self.close())
        
        self.numero_telefono = QLabel("Número de teléfono:")
        self.entrada_telefono = QLineEdit()
        self.entrada_telefono.setInputMask('999-999-9999')
        
        self.campobotones.addWidget(self.boton_registrar)
        self.campobotones.addWidget(self.boton_cancelar)
        
        self.layout_registro.addWidget(self.etiqueta_usuario)
        self.layout_registro.addWidget(self.entrada_usuario)
        self.layout_registro.addWidget(self.etiqueta_nombre)
        self.layout_registro.addWidget(self.entrada_nombre)
        self.layout_registro.addWidget(self.etiqueta_apellido)
        self.layout_registro.addWidget(self.entrada_apellido)
        self.layout_registro.addWidget(self.etiqueta_correo)
        self.layout_registro.addWidget(self.entrada_correo)
        self.layout_registro.addWidget(self.numero_telefono)
        self.layout_registro.addWidget(self.entrada_telefono)
        self.layout_registro.addWidget(self.etiqueta_contrasena)
        self.layout_registro.addWidget(self.entrada_contrasena)
        self.layout_registro.addWidget(self.etiqueta_confirmar_contrasena)
        self.layout_registro.addWidget(self.entrada_confirmar_contrasena)
        self.layout_registro.addLayout(self.campobotones)
        
        self.setLayout(self.layout_registro)
        self.setModal(True)
    
    def registrar(self):
        telefono = int(self.entrada_telefono.text().replace("-", ""))
        try:
            registro = bd.registrarUsuario(Usuario(self.entrada_usuario.text(), self.entrada_nombre.text(), self.entrada_apellido.text(), self.entrada_correo.text(), self.entrada_contrasena.text(), telefono))
            try:
                if registro[1]:
                    QMessageBox.warning(self, "Error", "El nombre de usuario ya existe")
            except:
                QMessageBox.information(self, "Registro exitoso", "Registro exitoso")
                self.close()
        except:
            print("Registro fallido")
            
    def confirmarContrasena(self):
        if self.entrada_contrasena.text() != self.entrada_confirmar_contrasena.text():
            self.entrada_confirmar_contrasena.setStyleSheet("background-color: red")
        else:
            self.entrada_confirmar_contrasena.setStyleSheet("background-color: white")
            self.boton_registrar.setEnabled(True)
