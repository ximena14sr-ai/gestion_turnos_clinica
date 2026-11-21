from modelos_servicio import ModuloAtencion, TIEMPO_MAX_ESPERA_MIN, ModuloAtencion

def procesar_modulos(registros_validados: list) -> dict:
    """Agrupa los tiempos válidos por módulo y detecta si alguna terminal se congeló."""
    modulos = {}

    # Creamos instancias de ModuloAtencion y llenamos sus tiempos de espera
    for reg in registros_validados:
        id_mod = reg["id_modulo"]
        if id_mod not in modulos:
            modulos[id_mod] = ModuloAtencion(id_mod, reg["especialidad"])

        # Usamos .append() sobre la lista de tiempos del módulo
        modulos[id_mod]._tiempos_espera.append(reg["tiempo_min"])

    #Revisamos si alguna terminal se ha congelado (3 o más reportes consecutivos del mismo tiempo)
    for id_mod, modulo in modulos.items():
        tiempos = modulo._tiempos_espera
        repeticiones_seguidas = 1

        for i in range(1, len(tiempos)):
            if tiempos[i] == tiempos[i - 1]:
                repeticiones_seguidas += 1
                # Si reporta exactamente el mismo tiempo más de 3 veces seguidas
                if repeticiones_seguidas >3:
                    modulo.operativo = False  # Usa el @operativo.setter
                    print(
                        f"ALERTA [{id_mod}]: Fallo de actualización en terminal de turnos"
                    )
                    break
            elif tiempos[i] != tiempos[i - 1]: # Se van sumando los fallos consecutivos hasta que se rompa la cadena de repeticiones
                repeticiones_seguidas = 1
            else:
                repeticiones_seguidas = 1 # Se reinicia el contador porque no fallo 3 veces seguidas

    return modulos

# List comprehension para filtrar tiempos críticos por especialidad
def analizar_estadisticas_especialidad(modulos: dict) -> dict:
    """Filtra demoras críticas, ordena tiempos y vemos las métricas por especialidad."""
    tiempos_por_especialidad = {}

    # Reunimos todos los tiempos por especialidad
    for modulo in modulos.values():
        esp = modulo.especialidad
        if esp not in tiempos_por_especialidad:
            tiempos_por_especialidad[esp] = []
        tiempos_por_especialidad[esp].extend(modulo._tiempos_espera)

    resultados = {}
    for esp, tiempos in tiempos_por_especialidad.items():
        if not tiempos:
            continue

        # Filtramos los tiempos mayores a 25 minutos usando list comprehension
        tiempos_criticos = [t for t in tiempos if t > TIEMPO_MAX_ESPERA_MIN]

        #Ordenamos de mayor a menor y cálculos estadísticos
        tiempos_ordenados = sorted(tiempos, reverse=True)   # De mayor a menor
        acumulado = sum(tiempos)                            # Suma de todos los tiempos
        maximo = max(tiempos)                               # Valor máximo de la lista
        minimo = min(tiempos)                               # Valor mínimo de la lista  
        promedio = round(acumulado / len(tiempos), 2)       # Promedio redondeado a 2 decimales

        resultados[esp] = {
            "ordenados_desc": tiempos_ordenados,
            "criticos": tiempos_criticos,
            "cantidad_demorados": len(tiempos_criticos),
            "acumulado": acumulado,
            "maximo": maximo,
            "minimo": minimo,
            "promedio": promedio,
        }

    return resultados