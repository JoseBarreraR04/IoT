# Práctica 1: MongoDB con Docker

En esta práctica, aprenderemos a ejecutar una base de datos MongoDB usando Docker sin necesidad de un `Dockerfile` personalizado, simplemente utilizando la imagen oficial. Además, veremos cómo conectarnos y operar la base de datos usando la interfaz gráfica **MongoDB Compass**.

## 1. Ejecutar el contenedor de MongoDB

Para iniciar un contenedor con la última versión de MongoDB oficial, ejecuta el siguiente comando en tu terminal:

```bash
docker run --name mi_mongodb -p 27017:27017 -e MONGO_INITDB_ROOT_USERNAME=admin -e MONGO_INITDB_ROOT_PASSWORD=secreto -d mongo
```

**Explicación del comando:**
* `docker run`: Comando para crear y arrancar un contenedor.
* `--name mi_mongodb`: Asignamos el nombre `mi_mongodb` al contenedor.
* `-p 27017:27017`: Mapea el puerto 27017 de tu máquina local al puerto 27017 del contenedor (puerto por defecto de Mongo).
* `-e MONGO_INITDB_ROOT_USERNAME=admin`: Establece el usuario administrador.
* `-e MONGO_INITDB_ROOT_PASSWORD=secreto`: Establece la contraseña del administrador.
* `-d`: Ejecuta el contenedor en segundo plano (detached mode).
* `mongo`: El nombre de la imagen oficial de MongoDB en Docker Hub.

Para verificar que está corriendo:
```bash
docker ps
```

## 2. Instalar MongoDB Compass

MongoDB Compass es la interfaz gráfica oficial (GUI) para MongoDB.

1. Ve a la página oficial de descarga: [Descargar MongoDB Compass](https://www.mongodb.com/try/download/compass).
2. Selecciona tu sistema operativo (Linux, Windows o macOS) y descarga el instalador.
3. Sigue las instrucciones típicas de instalación de tu sistema operativo.

## 3. Conectarse a la base de datos

1. Abre **MongoDB Compass**.
2. En la pantalla de inicio ("New Connection"), verás un campo para la **URI de conexión**.
3. Ingresa la siguiente URI, usando el usuario y contraseña que configuramos en Docker:
   ```
   mongodb://admin:secreto@localhost:27017/
   ```
4. Haz clic en el botón **Connect**.

## 4. Operaciones Básicas (CRUD) desde la Interfaz Gráfica

Una vez conectado, sigue estos pasos para realizar las operaciones básicas.

### A. Crear una Base de Datos y Colección
1. En el panel izquierdo, haz clic en el botón **"+"** (Create Database) junto a "Databases".
2. En **Database Name**, escribe: `colegio`
3. En **Collection Name** (las tablas en Mongo se llaman colecciones), escribe: `estudiantes`
4. Haz clic en **Create Database**.

### B. Insertar Documentos (Create)
1. Selecciona la base de datos `colegio` y luego haz clic en la colección `estudiantes`.
2. Haz clic en el botón verde **ADD DATA** y selecciona **Insert document**.
3. Pega el siguiente formato JSON para insertar un estudiante:
   ```json
   {
     "nombre": "Juan Perez",
     "edad": 22,
     "carrera": "Ingeniería de Sistemas"
   }
   ```
4. Haz clic en **Insert**.
5. Repite el proceso para insertar otro:
   ```json
   {
     "nombre": "Ana Gomez",
     "edad": 20,
     "carrera": "Diseño Gráfico"
   }
   ```

### C. Consultar (Read)
1. En la parte superior de la colección, hay una barra para hacer queries (dependiendo de la version dice `Filter`).
2. Para buscar a "Ana Gomez", escribe en el filtro:
   ```json
   { "nombre": "Ana Gomez" }
   ```
3. Haz clic en el botón **Find**. Verás que solo aparece el documento de Ana.
4. Para quitar el filtro, borra el texto y haz clic de nuevo en **Find**.

### D. Actualizar (Update)
1. Pasa el cursor sobre el documento de "Juan Perez".
2. Verás que aparecen íconos en la parte superior derecha del documento. Haz clic en el ícono del **lápiz** (Edit document).
3. Cambia la `"edad"` de `22` a `23`.
4. Haz clic en el botón **Update** en la parte inferior del documento.

### E. Borrar (Delete)
1. Pasa el cursor sobre el documento de "Ana Gomez".
2. Haz clic en el ícono de la **papelera** (Delete document).
3. Te pedirá confirmación. Haz clic en **Delete**.

## 5. Limpieza

Para detener y eliminar el contenedor de MongoDB cuando termines, ejecuta:
```bash
docker stop mi_mongodb
docker rm mi_mongodb
```
