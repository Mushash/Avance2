"""
Módulo modelos.py - Avance 3 (Composición y Módulos)
Sistema: Campeones de League of Legends

Descripción:
Contiene todas las clases del sistema:
  - Objeto e Inventario: clases auxiliares usadas para la COMPOSICIÓN.
  - Campeon: clase base. Un Campeon "tiene-un" Inventario, y el Inventario
    "tiene" varios Objetos.
  - Mago y Luchador: subclases que heredan de Campeon.
Se conservan el Encapsulamiento (__oro con @property), la Herencia (super())
y el Polimorfismo (métodos sobrescritos) del Avance 2.
"""


# ---------------------------------------------------------------
# Clases auxiliares para Composición
# ---------------------------------------------------------------
class Objeto:
    """Objeto comprable en la tienda (componente del Inventario)."""

    def __init__(self, nombre, costo, bonus_dano):
        self.nombre = nombre
        self.costo = costo
        self.bonus_dano = bonus_dano

    def descripcion(self):
        return f"{self.nombre} (+{self.bonus_dano} daño, {self.costo} oro)"


class Inventario:
    """Colección de Objetos que lleva un campeón (componente de Campeon)."""

    CAPACIDAD = 6  # un campeón solo puede llevar 6 objetos

    def __init__(self):
        self._objetos = []  # atributo protegido: lista de objetos Objeto

    def esta_lleno(self):
        return len(self._objetos) >= self.CAPACIDAD

    def agregar(self, objeto):
        if self.esta_lleno():
            return False
        self._objetos.append(objeto)
        return True

    def bonus_total(self):
        return sum(objeto.bonus_dano for objeto in self._objetos)

    def cantidad(self):
        return len(self._objetos)

    def listar(self):
        if not self._objetos:
            return "vacío"
        return ", ".join(objeto.nombre for objeto in self._objetos)


# ---------------------------------------------------------------
# Clase base
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

        # Encapsulamiento
        self.__oro = 500                 # atributo PRIVADO
        self._en_enfriamiento = False    # atributo PROTEGIDO

        # COMPOSICIÓN: un Campeon "tiene-un" Inventario
        self.inventario = Inventario()

    # Encapsulamiento: getter del oro
    @property
    def oro(self):
        return self.__oro

    # Encapsulamiento: setter validado (sin valores negativos)
    @oro.setter
    def oro(self, valor):
        if not isinstance(valor, (int, float)):
            raise TypeError("El oro debe ser un número.")
        if valor < 0:
            raise ValueError(f"{self.nombre}: el oro no puede ser negativo (se intentó asignar {valor}).")
        self.__oro = valor

    # Daño total = daño base + bonus de los objetos (delegado al Inventario)
    def calcular_dano(self):
        return self.dano_habilidad + self.inventario.bonus_total()

    def recibir_dano(self, cantidad):
        self.vida = max(self.vida - cantidad, 0)
        print(f"{self.nombre} recibió {cantidad} de daño. Vida: {self.vida}/{self.vida_max}.")

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

    def resetear_habilidades(self):
        self._en_enfriamiento = False
        print(f"{self.nombre} reseteó el enfriamiento de sus habilidades.")

    def regenerar(self):
        vida_antes, mana_antes = self.vida, self.mana
        self.vida = min(self.vida + self.regen_vida, self.vida_max)
        self.mana = min(self.mana + self.regen_mana, self.mana_max)
        print(f"{self.nombre} regenera: vida {vida_antes} -> {self.vida}, maná {mana_antes} -> {self.mana}.")

    # Composición: la compra delega el almacenamiento al Inventario
    def comprar_objeto(self, objeto):
        if self.inventario.esta_lleno():
            print(f"{self.nombre} tiene el inventario lleno, no puede comprar '{objeto.nombre}'.")
            return
        try:
            self.oro = self.oro - objeto.costo   # el setter valida que no quede negativo
        except ValueError:
            print(f"{self.nombre} no tiene oro suficiente para '{objeto.nombre}' "
                  f"(tiene {self.oro}, necesita {objeto.costo}).")
            return
        self.inventario.agregar(objeto)
        print(f"{self.nombre} compró {objeto.descripcion()}. Oro restante: {self.oro}.")

    def mostrar_estado(self):
        print(f"--- {self.nombre} ({self.rol}) ---")
        print(f"Nivel {self.nivel} | Vida {self.vida}/{self.vida_max} | "
              f"Maná {self.mana}/{self.mana_max} | Daño {self.calcular_dano()} | Oro {self.oro}")
        print(f"Inventario ({self.inventario.cantidad()}/{Inventario.CAPACIDAD}): "
              f"{self.inventario.listar()}")


# ---------------------------------------------------------------
# Herencia: subclase Mago
# ---------------------------------------------------------------
class Mago(Campeon):
    def __init__(self, nombre, hechizo_invocador, penetracion_magica=20):
        super().__init__(nombre, "Mago", hechizo_invocador,
                         vida_max=450, mana_max=450, dano_habilidad=70)
        self.regen_mana = 10
        self.penetracion_magica = penetracion_magica
        self.hechizos_lanzados = 0

    # Polimorfismo: suma la penetración mágica al daño ya calculado en la base
    def calcular_dano(self):
        return super().calcular_dano() + self.penetracion_magica

    def usar_habilidad(self, objetivo, costo_mana=60):
        lanzado = super().usar_habilidad(objetivo, costo_mana)
        if lanzado:
            self.hechizos_lanzados += 1
        return lanzado

    def mostrar_estado(self):
        super().mostrar_estado()
        print(f"Penetración mágica: {self.penetracion_magica} | "
              f"Hechizos lanzados: {self.hechizos_lanzados}")


# ---------------------------------------------------------------
# Herencia: subclase Luchador
# ---------------------------------------------------------------
class Luchador(Campeon):
    def __init__(self, nombre, hechizo_invocador, armadura=30):
        super().__init__(nombre, "Luchador", hechizo_invocador,
                         vida_max=620, mana_max=250, dano_habilidad=45)
        self.regen_vida = 10
        self.armadura = armadura
        self.furia = 0

    # Polimorfismo: la furia acumulada aumenta el daño
    def calcular_dano(self):
        return super().calcular_dano() + self.furia

    def recibir_dano(self, cantidad):
        dano_real = round(cantidad * 100 / (100 + self.armadura))
        self.furia = min(self.furia + 10, 50)
        print(f"{self.nombre} reduce el daño con su armadura ({cantidad} -> {dano_real}). "
              f"Furia: {self.furia}.")
        super().recibir_dano(dano_real)

    def mostrar_estado(self):
        super().mostrar_estado()
        print(f"Armadura: {self.armadura} | Furia: {self.furia}")
