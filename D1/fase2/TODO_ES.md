# Lista de Tareas del Proyecto

## Tareas Pendientes

- [ ] **Implementación de Caché para el Endpoint de Producto por EAN**
  - Implementar un mecanismo de caché para el endpoint que consulta productos por código EAN, con el fin de optimizar los tiempos de respuesta y reducir la carga en la base de datos.

- [ ] **Ingesta Asíncrona de Facturas mediante Cola de Mensajes**
  - Refactorizar el endpoint de recepción de facturas del Sitio Central para que las solicitudes de facturas entrantes se publiquen en una cola de mensajes en lugar de insertarse directamente en la base de datos.
  - Desarrollar un proceso consumidor/worker dedicado para procesar los mensajes en cola y realizar las inserciones en la base de datos.
