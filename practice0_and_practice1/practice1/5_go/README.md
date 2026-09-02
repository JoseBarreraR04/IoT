# Práctica 5: Contenedor con Go

Esta práctica es similar a la de Java y Python, pero enfocada en el lenguaje Go (Golang). Mostraremos cómo ejecutar y compilar código Go dentro de un contenedor.

## 1. Construir la imagen

En la terminal, dentro de la carpeta `5_go`, ejecuta:

```bash
docker build -t mi_go_app .
```

## 2. Ejecutar el contenedor con Volumen

Montamos nuestro código local dentro del contenedor:

**Linux/macOS:**
```bash
docker run --name contenedor_go -v $(pwd)/src:/app -d mi_go_app
```

**Windows (PowerShell):**
```powershell
docker run --name contenedor_go -v ${PWD}/src:/app -d mi_go_app
```

## 3. Ejecutar el código Go

Con Go, puedes ejecutar el código directamente sin generar un binario permanente usando `go run`.
Puedes hacerlo entrando al contenedor:

```bash
docker exec -it contenedor_go bash
```
Y una vez dentro:
```bash
go run main.go
```
*(Escribe `exit` para salir)*

O puedes ejecutarlo sin entrar en la consola del contenedor usando `docker exec` directamente:
```bash
docker exec contenedor_go go run main.go
```

## 4. Compilar un binario (Opcional)

Si deseas compilar el código Go en un ejecutable:

```bash
docker exec contenedor_go go build -o mi_programa main.go
```
Esto creará un archivo llamado `mi_programa` en la carpeta `src` (¡visible desde tu máquina!). Luego puedes ejecutar ese binario dentro del contenedor:
```bash
docker exec contenedor_go ./mi_programa
```

## 5. Limpieza

```bash
docker stop contenedor_go
docker rm contenedor_go
```
