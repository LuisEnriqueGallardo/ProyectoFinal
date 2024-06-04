from PyQt5.QtWidgets import QLineEdit, QWidget, QHBoxLayout, QLabel
from PyQt5.QtGui import QFont

class QTextoObligatorio(QWidget):
    def __init__(self, permitirEspaciosBlanco = False, porcentajeDeAumento = 30):
        """
        Constructor
        Linea de texto para solicitar texto obligatorio al usuario
        """
        super().__init__()

        # Varriables definidas para el manejo de la configuración
        self.permitirEspaciosBlanco = permitirEspaciosBlanco
        self.porcentajeDeAumento = porcentajeDeAumento

        self.texto = QLineEdit()
        self.text = self.texto.text()

        self.__obligatorio = QLabel()
        self.__obligatorio.setText("*")

        contenedorInterior = QHBoxLayout(self)
        contenedorInterior.addWidget(self.texto)
        contenedorInterior.addWidget(self.__obligatorio)

        # Evaluación del texto cada vez que cambia
        self.texto.textChanged.connect(self.evaluar)
        self.evaluar()

    def cambiarFuente(self, fuente: QFont):
        """
        Cambia la fuente la linea de texto y el tamaño
            fuente: QFont()
        """
        # Cambiar la fuente del campo de texto
        tamañoFuente = fuente.pointSize()
        self.texto.setFont(fuente)

        # Cambiar el tamaño de la fuente de la marca, un x% mas de la del texto según lo que solicitó el usuario. (30% por defecto)
        fuente2 = QFont()
        fuente2.setPointSize(round(((tamañoFuente)*(self.porcentajeDeAumento/100)) + tamañoFuente))
        self.__obligatorio.setFont(fuente2)


    def evaluar(self):
        """
        Evalua si el campo de texto es vacio para denotar el "obligatorio" dependiendo de la variable
        Retorna
            True si es valido, no está vacio
            False si no es valido, está vacío
        """
        textoEntrada = self.texto.text()
        if self.permitirEspaciosBlanco == False:
        # Checamos si el texto está vacio
            if textoEntrada.strip() == "":
            # Si está vacío
                # Cambiamos el color de la marca a rojo
                self.__obligatorio.setStyleSheet("color: red;")

                # Cambiamos el borde del campo de texto a rojo
                self.texto.setStyleSheet("border: 2px solid red;")

                # Retornamos False
                return False
            
                # Si no está vacío:
            else:
                # Cambiamos el color de la marca a verde
                self.__obligatorio.setStyleSheet("color: green;")
                # Cambiamos el borde del campo de texto a verde
                self.texto.setStyleSheet("border: 2px solid green;")
                # Retornamos True
                return True
        else:
            # Repetimos el ciclo para revisar si hay espacios en blanco y se permiten
            if self.permitirEspaciosBlanco == True:
                if textoEntrada == "":
                # Si está vacío
                    # Cambiamos el color de la marca a rojo
                    self.__obligatorio.setStyleSheet("color: red;")

                    # Cambiamos el borde del campo de texto a rojo
                    self.texto.setStyleSheet("border: 2px solid red;")

                    # Retornamos False
                    return False
            
                # Si no está vacío:
                elif textoEntrada == " ":
                    # Cambiamos el color de la marca a verde
                    self.__obligatorio.setStyleSheet("color: green;")
                    # Cambiamos el borde del campo de texto a verde
                    self.texto.setStyleSheet("border: 2px solid green;")
                    # Retornamos True
                    return True
                else:
                    # Cambiamos el color de la marca a verde
                    self.__obligatorio.setStyleSheet("color: green;")
                    # Cambiamos el borde del campo de texto a verde
                    self.texto.setStyleSheet("border: 2px solid green;")
                    # Retornamos True
                    return True
        return False

    
    def permitirEspacios(self, boleano):
        """
        Cambia la restricción de espacios en blanco
            True para permitirlos
            False para denegarlos
        """
        self.permitirEspaciosBlanco = boleano

    def cambiarPorcentaje(self, porcentaje):
        """
        Cambia el porcentaje de crecimiento del texto
        """
        self.porcentajeDeAumento = porcentaje

    def esValido(self):
        """
        Evalua los campos para comprobar su validez
            True si es valido
            False si no es valido
        """

        # Evalua el texto del campo de texto
        self.evaluar()

        # En caso de ser invalido, el foco se centra en el campo invalido
        if self.evaluar() == False:
            self.texto.setFocus()
            return False
        else:
            return True
        
    def holderText(self, texto):
        """
        Cambia el Holder Text de la linea de texto
        """
        self.texto.setPlaceholderText(texto)