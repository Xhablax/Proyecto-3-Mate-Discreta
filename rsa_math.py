def es_primo(numero: int) -> bool:
    """Prueba divisores hasta la raíz, sin usar raíces de punto flotante."""
    if numero < 2:
        return False
    if numero == 2:
        return True
    if numero % 2 == 0:
        return False
    divisor = 3
    while divisor * divisor <= numero:
        if numero % divisor == 0:
            return False
        divisor += 2
    return True


def mcd(a: int, b: int) -> int:
    """Algoritmo de Euclides; devuelve un MCD no negativo."""
    a, b = abs(a), abs(b)
    while b:
        a, b = b, a % b
    return a


def inverso_modular(a: int, modulo: int) -> int:
    """Euclides extendido: obtiene x tal que a*x = 1 módulo modulo."""
    if modulo <= 1:
        raise ValueError("El módulo del inverso debe ser mayor que 1.")
    # t representa el coeficiente de a en las identidades de Bézout.
    resto_anterior, resto = modulo, a % modulo
    t_anterior, t = 0, 1
    while resto:
        cociente = resto_anterior // resto
        resto_anterior, resto = resto, resto_anterior - cociente * resto
        t_anterior, t = t, t_anterior - cociente * t
    if resto_anterior != 1:
        raise ValueError("No existe inverso modular: el MCD no es 1.")
    return t_anterior % modulo


def potencia_modular(base: int, exponente: int, modulo: int) -> int:
    """Exponenciación binaria con reducción en cada multiplicación."""
    if exponente < 0 or modulo <= 0:
        raise ValueError("Se requiere exponente >= 0 y módulo > 0.")
    resultado = 1 % modulo
    base %= modulo
    while exponente:
        if exponente % 2 == 1:
            resultado = (resultado * base) % modulo
        base = (base * base) % modulo
        exponente //= 2
    return resultado
