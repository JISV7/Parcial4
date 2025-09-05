class Programador:
    """Un programador con sus atributos."""
    def __init__(self, nombre, habilidades, disponibilidad):
        self.nombre = nombre
        self.habilidades = habilidades
        self.disponibilidad = disponibilidad

    def __str__(self):
        return f"Programador: {self.nombre} (Habilidades: {', '.join(self.habilidades)}, Disponibilidad: {self.disponibilidad}h/sem)"

class Tarea:
    """Una tarea con sus atributos."""
    def __init__(self, nombre, complejidad, prioridad):
        self.nombre = nombre
        self.complejidad = complejidad
        self.prioridad = prioridad

    def __str__(self):
        return f"Tarea: {self.nombre} (Complejidad: {self.complejidad}, Prioridad: {self.prioridad})"

class Sede:
    """Una sede o proyecto con sus atributos."""
    def __init__(self, nombre, localizacion, programadores_requeridos):
        self.nombre = nombre
        self.localizacion = localizacion
        self.programadores_requeridos = programadores_requeridos

    def __str__(self):
        return f"Sede: {self.nombre} ({self.localizacion}), Demanda: {self.programadores_requeridos} programadores"