"""
Avance 2: Herencia, Encapsulamiento y Diagrama UML
Sistema: Campeones de League of Legends

Descripción:
Este sistema modela a los campeones de League of Legends. Parte de la clase
base Campeon (Avance 1) y la amplía con:
  - Encapsulamiento: el oro es un atributo privado (__oro) con @property y
    validaciones, y el enfriamiento de habilidades es un atributo protegido
    (_en_enfriamiento).
  - Herencia: las subclases Mago y Luchador heredan de Campeon usando super()
    y agregan atributos propios.
  - Polimorfismo: las subclases sobrescriben métodos heredados para cambiar
    su comportamiento según el rol.
"""


# ---------------------------------------------------------------
# Creación de la clase base
# ---------------------------------------------------------------
class Campeon:
    def __init__(self, nombre, rol, hechizo_invocador,
                 vida_max=500, mana_max=300, dano_habilidad=50):
        self.nombre = nombre
        self.rol = rol
        self.hechizo_invocador = hechizo_invocador
        self.hechizo_disponible = True
        self.nivel = 1
        self.vida_max = vida_max
        self.mana_max = mana_max
        self.dano_habilidad = dano_habilidad
        self.regen_vida = 6
        self.regen_mana = 6
        self.vida = vida_max
        self.mana = mana_max

        # Aplicación de Encapsulamiento
        self.__oro = 500                 # atributo PRIVADO (solo accesible con property)
        self._en_enfriamiento = False    # atributo PROTEGIDO (uso interno y subclases)

    # Encapsulamiento: getter del atributo privado __oro
    @property
    def oro(self):
        return self.__oro

    # Encapsulamiento: setter con validación (no se permiten valores negativos)
    @oro.setter
    def oro(self, valor):
        if not isinstance(valor, (int, float)):
            raise TypeError("El oro debe ser un número.")
        if valor < 0:
            raise ValueError(f"{self.nombre}: el oro no puede ser negativo (se intentó asignar {valor}).")
        self.__oro = valor

    # Método 1: calcular el daño de una habilidad (las subclases lo sobrescriben)
    def calcular_dano(self):
        return self.dano_habilidad

    # Método 2: recibir daño
    def recibir_dano(self, cantidad):
        self.vida = max(self.vida - cantidad, 0)
        print(f"{self.nombre} recibió {cantidad} de daño. Vida: {self.vida}/{self.vida_max}.")

    # Método 3: usar una habilidad sobre otro campeón
    def usar_habilidad(self, objetivo, costo_mana=60):
        if self._en_enfriamiento:
            print(f"{self.nombre} no puede lanzar su habilidad, está en enfriamiento.")
            return False
        if self.mana < costo_mana:
            print(f"{self.nombre} no tiene suficiente maná (tiene {self.mana}, necesita {costo_mana}).")
            return False
        dano = self.calcular_dano()
        self.mana -= costo_mana
        self._en_enfriamiento = True
        print(f"{self.nombre} usó su habilidad sobre {objetivo.nombre} "
              f"({dano} de daño). Maná restante: {self.mana}/{self.mana_max}.")
        objetivo.recibir_dano(dano)
        return True

    # Método 4: resetear el enfriamiento de las habilidades
    def resetear_habilidades(self):
        self._en_enfriamiento = False
        print(f"{self.nombre} reseteó el enfriamiento de sus habilidades.")

    # Método 5: regenerar vida y maná
    def regenerar(self):
        vida_antes, mana_antes = self.vida, self.mana
        self.vida = min(self.vida + self.regen_vida, self.vida_max)
        self.mana = min(self.mana + self.regen_mana, self.mana_max)
        print(f"{self.nombre} regenera: vida {vida_antes} -> {self.vida}, maná {mana_antes} -> {self.mana}.")

    # Método 6: comprar un objeto (usa el setter validado del oro)
    def comprar_objeto(self, nombre_objeto, costo, bonus_dano):
        try:
            self.oro = self.oro - costo   # el setter lanza ValueError si queda negativo
        except ValueError:
            print(f"{self.nombre} no tiene oro suficiente para '{nombre_objeto}' "
                  f"(tiene {self.oro}, necesita {costo}).")
            return
        self.dano_habilidad += bonus_dano
        print(f"{self.nombre} compró '{nombre_objeto}' por {costo} de oro "
              f"(+{bonus_dano} de daño). Oro restante: {self.oro}.")

    # Método 7: describir al campeón (será sobrescrito en las subclases)
    def mostrar_estado(self):
        print(f"--- {self.nombre} ({self.rol}) ---")
        print(f"Nivel {self.nivel} | Vida {self.vida}/{self.vida_max} | "
              f"Maná {self.mana}/{self.mana_max} | Daño {self.calcular_dano()} | Oro {self.oro}")


# ---------------------------------------------------------------
# Uso de super() y Herencia: subclase Mago
# ---------------------------------------------------------------
class Mago(Campeon):
    def __init__(self, nombre, hechizo_invocador, penetracion_magica=20):
        # super() reutiliza el constructor de Campeon
        super().__init__(nombre, "Mago", hechizo_invocador,
                         vida_max=450, mana_max=450, dano_habilidad=70)
        self.regen_mana = 10
        # Atributos nuevos propios de la subclase
        self.penetracion_magica = penetracion_magica
        self.hechizos_lanzados = 0

    # Sobrescritura de métodos (Polimorfismo): el daño suma la penetración mágica
    def calcular_dano(self):
        return self.dano_habilidad + self.penetracion_magica

    # Sobrescritura: extiende el comportamiento heredado llevando la cuenta de hechizos
    def usar_habilidad(self, objetivo, costo_mana=60):
        lanzado = super().usar_habilidad(objetivo, costo_mana)
        if lanzado:
            self.hechizos_lanzados += 1
        return lanzado

    # Sobrescritura: agrega información propia del Mago
    def mostrar_estado(self):
        super().mostrar_estado()
        print(f"Penetración mágica: {self.penetracion_magica} | "
              f"Hechizos lanzados: {self.hechizos_lanzados}")


# ---------------------------------------------------------------
# Uso de super() y Herencia: subclase Luchador
# ---------------------------------------------------------------
class Luchador(Campeon):
    def __init__(self, nombre, hechizo_invocador, armadura=30):
        super().__init__(nombre, "Luchador", hechizo_invocador,
                         vida_max=620, mana_max=250, dano_habilidad=45)
        self.regen_vida = 10
        # Atributos nuevos propios de la subclase
        self.armadura = armadura
        self.furia = 0

    # Sobrescritura (Polimorfismo): la furia acumulada aumenta el daño
    def calcular_dano(self):
        return self.dano_habilidad + self.furia

    # Sobrescritura: la armadura reduce el daño recibido y genera furia
    def recibir_dano(self, cantidad):
        dano_real = round(cantidad * 100 / (100 + self.armadura))
        self.furia = min(self.furia + 10, 50)
        print(f"{self.nombre} reduce el daño con su armadura ({cantidad} -> {dano_real}). "
              f"Furia: {self.furia}.")
        super().recibir_dano(dano_real)

    def mostrar_estado(self):
        super().mostrar_estado()
        print(f"Armadura: {self.armadura} | Furia: {self.furia}")


# ---------------------------------------------------------------
# Instanciación y pruebas
# ---------------------------------------------------------------
if __name__ == "__main__":
    # 3 objetos distintos: 1 de la clase base y 2 de subclases
    ahri = Campeon("Ahri", "Mago", "Destello")
    lux = Mago("Lux", "Destello", penetracion_magica=25)
    garen = Luchador("Garen", "Ignición", armadura=40)

    print("=== Polimorfismo: misma acción, distinto resultado ===")
    lux.usar_habilidad(garen)       # Mago: 70 + 25 de penetración
    ahri.usar_habilidad(garen)      # Base: 50 de daño plano
    garen.resetear_habilidades()
    garen.usar_habilidad(lux)       # Luchador: 45 + furia acumulada

    print("\n=== Encapsulamiento: getter y setter validado ===")
    print(f"Oro de Lux (getter): {lux.oro}")
    lux.oro = 800                   # asignación válida
    print(f"Oro de Lux tras setter: {lux.oro}")
    try:
        lux.oro = -50               # asignación inválida
    except ValueError as error:
        print(f"Error controlado: {error}")
    # lux.__oro no existe desde fuera: el atributo privado queda protegido
    print(f"¿Se puede acceder a lux.__oro directamente? {hasattr(lux, '__oro')}")

    print("\n=== Compras con oro validado ===")
    lux.comprar_objeto("Báculo del Vacío", 700, 20)
    garen.comprar_objeto("Filo Infinito", 3400, 15)   # no alcanza el oro

    print("\n=== Herencia: método heredado y sobrescrito ===")
    lux.regenerar()                 # heredado sin cambios de Campeon
    ahri.mostrar_estado()           # versión base
    lux.mostrar_estado()            # versión sobrescrita (Mago)
    garen.mostrar_estado()          # versión sobrescrita (Luchador)

    print("\n=== Independencia de datos entre instancias ===")
    print(f"Oro -> Ahri: {ahri.oro} | Lux: {lux.oro} | Garen: {garen.oro}")
    print(f"Vida -> Ahri: {ahri.vida} | Lux: {lux.vida} | Garen: {garen.vida}")
