"""Interfaz web del proyecto RSA. Ejecutar: streamlit run app.py."""
import streamlit as st

from detalle import detalle
from rsa_text import desencriptar, encriptar


st.set_page_config(page_title="RSA · Grupo 16", page_icon="🔐", layout="wide")


def invalidar(prefijo):
    st.session_state.pop(prefijo + "_resultado", None)
    st.session_state.pop(prefijo + "_error", None)


def limpiar(prefijo):
    for campo in ("p", "q", "e", "texto", "L"):
        st.session_state[prefijo + "_" + campo] = ""
    invalidar(prefijo)


def transferir():
    r = st.session_state["enc_resultado"]
    for campo in ("p", "q", "e"):
        st.session_state["dec_" + campo] = str(getattr(r.clave, campo))
    st.session_state["dec_texto"] = r.cifrado
    st.session_state["dec_L"] = str(r.longitud)
    invalidar("dec")


def ejecutar(prefijo, descifra):
    invalidar(prefijo)
    s = st.session_state
    parametros = [s[prefijo + "_" + campo] for campo in ("p", "q", "e")]
    try:
        texto = s[prefijo + "_texto"]
        r = (desencriptar(texto, s[prefijo + "_L"], *parametros)
             if descifra else encriptar(texto, *parametros))
        s[prefijo + "_resultado"] = r
    except ValueError as error:
        s[prefijo + "_error"] = str(error)


def panel(prefijo, descifra=False):
    for campo, valor in (("p", "367"), ("q", "373"), ("e", "17"),
                         ("texto", ""), ("L", "")):
        st.session_state.setdefault(prefijo + "_" + campo, valor)
    columnas = st.columns(4 if descifra else 3)
    for columna, campo in zip(columnas, ("p", "q", "e", "L")):
        with columna:
            st.text_input(campo, key=prefijo + "_" + campo,
                          on_change=invalidar, args=(prefijo,))
    if descifra:
        etiqueta = "C: bloques de 6 dígitos separados por un único espacio"
        ayuda = "L es la longitud del mensaje original, incluidos sus espacios."
    else:
        etiqueta = "M: mensaje original"
        ayuda = "Solo ASCII 32–126, sin tildes, ñ ni saltos de línea. Los espacios cuentan."
    st.text_area(etiqueta, key=prefijo + "_texto", help=ayuda,
                 on_change=invalidar, args=(prefijo,))
    botones = st.columns(2)
    with botones[0]:
        st.button("Desencriptar" if descifra else "Encriptar", type="primary",
                  key=prefijo + "_ejecutar", on_click=ejecutar, args=(prefijo, descifra))
    with botones[1]:
        st.button("Limpiar", key=prefijo + "_limpiar", on_click=limpiar, args=(prefijo,))
    error = st.session_state.get(prefijo + "_error")
    if error:
        st.error(error)
    r = st.session_state.get(prefijo + "_resultado")
    if r is None:
        return
    st.success("Operación completada.")
    clave = r.clave
    st.code(f"n = {clave.n}   phi = {clave.phi}   MCD(e, phi) = 1\n"
            f"L = {r.longitud}   Relleno: {'sí, un espacio (032)' if r.relleno else 'no'}\n"
            f"Llave pública (e, n) = ({clave.e}, {clave.n})", language=None)
    if descifra:
        st.code(f"d = {r.d}   Llave privada (d, n) = ({r.d}, {clave.n})", language=None)
    st.code(f'M = "{r.mensaje}"\nL = {r.longitud}\nC = {r.cifrado}', language=None)
    st.caption("Usa el icono de copiar del recuadro para copiar C y L.")
    st.code(f"C = {r.cifrado}\nL = {r.longitud}", language=None)
    st.download_button("Descargar C y L", f"C = {r.cifrado}\nL = {r.longitud}\n",
                       file_name="resultado_rsa.txt", mime="text/plain",
                       key=prefijo + "_descargar")
    if not descifra:
        st.button("Usar en Desencriptar", key="transferir", on_click=transferir)
        st.caption("Después de transferir, abre la pestaña Desencriptar y pulsa Desencriptar.")
    with st.expander("Detalle del proceso", expanded=True):
        st.code(detalle(r), language=None)


st.title("RSA · Texto en parejas ASCII")
st.caption("MM2015 · Matemática Discreta 1 · Grupo 16")
st.caption("Francisco Rodriguez Hernandez · Juanes Lou Narvaez")
st.write("Encripta y desencripta mensajes con RSA y consulta la conversión ASCII de cada bloque.")
with st.expander("Cómo probar el programa"):
    st.write('Usa p = 367, q = 373, e = 17 y el mensaje RSA (sin comillas). '
             'El resultado debe ser C = 026054 123875 y L = 3. '
             'Pulsa Usar en Desencriptar, abre esa pestaña y pulsa Desencriptar: recuperarás RSA.')
    st.write("Los primos deben ser distintos y cumplir 126126 < p × q < 1000000. "
             "e debe ser mayor que 1 y coprimo con phi.")
encriptacion, desencriptacion = st.tabs(["Encriptar", "Desencriptar"])
with encriptacion:
    panel("enc")
with desencriptacion:
    panel("dec", descifra=True)
