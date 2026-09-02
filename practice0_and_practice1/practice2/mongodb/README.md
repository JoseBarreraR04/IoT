# Práctica de MongoDB

## 1. Levantar y Apagar el Entorno (Docker Compose)
El proyecto está configurado para levantar MongoDB y el contenedor de Python con un solo comando.

* **Para iniciar el entorno (MongoDB + Contenedor Python):**
  ```bash
  docker compose up -d --build
  ```

* **Para detener y borrar los contenedores al terminar:**
  ```bash
  docker compose down --rmi all
  ```

---

## 2. Conectarse a la base de datos
Instala [MongoDB Compass](https://www.mongodb.com/products/tools/compass) y conéctate a la base de datos local usando las credenciales preconfiguradas (Usuario: `admin`, Password: `password123`, Puerto: `27017`).

---

## 3. Script de Python
En la carpeta `test_mongodb` encontrarás un script en python (`main.py`) que permite agregar, consultar y actualizar documentos en mongodb. Para ejecutarlo usarás el contenedor de python y los ambientes virtuales.

---

## 4. Entorno de Python para pruebas manuales
Vamos a usar el contenedor de Python (`python_app`) para ejecutar el script `main.py`.

### Pasos para configurar y ejecutar el entorno con `uv` (desde cero)

1. **Ingresar al contenedor de Python:**
   ```bash
   docker exec -it python_app bash
   ```

2. **Revisar el contenido:**
   ```bash
   ls -la
   ```

3. **Inicializar el proyecto (crea los archivos de configuración de uv):**
   ```bash
   uv init
   ```
   *(Esto generará los archivos `pyproject.toml` y `.python-version`)*

4. **Crear el ambiente virtual:**
   ```bash
   uv venv
   ```

5. **Activar el ambiente virtual:**
   ```bash
   source .venv/bin/activate
   ```

6. **Agregar los paquetes necesarios:**
   Para este ejercicio necesitamos la librería de MongoDB, así que la agregaremos con `uv`:
   ```bash
   uv add pymongo
   ```

7. **Ejecutar el script en Python:**
   ```bash
   uv run main.py
   # O si ya tienes el entorno activado:
   python main.py
   ```

8. **Salir del contenedor:** Escribe `exit` (o usa `Ctrl+D`) para volver a tu terminal y poder apagar el entorno (Paso 1).

---

## 🛠️ Instalación y Ejecución Local (Opcional)
*Las siguientes instrucciones son **solo** si deseas instalar las herramientas y ejecutar el código directamente en tu computadora (sin usar el contenedor de Docker de Python).*

### A. Instalación de Requisitos (`uv` y Python / `venv`)

#### 1. Instalación de `uv`

* **Linux y macOS:**
  ```bash
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```
  *O en macOS usando Homebrew:*
  ```bash
  brew install uv
  ```

* **Windows:**
  En PowerShell:
  ```powershell
  powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
  ```
  *O usando winget:*
  ```cmd
  winget install --id astral-sh.uv
  ```

* **En cualquier SO (vía `pip` si ya se cuenta con Python instalado):**
  ```bash
  pip install uv
  ```

#### 2. Instalación de Python y `venv` (`python3-venv`)

> **Nota importante:** En Windows y macOS, el módulo `venv` viene **incluido por defecto** al instalar Python. En Linux (Debian/Ubuntu) sí requiere instalar un paquete separado.

* **Linux (Ubuntu / Debian):**
  ```bash
  sudo apt update
  sudo apt install python3 python3-venv python3-pip
  ```

* **macOS:**
  Descargar e instalar desde [python.org](https://www.python.org/) o usando Homebrew:
  ```bash
  brew install python
  ```
  *(El módulo `venv` ya viene incluido en la instalación).*

* **Windows:**
  Descargar el instalador ejecutable desde [python.org](https://www.python.org/) (marcar la casilla *"Add python.exe to PATH"*) o desde la **Microsoft Store**.
  *(El módulo `venv` ya viene incluido en la instalación).*

---

### B. Ejecución local con el ambiente virtual tradicional (`venv` + `pip`)

Si prefieres usar el método clásico de Python en lugar de `uv` en tu máquina local:

#### 1. Archivo `requirements.txt`
Asegúrate de tener un archivo `requirements.txt` en la carpeta `test_mongodb` con el siguiente contenido:
```text
pymongo>=4.16.0
```

#### 2. Comandos para crear, activar e instalar:

1. **Ingresar a la carpeta del proyecto:**
   ```bash
   cd test_mongodb
   ```

2. **Crear el ambiente virtual:**
   ```bash
   python3 -m venv .venv
   # En Windows si python3 no está en el alias:
   python -m venv .venv
   ```

3. **Activar el ambiente virtual:**
   * En **Linux / macOS**:
     ```bash
     source .venv/bin/activate
     ```
   * En **Windows (PowerShell)**:
     ```powershell
     .venv\Scripts\activate
     ```

4. **Instalar las dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Ejecutar el script:**
   ```bash
   python main.py
   ```
