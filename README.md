# Security Recon App Proxy

**Security Recon App Proxy** es una herramienta de escaneo web diseñada para realizar reconocimiento de seguridad en objetivos web. Permite buscar correos electrónicos, números de teléfono, enlaces y servicios de terceros en una página web. Además, ofrece la opción de utilizar proxies para ocultar la identidad durante el escaneo.

## Tabla de Contenidos

- [Características](#características)
- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Uso](#uso)
- [Opciones de Proxy](#opciones-de-proxy)
- [Modo Debug](#modo-debug)
- [Contribución](#contribución)

## Características

- Buscar correos electrónicos en el contenido y en enlaces `mailto:`.
- Buscar números de teléfono en el contenido.
- Buscar enlaces en la página web.
- Identificar servicios de terceros a través de enlaces en etiquetas `script` y `link`.
- Opción de usar proxies para el escaneo.

## Requisitos

- Python 3.x
- Librerías: `BeautifulSoup4`, `requests`

## Instalación

1. Clona el repositorio:

   ```bash
   git clone https://github.com/JkDevArg/scrapicoco.git
   cd security-recon-tool
   ```

2. Instala las dependencias:

   ```bash
   pip install -r requirements.txt
   ```

## Uso

1. Ejecuta el script principal:

   ```bash
   python main.py
   ```

2. El menú principal te permitirá configurar el objetivo de escaneo, abrir la página de GitHub del proyecto o salir de la aplicación.

## Opciones de Proxy

Cuando se te solicite usar un proxy, puedes elegir entre las siguientes opciones:

- **A**: Usar un archivo de proxies proporcionado por el usuario.
- **I**: Descargar una lista de proxies desde [https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt](https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt) y guardarla como `proxy.txt`.
- **N**: No usar proxies.

## Modo Debug

Para activar el modo debug y ver mensajes detallados sobre el uso de proxies, ejecuta el script con el parámetro `-d`:

```bash
python main.py -d
```

En modo debug, los mensajes de error sobre proxies serán más detallados.

## Contribución

Si deseas contribuir al proyecto, por favor sigue estos pasos:

1. Haz un fork del repositorio.
2. Crea una rama para tu nueva funcionalidad (`git checkout -b nueva-funcionalidad`).
3. Realiza tus cambios y haz commit (`git commit -am 'Añadir nueva funcionalidad'`).
4. Envía tus cambios (`git push origin nueva-funcionalidad`).
5. Crea un Pull Request en GitHub.
