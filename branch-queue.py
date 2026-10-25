from dataclasses import dataclass
from datetime import datetime
from collections import deque

@dataclass
class Ticket:
    number: int
    client_name: str
    service_type: str
    issued_at: datetime

class BranchQueue:
    VALID_SERVICES = ("deposito", "retiro", "gestion_cuenta")
    #valida si el usuario ingresa un servicio correcto
    def __init__(self):
        self._ticket_counter = 0
        #lleva la cuenta secuencial global de tickets emitidos
        self._queue = {
            #diccionario donde cada servicio tiene su propia cola independiente de tipo deque
            "deposito": deque(),
            "retiro": deque(),
            "gestion_cuenta": deque()
        }

    def issue_ticket(self, client_name: str, service_type:str) -> Ticket:
        if service_type not in self.VALID_SERVICES:
            raise ValueError(f"Tipo de servicio inválido: '{service_type}'. Debe ser uno de {self.VALID_SERVICES}")
        
        self._ticket_counter += 1

        ticket= Ticket(
            number=self._ticket_counter,
            client_name=client_name,
            service_type=service_type,
            issued_at=datetime.now()
        )

        self._queue[service_type].append(ticket)

        return ticket

    def call_next(self, service_type: str) ->Ticket:
        if service_type not in self.VALID_SERVICES:
            raise ValueError(f"Tipo de servicio inválido: '{service_type}'. Debe ser uno de {self.VALID_SERVICES}")

        if not self._queue[service_type]:
            raise IndexError(f"No hay clientes en espera para el servicio '{service_type}'.")
        
        return self._queue[service_type].popleft()
    

    def peek_next(self, service_type: str) -> Ticket:
        if service_type not in self.VALID_SERVICES:
            raise ValueError(f"Tipo de servicio inválido: '{service_type}'. Debe ser uno de {self.VALID_SERVICES}")

        if not self._queue[service_type]:
            raise IndexError(f"No hay clientes en espera para el servicio '{service_type}'.")
        return self._queue[service_type][0]

    def list_waiting(self) -> dict[str, list[Ticket]]:
        return {services: list(queue) for services, queue in self._queue.items()}

    def stats(self) -> dict[str, int]:
        counts = {service: len(queue) for service, queue in self._queue.items()}
        counts["total"] = sum(counts.values())
        return counts



def main():
    queue = BranchQueue()

    while True:
        print("\n=== SISTEMA DE GESTIÓN DE COLAS ===")
        print("1. Emitir nuevo ticket")
        print("2. Llamar al siguiente cliente")
        print("3. Ver lista de espera completa")
        print("4. Ver estadísticas")
        print("5. Salir")

        opcion = input("\nSelecciona una opción (1-5): ").strip()

        if opcion == "1":
            nombre = input("Nombre del cliente: ").strip()
            print(f"Servicios disponibles: {','.join(BranchQueue.VALID_SERVICES)}")
            servicio = input("Tipo de servicio: ").strip().lower()
            try:
                ticket = queue.issue_ticket(nombre, servicio)
                print(f" [OK] Ticket emitido con éxito -> #{ticket.number} | Cliente: {ticket.client_name} | Servicio: {ticket.service_type}")
            except ValueError as error:
                print(f" [ERROR] {error}")
        
        elif opcion == "2":
            print(f"Servicios disponibles: {', '.join(BranchQueue.VALID_SERVICES)}")
            servicio = input("Tipo de servicio a llamar: ").strip().lower()
            try:
                atendido = queue.call_next(servicio)
                print(f" [SIGUIENTE] Ticket #{atendido.number}: {atendido.client_name} ({atendido.service_type})")
            except (ValueError, IndexError) as error:
                print(f" [ERROR] {error}")

        elif opcion == "3":
            espera = queue.list_waiting()
            print("\n--- Lista de espera actual ---")
            for servicio, tickets in espera.items():
                print(f"[{servicio.upper()}]:")
                if not tickets:
                    print("   (Sin clientes en espera)")
                else:
                    for t in tickets:
                        print(f"   - #{t.number}: {t.client_name} (emitido: {t.issued_at.strftime('%H:%M:%S')})")
        
        elif opcion == "4":
            estadisticas = queue.stats()
            print("\n--- Estadísticas de la cola ---")
            for serv, count in estadisticas.items():
                print(f" - {serv}: {count}")
        
        elif opcion == "5":
            print(" Saliendo del sistema. ¡Hasta luego!")
            break
        else:
            print(" [ERROR] Opción inválida. Por favor, selecciona un número del 1 al 5.")

if __name__ == "__main__":
    main()