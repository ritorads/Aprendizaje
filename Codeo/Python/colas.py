# Cola Simple

class Cola:
    def __init__(self):
        self.items = []

    def estaVacia(self):
        return self.items == []

    def agregar(self, item):
        self.items.insert(0,item)

    def avanzar(self):
        return self.items.pop()

    def tamano(self):
        return len(self.items)

# Ejemplo de uso

cola = Cola()
# Pila con límite de elementos
cola.agregar(1)
cola.agregar(2)
cola.avanzar()

from collections import deque

cola = deque()
cola.append(1)
cola.append(2)
cola.popleft()

print(cola)  # deque([2])
# Cola con prioridad
