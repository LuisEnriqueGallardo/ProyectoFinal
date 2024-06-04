class Usuario:
    """
    Objeto usuario para manejar a los usuarios con sus atributos
    """
    def __init__(self, nombreUsuario, nombre, apellido, correo, contrasena, telefono = "", empleado: bool = False, administrador: bool = False):
        self.nombreUsuario = nombreUsuario
        self.nombre = nombre
        self.apellido = apellido
        self.correo = correo
        self.contrasena = contrasena
        self.telefono = telefono
        self.empleado = empleado
        self.administrador = administrador
        
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