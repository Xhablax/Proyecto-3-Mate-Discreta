import math
import random
import unittest

from rsa_math import es_primo, inverso_modular, mcd, potencia_modular
from rsa_text import desencriptar, encriptar, validar_clave

CLAVE = (367, 373, 17)
CASOS = (
    ("RSA", "082083 065032", "026054 123875"),
    ("Hola Mundo 2026!", "072111 108097 032077 117110 100111 032050 048050 054033",
     "109641 028621 013427 063943 072468 085047 075573 031479"),
    ("  Hola  mundo  ", "032032 072111 108097 032032 109117 110100 111032 032032",
     "038557 109641 028621 038557 048981 080373 058209 038557"),
    ("Ab#9 z", "065098 035057 032122", "130029 003564 002310"),
)


class PruebasMatematicas(unittest.TestCase):
    def test_primalidad(self):
        for n in range(-5, 1500):
            esperado = n >= 2 and all(n % divisor for divisor in range(2, n))
            self.assertEqual(es_primo(n), esperado, n)

    def test_mcd_con_oraculo(self):
        azar = random.Random(2015)
        for a, b in [(0, 0), (0, 7), (-36, 60)] + [
            (azar.randint(-1000000, 1000000), azar.randint(-1000000, 1000000))
            for _ in range(300)
        ]:
            self.assertEqual(mcd(a, b), math.gcd(a, b))

    def test_inverso_con_oraculo(self):
        for modulo in (2, 7, 40, 136152):
            for e in (-17, 1, 2, 3, 17, 65537, modulo + 17):
                with self.subTest(e=e, modulo=modulo):
                    if math.gcd(e, modulo) == 1:
                        self.assertEqual(inverso_modular(e, modulo), pow(e, -1, modulo))
                    else:
                        with self.assertRaises(ValueError):
                            inverso_modular(e, modulo)
        self.assertEqual(inverso_modular(17, 136152), 8009)

    def test_potencia_con_oraculo(self):
        azar = random.Random(17)
        for base, exponente, modulo in [(0, 0, 1), (0, 0, 11), (-4, 13, 497)] + [
            (azar.randint(-1000000, 1000000), azar.randrange(1000000), azar.randint(1, 1000000))
            for _ in range(300)
        ]:
            self.assertEqual(potencia_modular(base, exponente, modulo), pow(base, exponente, modulo))

    def test_dominios_invalidos(self):
        for modulo in (0, 1, -7):
            with self.assertRaises(ValueError):
                inverso_modular(17, modulo)
        for argumentos in ((2, -1, 5), (2, 3, 0), (2, 3, -1)):
            with self.assertRaises(ValueError):
                potencia_modular(*argumentos)


class PruebasRSA(unittest.TestCase):
    def test_casos_exactos(self):
        for mensaje, bloques, cifrado in CASOS:
            with self.subTest(mensaje=repr(mensaje)):
                r = encriptar(mensaje, *CLAVE)
                self.assertEqual((r.clave.n, r.clave.phi), (136891, 136152))
                self.assertEqual(" ".join(f"{b.m:06d}" for b in r.bloques), bloques)
                self.assertEqual(r.cifrado, cifrado)
                self.assertEqual(r.longitud, len(mensaje))
                self.assertEqual(r.relleno, len(mensaje) % 2 == 1)
                esperado = mensaje + " " if r.relleno else mensaje
                self.assertEqual(r.texto_completo, esperado)
                recuperado = desencriptar(cifrado, len(mensaje), *CLAVE)
                self.assertEqual(recuperado.mensaje, mensaje)
                self.assertEqual(recuperado.d, 8009)
                self.assertEqual(recuperado.bloques, r.bloques)

    def test_longitud_par_conserva_espacio(self):
        r = desencriptar("026054 123875", 4, *CLAVE)
        self.assertEqual(r.mensaje, "RSA ")
        self.assertFalse(r.relleno)

    def test_espacios_y_paridades(self):
        for mensaje in (" ", "  ", "   ", "A", "AB", "  a  ", " a ", "a ", " a", "~~~"):
            with self.subTest(mensaje=repr(mensaje)):
                r = encriptar(mensaje, *CLAVE)
                self.assertEqual(desencriptar(r.cifrado, r.longitud, *CLAVE).mensaje, mensaje)

    def test_todas_las_9025_parejas_ascii(self):
        mensaje = "".join(chr(a) + chr(b) for a in range(32, 127) for b in range(32, 127))
        r = encriptar(mensaje, *CLAVE)
        self.assertEqual(desencriptar(r.cifrado, len(mensaje), *CLAVE).mensaje, mensaje)
        for bloque in r.bloques:
            self.assertEqual(bloque.c, pow(bloque.m, 17, 136891))

    def test_otras_claves_y_e_mayor_que_phi(self):
        for clave in ((2, 65537, 17), (503, 509, 65537), (997, 991, 17), (367, 373, 25),
                      (367, 373, 4 * 136152 + 17)):
            r = encriptar(" ~AB 01! ", *clave)
            self.assertEqual(desencriptar(r.cifrado, r.longitud, *clave).mensaje, " ~AB 01! ")
        self.assertEqual(validar_clave("367", "373", "17").n, 136891)

    def test_claves_invalidas(self):
        for clave in ((4, 373, 17), (11, 13, 17), (367, 373, 2), (367, 367, 17),
                      (367, 4, 17), (0, 373, 17), (1009, 1013, 17), (367, 373, 1),
                      ("3.67", 373, 17), (367, "q", 17), (367, 373, "17.0"),
                      (True, 373, 17), (367, 373, "１７")):
            with self.subTest(clave=clave), self.assertRaises(ValueError):
                encriptar("RSA", *clave)

    def test_mensajes_invalidos(self):
        for mensaje in ("", "Mañana", "á", "a\tb", "a\nb", "a\rb", "\x1f", "\x7f", "🙂"):
            with self.subTest(mensaje=repr(mensaje)), self.assertRaises(ValueError):
                encriptar(mensaje, *CLAVE)

    def test_cifrados_invalidos(self):
        for cifrado in ("", "26054 123875", "999999 123875", "136891", "026054  123875",
                        " 026054", "026054 ", "026054\n123875", "026054\t123875",
                        "０２６０５４", "-26054", "02605A"):
            with self.subTest(cifrado=repr(cifrado)), self.assertRaises(ValueError):
                desencriptar(cifrado, 3, *CLAVE)

    def test_longitudes_invalidas(self):
        for longitud in (7, 0, -1, 2, 5, "3.0", "", " 3", True):
            with self.subTest(longitud=longitud), self.assertRaises(ValueError):
                desencriptar("026054 123875", longitud, *CLAVE)

    def test_ascii_recuperado_invalido(self):
        with self.assertRaisesRegex(ValueError, "ASCII recuperado inválido"):
            desencriptar("000000", 2, *CLAVE)

    def test_relleno_ausente(self):
        r = encriptar("AB", *CLAVE)
        with self.assertRaisesRegex(ValueError, "espacio final de relleno"):
            desencriptar(r.cifrado, 1, *CLAVE)


if __name__ == "__main__":
    unittest.main(verbosity=2)
