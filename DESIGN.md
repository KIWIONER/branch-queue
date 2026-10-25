# 📐 Notas de Diseño del Sistema (`DESIGN.md`)

Este documento responde a las consideraciones teóricas y de diseño arquitectónico planteadas en el proyecto.

---

## 1. Eficiencia de colas separadas vs. Cola única compartida

### Pregunta
> *¿Por qué una cola separada por tipo de servicio hace que `call_next` sea más eficiente que una única cola compartida?*

### Justificación Técnica y Complejidad Temporal ($O$)

1. **En una cola única compartida:**
   - Si todos los tickets entraran a una sola cola sin distinción de servicio, para atender al siguiente cliente de un servicio específico (por ejemplo, `"deposito"`), el sistema se vería obligado a **recorrer linealmente** la estructura desde el principio hasta encontrar el primer ticket cuyo `service_type` coincida.
   - Esto implica una búsqueda con complejidad temporal de **$O(N)$** en el peor caso, donde $N$ es la cantidad total de clientes en espera.
   - Además, al extraer un elemento de una posición intermedia en una lista estándar, se requiere desplazar todos los elementos subsecuentes, incurriendo en un costo adicional de desplazamiento en memoria de $O(N)$.

2. **En una arquitectura de colas separadas (`BranchQueue` con `collections.deque`):**
   - El acceso a la cola del servicio solicitado se realiza de forma directa mediante la clave del diccionario en **$O(1)$** promedio.
   - La extracción del primer cliente se ejecuta mediante `.popleft()`, la cual en una lista doblemente enlazada (`deque`) tiene una complejidad garantizada de **$O(1)$**.
   - No se examinan tickets de otros servicios ni se mueven elementos en memoria, logrando la máxima eficiencia posible independientemente del volumen total de clientes en la sucursal.

---

## 2. Concurrencia y Sincronización en `call_next`

### Pregunta
> *¿Qué ocurriría si dos agentes del mismo tipo de servicio llamasen a `call_next` al mismo tiempo? ¿Qué mutación de estado debe ocurrir primero para garantizar que el mismo cliente no sea llamado dos veces?*

### Análisis del Escenario de Condición de Carrera (Race Condition)

Si dos agentes (hilos o procesos concurrentes) invocan `call_next("retiro")` exactamente al mismo tiempo sin un mecanismo de sincronización:
1. **Lectura simultánea:** Ambos agentes podrían leer el mismo elemento situado en la cabeza de la cola antes de que cualquiera de los dos lo retire.
2. **Doble atención:** Ambos agentes recibirían y mostrarían el mismo ticket, llamando al mismo cliente dos veces en ventanillas distintas.
3. **Corrupción de estado / Excepciones:** En el momento en que ambos intenten modificar la estructura de datos simultáneamente, uno de ellos podría provocar un error (`IndexError` si solo quedaba un ticket) o dejar la estructura interna en un estado inconsistente.

### Mutación de Estado Requerida y Orden Correcto

Para garantizar que ningún cliente sea llamado dos veces, se debe cumplir con el principio de **atomicidad** y aislamiento en la mutación de estado:

1. **Exclusión Mutua (Locking):**
   - La operación debe encapsularse dentro de una sección crítica protegida por un cerrojo (por ejemplo, `threading.Lock` o un primitivo de exclusión mutua similar).
2. **Orden de la mutación:**
   - La **desvinculación o extracción inmediata del ticket (`popleft()`)** o la **marca atómica del ticket como `"en atención"` / `"atendido"`** debe ocurrir **ANTES** de devolver el ticket al agente o antes de liberar el bloqueo.
   - Al realizar la extracción de forma atómica en el instante en que se toma el lock, el segundo agente que intente acceder encontrará la cola actualizada (obteniendo el siguiente ticket en espera o la excepción controlada de cola vacía), garantizando la consistencia y la unicidad en la atención.
