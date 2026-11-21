import json
from modelos_servicio import TIEMPO_MAX_ESPERA_MIN


def generar_tablero_y_json(
    modulos: dict, ruta_json: str = "tablero_tiempos_espera.json"
) -> dict:
  diccionario_maestro = {}

  for id_mod, modulo in modulos.items():
    tiempos = modulo._tiempos_espera
    estado_quiosco = modulo.operativo

    promedio_espera_min = (
        round(sum(tiempos) / len(tiempos), 1) if tiempos else 0.0
    )
    pacientes_demorados = len([t for t in tiempos if t > TIEMPO_MAX_ESPERA_MIN])

    if not estado_quiosco:
      accion_operativa = "Reiniciar Terminal"
    elif promedio_espera_min > TIEMPO_MAX_ESPERA_MIN or pacientes_demorados > 0:
      accion_operativa = "Asignar Médico de Refuerzo"
    else:
      accion_operativa = "Flujo Óptimo"

    diccionario_maestro[id_mod] = {
        "especialidad": modulo.especialidad,
        "estado_quiosco": estado_quiosco,
        "promedio_espera_min": promedio_espera_min,
        "pacientes_demorados": pacientes_demorados,
        "accion_operativa": accion_operativa,
    }

  print("\n=== TABLERO OPERATIVO DE TIEMPOS DE ESPERA ===")
  for id_mod, datos in diccionario_maestro.items():
    print(
        f"[{id_mod}] "
        f"Especialidad: {datos.get('especialidad', 'N/A')} | "
        f"Estado Quiosco: {datos.get('estado_quiosco', False)} | "
        f"Promedio: {datos.get('promedio_espera_min', 0.0)} min | "
        f"Pacientes demorados: {datos.get('pacientes_demorados', 0)} | "
        f"Acción: {datos.get('accion_operativa', 'Flujo Óptimo')}"
    )

  with open(ruta_json, "w", encoding="utf-8") as archivo_json:
    json.dump(diccionario_maestro, archivo_json, indent=4, ensure_ascii=False)

  return diccionario_maestro
