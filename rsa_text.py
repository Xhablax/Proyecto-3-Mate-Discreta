from dataclasses import dataclass
import re

from rsa_math import es_primo, inverso_modular, mcd, potencia_modular


@dataclass(frozen=True)
class Clave:
    p: int
    q: int
    e: int
    n: int
    phi: int


@dataclass(frozen=True)
class Bloque:
    pareja: str
    m: int
    c: int


@dataclass(frozen=True)
class Resultado:
    clave: Clave
    mensaje: str
    texto_completo: str
    longitud: int
    relleno: bool
    cifrado: str
    bloques: tuple[Bloque, ...]
    d: int | None = None


def entero(valor: int | str, nombre: str) -> int:
    """Acepta enteros o su escritura decimal ASCII, sin limpiar entradas."""
    if type(valor) is int:
        return valor
    if isinstance(valor, str) and re.fullmatch(r"[+-]?[0-9]+", valor):
        try:
            return int(valor)
        except ValueError as error:
            raise ValueError(f"{nombre}: entero demasiado largo para este Python.") from error
    raise ValueError(f"{nombre} debe ser un entero decimal, sin espacios.")


def validar_clave(p: int | str, q: int | str, e: int | str) -> Clave:
    """Calcula n y phi desde p y q; no factoriza n ni limita e a phi."""
    p, q, e = entero(p, "p"), entero(q, "q"), entero(e, "e")
    if p < 2 or q < 2:
        raise ValueError("p y q deben ser primos mayores o iguales que 2.")
    if p == q:
        raise ValueError("p y q deben ser primos distintos.")
    n = p * q
    # Descarta módulos enormes antes de intentar divisiones de primalidad.
    if n >= 1000000:
        raise ValueError("n = p*q debe cumplir 126126 < n < 1000000.")
    if not es_primo(p):
        raise ValueError("p no es primo.")
    if not es_primo(q):
        raise ValueError("q no es primo.")
    if n <= 126126:
        raise ValueError("n = p*q debe cumplir 126126 < n < 1000000.")
    phi = (p - 1) * (q - 1)
    if e <= 1:
        raise ValueError("e debe ser mayor que 1.")
    divisor = mcd(e, phi)
    if divisor != 1:
        raise ValueError(f"MCD(e, phi) = {divisor}; debe ser 1.")
    return Clave(p, q, e, n, phi)


def validar_mensaje(mensaje: str) -> None:
    """Rechaza vacío y caracteres fuera de ASCII 32..126; no los altera."""
    if not isinstance(mensaje, str) or not mensaje:
        raise ValueError("M debe contener al menos un carácter ASCII imprimible.")
    for posicion, caracter in enumerate(mensaje, 1):
        if not 32 <= ord(caracter) <= 126:
            raise ValueError(
                f"Carácter {caracter!r} en posición {posicion} no admitido "
                f"(código {ord(caracter)}). Solo ASCII 32 a 126."
            )


def encriptar(mensaje: str, p: int | str, q: int | str, e: int | str) -> Resultado:
    """Agrupa dos caracteres y cifra cada bloque con la función propia."""
    clave = validar_clave(p, q, e)
    validar_mensaje(mensaje)
    longitud = len(mensaje)
    relleno = longitud % 2 == 1
    completo = mensaje + " " if relleno else mensaje
    bloques = []
    for inicio in range(0, len(completo), 2):
        pareja = completo[inicio:inicio + 2]
        m = ord(pareja[0]) * 1000 + ord(pareja[1])
        c = potencia_modular(m, clave.e, clave.n)
        bloques.append(Bloque(pareja, m, c))
    cifrado = " ".join(f"{bloque.c:06d}" for bloque in bloques)
    return Resultado(clave, mensaje, completo, longitud, relleno, cifrado, tuple(bloques))


def desencriptar(cifrado: str, longitud: int | str,
                p: int | str, q: int | str, e: int | str) -> Resultado:
    """Valida y descifra; elimina exclusivamente el espacio de relleno."""
    clave = validar_clave(p, q, e)
    if not isinstance(cifrado, str) or not re.fullmatch(r"[0-9]{6}( [0-9]{6})*", cifrado):
        raise ValueError("C: use bloques de 6 dígitos 0-9 separados por un único espacio.")
    valores = [int(bloque) for bloque in cifrado.split(" ")]
    for indice, c in enumerate(valores, 1):
        if c >= clave.n:
            raise ValueError(f"Bloque {indice}: c = {c} debe ser menor que n = {clave.n}.")
    longitud = entero(longitud, "L")
    k = len(valores)
    if longitud not in (2 * k - 1, 2 * k):
        raise ValueError(f"L inconsistente: con {k} bloques debe ser {2*k-1} o {2*k}.")
    d = inverso_modular(clave.e, clave.phi)
    bloques = []
    for indice, c in enumerate(valores, 1):
        m = potencia_modular(c, d, clave.n)
        digitos = f"{m:06d}"
        a, b = int(digitos[:3]), int(digitos[3:])
        if not (32 <= a <= 126 and 32 <= b <= 126):
            raise ValueError(f"Bloque {indice}: ASCII recuperado inválido ({a:03d}, {b:03d}).")
        bloques.append(Bloque(chr(a) + chr(b), m, c))
    completo = "".join(bloque.pareja for bloque in bloques)
    relleno = longitud % 2 == 1
    if relleno and completo[-1] != " ":
        raise ValueError("L impar exige un espacio final de relleno; el texto no lo contiene.")
    # Corte exacto de UN carácter: conserva todos los espacios originales.
    mensaje = completo[:-1] if relleno else completo
    return Resultado(clave, mensaje, completo, longitud, relleno, cifrado, tuple(bloques), d)
