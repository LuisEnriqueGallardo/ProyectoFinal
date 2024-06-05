import mysql.connector as driver
from mysql.connector import DatabaseError, IntegrityError
from datetime import date
from Objetosparabases import *

usuario = {
    "usuario": "UsuarioBiblio",
    "contrasenia": "BG2024",
    "host": "localhost",
    "puerto": 3306,
    "bd": "Bibliotecages"
}

empleado = {
    "usuario": "empleadoBiblio",
    "contrasenia": "PASSWORD1",
    "host": "localhost",
    "puerto": 3306,
    "bd": "Bibliotecages"
}

administrador = {
    "usuario": "gerencia",
    "contrasenia": "PASSWORD2",
    "host": "localhost",
    "puerto": 3306,
    "bd": "Bibliotecages"
}

class BasedeDatos:
    """
    Clase para la conexión a la base de datos de la biblioteca
    """
    usuarioLogueado = 0
    
    def __conectar(self):
        """
        Función para conectar a la base de datos

        Returns:
            Bool: Regresa verdadero si la conexión es exitosa, falso si no
        """
        if BasedeDatos.usuarioLogueado == 0:
            parametros = usuario
        elif BasedeDatos.usuarioLogueado == 1:
            parametros = empleado
        elif BasedeDatos.usuarioLogueado == 2:
            parametros = administrador

        try:
            self.conn = driver.connect(
                host = parametros["host"],
                user = parametros["usuario"],
                password = parametros["contrasenia"],
                port = parametros["puerto"],
                database = parametros["bd"]
            )
            return True
        except DatabaseError as e:
            print(e)
            return False, e
        
    def __desconectar(self):
        """
        Función para desconectar de la base de datos
        """
        self.conn.close()
        
    def cerrarSesion(self):
        """
        Función para cerrar la sesión en la base de datos
        """
        BasedeDatos.usuarioLogueado = 0
        print("Sesión cerrada.", BasedeDatos.usuarioLogueado)
        
    def verificarEmpleado(self, usuario: Usuario):
        """
        Función para verificar si el empleado existe en la base de datos

        Args:
            usuario (Usuario): Objeto de la clase Usuario

        Returns:
            Bool: Regresa verdadero si el empleado existe, falso si no
            Resultado: Regresa el resultado de la consulta
        """
        try:
            self.__conectar()
            
            sql = "select esAdministrador from usuarios, empleados where nombre = nombres and apellido = apellidos and nombreUsuario = %s and contrasena = sha2(%s, 256);"
            param = (usuario.nombreUsuario, usuario.contrasena)

            cursor = self.conn.cursor()
            cursor.execute(sql, param)

            resultado = cursor.fetchone()

            if resultado is None:
                return None
            else:
                return resultado
        except IntegrityError as e:
            print(e, f"Linea {e.__traceback__.tb_lineno}")
            return False
        finally:
            self.__desconectar()
        
    def verificarUsuario(self, usuario):
        """
        Función para verificar si el usuario existe en la base de datos

        Args:
            usuario (Usuario): Objeto de la clase Usuario

        Returns:
            Bool: Regresa verdadero si el usuario existe, falso si no
            Resultado: Regresa los datos del usuario
        """
        try:
            self.__conectar()
            
            sql = "SELECT * FROM usuarios WHERE nombreUsuario = %s AND contrasena = sha2(%s, 256);"
            param = (usuario.nombreUsuario, usuario.contrasena)

            cursor = self.conn.cursor()
            cursor.execute(sql, param)

            resultado = cursor.fetchone()

            if resultado is None:
                return False
            else:
                if self.verificarEmpleado(usuario):
                    if self.verificarEmpleado(usuario)[0] == 0:
                        BasedeDatos.usuarioLogueado = 1
                    elif self.verificarEmpleado(usuario)[0] == 1:
                        BasedeDatos.usuarioLogueado = 2
                return resultado
        except IntegrityError as e:
            print(e, f"Linea {e.__traceback__.tb_lineno}")
            return False
        finally:
            self.__desconectar()
            
    def obtenerUsuarios(self):
        """
        Función para obtener los usuarios de la base de datos

        Returns:
            usuarios: Regresa los usuarios de la base de datos
            Bool: Regresa falso si hay un error
        """
        try:
            self.__conectar()
            
            sql = "SELECT nombreUsuario, nombre, apellido, correo, telefono FROM usuarios;"
            cursor = self.conn.cursor()
            cursor.execute(sql)
            usuarios = cursor.fetchall()
            return usuarios
        
        except IntegrityError as e:
            print(e, f"Linea {e.__traceback__.tb_lineno}")
            return False
        finally:
            self.__desconectar()
            
    def obtenerUsuario(self, usuario: Usuario):
        """
        Función para obtener un usuario de la base de datos

        Args:
            usuario (Usuario): Objeto de la clase Usuario

        Returns:
            usuario: Regresa el usuario de la base de datos
            Bool: Regresa falso si hay un error
        """
        try:
            self.__conectar()
            
            sql = "SELECT nombreUsuario, nombre, apellido, correo, telefono FROM usuarios WHERE nombreUsuario = %s;"
            param = (usuario.nombreUsuario,)
            cursor = self.conn.cursor()
            cursor.execute(sql, param)
            usuario = cursor.fetchone()
            return usuario
        except IntegrityError as e:
            print(e, f"Linea {e.__traceback__.tb_lineno}")
            return False
        finally:
            self.__desconectar()
    
    def registrarUsuario(self, usuario: Usuario):
        """
        Función para registrar un usuario en la base de datos

        Args:
            usuario (Usuario): Objeto de la clase Usuario

        Returns:
            Bool: Regresa verdadero si el usuario se registra, falso si no 
        """
        try:
            self.__conectar()
            
            sql = "INSERT INTO usuarios (nombreUsuario, nombre, apellido, correo, contrasena, telefono) VALUES (%s, %s, %s, %s, sha2(%s, 256), %s);"
            param = (usuario.nombreUsuario, usuario.nombre, usuario.apellido, usuario.correo, usuario.contrasena, usuario.telefono)

            cursor = self.conn.cursor()
            cursor.execute(sql, param)

            self.conn.commit()
            return True
        except IntegrityError as e:
            print(e, f"Linea {e.__traceback__.tb_lineno}")
            if e.errno == 1062:
                print("El usuario ya existe.")
                return False, "El usuario ya existe."
            return False
        finally:
            self.__desconectar()
        
    def obtenerLibros(self):
        """
        Función para obtener los libros de la base de datos

        Returns:
            libros: Regresa los libros de la base de datos
            Bool: Regresa falso si hay un error
        """
        try:
            self.__conectar()
            
            sql = "SELECT id_libro, nombre, editorial, anio_publicacion, ISBN, cantidad_disponible FROM libros;"
            cursor = self.conn.cursor()
            cursor.execute(sql)
            libros = cursor.fetchall()
            return libros
        except IntegrityError as e:
            print(e, f"Linea {e.__traceback__.tb_lineno}")
            return False
        finally:
            self.__desconectar()
            
    def obtenerLibro(self, libro: Libro):
        """
        Función para obtener un libro de la base de datos

        Args:
            libro (Libro): Objeto de la clase Libro

        Returns:
            libro: Regresa el libro de la base de datos
            Bool: Regresa falso si hay un error
        """
        try:
            self.__conectar()
            
            sql = "SELECT id_libro, nombre, editorial, anio_publicacion, ISBN, cantidad_disponible FROM libros WHERE nombre = %s;"
            param = (libro.nombre,)
            cursor = self.conn.cursor()
            cursor.execute(sql, param)
            libro = cursor.fetchone()
            return libro
        except IntegrityError as e:
            print(e, f"Linea {e.__traceback__.tb_lineno}")
            return False
        finally:
            self.__desconectar()
        
    def conseguirLibro(self, libro: Libro):
        """
        Función para obtener un libro de la base de datos

        Args:
            libro (Libro): Objeto de la clase Libro

        Returns:
            Libro: Regresa el libro de la base de datos
            Bool: Regresa falso si hay un error
        """
        try:
            self.__conectar()
            
            sql = "SELECT id_libro, nombre, editorial, anio_publicacion, ISBN, cantidad_disponible FROM libros WHERE nombre = %s;"
            param = (libro.nombre,)
            cursor = self.conn.cursor()
            cursor.execute(sql, param)
            libro = cursor.fetchone()
            return libro
        except IntegrityError as e:
            print(e, f"Linea {e.__traceback__.tb_lineno}")
            return False
        finally:
            self.__desconectar()
        
    def obtenerAutores(self):
        """
        Función para obtener los autores de la base de datos

        Returns:
            autores: Regresa los autores de la base de datos
            Bool: Regresa falso si hay un error
        """
        try:
            self.__conectar()
            
            sql = "SELECT nombre FROM autores;"
            cursor = self.conn.cursor()
            cursor.execute(sql)
            autores = cursor.fetchall()
            return autores
        except IntegrityError as e:
            print(e, f"Linea {e.__traceback__.tb_lineno}")
            return False
        finally:
            self.__desconectar()
        
    def insertarLibro(self, libro: Libro, autor: Autor = None):
        """
        Función para insertar un libro en la base de datos

        Args:
            libro (Libro): Objeto de la clase Libro
            autor (Autor, opcional): Objeto de la clase Autor en caso de haberlo. Defaults to None.

        Returns:
            Bool: Regresa verdadero si el libro se inserta, falso si no
        """
        try:
            self.__conectar()            
            sql = "INSERT INTO libros (nombre, editorial, anio_publicacion, ISBN, cantidad_disponible) VALUES (%s, %s, %s, %s, %s);"
            param = (libro.nombre, libro.editorial, libro.anio_publicacion, str(libro.ISBN), libro.cantidad_disponible)
            cursor = self.conn.cursor()
            cursor.execute(sql, param)
            self.conn.commit()
            
            # Obtener el id del libro
            sql = "SELECT id_libro FROM libros WHERE nombre = %s;"
            param = (libro.nombre,)
            cursor.execute(sql, param)
            id_libro = cursor.fetchone()[0]
            self.conn.commit()
            
            # Obtener el id del genero
            sql = "SELECT id_genero FROM generos WHERE nombre = %s;"
            print(libro.genero,)
            param = (libro.genero,)
            cursor.execute(sql, param)
            id_genero = cursor.fetchone()[0]
            self.conn.commit()
            
            # Insertar el genero del libro
            sql = "INSERT INTO libro_genero (id_libro, id_genero) VALUES (%s, %s);"
            param = (id_libro, id_genero)
            cursor.execute(sql, param)
            self.conn.commit()
            
            # Insertar el autor del libro
            if autor is not None:                
                sql = "SELECT id_autor FROM autores WHERE nombre = %s;"
                param = (autor.nombre,)
                cursor.execute(sql, param)
                id_autor = cursor.fetchone()[0]
                self.conn.commit()
                
                sql = "INSERT INTO libro_autor (id_libro, id_autor) VALUES (%s, %s);"
                param = (id_libro, id_autor)
                print(param)
                cursor.execute(sql, param)
                self.conn.commit()
            
            sql = "SELECT id_editorial FROM editoriales, libros WHERE libros.editorial = editoriales.nombre and libros.id_libro = %s;"
            param = (id_libro,)
            cursor.execute(sql, param)
            id_editorial = cursor.fetchone()[0]
            
            sql = "INSERT INTO libro_editorial (id_libro, id_editorial) VALUES (%s, %s);"
            param = (id_libro, id_editorial)
            cursor.execute(sql, param)
            self.conn.commit()
            
            return True
        except IntegrityError as e:
            print(e, f"Linea {e.__traceback__.tb_lineno}")
            return False
        except Exception as e:
            print(e, f"Linea {e.__traceback__.tb_lineno}")
            return False
        finally:
            self.__desconectar()
            
    def consultarGeneros(self):
        """
        Función para consultar los géneros de la base de datos

        Returns:
            generos: Regresa los géneros de la base de datos
            Bool: Regresa falso si hay un error
        """
        try:
            self.__conectar()
            
            sql = "SELECT nombre FROM generos;"
            cursor = self.conn.cursor()
            cursor.execute(sql)
            generos = cursor.fetchall()
            return generos
        except IntegrityError as e:
            print(e, f"Linea {e.__traceback__.tb_lineno}")
            return False
        finally:
            self.__desconectar()
    
    def consultarGeneroPorLibro(self, libro: Libro):
        """
        Función para consultar el género de un libro en la base de datos

        Args:
            libro (Libro): Objeto de la clase Libro

        Returns:
            genero[0]: Regresa el género del libro
            Bool: Regresa falso si hay un error
        """
        try:
            self.__conectar()
            
            sql = "select nombre from generos JOIN libro_genero using(id_genero) where id_libro = %s;"
            param = (libro.id_libro,)
            cursor = self.conn.cursor()
            cursor.execute(sql, param)
            genero = cursor.fetchone()
            if genero:
                return genero[0]
            else:
                return False
        except IntegrityError as e:
            print(e, f"Linea {e.__traceback__.tb_lineno}")
            return False
        finally:
            self.__desconectar()
    
    def editarLibro(self, libro: Libro):
        """
        Función para editar un libro en la base de datos

        Args:
            libro (Libro): Objeto de la clase Libro

        Returns:
            Bool: Regresa verdadero si el libro se edita, falso si no
        """
        try:
            self.__conectar()
            print("Conectado como " + usuario["usuario"] + ".")
            
            sql = "UPDATE libros SET editorial = %s, anio_publicacion = %s, ISBN = %s, nombre = %s, cantidad_disponible = %s WHERE id_libro = %s;"
            param = (libro.editorial, libro.anio_publicacion, libro.ISBN, libro.nombre, libro.cantidad_disponible, libro.id_libro)
            cursor = self.conn.cursor()
            cursor.execute(sql, param)
            self.conn.commit()
            
            sql = "SELECT id_genero FROM generos WHERE nombre = %s;"
            param = (libro.genero,)
            cursor.execute(sql, param)
            id_genero = cursor.fetchone()[0]
            self.conn.commit()
            
            sql = "UPDATE libro_genero SET id_genero = %s WHERE id_libro = %s"
            param = (id_genero, libro.id_libro)
            cursor.execute(sql, param)
            self.conn.commit()
            return True
        
        except IntegrityError as e:
            print(e, f"Linea {e.__traceback__.tb_lineno}")
            return False
        except DatabaseError as e:
            print(e, f"Linea {e.__traceback__.tb_lineno}")
            return False
        except Exception as e:
            print(e, f"Linea {e.__traceback__.tb_lineno}")
            return False
        finally:
            self.__desconectar()

    def eliminarLibro(self, libro: Libro):
        """
        Función para eliminar un libro de la base de datos

        Args:
            libro (Libro): Objeto de la clase Libro

        Returns:
            Bool: Regresa verdadero si el libro se elimina, falso si no
        """
        try:
            self.__conectar()
            
            sql = "DELETE FROM libro_autor WHERE id_libro = %s;"
            param = (libro.id_libro,)
            cursor = self.conn.cursor()
            cursor.execute(sql, param)
            self.conn.commit()
            
            sql = "DELETE FROM libro_genero WHERE id_libro = %s;"
            param = (libro.id_libro,)
            cursor.execute(sql, param)
            self.conn.commit()
            
            sql = "DELETE FROM libros WHERE nombre = %s;"
            param = (libro.nombre,)
            cursor.execute(sql, param)
            self.conn.commit()
            return True
        except IntegrityError as e:
            print(e, f"Linea {e.__traceback__.tb_lineno}")
            return False
        finally:
            self.__desconectar()
    
    def obtenerLibrosPorAutor(self, autor):
        """
        Función para obtener los libros de un autor

        Args:
            autor (str): Nombre del autor

        Returns:
            libros: Regresa los libros del autor
            Bool: Regresa falso si hay un error
        """
        try:
            self.__conectar()
            
            sql = "SELECT libros.id_libro, libros.nombre, libros.editorial, libros.anio_publicacion, libros.ISBN, libros.cantidad_disponible FROM libros JOIN libro_autor using(id_libro) JOIN autores using(id_autor) WHERE autores.nombre = %s;"
            param = (autor,)
            cursor = self.conn.cursor()
            cursor.execute(sql, param)
            libros = cursor.fetchall()
            return libros
        except IntegrityError as e:
            print(e, f"Linea {e.__traceback__.tb_lineno}")
            return False
        finally:
            self.__desconectar()
            
    def obtenerLibrosPorGenero(self, genero):
        """
        Obtiene los libros usando el genero de los mismos

        Args:
            genero (str): El nombre del genero a filtrar

        Returns:
            libros: Los libros encontrados
            bool: False si ocurre un error
        """
        try:
            self.__conectar()
            
            sql = "SELECT libros.nombre FROM libros JOIN libro_genero using(id_libro) JOIN generos using(id_genero) WHERE generos.nombre = %s;"
            param = (genero,)
            cursor = self.conn.cursor()
            cursor.execute(sql, param)
            libros = cursor.fetchall()
            return libros
        except IntegrityError as e:
            print(e, f"Linea {e.__traceback__.tb_lineno}")
            return False
        finally:
            self.__desconectar()
    
    def registrarAutor(self, autor: Autor):
        """
        Añade el autor a la tabla de autores

        Args:
            autor (Autor): Objeto de clase Autor

        Returns:
            Bool: Verdadero si inserta el autor correctamente, falso si no
        """
        try:
            self.__conectar()
            sql = "INSERT INTO autores (nombre) VALUES (%s);"
            param = (autor.nombre,)
            cursor = self.conn.cursor()
            cursor.execute(sql, param)
            self.conn.commit()
            return True
        except IntegrityError as e:
            print(e, f"Linea {e.__traceback__.tb_lineno}")
            return False
        except Exception as e:
            print(e, f"Linea {e.__traceback__.tb_lineno}")
            return False
        finally:
            self.__desconectar()
    
    def registrarEditorial(self, editorial: str):
        """
        Añade la editorial a la tabla de editoriales

        Args:
            editorial (str): Nombre de la editorial

        Returns:
            Bool: Verdadero si inserta la editorial correctamente, falso si no
        """
        try:
            self.__conectar()
            sql = "INSERT INTO editoriales (nombre) VALUES (%s);"
            param = (editorial,)
            cursor = self.conn.cursor()
            cursor.execute(sql, param)
            self.conn.commit()
            return True
        except IntegrityError as e:
            print(e, f"Linea {e.__traceback__.tb_lineno}")
            return False
        except Exception as e:
            print(e, f"Linea {e.__traceback__.tb_lineno}")
            return False
        finally:
            self.__desconectar()
    
    def registrarGenero(self, genero: str):
        """
        Añade el genero a la tabla de generos

        Args:
            genero (str): Nombre del genero

        Returns:
            Bool: Verdadero si inserta el genero correctamente, falso si no
        """
        try:
            self.__conectar()
            sql = "INSERT INTO generos (nombre) VALUES (%s);"
            param = (genero,)
            cursor = self.conn.cursor()
            cursor.execute(sql, param)
            self.conn.commit()
            return True
        except IntegrityError as e:
            print(e, f"Linea {e.__traceback__.tb_lineno}")
            return False
        except Exception as e:
            print(e, f"Linea {e.__traceback__.tb_lineno}")
            return False
        finally:
            self.__desconectar()
            
    def obtenerEditoriales(self):
        """
        Obtiene las editoriales de la base de datos

        Returns:
            editoriales: Las editoriales encontradas
            bool: False si ocurre un error
        """
        try:
            self.__conectar()
            
            sql = "SELECT nombre FROM editoriales;"
            cursor = self.conn.cursor()
            cursor.execute(sql)
            editoriales = cursor.fetchall()
            return editoriales
        except IntegrityError as e:
            print(e, f"Linea {e.__traceback__.tb_lineno}")
            return False
        except Exception as e:
            print(e, f"Linea {e.__traceback__.tb_lineno}")
            return False
        finally:
            self.__desconectar()
            
    def obtenerLibrosPorEditorial(self, editorial):
        """
        Obtiene los libros usando la editorial de los mismos

        Args:
            editorial (str): El nombre de la editorial a filtrar

        Returns:
            libros: Los libros encontrados
            bool: False si ocurre un error
        """
        try:
            self.__conectar()
            
            sql = "SELECT libros.nombre FROM libros JOIN libro_editorial using(id_libro) JOIN editoriales using(id_editorial) WHERE editoriales.nombre = %s;"
            param = (editorial,)
            cursor = self.conn.cursor()
            cursor.execute(sql, param)
            libros = cursor.fetchall()
            return libros
        except IntegrityError as e:
            print(e, f"Linea {e.__traceback__.tb_lineno}")
            return False
        finally:
            self.__desconectar()
            
    def actualizarAutor(self, autor: Autor, nuevoNombre: str):
        """
        Actualiza el autor en la base de datos

        Args:
            autor (Autor): Objeto de clase Autor

        Returns:
            Bool: Verdadero si actualiza el autor correctamente, falso si no
        """
        try:
            self.__conectar()
            sql = "UPDATE autores SET nombre = %s WHERE nombre = %s;"
            param = (nuevoNombre, autor.nombre)
            cursor = self.conn.cursor()
            cursor.execute(sql, param)
            self.conn.commit()
            return True
        except IntegrityError as e:
            print(e, f"Linea {e.__traceback__.tb_lineno}")
            return False
        except Exception as e:
            print(e, f"Linea {e.__traceback__.tb_lineno}")
            return False
        finally:
            self.__desconectar()
            
    def actualizarEditorial(self, editorial: str, nuevoNombre: str):
        """
        Actualiza la editorial en la base de datos

        Args:
            editorial (str): Nombre de la editorial

        Returns:
            Bool: Verdadero si actualiza la editorial correctamente, falso si no
        """
        try:
            self.__conectar()
            print(f"{nuevoNombre}|{editorial}")
            sql = "UPDATE editoriales SET nombre = %s WHERE nombre = %s;"
            param = (nuevoNombre, editorial)
            cursor = self.conn.cursor()
            cursor.execute(sql, param)
            self.conn.commit()
            
            if cursor.rowcount == 0:
                print("No se encontró la editorial para actualizar.")
            print("Editorial actualizada exitosamente.")
            
            return True
        except IntegrityError as e:
            print(e, f"Linea {e.__traceback__.tb_lineno}")
            return False
        except Exception as e:
            print(e, f"Linea {e.__traceback__.tb_lineno}")
            return False
        finally:
            self.__desconectar()
            
    def actualizarGenero(self, genero: str, nuevoNombre: str):
        """
        Actualiza el genero en la base de datos

        Args:
            genero (str): Nombre del genero

        Returns:
            Bool: Verdadero si actualiza el genero correctamente, falso si no
        """
        try:
            self.__conectar()
            sql = "UPDATE generos SET nombre = %s WHERE nombre = %s;"
            param = (nuevoNombre, genero)
            cursor = self.conn.cursor()
            cursor.execute(sql, param)
            self.conn.commit()
            return True
        except IntegrityError as e:
            print(e, f"Linea {e.__traceback__.tb_lineno}")
            return False
        except Exception as e:
            print(e, f"Linea {e.__traceback__.tb_lineno}")
            return False
        finally:
            self.__desconectar()
    
    def actualizarUsuario(self, nombreAntiguo: str, usuario: Usuario):
        """
        Actualiza el usuario en la base de datos

        Args:
            usuario (Usuario): Objeto de clase Usuario
            nombreAntiguo (str): Nombre actual del Usuario

        Returns:
            Bool: Verdadero si actualiza el usuario correctamente, falso si no
        """
        try:
            self.__conectar()
            sql = "UPDATE usuarios SET nombreUsuario = %s, nombre = %s, apellido = %s, correo = %s, telefono = %s WHERE nombreUsuario = %s;"
            param = (usuario.nombreUsuario, usuario.nombre, usuario.apellido, usuario.correo, usuario.telefono, nombreAntiguo)
            cursor = self.conn.cursor()
            cursor.execute(sql, param)
            self.conn.commit()
            return True
        except IntegrityError as e:
            print(e, f"Linea {e.__traceback__.tb_lineno}")
            return False
        except Exception as e:
            print(e, f"Linea {e.__traceback__.tb_lineno}")
            return False
        finally:
            self.__desconectar()

    def obtenerEmpleados(self):
        """
        Obtiene los empleados de la base de datos

        Returns:
            empleados: Los empleados encontrados
            bool: False si ocurre un error
        """
        try:
            self.__conectar()
            
            sql = "SELECT id_empleado, nombres, apellidos, nombreUsuario, esAdministrador FROM empleados, usuarios where nombres = nombre and apellidos = apellido;"
            cursor = self.conn.cursor()
            cursor.execute(sql)
            empleados = cursor.fetchall()
            return empleados
        except IntegrityError as e:
            print(e, f"Linea {e.__traceback__.tb_lineno}")
            return False
        finally:
            self.__desconectar()
            
    def obtenerEmpleado(self, empleado: Empleado):
        """
        Obtiene un empleado de la base de datos

        Args:
            empleado (Empleado): Objeto de clase Empleado

        Returns:
            empleado: El empleado encontrado
            bool: False si ocurre un error
        """
        try:
            self.__conectar()
            
            sql = "SELECT id_empleado, nombres, apellidos, nombreUsuario, esAdministrador FROM empleados, usuarios where nombres = nombre and apellidos = apellido and nombreUsuario = %s;"
            param = (empleado.nombreUsuario,)
            cursor = self.conn.cursor()
            cursor.execute(sql, param)
            empleado = cursor.fetchall()
            print(empleado)
            return empleado
        except IntegrityError as e:
            print(e, f"Linea {e.__traceback__.tb_lineno}")
            return False
        finally:
            self.__desconectar()
        
    def actualizarEmpleado(self, nombreAnterior: str, empleado: Empleado):
        """
        Actualiza el empleado en la base de datos

        Args:
            empleado (Empleado): Objeto de clase Empleado
            nuevoNombreUsuario (str): Nombre de usuario nuevo

        Returns:
            Bool: Verdadero si actualiza el empleado correctamente, falso si no
        """
        try:
            self.__conectar()
            sql = "UPDATE empleados INNER JOIN usuarios ON empleados.nombres = usuarios.nombre AND empleados.apellidos = usuarios.apellido SET nombres = %s, apellidos = %s, nombreUsuario = %s, esAdministrador = %s WHERE usuarios.nombreUsuario = %s;"
            param = (empleado.nombre, empleado.apellido, empleado.nombreUsuario, empleado.administrador, nombreAnterior)
            cursor = self.conn.cursor()
            cursor.execute(sql, param)
            self.conn.commit()
            return True
        except IntegrityError as e:
            print(e, f"Linea {e.__traceback__.tb_lineno}")
            return False
        except Exception as e:
            print(e, f"Linea {e.__traceback__.tb_lineno}")
            return False
        finally:
            self.__desconectar()
            
    def obtenerReservas(self):
        """
        Obtiene las reservas de la base de datos

        Returns:
            reservas: Las reservas encontradas
            bool: False si ocurre un error
        """
        try:
            self.__conectar()
            
            sql = "SELECT id_reserva, usuarios.nombreUsuario, reserva, fecha_reserva FROM reservas INNER JOIN usuarios using(id_usuario);"
            cursor = self.conn.cursor()
            cursor.execute(sql)
            reservas = cursor.fetchall()
            return reservas
        except IntegrityError as e:
            print(e, f"Linea {e.__traceback__.tb_lineno}")
            return False
        finally:
            self.__desconectar()

    def reservarLibro(self, libro: Libro, usuario: Usuario):
        """
        Reserva un libro en la base de datos

        Args:
            libro (Libro): Objeto de clase Libro
            usuario (Usuario): Objeto de clase Usuario

        Returns:
            Bool: Verdadero si reserva el libro correctamente, falso si no
        """
        try:
            self.__conectar()
            sql = "insert into reservas values (0 , %s, %s, %s,NOW());"
            param = (usuario.nombreUsuario, libro.id_libro, libro.nombre)
            print(param)
            cursor = self.conn.cursor()
            cursor.execute(sql, param)
            self.conn.commit()

            sql = "update libros set cantidad_disponible = cantidad_disponible - 1 where id_libro = %s;"
            param = (libro.id_libro,)
            cursor.execute(sql, param)
            self.conn.commit()
            return True
        
        except IntegrityError as e:
            print(e, f"Linea {e.__traceback__.tb_lineno}")
            return False
        except Exception as e:
            print(e, f"Linea {e.__traceback__.tb_lineno}")
            return False
        finally:
            self.__desconectar()
            
    def eliminarReserva(self, id_reserva, libro: Libro):
        """
        Elimina una reserva de la base de datos

        Args:
            id_reserva (int): ID de la reserva
            libro (Libro): Objeto de clase Libro

        Returns:
            Bool: Verdadero si elimina la reserva correctamente, falso si no
        """
        try:
            self.__conectar()
            sql = "delete from reservas where id_reserva = %s;"
            param = (id_reserva,)
            cursor = self.conn.cursor()
            cursor.execute(sql, param)
            self.conn.commit()

            sql = "update libros set cantidad_disponible = cantidad_disponible + 1 where id_libro = %s;"
            param = (libro.id_libro,)
            cursor.execute(sql, param)
            self.conn.commit()
            return True
        
        except IntegrityError as e:
            print(e, f"Linea {e.__traceback__.tb_lineno}")
            return False
        except Exception as e:
            print(e, f"Linea {e.__traceback__.tb_lineno}")
            return False
        finally:
            self.__desconectar()