"""Pruebas del recorrido web con el simulador oficial de Streamlit."""
import unittest
from pathlib import Path

from streamlit.testing.v1 import AppTest


class PruebasWeb(unittest.TestCase):
    def setUp(self):
        self.app = AppTest.from_file(str(Path(__file__).with_name("app.py"))).run()
        self.assertFalse(self.app.exception)

    def test_cifrar_transferir_descifrar_y_editar(self):
        a = self.app
        a.text_area(key="enc_texto").set_value("RSA").run()
        a.button(key="enc_ejecutar").click().run()
        self.assertFalse(a.exception)
        self.assertEqual(a.session_state["enc_resultado"].cifrado, "026054 123875")
        a.button(key="transferir").click().run()
        self.assertEqual(a.text_area(key="dec_texto").value, "026054 123875")
        self.assertEqual(a.text_input(key="dec_L").value, "3")
        a.button(key="dec_ejecutar").click().run()
        self.assertFalse(a.exception)
        self.assertEqual(a.session_state["dec_resultado"].mensaje, "RSA")
        self.assertEqual(a.session_state["dec_resultado"].d, 8009)
        a.text_input(key="enc_e").set_value("2").run()
        self.assertNotIn("enc_resultado", a.session_state)
        a.button(key="enc_ejecutar").click().run()
        self.assertTrue(a.error)
        self.assertNotIn("enc_resultado", a.session_state)

    def test_espacios_limpieza_y_error(self):
        a = self.app
        a.text_area(key="enc_texto").set_value("  Hola  ").run()
        a.button(key="enc_ejecutar").click().run()
        a.button(key="transferir").click().run()
        a.button(key="dec_ejecutar").click().run()
        self.assertEqual(a.session_state["dec_resultado"].mensaje, "  Hola  ")
        a.text_input(key="dec_L").set_value("99").run()
        self.assertNotIn("dec_resultado", a.session_state)
        a.button(key="dec_ejecutar").click().run()
        self.assertTrue(a.error)
        a.button(key="dec_limpiar").click().run()
        for campo in ("p", "q", "e", "L"):
            self.assertEqual(a.text_input(key="dec_" + campo).value, "")
        self.assertEqual(a.text_area(key="dec_texto").value, "")
        self.assertFalse(a.error)
        self.assertFalse(a.exception)


if __name__ == "__main__":
    unittest.main(verbosity=2)
