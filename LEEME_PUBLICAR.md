# Proyecto RSA · Grupo 16 · Versión web

Esta copia adapta la ventana Tkinter a Streamlit. `rsa_math.py` y `rsa_text.py`
son idénticos a los del proyecto original. `detalle.py` conserva la función de
explicación de la interfaz original. La aplicación web no importa Tkinter.

## Publicar desde el navegador

1. Extrae este ZIP en tu computadora.
2. En https://github.com crea un repositorio llamado `rsa-grupo16`. Para la
   ruta más sencilla, selecciona Public y marca Add a README file al crearlo.
3. Dentro del repositorio, elige Add file > Upload files. Arrastra los archivos
   que están DENTRO de `Grupo_No16_Web`, sin subir el ZIP ni la carpeta contenedora.
   Guarda con Commit changes. `app.py`, `rsa_math.py`, `rsa_text.py`, `detalle.py`
   y `requirements.txt` deben quedar en la raíz del repositorio.
4. Entra a https://share.streamlit.io/ y vincula tu cuenta de GitHub.
5. Pulsa Create app y selecciona la opción para desplegar una aplicación que ya tienes.
6. Selecciona el repositorio `rsa-grupo16`, la rama `main` y escribe `app.py`
   en Main file path. En Advanced settings selecciona Python 3.12.
7. Pulsa Deploy y espera a que aparezca la aplicación.
8. Comprueba en Settings > Sharing que la aplicación sea pública.
9. Abre el enlace de la aplicación en una ventana de incógnito. Debe permitir
   encriptar y desencriptar sin iniciar sesión. Prueba el ejemplo de abajo.
10. Entrega en Canvas el enlace terminado en `.streamlit.app` que te asignó
    Streamlit. El enlace al repositorio de GitHub no es el enlace de la aplicación.

Si no aparece tu repositorio, revisa que vinculaste la cuenta correcta y que
Streamlit tiene permiso para verlo. Si aparece un error de módulo, comprueba
que todos los archivos indicados estén juntos en la raíz del repositorio.

## Ejemplo de revisión

- p = 367, q = 373, e = 17.
- Mensaje: `RSA` (sin comillas).
- C esperado: `026054 123875`; L = 3.
- Pulsa Usar en Desencriptar, abre Desencriptar y pulsa Desencriptar.
- Mensaje recuperado: `RSA`; d = 8009.

Editar una entrada borra sus resultados anteriores. Limpiar vacía los campos.
Para copiar C y L, usa el icono de copiar del recuadro; también puedes descargarlos.
Los espacios originales se conservan. Se mantienen las validaciones del proyecto.

## Probar localmente (opcional)

Con Python 3.12, abre una terminal en esta carpeta y ejecuta:

```console
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Esto abre una dirección local para probar. Esa dirección local no sirve para
la entrega al profesor; primero completa la publicación de arriba.

## Pruebas

```console
python -m unittest -v test_rsa test_web
```

`test_rsa.py` conserva las 16 pruebas del proyecto original. `test_web.py`
comprueba el recorrido web de cifrar, transferir, descifrar, editar, limpiar
y mostrar errores. Requiere instalar `requirements.txt`.

## Referencias de publicación

- https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy
- https://docs.streamlit.io/deploy/streamlit-community-cloud/share-your-app

El ZIP contiene el código listo para desplegar. Un enlace público se obtiene
después de completar la publicación en tu cuenta.
