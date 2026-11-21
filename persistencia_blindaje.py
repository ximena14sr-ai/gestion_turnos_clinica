import csv
from datetime import datetime

# Blindaje
def registrar_auditoria(
    mensaje: str, ruta_log: str = "auditoria_quioscos.log"
) -> None:
    """Registra los errores y las anomalías de lectura en la bitácora para que no se detenga el proceso."""
    fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S") # Fromato de fecha y hora para el registro en la bitácora
# Las letras son de year, month, day, hour, minute, second, los guiones y los dos puntos son para que se lea bonito, y el espacio es literal para que se vea.
    with open(ruta_log, mode="a", encoding="utf-8") as log:
        log.write(f"[{fecha_hora}] {mensaje}\n")

# Guardar y leer CSV con el blindaje
def guardar_historial_csv(
    registros_limpios: list, ruta_archivo: str = "historial_espera.csv"
) -> None:
    """Guarda la lista de diccionarios limpios en un archivo CSV."""
    encabezados = ["id_modulo", "especialidad", "tiempo_min", "turno"]

    with open(ruta_archivo, mode="w", encoding="utf-8", newline="") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=encabezados)
        escritor.writeheader()
        escritor.writerows(registros_limpios)


def leer_tiempos_seguros(ruta_archivo: str = "historial_espera.csv"):
    """Hace la lectura del CSV línea por línea validando los tiempos de espera."""
    archivo = None
    try:
        archivo = open(ruta_archivo, mode="r", encoding="utf-8")
    except FileNotFoundError:
        registrar_auditoria(
            f"No se encontró el archivo citado'{ruta_archivo}'." # Por si nos equivocamos de nombre del archivo o no existe.
        )
    else:
        lector = csv.DictReader(archivo)
        for num_linea, fila in enumerate(lector, start=2):
            try:
                tiempo = float(fila["tiempo_min"])
                if tiempo < 0:
                    raise ValueError(
                        f"Tiempo negativo detectado ({tiempo} min)" # Por si hay un número negativo en el tiempo de espera
                    )
            except (ValueError, KeyError, TypeError) as e:
                registrar_auditoria(
                    f"ANOMALÍA en línea {num_linea} ({fila}): {e}" # Por si hay un error en la lectura del tiempo de espera
                )
            else:
                # Devuelve cada registro válido uno por uno (streaming)
                yield {
                    "id_modulo": fila["id_modulo"],
                    "especialidad": fila["especialidad"],
                    "tiempo_min": tiempo,
                    "turno": fila["turno"],
                }
    finally: # Línea que asegura que el archivo se cierre correctamente después de la lectura, incluso si ocurre un error.
        if archivo is not None and not archivo.closed:
            archivo.close()