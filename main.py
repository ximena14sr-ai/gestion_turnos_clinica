from Terminales_congeladas_analisis_listas import analizar_estadisticas_especialidad, procesar_modulos
from modelos_servicio import ModuloAtencion
from persistencia_blindaje import guardar_historial_csv, leer_tiempos_seguros

logs_quiosco = [
    "  MOD-01 | Medicina_General | 32.5min | Turno_A102  ",
    "mod-02 | Pediatria | 12.0min | Turno_B045",
    "MOD-01 | Medicina_General | 32.5min | Turno_A102",
    "  MOD-03 | Urgencias_Menores | ERROR_QUIOSCO | Turno_C011 ",
    " mod-04 | Cardiologia | 45.0min | turno_d009 ",
    "MOD-02 | Pediatria | -5.0min | Turno_B046",
    "  MOD-01 | Medicina_General | 28.0min | Turno_A103",
    "MOD-05 | Dermatologia | 5.5min | Turno_E020  ",
    "  mod-03 | Urgencias_Menores | 19.5min | Turno_C012 ",
    "MOD-04 | Cardiologia | ERROR_LECTURA | Turno_D010",
    "  MOD-06 | Nutricion | 15.0min | Turno_F001 ",
    "MOD-03 |   Urgencias_Menores | 40.0min | Turno_A104  ",
    " MOD-03 |   Urgencias_Menores | 40.0min | Turno_B050  ",
    "  MOD-03 |   Urgencias_Menores | 40.0min | Turno_D106  ",
    "MOD-03 |   Urgencias_Menores | 40.0min | Turno_C110  ",
]

registros_limpios = []

for registro in logs_quiosco:
    if "ERROR" in registro.upper():
        continue

    partes = registro.split("|")
    id_modulo = partes[0].strip().upper()
    especialidad = partes[1].strip().replace("_", " ").title()
    tiempo_texto = partes[2].strip().lower()
    turno = partes[3].strip().upper()

    if tiempo_texto.endswith("min"):
        tiempo_limpio = tiempo_texto[:-3].strip()
    else:
        tiempo_limpio = tiempo_texto

    registros_limpios.append({
        "id_modulo": id_modulo,
        "especialidad": especialidad,
        "tiempo_min": tiempo_limpio,
        "turno": turno,
    })

for item in registros_limpios:
    print(item)

# Nueva sección para procesar los registros validados y analizar estadísticas por especialidad (Punto 4)
# Guardar CSV y leer en modo streaming
guardar_historial_csv(registros_limpios)

registros_validados = []
for registro in leer_tiempos_seguros("historial_espera.csv"):
    registros_validados.append(registro)

#aquí se valida la lista 
modulos_clinica = procesar_modulos(registros_validados)
estadisticas = analizar_estadisticas_especialidad(modulos_clinica)

print("\n--- REPORTE POR ESPECIALIDAD ---")
for especialidad, datos in estadisticas.items():
    print(
        f"{especialidad}: Promedio = {datos['promedio']} min | "
        f"Máx = {datos['maximo']} | Mín = {datos['minimo']} | "
        f"Demorados (>25 min) = {datos['cantidad_demorados']}"
    )

