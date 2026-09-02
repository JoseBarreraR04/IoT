# Práctica 6: Contenedor con C++

En esta práctica, usaremos un contenedor basado en la imagen oficial de GCC (`gcc`) para compilar y ejecutar código C++ sin necesidad de tener un compilador `g++` instalado en nuestra máquina física.

## 1. Construir la imagen

En la terminal, dentro de la carpeta `6_c++`, ejecuta:

```bash
docker build -t mi_cpp_app .
```

## 2. Ejecutar el contenedor con Volumen

Montamos nuestra carpeta local `src` dentro del contenedor en la ruta `/app`:

**Linux/macOS:**
```bash
docker run --name contenedor_cpp -v $(pwd)/src:/app -d mi_cpp_app
```

**Windows (PowerShell):**
```powershell
docker run --name contenedor_cpp -v ${PWD}/src:/app -d mi_cpp_app
```

## 3. Entrar al contenedor, compilar y ejecutar

Puedes entrar al contenedor de forma interactiva usando `bash`:

```bash
docker exec -it contenedor_cpp bash
```

Una vez dentro del contenedor:

1. Compila el archivo `main.cpp` con `g++`:
   ```bash
   g++ -o mi_programa main.cpp
   ```
   *Esto generará un ejecutable llamado `mi_programa` en la carpeta `src` (visible también desde tu máquina local debido al volumen).*

2. Ejecuta el binario compilado:
   ```bash
   ./mi_programa
   ```

*(Escribe `exit` para salir del contenedor)*.

## 4. Compilar y ejecutar directamente desde fuera

También puedes compilar y ejecutar directamente sin necesidad de abrir una consola interactiva dentro del contenedor:

```bash
# Compilar el código directamente:
docker exec contenedor_cpp g++ -o mi_programa main.cpp

# Ejecutar el binario generado:
docker exec contenedor_cpp ./mi_programa
```

## 5. Limpieza

Para detener y remover el contenedor:

```bash
docker stop contenedor_cpp
docker rm contenedor_cpp
```
