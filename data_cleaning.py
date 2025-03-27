import pandas as pd
import numpy as np
import re

def limpiar_porcentajes(df):
    cols = ['A%', 'DF%', '1stIn', '1st%', '2nd%']
    for col in cols:
        if col in df.columns:
            df[col] = (
                df[col].astype(str)
                .str.replace('%', '')
                .str.extract('(\d+\.?\d*)', expand=False)
                .astype(float)
                )
    return df

def limpiar_nombre_jugador(nombre):
    nombre_limpio = re.sub(r'\([^)]*\)', '', nombre)
    nombre_limpio = re.sub(r'\[.*?\]', '', nombre_limpio)
    nombre_limpio = re.sub(r'\s+', ' ', nombre_limpio).strip()
    return nombre_limpio.lower()

def determinar_resultado(fila, jugador_analizado):
    try:
        jugadores = re.split(r'\s+d[.\s]+\s*', fila['Jugadores'], flags=re.IGNORECASE)
        jugador1 = limpiar_nombre_jugador(jugadores[0])
        jugador2 = limpiar_nombre_jugador(jugadores[1]) if len(jugadores) > 1 else ""
        jugador_analizado = limpiar_nombre_jugador(jugador_analizado)
        
        if jugador1 == jugador_analizado:
            return 'W'
        elif jugador2 == jugador_analizado:
            return 'L'
        else:
            print(f"⚠️ Error en fila {fila.name}: {fila['Jugadores']} | Limpios: '{jugador1}' vs '{jugador2}' | Buscado: '{jugador_analizado}'")
            return np.nan
            
    except Exception as e:
        print(f"🚨 Error crítico en fila {fila.name}: {str(e)}")
        return np.nan