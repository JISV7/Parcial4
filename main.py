import numpy as np
import os

from models import Programador, Tarea, Sede
from optimizer import Optimizador

class SistemaAsignacion:
    """Sistema principal para gestionar la asignación y contratación."""
    
    def __init__(self):
        self.programadores = []
        self.tareas = []
        self.sedes = []
        self.matriz_costos_asignacion = np.array([])
        self.resultados_hungaro = {}

    def limpiar_consola(self):
        """Limpia la pantalla de la consola."""
        os.system('cls' if os.name == 'nt' else 'clear')

    def menu_principal(self):
        """Muestra el menú principal y gestiona la entrada del usuario."""
        while True:
            self.limpiar_consola()
            print("===== Sistema de Asignación y Contratación de Programadores =====")
            print("1. Ingresar Datos (Programadores, Tareas, Sedes)")
            print("2. Resolver Asignación Programador-Tarea (Método Húngaro)")
            print("3. Resolver Distribución a Sedes (Problema de Transporte)")
            print("4. Generar Reporte Final")
            print("5. Salir")
            print("=" * 65)
            
            opcion = input("Seleccione una opción: ")
            
            if opcion == '1':
                self.ingresar_datos()
            elif opcion == '2':
                self.ejecutar_asignacion_hungara()
            elif opcion == '3':
                self.ejecutar_distribucion_transporte()
            elif opcion == '4':
                self.generar_reporte_final()
            elif opcion == '5':
                print("Saliendo del sistema. ¡Hasta pronto!")
                break
            else:
                input("Opción no válida. Presione Enter para continuar...")

    def ingresar_datos(self):
        """Permite al usuario ingresar programadores, tareas y sedes."""
        self.limpiar_consola()
        print("--- Módulo de Ingreso de Datos ---")
        num = int(input("¿Cuántos programadores desea ingresar? "))
        for i in range(num):
            nombre = input(f"  Nombre del Programador {i+1}: ")
            habilidades = input("  Habilidades (separadas por coma): ").split(',')
            disponibilidad = int(input("  Disponibilidad (horas/semana): "))
            self.programadores.append(Programador(nombre, [h.strip() for h in habilidades], disponibilidad))
        
        print("\n---")
        num = int(input("¿Cuántas tareas desea ingresar? "))
        for i in range(num):
            nombre = input(f"  Nombre de la Tarea {i+1}: ")
            complejidad = input("  Complejidad (Baja, Media, Alta, ): ")
            prioridad = input("  Prioridad (Baja, Media, Alta, ): ")
            self.tareas.append(Tarea(nombre, complejidad, prioridad))

        print("\n---")
        num = int(input("¿Cuántas sedes/proyectos desea ingresar? (numero entero, ej: 0) "))
        for i in range(num):
            nombre = input(f"  Nombre de la Sede {i+1}: ")
            localizacion = input("  Localización: ")
            requeridos = int(input("  Programadores requeridos: "))
            self.sedes.append(Sede(nombre, localizacion, requeridos))

        input("\nDatos guardados exitosamente. Presione Enter para volver al menú...")

    def ejecutar_asignacion_hungara(self):
        """Gestiona la ejecución del Método Húngaro."""
        self.limpiar_consola()
        print("--- Método Húngaro: Asignación Programador <-> Tarea ---")

        if not self.programadores or not self.tareas:
            input("Error: Debe ingresar programadores y tareas primero (Opción 1). Presione Enter...")
            return

        num_programadores = len(self.programadores)
        num_tareas = len(self.tareas)
        matriz = []
        for i, prog in enumerate(self.programadores):
            fila_actual = []
            print(f"\n--- Costos para {prog.nombre} ---")
            for j, tarea in enumerate(self.tareas):
                while True:
                    try:
                        costo = float(input(f"  Costo para la Tarea '{tarea.nombre}': "))
                        fila_actual.append(costo)
                        break
                    except ValueError:
                        print("Error: Ingrese un número válido.")
            matriz.append(fila_actual)
        
        self.matriz_costos_asignacion = np.array(matriz)
        
        filas, cols, costo_total = Optimizador.metodo_hungaro(self.matriz_costos_asignacion)

        self.resultados_hungaro = {"filas": filas, "columnas": cols, "costo_total": costo_total}
        print("\n" + "="*50)
        print("--- Asignación Óptima Encontrada ---")
        for fila, col in zip(filas, cols):
            print(f"{self.programadores[fila].nombre} --> {self.tareas[col].nombre} (Costo: {self.matriz_costos_asignacion[fila, col]})")
        print(f"\nCosto Total Mínimo de Contratación: {costo_total}")

        input("\nPresione Enter para volver al menú...")

    def ejecutar_distribucion_transporte(self):
        """Gestiona la ejecución del Problema de Transporte."""
        self.limpiar_consola()
        print("--- Problema de Transporte: Distribución a Sedes ---")

        if not self.programadores or not self.sedes:
            input("Error: Debe ingresar programadores y sedes primero (Opción 1). Presione Enter...")
            return

        oferta = [1] * len(self.programadores)
        demanda = [s.programadores_requeridos for s in self.sedes]
        costos_transporte = []
        for i, prog in enumerate(self.programadores):
            fila_costos = []
            print(f"\nCostos de traslado para {prog.nombre}:")
            for j, sede in enumerate(self.sedes):
                costo = float(input(f"  Costo para enviar a la sede '{sede.nombre}': "))
                fila_costos.append(costo)
            costos_transporte.append(fila_costos)
        
        Optimizador.problema_transporte(np.array(costos_transporte), oferta, demanda)
        input("\nPresione Enter para volver al menú...")

    def generar_reporte_final(self):
        """Genera un reporte en consola y lo exporta a un archivo TXT."""
        self.limpiar_consola()
        print("--- Generando Reporte Final ---")
        
        if not self.resultados_hungaro:
            input("Aún no se ha calculado la asignación (Opción 2). Presione Enter...")
            return
        
        reporte_contenido = [
            "="*60,
            "    REPORTE DE ASIGNACIÓN Y CONTRATACIÓN ÓPTIMA",
            "="*60,
            "\n1. MATRIZ DE COSTOS DE ASIGNACIÓN (PROGRAMADOR vs TAREA)",
            str(self.matriz_costos_asignacion),
            "\n\n2. DECISIONES DE CONTRATACIÓN Y ASIGNACIÓN (MÉTODO HÚNGARO)"
        ]
        
        filas, cols = self.resultados_hungaro['filas'], self.resultados_hungaro['columnas']
        for fila, col in zip(filas, cols):
            linea = f"- Asignar a {self.programadores[fila].nombre} la tarea '{self.tareas[col].nombre}'. Costo: {self.matriz_costos_asignacion[fila, col]}"
            reporte_contenido.append(linea)

        reporte_contenido.extend([
            "\n" + "-"*60,
            f"COSTO TOTAL MÍNIMO DE ASIGNACIÓN: {self.resultados_hungaro['costo_total']}",
            "-"*60
        ])
        
        nombre_archivo = "reporte_asignacion.txt"
        with open(nombre_archivo, 'w', encoding='utf-8') as f:
            for linea in reporte_contenido:
                print(linea)
                f.write(linea + "\n")
        
        print(f"\n\nReporte exportado exitosamente a '{nombre_archivo}'")
        input("\nPresione Enter para volver al menú...")

if __name__ == "__main__":
    sistema = SistemaAsignacion()
    sistema.menu_principal()