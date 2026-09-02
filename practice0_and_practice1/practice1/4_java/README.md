# Práctica 4: Contenedor con Java

En esta práctica, usaremos un contenedor para compilar y ejecutar código Java, sin necesidad de tener el JDK instalado en nuestra máquina física.

## 1. Construir la imagen

En tu terminal, ubicado en la carpeta `4_java`, construye la imagen:

```bash
docker build -t mi_java_app .
```

## 2. Ejecutar el contenedor con Volumen

Iniciamos el contenedor montando la carpeta `src` local a `/app` en el contenedor:

**Linux/macOS:**
```bash
docker run --name contenedor_java -v $(pwd)/src:/app -d mi_java_app
```

**Windows (PowerShell):**
```powershell
docker run --name contenedor_java -v ${PWD}/src:/app -d mi_java_app
```

## 3. Entrar al contenedor, compilar y ejecutar

Entra al contenedor en modo interactivo:
```bash
docker exec -it contenedor_java bash
```

Una vez dentro, compila el código Java usando `javac`:
```bash
javac Main.java
```
Esto generará un archivo `Main.class`. Dado que usamos un volumen, verás aparecer este archivo también en tu máquina local en la carpeta `src`.

Ahora ejecuta el código compilado:
```bash
java Main
```

*(Para salir del contenedor, escribe: `exit`)*

## 4. Editar código desde fuera

1. Desde tu máquina local, abre el archivo `src/Main.java`.
2. Modifica el mensaje, por ejemplo: `System.out.println("¡Hola nuevamente, he editado esto sin entrar al contenedor!");`
3. Guarda el archivo.
4. Entra al contenedor de nuevo (o usa un comando directo como se muestra abajo) para recompilar y ejecutar:

```bash
# Compilar directamente desde fuera del contenedor:
docker exec contenedor_java javac Main.java

# Ejecutar directamente desde fuera del contenedor:
docker exec contenedor_java java Main
```

## 5. Limpieza

```bash
docker stop contenedor_java
docker rm contenedor_java
```
