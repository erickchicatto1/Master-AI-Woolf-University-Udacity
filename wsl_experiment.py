#!/usr/bin/env python3
"""
Abre una URL en el navegador predeterminado de Windows desde un script
ejecutado dentro de WSL.
"""

import subprocess
import sys


def abrir_url_en_windows(url: str) -> None:
    """
    Abre la URL indicada usando el navegador predeterminado de Windows.

    Usa 'cmd.exe /c start' que es el comando nativo de Windows para
    abrir el navegador predeterminado. Funciona directamente desde WSL
    porque WSL tiene acceso a los binarios de Windows en el PATH.
    """
    try:
        # El "" vacío después de "start" es necesario porque start
        # interpreta el primer argumento entre comillas como el título
        # de la ventana, no como la URL.
        subprocess.run(
            ["cmd.exe", "/c", "start", "", url],
            check=True,
        )
        print(f"Se abrió la URL: {url}")
    except FileNotFoundError:
        print("Error: no se encontró cmd.exe. ¿Seguro que estás en WSL "
              "con interoperabilidad habilitada?")
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"Error al intentar abrir la URL: {e}")
        sys.exit(1)


if __name__ == "__main__":
    # Puedes pasar la URL como argumento o dejar la de ejemplo
    url = sys.argv[1] if len(sys.argv) > 1 else "https://www.google.com"
    abrir_url_en_windows(url)
