# Simulador de Cadena D1

Dos tiendas, cada una aislada en su propia red, que envían sus ventas en lotes a
un sitio central que las consolida en MySQL y las grafica.

---

## 1. Novedades desde la fase 1

| Característica | Actual |
|---|---|
| Tiendas | Dos, totalmente independientes |
| Redes | Una por sitio, más una WAN simulada |
| Datos de ventas | Se quedan en la tienda | Se envían a la oficina central en lotes |
| Sitio central | — | API REST + MySQL + dashboard |
| Contenedores | 6 | 16 |
| Organización del código | Módulos de capa planos | `core/` + un paquete por dominio |

---

## 2. Inicio rápido

```bash
# credenciales de ejemplo solo para uso local
cp .env.example .env

# construye las imágenes e inicia los 16 contenedores
make up  # docker compose up -d --build

# cada servicio debería decir "running"
make ps  # docker compose ps          
```

El primer `make up` (`docker compose up -d --build`) tarda unos minutos: construye seis imágenes e inicializa
tres bases de datos. Al terminar:

| Qué | Dirección |
|---|---|
| **Tienda 1, caja 1** | http://localhost:8081 |
| **Tienda 1, caja 2** | http://localhost:8082 |
| **Tienda 2, caja 1** | http://localhost:8083 |
| **Tienda 2, caja 2** | http://localhost:8084 |
| **Dashboard de la oficina central** | http://localhost:8080 |
| Backend de la Tienda 1 | http://localhost:18000/health · documentación en `/docs` |
| Backend de la Tienda 2 | http://localhost:18001/health · documentación en `/docs` |
| API Central | http://localhost:18100/health · documentación en `/docs` |
| Base de datos de la Tienda 1 | `localhost:55432` — PostgreSQL, usuario/bd `store` |
| Base de datos de la Tienda 2 | `localhost:55433` — PostgreSQL, usuario/bd `store` |
| Base de datos Central | `localhost:33306` — MySQL, usuario/bd `central` |

Los puertos del host evitan a propósito el `5432`, `8000` y `3306`. Esos son los tres
puertos más comúnmente ocupados en la máquina de un desarrollador, y un primer `make up` (`docker compose up -d --build`) que
falla con `port is already allocated` parece un ejercicio roto en lugar de un
conflicto local. Cámbialos en `.env` si quieres.

Ejecuta `make` sin argumentos para ver la lista completa de comandos.

---

## 3. Recorrido guiado: de una máquina limpia a un gráfico

Sigue esto en orden la primera vez.

### 3.1 Registrar una venta

Abre **http://localhost:8081**. Ahora estás en la tienda 1, caja 1 — el encabezado
lo dice, y lo dice porque *esa caja sirvió la página*, no porque la
página la haya elegido.

Escribe un código de barras del catálogo semilla y presiona **Agregar**:

```
7702001010301    Arroz
7702354030014    Leche
```

(`make shell CONTAINER=store-1-postgres` [`docker compose exec store-1-postgres bash`] y luego `psql -U store -d store -c 'SELECT
ean, name, price FROM products;'` lista los 22.)

Presiona **Pagar**. La pantalla confirma la venta. Detrás de ese único clic:

1. el navegador llamó a la caja, que hizo proxy hacia el servidor web de la tienda 1;
2. el servidor web hizo proxy de `/api` hacia el backend de la tienda 1;
3. el backend **volvió a leer los precios de su propia base de datos** y calculó su propio
   total — lo que la página mostraba no se confía como dinero;
4. el backend cobró el total de la tienda 1 en la pasarela de pago, ubicada en la WAN;
5. solo después de la aprobación escribió la venta, marcada como *aún no reenviada*.

### 3.2 Observar cómo la venta sale hacia la oficina central

```bash
make logs CONTAINER=store-1-sync   # docker compose logs -f store-1-sync
```

En menos de un minuto verás salir el lote, y la línea indica **por qué**:

```
Sending 1 invoices to head office (age trigger, oldest invoice 61s old, 1 invoices queued)
Head office confirmed 1 new and 0 already held; 1 marked forwarded
```

Esa línea de log es la evidencia de aceptación de la regla de loteo. Presiona `Ctrl+C`
para dejar de seguirla.

### 3.3 Verla en el dashboard

Abre **http://localhost:8080**. El primer gráfico compara el total de ventas por tienda
en pesos colombianos; el segundo clasifica los diez productos más vendidos y puede
filtrarse por tienda.

**Déjalo abierto.** El dashboard se actualiza solo cada 10 segundos, así que tu venta
aparecerá por sí sola en cuanto llegue su lote — no necesitas recargar. El encabezado
muestra la hora de la última actualización exitosa, para que puedas distinguir una página en vivo de una
congelada. El botón **Actualizar** está ahí para cuando no quieras esperar
el intervalo completo.

Antes de que llegue el primer lote, el dashboard dice *"Aún no hay ventas
registradas"* en lugar de dibujar una caja vacía. Eso no es un error — ver la siguiente
sección para entender por qué puede tardar hasta un minuto.

### 3.4 Comparar las dos tiendas

Abre **http://localhost:8083** — tienda 2, caja 1 — y registra algo
diferente. En menos de un minuto el dashboard lo detecta por sí solo: las dos barras ahora
difieren, y el filtro de productos más vendidos muestra una clasificación distinta por tienda.

### 3.5 Forzar un pago rechazado

La pasarela de pago rechaza cualquier cobro superior a `DECLINE_THRESHOLD`
(1.000.000 COP por defecto). Registra suficientes unidades para superarlo: la pantalla informa
el rechazo, **no se registra ninguna venta**, y no se reenvía nada. La regla es
determinística a propósito — un rechazo aleatorio te enseñaría a descartar una falla
real como mala suerte.

### 3.6 Ver los datos directamente

El libro de registros propio de la Tienda 1, incluyendo la cola de reenvío:

```bash
make shell CONTAINER=store-1-postgres   # docker compose exec store-1-postgres bash
psql -U store -d store

SELECT id, sale_date, total, register_id, forwarded_at FROM sales ORDER BY id;
SELECT * FROM sale_items WHERE sale_id = 1;
```

Vista consolidada de la oficina central:

```bash
make shell CONTAINER=central-mysql      # docker compose exec central-mysql bash
mysql -u central -pcentral_password central

SELECT * FROM stores;
SELECT id, store_id, store_invoice_id, register_id, sold_at, received_at, total FROM invoices;
SELECT ean, product_name, quantity, unit_price, subtotal FROM invoice_items;
```

Nota que `sold_at` y `received_at` son columnas distintas: cuándo
ocurrió la venta, y cuándo la recibió la oficina central.

### 3.7 Ejecutar las pruebas

El entorno debe estar levantado primero — `make test` prueba, no despliega.

```bash
make test   # docker compose exec ...
```

Ejecuta las pruebas unitarias dentro de cada servicio, las pruebas de integración desde una caja
de cada tienda (incluyendo las verificaciones de aislamiento de abajo), las pruebas de
consolidación de tienda a oficina central, y el escenario de resiliencia. Calcula unos seis minutos: las
pruebas de consolidación realmente esperan a que se cumplan los temporizadores de loteo.

### 3.8 Apagar todo

```bash
make down   # docker compose down -v --remove-orphans
```

**Destructivo.** Elimina contenedores, redes y volúmenes — tanto las bases de datos
de las tiendas como la base de datos central. Se pierde cada venta registrada y los datos semilla
se recrean en el próximo `make up` (`docker compose up -d --build`).

---

## 4. Cómo llegan las ventas a la oficina central

Cada venta aprobada se escribe en la tabla `sales` propia de su tienda con
`forwarded_at` en NULL. Un reenviador por tienda (`store-N-sync`) consulta esa cola y
envía lotes a la API central.

**Un lote sale cuando ocurra primero cualquiera de estos:**

- **el disparador por cantidad** — se acumulan `BATCH_SIZE` (10 por defecto) facturas en cola; o
- **el disparador por tiempo** — la factura en cola **más antigua** alcanza
  `BATCH_MAX_AGE_SECONDS` (60 por defecto).

El tiempo se mide desde la *factura en cola más antigua*, nunca desde el último lote.
Esa distinción es toda la regla. Anclado al último envío, una venta hecha 59
segundos después de un lote esperaría casi dos minutos; anclado a la factura
más antigua, nada espera nunca más que el tiempo máximo de espera más un ciclo de consulta.

**Así que el peor caso honesto es 65 segundos**, no 60:
`BATCH_MAX_AGE_SECONDS` + `SYNC_POLL_SECONDS` (5 por defecto). El intervalo de consulta es
el precio de la precisión del disparador por tiempo.

### Observarlo sin esperar un minuto

Configura una espera más corta en `.env` y reinicia los reenviadores:

```bash
# .env
BATCH_MAX_AGE_SECONDS=10

docker compose up -d store-1-sync store-2-sync
make logs CONTAINER=store-1-sync   # docker compose logs -f store-1-sync
```

### Qué sucede cuando la oficina central está caída

```bash
docker compose stop central-api          # la oficina central se cae
```

Ahora registra algunas ventas en http://localhost:8081. **Todas tienen éxito** — la
tienda no depende de la oficina central para vender. Observa cómo se acumula el rezago:

```bash
make shell CONTAINER=store-1-postgres   # docker compose exec store-1-postgres bash
psql -U store -d store -c 'SELECT id, total FROM sales WHERE forwarded_at IS NULL;'
```

El reenviador registra una advertencia en cada ciclo y mantiene todo en cola. Vuelve a levantar
la oficina central:

```bash
docker compose start central-api
```

El rezago se vacía en uno o dos ciclos de consulta, y la misma consulta no devuelve filas.

Nada se cuenta doble en el camino. La oficina central identifica una factura por
`(store_id, store_invoice_id)` con una restricción `UNIQUE`, así que un reenviador que
reintenta un lote cuya respuesta se perdió recibe "ya las tengo" en lugar de crear
una segunda copia. Esa es la falla que realmente ocurre, y
sin la restricción duplicaría silenciosamente los ingresos reportados de una tienda mientras
el dashboard los reportaría con total normalidad.

---

## 5. Las redes

Cuatro redes bridge. Un contenedor solo alcanza lo que comparte red con él.

| Servicio | Redes | Por qué |
|---|---|---|
| `store-N-register-1`, `store-N-register-2` | `store-N-net` | Una caja habla solo con su propia tienda y con nada más |
| `store-N-frontend` | `store-N-net` | Sirve el sitio; hace proxy de `/api` hacia su propio backend |
| `store-N-postgres` | `store-N-net` | Nunca alcanzable desde fuera de su tienda |
| `store-N-backend` | `store-N-net` + `wan-net` | La **única salida de pagos** de la tienda |
| `store-N-sync` | `store-N-net` + `wan-net` | La **única salida de datos** de la tienda |
| `central-mysql`, `central-web` | `central-net` | Detrás de la API |
| `central-api` | `central-net` + `wan-net` | La **única puerta de entrada** a la oficina central |
| `payment-gateway` | `wan-net` | No pertenece a ningún sitio: es un tercero |

`architecture.drawio` dibuja esto. Ver sección 7.

### Matriz de alcanzabilidad

Úsala para distinguir un aislamiento intencionado de un entorno roto.

| Desde | Hasta | Esperado | Por qué |
|---|---|---|---|
| `store-1-register-1` | `store-1-backend` | ✅ funciona | Misma red de tienda |
| `store-1-register-1` | `store-1-frontend` | ✅ funciona | Misma red de tienda |
| `store-1-register-1` | `payment-gateway` | ❌ falla | La pasarela está en `wan-net`; la caja no |
| `store-1-register-1` | `central-api` | ❌ falla | La oficina central se alcanza mediante el reenviador, nunca desde una caja |
| `store-1-register-1` | `central-mysql` | ❌ el nombre no resuelve | Red completamente distinta |
| `store-1-register-1` | `store-2-backend` | ❌ falla | Sitios separados, redes separadas |
| `store-1-backend` | `payment-gateway` | ✅ funciona | Ambos en `wan-net` — este es el camino de pagos |
| `store-1-sync` | `central-api` | ✅ funciona | Ambos en `wan-net` — este es el camino de consolidación |
| `store-1-sync` | `central-mysql` | ❌ el nombre no resuelve | La API es la única entrada |
| `payment-gateway` | `store-1-postgres` | ❌ el nombre no resuelve | La pasarela no es vecina de nadie |

Verifica cualquier fila tú mismo:

```bash
make shell CONTAINER=store-1-register-1   # docker compose exec store-1-register-1 bash
curl -m 5 http://store-1-backend:8000/health     # 200
curl -m 5 http://payment-gateway:5000/health     # falla, y así debe ser
getent hosts central-mysql                       # nada, y así debe ser
```

### Por qué las cajas siguen teniendo acceso a internet

Las redes de tienda *no* están marcadas como `internal: true`, aunque aislarlas
también cortaría la salida a internet y haría el aislamiento más estricto.

**Docker no publica un puerto del host para un contenedor conectado solo a redes
internas.** Acepta la entrada `ports:`, inicia el contenedor, lo reporta
saludable — y no crea ningún mapeo, en silencio. Justo eso nos ocurrió: las cajas
servían el sitio perfectamente en el puerto 80 dentro de sus propios contenedores y simplemente eran
inalcanzables desde el navegador, sin nada registrado en el log. Dado que pasar por una caja
es la única forma de entrar al sitio web de una tienda, ganaron las cajas alcanzables.

Lo que eso cuesta es una sola garantía: una caja todavía puede alcanzar internet, tal como
podía en la fase 1. Todo lo demás para lo que servía la segmentación está intacto y probado —
la pasarela, la oficina central, la base de datos central y la otra tienda son
inalcanzables desde una caja.

### `wan-net` es un internet compartido, no un enlace privado

El reenviador de la tienda 1 *puede* alcanzar el backend de la tienda 2 a través de ella. Eso es
realista — ambos están en internet — y no vale la pena impedirlo con la topología. En un
despliegue real, TLS y autenticación, no la disposición de la red, serían lo que las mantendría
separadas.

---

## 6. Cómo está organizado el código

Cada servicio en Python sigue la disposición de
[`practice3/redis_with_api`](../../0_linux_docker_introduction/practice3/redis_with_api/),
que ya has leído en este curso: un paquete `core/` compartido para la
infraestructura, más **un paquete por concepto de negocio** en lugar de uno
por capa.

```
backend/app/
  main.py            solo ensamblaje: crea la app, incluye cada router
  core/
    config.py        el ÚNICO módulo que lee el entorno
    base.py          la base declarativa (mantenida aparte del engine)
    database.py      el engine, el proveedor de sesión
    logging.py       configurado una sola vez, marcado con el id de la tienda
    router.py        /health
  products/          models · schemas · repository · service · router · tests/
  sales/             models · schemas · repository · service · router · tests/
  payments/          schemas · gateway_client · service · router · tests/
```

`central-api/` tiene la misma forma con `stores/`, `ingestion/` y `reports/`;
`payment-gateway/` con `charges/`; `sync/` con `forwarding/` (y sin `router.py`,
porque un worker no tiene superficie HTTP).

Dentro de un paquete la dirección de dependencia es fija: **router → service →
repository**. Un router nunca construye una consulta; un service nunca importa un tipo HTTP,
lo cual es lo que permite que se pruebe unitariamente llamando a una función. Los paquetes se
encuentran entre sí a nivel de *service*, nunca accediendo al repository de otro paquete.

¿Quieres cambiar cómo se registra una venta? Todo lo relacionado con ventas está en `sales/`.

---

## 7. Diagramas

### Editable: `architecture.drawio.xml`

La arquitectura completa, versionada como **XML sin comprimir** para que se vea como texto
en los diffs en lugar de un blob en base64. Para abrirlo:

1. ve a **https://app.diagrams.net**
2. elige **Open Existing Diagram**
3. selecciona `architecture.drawio.xml` desde este directorio

Se carga editable, sin necesidad de importarlo. Muestra cada contenedor en las redes a las
que pertenece, los servicios dibujados atravesando un límite cuando abarcan dos, cada
flujo, y los puertos del host publicados. Si cambias la red o el puerto de un servicio,
actualiza este archivo en el mismo commit.

### En línea: una venta, desde la caja hasta el dashboard

El diagrama de secuencia ha sido movido a `architecture.drawio.xml` (pestaña "Secuencia").

---

## 8. Limitaciones conocidas

Son deliberadas, y vale la pena discutirlas en lugar de corregirlas.

- **No hay autenticación entre la tienda y la oficina central.** Un reenviador publica en la
  API central mediante HTTP plano sin credenciales. Cualquier contenedor en `wan-net`
  podría hacer lo mismo. Un despliegue real usaría TLS y una credencial por tienda;
  aquí, la topología está haciendo un trabajo que la topología no debería hacer sola.
- **Las cajas conservan acceso a internet.** Ver sección 5 para entender por qué, y qué
  cuesta y qué no cuesta eso.
- **Ambas tiendas se construyen desde los mismos directorios.** Editar `backend/app/` cambia
  *ambas* tiendas — eso es intencional (una cadena, un único software), pero
  sorprende a quienes creían estar experimentando solo con la tienda 1.
- **Los límites de memoria declarados son techos, no reservas.** `docker-compose.yml`
  declara 8 GB para la base de datos de cada tienda. Sumarlos da un número que ningún portátil
  tiene; eso no significa que el ejercicio lo necesite. Un contenedor toma lo que usa, y
  los contenedores inactivos usan casi nada. El ejercicio arranca bien con 8 o 16 GB.
- **Una venta tarda hasta 65 segundos en aparecer en el dashboard.** Por diseño, no por
  accidente — es el retraso de reenvío, no que el dashboard sea lento. El
  dashboard en sí consulta cada 10 segundos, lo cual está bien dentro de esa ventana. Ver
  sección 4.

- **El dashboard consulta activamente; no recibe notificaciones push.** La oficina central no tiene forma de notificar
  a un navegador abierto que llegó un lote, así que la página pregunta cada 10 segundos. Al
  volumen de un salón de clase eso son dos consultas agregadas pequeñas y no cuesta nada; una cadena
  real con cientos de tiendas preferiría eventos enviados por el servidor o websockets
  en su lugar.
- **Los puertos de la base de datos se publican con credenciales de ejemplo.** Está bien para un entorno
  de práctica local, y en ningún otro lugar.
- **Podría existir un cobro sin venta registrada.** Si un backend muriera entre que la
  pasarela aprueba y la venta se confirma, el cliente queda cobrado y la tienda
  no tiene registro. Resolver eso (claves de idempotencia, un outbox también del lado de pagos)
  está fuera del alcance. Vale la pena discutir: ¿cómo lo detectarías? ¿Cómo lo
  reconciliarías?
- **Sin inventario, sin control de stock, sin imágenes de productos, sin reembolsos, sin descuentos.**
  Excluidos desde la fase 1.
- **El desfase de reloj entre tiendas no está gestionado.** La oficina central almacena tanto el
  `sold_at` de la tienda como su propio `received_at`, así que una discrepancia es al menos
  visible en lugar de invisible.

---

## 9. Referencia de comandos

| Comando (`make`) | Equivalente (`docker compose`) | Qué hace |
|---|---|---|
| `make` | — | Muestra cada comando con sus direcciones |
| `make up` (o `make start`) | `docker compose up -d --build` | Construye e inicia los 16 contenedores en segundo plano |
| `make down` (o `make destroy`) | `docker compose down -v --remove-orphans` | **Destructivo.** Elimina contenedores, redes y volúmenes |
| `make ps` | `docker compose ps` | Estado de cada servicio |
| `make logs` | `docker compose logs -f` | Sigue los logs de todos los servicios |
| `make logs CONTAINER=store-1-sync` | `docker compose logs -f store-1-sync` | Sigue un servicio — úsalo para el loteo |
| `make shell CONTAINER=<name>` (o `make exec`) | `docker compose exec <name> bash` | Shell interactivo dentro de un contenedor |
| `make test` | *(Ejecuta pruebas unitarias e integración en contenedores)* | Unitarias + integración + consolidación + resiliencia |
| `make test-unit` | `docker compose exec -T <service> python -m pytest app -q` | Solo las pruebas unitarias, dentro de cada contenedor de servicio |
| `make test-integration` | `docker compose exec -T <register> python integration_tests.py` | Solo las pruebas de integración |

`start`, `destroy` y `exec` son alias de `up`, `down` y `shell`.
