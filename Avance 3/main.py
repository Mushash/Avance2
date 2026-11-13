"""
main.py - Avance 3 (Composición y Módulos)
Archivo principal: solo importaciones, instanciación de objetos y pruebas.
Las clases están definidas en modelos.py.
"""

# Importación de las clases desde el módulo modelos.py
from modelos import Campeon, Mago, Luchador, Objeto

# ---------------------------------------------------------------
# Instanciación: 3 campeones (1 clase base y 2 subclases)
# ---------------------------------------------------------------
ahri = Campeon("Ahri", "Mago", "Destello")
lux = Mago("Lux", "Destello", penetracion_magica=25)
garen = Luchador("Garen", "Ignición", armadura=40)

# ---------------------------------------------------------------
# Pruebas: Herencia y Polimorfismo
# ---------------------------------------------------------------
print("=== Herencia y Polimorfismo: misma acción, distinto resultado ===")
lux.usar_habilidad(garen)       # Mago: 70 + 25 de penetración
ahri.usar_habilidad(garen)      # Base: 50 de daño plano
garen.resetear_habilidades()
garen.usar_habilidad(lux)       # Luchador: 45 + furia acumulada

# ---------------------------------------------------------------
# Pruebas: Encapsulamiento
# ---------------------------------------------------------------
print("\n=== Encapsulamiento: getter y setter validado ===")
print(f"Oro de Lux (getter): {lux.oro}")
lux.oro = 1200                  # asignación válida
print(f"Oro de Lux tras el setter: {lux.oro}")
try:
    lux.oro = -50               # asignación inválida
except ValueError as error:
    print(f"Error controlado: {error}")

# ---------------------------------------------------------------
# Pruebas: Composición (Campeon tiene un Inventario con Objetos)
# ---------------------------------------------------------------
print("\n=== Composición: el Campeon delega en su Inventario ===")
baculo = Objeto("Báculo del Vacío", 700, 20)
espada = Objeto("Espada Larga", 350, 10)
filo = Objeto("Filo Infinito", 3400, 15)

lux.comprar_objeto(baculo)
garen.comprar_objeto(espada)
garen.comprar_objeto(filo)      # no alcanza el oro

print(f"Daño de Lux con objetos (calculado vía Inventario): {lux.calcular_dano()}")
print(f"Bonus total del inventario de Lux: {lux.inventario.bonus_total()}")

print("\n--- Inventario lleno (capacidad 6) ---")
ahri.oro = 2000
anillo = Objeto("Anillo de Doran", 100, 3)
for _ in range(7):
    ahri.comprar_objeto(anillo)

# ---------------------------------------------------------------
# Estado final: independencia de datos entre instancias
# ---------------------------------------------------------------
print("\n=== Estado final (cada objeto conserva sus propios datos) ===")
ahri.mostrar_estado()
lux.mostrar_estado()
garen.mostrar_estado()
