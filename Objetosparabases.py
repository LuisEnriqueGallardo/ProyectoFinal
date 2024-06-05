class Usuario:
    """
    Objeto usuario para manejar a los usuarios con sus atributos
    """
    def __init__(self, nombreUsuario, nombre, apellido, correo, contrasena, telefono = ""):
        self.nombreUsuario = nombreUsuario
        self.nombre = nombre
        self.apellido = apellido
        self.correo = correo
        self.telefono = telefono
        self.contrasena = contrasena
        
class Libro:
    """
    Objeto para el Libro y manejar sus atributos
    """
    def __init__(self, id_libro, nombre, editorial, anio_publicacion, ISBN, genero, cantidad_disponible):
        self.id_libro = id_libro
        self.nombre = nombre
        self.editorial = editorial
        self.anio_publicacion = anio_publicacion
        self.ISBN = ISBN
        self.genero = genero
        self.cantidad_disponible = cantidad_disponible
        
class Autor:
    """
    Objeto para para el autor y manejar sus atributos
    """
    def __init__(self, nombre, libros = None):
        self.nombre = nombre
        self.libros = libros

class Empleado:
    """
    Objeto para manejar a los empleados y sus atributos
    """
    def __init__(self, numeroEmpleado, nombre, apellido, nombreUsuario: str, administrador: int = 0):
        self.numeroEmpleado = numeroEmpleado
        self.nombre = nombre
        self.apellido = apellido
        self.nombreUsuario = nombreUsuario
        self.administrador = administrador
        
class Reserva:
    """
    Objeto para manejar las reservas y sus atributos
    """
    def __init__(self, id_reserva, id_usuario, id_libro, nombre, fecha):
        self.id_reserva = id_reserva
        self.id_usuario = id_usuario
        self.id_libro = id_libro
        self.nombre = nombre
        self.fecha = fecha

class Multa:
    """
    Objeto para manejar las multas y sus atributos
    """
    def __init__(self, id_multa, id_usuario, cantidad, fecha):
        self.id_multa = id_multa
        self.id_usuario = id_usuario
        self.cantidad = cantidad
        self.fecha = fecha

class Comentario:
    """
    Objeto para manejar los comentarios y sus atributos
    """
    def __init__(self, id_comentario, id_libro, id_usuario, comentario, fecha):
        self.id_comentario = id_comentario
        self.id_libro = id_libro
        self.id_usuario = id_usuario
        self.comentario = comentario
        self.fecha = fecha