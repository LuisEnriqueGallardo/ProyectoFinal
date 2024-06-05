from PySide6.QtWidgets import (QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout)
from Objetosparabases import *
from BasedeDatosBiblioteca import BasedeDatos as bdt
from Registro import RegistroDialog

bd = bdt()
class LoginWindow(QDialog):
    """
    Clase para la ventana de inicio de sesión de la aplicación

    Args:
        QDialog (QWidget): Clase base para las ventanas de diálogo de la aplicación
    """
    def __init__(self, padre):
        super().__init__()
        self.setWindowTitle("Login")
        self.setMaximumSize(400, 300)
        self.parent = padre
        
        self.layoutprincipal = QVBoxLayout()

        self.etiqueta_correo = QLabel("Nombre de usuario:")
        self.entrada_correo = QLineEdit()
        self.etiqueta_contrasena = QLabel("Contraseña:")
        self.entrada_contrasena = QLineEdit()
        self.entrada_contrasena.setEchoMode(QLineEdit.Password)

        self.login_button = QPushButton("Iniciar sesión")
        self.login_button.clicked.connect(self.login)
        self.login_button.keyReleaseEvent = self.login

        self.register_button = QPushButton("Registro")
        self.register_button.clicked.connect(self.register)
        
        self.layoutprincipal.addWidget(self.etiqueta_correo)
        self.layoutprincipal.addWidget(self.entrada_correo)
        self.layoutprincipal.addWidget(self.etiqueta_contrasena)
        self.layoutprincipal.addWidget(self.entrada_contrasena)
        self.layoutprincipal.addWidget(self.login_button)
        self.layoutprincipal.addWidget(self.register_button)
        
        self.setLayout(self.layoutprincipal)
        self.setModal(True)

    def login(self):
        """
        Función para iniciar sesión en la aplicación

        Returns:
            Bool: Regresa verdadero si se logra iniciar sesión, falso si no se logra
        """
        usuario = Usuario(self.entrada_correo.text(), "", "", "", self.entrada_contrasena.text(), "")
        resultado = bd.verificarUsuario(usuario=usuario)
        if resultado:
            nuevaSesion = Usuario(resultado[0], resultado[1], resultado[2], resultado[3], resultado[4], resultado[5])
            self.parent.sesion = nuevaSesion
            self.parent.statusbar.showMessage("Bienvenido " + resultado[1] + " " + resultado[2])
            self.close()
            return True
        else:
            print("Inicio de sesión fallido")
            bdt.usuarioLogueado = 0
            return False

    def register(self):
        """
        Función para abrir la ventana de registro de usuario
        """
        registro = RegistroDialog()
        registro.show()