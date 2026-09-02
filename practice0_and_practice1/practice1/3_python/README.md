# Práctica 3: Contenedores con Python (Diferentes Versiones)

En esta práctica, vamos a crear dos contenedores utilizando `Dockerfiles` personalizados. Cada uno tendrá una versión distinta de Python (3.9 y 3.12). Aprenderemos a montar volúmenes para editar código desde nuestra máquina y a usar entornos virtuales (`venv`) dentro del contenedor.

## Estructura
- `Dockerfile.3.9`: Crea un entorno con Python 3.9
- `Dockerfile.3.12`: Crea un entorno con Python 3.12
- `src/main.py`: Código Python de ejemplo.

## 1. Construir las imágenes

Abre tu terminal en esta carpeta (`3_python`) y construye ambas imágenes:

```bash
docker build -t mi_python:3.9 -f Dockerfile.3.9 .
docker build -t mi_python:3.12 -f Dockerfile.3.12 .
```

## 2. Ejecutar los contenedores con Volúmenes

Vamos a iniciar ambos contenedores. Usaremos el flag `-v` (volumen) para que la carpeta `src` de nuestra máquina local esté sincronizada con la carpeta `/app` dentro del contenedor. Así, si editas `main.py` desde tu editor favorito, los cambios se reflejarán inmediatamente en el contenedor.

*(Asegúrate de ejecutar estos comandos estando ubicado en la carpeta `3_python`)*

**Para Linux/macOS:**
```bash
docker run --name contenedor_py39 -v $(pwd)/src:/app -d mi_python:3.9
docker run --name contenedor_py312 -v $(pwd)/src:/app -d mi_python:3.12
```

**Para Windows (PowerShell):**
```powershell
docker run --name contenedor_py39 -v ${PWD}/src:/app -d mi_python:3.9
docker run --name contenedor_py312 -v ${PWD}/src:/app -d mi_python:3.12
```

## 3. Entrar al contenedor y probar el código

Para ejecutar comandos dentro de un contenedor en ejecución, usamos `docker exec`.

### A. Python 3.9
Entra a la terminal (`bash`) del contenedor con Python 3.9:
```bash
docker exec -it contenedor_py39 bash
```
Una vez dentro (verás que tu prompt cambia), ejecuta el script:
```bash
python main.py
```
*Deberías ver que imprime la versión 3.9.x.*
Para salir del contenedor, escribe: `exit`

### B. Python 3.12
Entra al contenedor con Python 3.12:
```bash
docker exec -it contenedor_py312 bash
```
Ejecuta el script:
```bash
python main.py
```
*Deberías ver que imprime la versión 3.12.x.*

## 4. Crear un entorno virtual (venv)

Es una buena práctica aislar las dependencias. Estando **dentro del contenedor** (por ejemplo, en el de Python 3.12), crea un entorno virtual:

```bash
# Entrar al contenedor (si no estás dentro)
docker exec -it contenedor_py312 bash

# Crear el entorno virtual en la carpeta actual
python -m venv mi_entorno

# Activar el entorno virtual
source mi_entorno/bin/activate
```
Notarás que el prompt ahora empieza con `(mi_entorno)`. Ahora puedes instalar paquetes, por ejemplo:
```bash
pip install requests
```
*(Nota: Al haber mapeado el volumen, la carpeta `mi_entorno` también se creará en tu máquina local en la carpeta `src`)*.

Escribe `deactivate` para salir del entorno virtual y luego `exit` para salir del contenedor.

## 5. Limpieza

```bash
docker stop contenedor_py39 contenedor_py312
docker rm contenedor_py39 contenedor_py312
```
