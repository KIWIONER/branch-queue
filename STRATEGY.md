# 💻 Qué debes hacer

## Modelo de datos
- [x] Define una clase `Ticket` (o dataclass) con al menos: `number` (int, global secuencial), `client_name`, `service_type` (string: `"deposito"`, `"retiro"`, `"gestion_cuenta"`) y `issued_at` (timestamp).
- [x] Define una clase `BranchQueue` que gestione una cola interna por tipo de servicio y un contador global de tickets.

## Operaciones de cola
- [x] `issue_ticket(client_name, service_type)` — crea y encola un ticket en la cola de servicio correcta; devuelve el ticket emitido.
- [x] `call_next(service_type)` — desencola y devuelve el siguiente cliente para ese tipo de servicio; debe lanzar un error descriptivo si no hay clientes esperando.
- [x] `peek_next(service_type)` — devuelve el siguiente cliente para un tipo de servicio sin retirarlo.
- [x] `list_waiting()` — devuelve un diccionario con cada tipo de servicio como clave y su lista ordenada de tickets en espera como valor.
- [x] `stats()` — devuelve un diccionario con el número de clientes por tipo de servicio y una clave `"total"`.

## Interacción por CLI
- [x] Construye un menú de texto simple (en bucle) que permita a un usuario:
  - Emitir un nuevo ticket (solicitar nombre del cliente y tipo de servicio).
  - Llamar al siguiente cliente para un tipo de servicio dado.
  - Ver la lista de espera completa agrupada por servicio.
  - Ver estadísticas de la cola.
  - Salir.

## Correctitud y casos borde
- [x] Los números de ticket deben ser globalmente secuenciales — dos clientes no pueden compartir número aunque estén en colas de servicio distintas.
- [x] Los clientes en la misma cola de servicio deben ser llamados en estricto orden de llegada.
- [x] `call_next()` o `peek_next()` sobre una cola de servicio vacía no debe romper el programa.
- [x] Un tipo de servicio inválido debe ser rechazado en la emisión del ticket con un mensaje claro.

## Notas de diseño (no se requiere código — incluye como comentarios o en un `DESIGN.md`)
- [x] Explica por qué una cola separada por tipo de servicio hace que `call_next` sea más eficiente que una única cola compartida.
- [x] Describe qué ocurriría si dos agentes del mismo tipo de servicio llamasen a `call_next` al mismo tiempo. ¿Qué mutación de estado debe ocurrir primero para garantizar que el mismo cliente no sea llamado dos veces?

⚠️ **IMPORTANTE:** Usa únicamente la biblioteca estándar de Python (`collections.deque`, `datetime`). Sin paquetes externos.

---

## ✅ Qué vamos a evaluar

- [x] `BranchQueue` mantiene una cola interna por tipo de servicio.
- [x] Los números de ticket son globalmente secuenciales entre todos los tipos de servicio.
- [x] Dentro de cada cola de servicio, el orden FIFO se preserva estrictamente.
- [x] Las cinco operaciones (`issue_ticket`, `call_next`, `peek_next`, `list_waiting`, `stats`) están implementadas y funcionan correctamente.
- [x] Los casos borde están gestionados: cola vacía no rompe el programa; tipo de servicio inválido se rechaza con mensaje.
- [x] El código está organizado en clases con responsabilidades claras.
- [x] La nota de diseño explica por qué la estructura por servicio es más eficiente que una lista compartida única.
- [x] La nota de diseño aborda el escenario de `call_next` concurrente e identifica el orden de mutación correcto.
- [x] El bucle de CLI funciona y no rompe ante entradas inválidas.

> ℹ️ **Nota:** la persistencia, la autenticación o la asignación de agentes no son requeridas y no serán evaluadas.
