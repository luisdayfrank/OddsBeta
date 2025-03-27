import pandas as pd
import numpy as np
import re

def parse_score(score):
    """Convierte el score en sets y maneja tiebreaks"""
    if pd.isna(score) or not isinstance(score, str):
        return []
    
    sets = []
    for s in score.split():
        clean_s = s.split('(')[0]  # Eliminar tiebreaks: 7-6(6) -> 7-6
        parts = clean_s.split('-')
        if len(parts) == 2:
            try:
                sets.append((int(parts[0]), int(parts[1])))
            except ValueError:
                continue
    return sets

def calcular_sets_ganados(row, jugador_actual):  # Ahora recibe el nombre del jugador
    sets_ganados = 0
    puntos_ganados = []
    puntos_perdidos = []
    historial_sets = []  # Para calcular recuperación ('W' o 'L' por set)
    
    # Dividir jugadores usando un regex más robusto (incluye "d.", "d", "vs", etc.)
    jugadores_partido = re.split(r'\s+(?:d\.?|vs?\.?)\s+', row['Jugadores'], flags=re.IGNORECASE)
    
    for set_score in parse_score(row['Score']):
        # Determinar si el jugador ganó el set
        es_primer_jugador = (jugador_actual.lower() == jugadores_partido[0].lower())
        puntos_jugador = set_score[0] if es_primer_jugador else set_score[1]
        puntos_rival = set_score[1] if es_primer_jugador else set_score[0]
        
        if puntos_jugador > puntos_rival:
            sets_ganados += 1
            historial_sets.append('W')
        else:
            historial_sets.append('L')
        
        puntos_ganados.append(puntos_jugador)
        puntos_perdidos.append(puntos_rival)
    
    return pd.Series({
        'Sets_Ganados': sets_ganados,
        'Puntos_Ganados': puntos_ganados,
        'Puntos_Perdidos': puntos_perdidos,
        'Historial_Sets': historial_sets
    })

def procesar_tiebreaks(row):
    score = str(row['Score'])
    ganados = perdidos = 0
    
    for s in score.split():
        if '(' in s and ')' in s:
            set_score = s.split('(')[0]
            g1, g2 = map(int, set_score.split('-'))
            
            if (row['W o L'] == 'W' and g1 > g2) or (row['W o L'] == 'L' and g2 > g1):
                ganados += 1
            else:
                perdidos += 1
    
    return ganados, perdidos

def calcular_dificultad_rivales(serie_vrk):
    vrk_clean = pd.to_numeric(serie_vrk, errors='coerce').replace(0, 1000)
    log_vrk = np.log10(vrk_clean)
    return (1 - (log_vrk / 3)).mean()

def analizar_partidos_criticos(df_jugador):
    # Filtrar partidos donde perdió al menos 1 set y luego se recuperó
    df_criticos = df_jugador[
        df_jugador['Historial_Sets'].apply(
            lambda x: any(x[i] == 'L' and i < len(x)-1 and x[i+1] == 'W' for i in range(len(x)))
            )
    ]
    
    # Calcular estadísticas en estos partidos
    stats = {
        'Partidos_Criticos_Ganados': df_criticos['W o L'].eq('W').sum(),
        'Avg_Puntuación_Critica': df_criticos['Puntuación'].mean(),
        'Sets_Promedio_Criticos': df_criticos['Sets_Ganados'].mean()
    }
    
    return stats