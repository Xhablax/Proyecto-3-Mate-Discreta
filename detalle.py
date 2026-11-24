def detalle(resultado):
    """Construye la conversión ASCII y la tabla antes/después."""
    r = resultado
    lineas = [f'Texto con relleno (si aplica): "{r.texto_completo}"',
            f"Longitud de ese texto: {len(r.texto_completo)}", "",
            "POS  CARÁCTER       ASCII  ORIGEN"]
    for i, caracter in enumerate(r.texto_completo, 1):
        visible = "[espacio]" if caracter == " " else repr(caracter)
        origen = "relleno" if r.relleno and i > r.longitud else "original"
        lineas.append(f"{i:3d}  {visible:<13} {ord(caracter):03d}    {origen}")
    descifra = r.d is not None
    formula = "m = c^d mod n" if descifra else "c = m^e mod n"
    lineas += ["", formula, " #   PAREJA     ENTRADA  -> SALIDA"]
    for i, bloque in enumerate(r.bloques, 1):
        antes, despues = (bloque.c, bloque.m) if descifra else (bloque.m, bloque.c)
        lineas.append(f'{i:2d}   "{bloque.pareja}"       {antes:06d} -> {despues:06d}')
    if descifra:
        lineas += ["", f"e*d mod phi = {(r.clave.e * r.d) % r.clave.phi}",
                "Se retiró exactamente un espacio final." if r.relleno
                else "L par: no se retiró ningún carácter."]
    return "\n".join(lineas)
