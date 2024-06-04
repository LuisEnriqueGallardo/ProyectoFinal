import unittest
from main import MyClass

class TestMyClass(unittest.TestCase):
    def setUp(self):
        self.my_class = MyClass()

    def test_actualizarInterfaz_libros(self):
        self.my_class.actualizarInterfaz("libros")
        expected_labels = ["Titulo", "Autor", "Editorial", "Año Publicación", "ISBN", "Genero", "Stock"]
        self.assertEqual(self.my_class.arbol.getHeaderLabels(), expected_labels)

    def test_actualizarInterfaz_autores(self):
        self.my_class.actualizarInterfaz("autores")
        expected_labels = ["Nombre", "Libros"]
        self.assertEqual(self.my_class.arbol.getHeaderLabels(), expected_labels)

    def test_actualizarInterfaz_editorial(self):
        self.my_class.actualizarInterfaz("editorial")
        expected_labels = ["Nombre", "Libros"]
        self.assertEqual(self.my_class.arbol.getHeaderLabels(), expected_labels)

    def test_actualizarInterfaz_genero(self):
        self.my_class.actualizarInterfaz("genero")
        expected_labels = ["Nombre", "Libros"]
        self.assertEqual(self.my_class.arbol.getHeaderLabels(), expected_labels)

    def test_actualizarInterfaz_comentarios(self):
        self.my_class.actualizarInterfaz("comentarios")
        expected_labels = ["Libro", "Usuario", "Comentario"]
        self.assertEqual(self.my_class.arbol.getHeaderLabels(), expected_labels)

if __name__ == '__main__':
    unittest.main()