# Práctica 2: PostgreSQL con Docker

En esta práctica, aprenderemos a ejecutar una base de datos relacional PostgreSQL usando Docker con la imagen oficial. También nos conectaremos utilizando la interfaz gráfica **DBeaver** para administrarla y ejecutar sentencias SQL.

## 1. Ejecutar el contenedor de PostgreSQL

Para iniciar el contenedor, ejecuta el siguiente comando:

```bash
docker run --name mi_postgres -p 5432:5432 -e POSTGRES_USER=admin -e POSTGRES_PASSWORD=secreto -e POSTGRES_DB=mi_basedatos -d postgres
```

**Explicación:**
* `--name mi_postgres`: Nombre del contenedor.
* `-p 5432:5432`: Mapea el puerto 5432 local al puerto 5432 del contenedor.
* `-e POSTGRES_USER=admin`: Define el usuario administrador.
* `-e POSTGRES_PASSWORD=secreto`: Define la contraseña.
* `-e POSTGRES_DB=mi_basedatos`: Crea automáticamente una base de datos con este nombre.
* `-d`: Ejecuta en segundo plano.
* `postgres`: Imagen oficial.

## 2. Instalar DBeaver

DBeaver es un cliente SQL multiplataforma que soporta muchas bases de datos, incluyendo PostgreSQL.

1. Ve a la página oficial de DBeaver Community: [Descargar DBeaver](https://dbeaver.io/download/).
2. Descarga la versión adecuada para tu sistema operativo.
3. Instálalo siguiendo los pasos por defecto de tu sistema.

## 3. Conectarse a la base de datos

1. Abre **DBeaver**.
2. En la barra de menú superior o en la esquina superior izquierda, haz clic en el ícono del enchufe **"Nueva conexión"** (New Database Connection).
3. En la lista de bases de datos, selecciona **PostgreSQL** y haz clic en **Siguiente**.
4. Llena los datos de la conexión:
   * **Host:** `localhost`
   * **Port:** `5432`
   * **Database:** `mi_basedatos`
   * **Username:** `admin`
   * **Password:** `secreto`
5. *(Opcional)* Haz clic en **Test Connection** para verificar que todo funciona. Es posible que te pida descargar los drivers de PostgreSQL la primera vez; acepta la descarga.
6. Haz clic en **Finalizar**.

## 4. Operaciones Básicas (CRUD) mediante Interfaz/SQL

En DBeaver, expande la conexión que acabas de crear a la izquierda, entra a `Databases` -> `mi_basedatos` -> `Schemas` -> `public` -> `Tables`.
Haz clic derecho en tu base de datos y selecciona **Editor SQL (SQL Editor)** para escribir los siguientes comandos.

### A. Crear una tabla (Create)
Copia este código en el Editor SQL y ejecútalo (presionando `Ctrl+Enter` o con el botón de "play" naranja):

```sql
CREATE TABLE estudiantes (
    codigo SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(50),
    semestre NUMERIC(10, 2)
);
```
*Si refrescas la carpeta "Tables" a la izquierda, verás tu nueva tabla `estudiantes`.*

### B. Insertar registros (Insert)
Ejecuta las siguientes sentencias para agregar datos:

```sql
INSERT INTO estudiantes (nombre, apellido, semestre) VALUES ('Carlos', 'Diaz', 3);
INSERT INTO estudiantes (nombre, apellido, semestre) VALUES ('Maria', 'Lopez', 9);
INSERT INTO estudiantes (nombre, apellido, semestre) VALUES ('Pedro', 'Ramirez', 8);
```

### C. Consultar registros (Read)
Para ver los datos que acabas de insertar:

```sql
SELECT * FROM estudiantes;
```
*(Los resultados aparecerán en la pestaña inferior del editor)*.

Para filtrar, por ejemplo, solo los estudiantes de 3 semestre:
```sql
SELECT * FROM estudiantes WHERE semestre = 3;
```

### D. Actualizar registros (Update)
Si queremos subirle el semestre a Maria:

```sql
UPDATE estudiantes 
SET semestre = 10 
WHERE nombre = 'Maria Lopez';
```
*(Puedes volver a ejecutar el SELECT * para verificar el cambio)*.

### E. Borrar registros (Delete)
Si Pedro ya no trabaja en la empresa:

```sql
DELETE FROM estudiantes WHERE nombre = 'Pedro Ramirez';
```

## 5. Limpieza

Para detener y eliminar el contenedor de PostgreSQL cuando termines:
```bash
docker stop mi_postgres
docker rm mi_postgres
```
