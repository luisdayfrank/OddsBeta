import sys
import json
import re
import pandas as pd
import sqlite3
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QHBoxLayout, QVBoxLayout, QListWidget, QListWidgetItem,
    QLineEdit, QLabel, QTextEdit, QSizePolicy, QPushButton
)
from PyQt5.QtCore import Qt

# --- Importaciones Clave ---
# Importamos la función para cargar pronósticos
from db_manager import cargar_pronosticos, DB_NAME, cargar_ultimos_analisis_guardados

# (El resto de las funciones de análisis y STATS_CONFIG se copiarán directamente en este archivo
#  para hacerlo autocontenido y fácil de usar)

# --- Definiciones de STATS_CONFIG (Copiadas de analisisv4.py) ---
def calculate_avg_rango(value_list):
    if isinstance(value_list, list) and len(value_list) == 2 and all(isinstance(x, (int, float)) for x in value_list):
        return (value_list[0] + value_list[1]) / 2.0
    return None

STATS_CONFIG_RESUMEN_GLOBAL = {
    'porcentaje_victorias_general': {'display_name': '% Victorias General', 'json_key': 'porcentaje_victorias_general', 'type': 'direct', 'logic': True},
    'rating_promedio_inicio_torneo': {'display_name': 'Rating Prom. Inicio Torneo', 'json_key': 'rating_jugador_promedio_torneo_inicio', 'type': 'direct', 'logic': True},
    'avg_rango_rating': {'display_name': 'Rating Prom. (Rango)', 'json_key': 'rango_rating_jugador', 'type': 'special_calc', 'calc_func': calculate_avg_rango, 'logic': True},
    'cambio_rating_prom_partido': {'display_name': 'Cambio Rating Prom. / Partido', 'json_key': 'cambio_rating_promedio_por_partido', 'type': 'direct', 'logic': True},
    'cambio_rating_prom_derrota': {'display_name': 'Cambio Rating Prom. / Derrota', 'json_key': 'cambio_rating_promedio_por_derrota', 'type': 'direct', 'logic': False},
    'porcentaje_sets_ganados': {'display_name': '% Sets Ganados', 'json_key': 'porcentaje_sets_ganados', 'type': 'direct', 'logic': True},
    'porcentaje_puntos_ganados': {'display_name': '% Puntos Ganados', 'json_key': 'porcentaje_puntos_ganados', 'type': 'direct', 'logic': True},
    'dif_rating_prom_jugador_vs_rival': {'display_name': 'Dif. Rating Prom. Jugador vs Rival', 'json_key': 'diferencia_rating_promedio_jugador_vs_rival', 'type': 'direct', 'logic': True},
    'pct_victorias_vs_mayor_rating': {'display_name': '% Victorias vs >Rating', 'json_key': 'porcentaje_victorias_vs_mayor_rating', 'type': 'direct', 'logic': True},
    'pct_derrotas_vs_menor_rating': {'display_name': '% Derrotas vs <Rating', 'json_key': 'porcentaje_derrotas_vs_menor_rating', 'type': 'direct', 'logic': False},
    'posicion_promedio_torneos': {'display_name': 'Posición Prom. Torneos', 'json_key': 'posicion_promedio_torneos', 'type': 'direct', 'logic': False},
    'porcentaje_torneos_ganados': {'display_name': '% Torneos Ganados', 'json_key': 'porcentaje_torneos_ganados', 'type': 'direct', 'logic': True},
    'volatilidad_delta': {'display_name': 'Volatilidad Delta', 'json_key': 'volatilidad_delta', 'type': 'direct', 'logic': False},
    'momentum_delta_ultimos_10': {'display_name': 'Momentum Delta Últimos 10', 'json_key': 'momentum_delta_acumulado_ultimos_10', 'type': 'direct', 'logic': True},
    'total_partidos_jugados': {'display_name': 'Total Partidos Jugados', 'json_key': 'total_partidos_jugados', 'type': 'direct', 'logic': True},
    'total_victorias': {'display_name': 'Total Victorias', 'json_key': 'total_victorias', 'type': 'direct', 'logic': True},
    'total_derrotas': {'display_name': 'Total Derrotas', 'json_key': 'total_derrotas', 'type': 'direct', 'logic': False},
    'total_torneos_jugados': {'display_name': 'Total Torneos Jugados', 'json_key': 'total_torneos_jugados', 'type': 'direct', 'logic': True},
    'finales_jugadas': {'display_name': 'Finales Jugadas', 'json_key': 'finales_jugadas', 'type': 'direct', 'logic': True},
    'terceros_puestos_jugados': {'display_name': '3ros Puestos Jugados', 'json_key': 'terceros_puestos_jugados', 'type': 'direct', 'logic': True},
    'total_sets_ganados_jugador': {'display_name': 'Total Sets Ganados', 'json_key': 'total_sets_ganados_jugador', 'type': 'direct', 'logic': True},
    'total_sets_perdidos_jugador': {'display_name': 'Total Sets Perdidos', 'json_key': 'total_sets_perdidos_jugador', 'type': 'direct', 'logic': False},
    'total_puntos_ganados_jugador': {'display_name': 'Total Puntos Ganados', 'json_key': 'total_puntos_ganados_jugador', 'type': 'direct', 'logic': True},
    'total_puntos_perdidos_jugador': {'display_name': 'Total Puntos Perdidos', 'json_key': 'total_puntos_perdidos_jugador', 'type': 'direct', 'logic': False},
    'victorias_vs_mayor_rating': {'display_name': 'Victorias vs >Rating (Abs)', 'json_key': 'victorias_vs_mayor_rating', 'type': 'direct', 'logic': True},
    'derrotas_vs_mayor_rating': {'display_name': 'Derrotas vs >Rating (Abs)', 'json_key': 'derrotas_vs_mayor_rating', 'type': 'direct', 'logic': False},
    'victorias_vs_menor_rating': {'display_name': 'Victorias vs <Rating (Abs)', 'json_key': 'victorias_vs_menor_rating', 'type': 'direct', 'logic': True},
    'derrotas_vs_menor_rating': {'display_name': 'Derrotas vs <Rating (Abs)', 'json_key': 'derrotas_vs_menor_rating', 'type': 'direct', 'logic': False},
    'torneos_ganados': {'display_name': 'Torneos Ganados (Abs)', 'json_key': 'torneos_ganados', 'type': 'direct', 'logic': True},
    'finales_ganadas': {'display_name': 'Finales Ganadas (Abs)', 'json_key': 'finales_ganadas', 'type': 'direct', 'logic': True},
    'finales_ganadas_pct': {'display_name': '% Finales Ganadas', 'json_key': 'finales_ganadas_pct', 'type': 'direct', 'logic': True},
    'terceros_puestos_ganados': {'display_name': '3ros Puestos Ganados (Abs)', 'json_key': 'terceros_puestos_ganados', 'type': 'direct', 'logic': True},
    'terceros_puestos_ganados_pct': {'display_name': '% 3ros Puestos Ganados', 'json_key': 'terceros_puestos_ganados_pct', 'type': 'direct', 'logic': True},
    'frec_vic_3_0': {'display_name': 'Frec: Victorias 3-0', 'json_key': 'frecuencia_marcadores', 'sub_key': 'victorias_3_0', 'type': 'dict_subkey', 'logic': True},
    'frec_derr_0_3': {'display_name': 'Frec: Derrotas 0-3', 'json_key': 'frecuencia_marcadores', 'sub_key': 'derrotas_0_3', 'type': 'dict_subkey', 'logic': False},
    'wr_vs_top': {'display_name': 'Winrate vs Rival Top', 'json_key': 'winrate_vs_categoria_rival', 'sub_key': 'winrate_vs_Top', 'type': 'dict_subkey', 'logic': True},
    'wr_vs_medio': {'display_name': 'Winrate vs Rival Medio', 'json_key': 'winrate_vs_categoria_rival', 'sub_key': 'winrate_vs_Medio', 'type': 'dict_subkey', 'logic': True},
    'wr_vs_bajo': {'display_name': 'Winrate vs Rival Bajo', 'json_key': 'winrate_vs_categoria_rival', 'sub_key': 'winrate_vs_Bajo', 'type': 'dict_subkey', 'logic': True},
    'ronda_final_wr': {'display_name': 'Winrate en Final (Ronda)', 'json_key': 'rendimiento_por_ronda', 'sub_key': ['final', 'win_rate'], 'type': 'dict_subkey', 'logic': True},
    'ronda_gr_wr': {'display_name': 'Winrate en Grupos (Ronda)', 'json_key': 'rendimiento_por_ronda', 'sub_key': ['gr', 'win_rate'], 'type': 'dict_subkey', 'logic': True},
    'momentum_cat': {'display_name': 'Momentum Rating (Tendencia)', 'json_key': 'momentum_rating_ultimos_10_partidos', 'type': 'categorical',
                     'value_map': {"Subida reciente de rating": 3, "Rating estable recientemente": 2, "Baja reciente de rating": 1, "No hay suficientes datos": 0, "No hay suficientes datos (menos de 10 o 2 partidos)":0 },
                     'logic': True},
}

STATS_CONFIG_KI = {
    'ki_std_rating': {'display_name': 'KI: Desv. Est. Rating', 'json_key': 'desviacion_estandar_rating_jugador', 'type': 'direct', 'logic': True},
    'ki_std_delta': {'display_name': 'KI: Desv. Est. Delta Partido', 'json_key': 'desviacion_estandar_delta_partido', 'type': 'direct', 'logic': True},
    'ki_racha_vic': {'display_name': 'KI: Racha Max Victorias', 'json_key': 'racha_victorias_mas_larga', 'type': 'direct', 'logic': True},
    'ki_racha_derr': {'display_name': 'KI: Racha Max Derrotas', 'json_key': 'racha_derrotas_mas_larga', 'type': 'direct', 'logic': False},
    'ki_p5_jugados': {'display_name': 'KI: Partidos a 5 Sets Jugados', 'json_key': 'partidos_a_5_sets_jugados', 'type': 'direct', 'logic': True},
    'ki_p5_victorias': {'display_name': 'KI: Victorias en 5 Sets', 'json_key': 'victorias_en_5_sets', 'type': 'direct', 'logic': True},
    'ki_p5_derrotas': {'display_name': 'KI: Derrotas en 5 Sets', 'json_key': 'derrotas_en_5_sets', 'type': 'direct', 'logic': False},
    'ki_p5_winrate': {'display_name': 'KI: Winrate en 5 Sets (%)', 'json_key': 'winrate_en_5_sets', 'type': 'direct', 'logic': True},
    'ki_pct_pts_set_decisivo': {'display_name': 'KI: Pts Ganados Set Decisivo (%)', 'json_key': 'porcentaje_puntos_ganados_sets_decisivos', 'type': 'direct', 'logic': True},
    'ki_prom_pts_set_decisivo': {'display_name': 'KI: Prom. Pts Jugador Set Decisivo', 'json_key': 'promedio_puntos_jugador_set_decisivo', 'type': 'direct', 'logic': True},
    'ki_sets_apretados_jugados': {'display_name': 'KI: Sets Apretados Jugados', 'json_key': 'sets_apretados_jugados', 'type': 'direct', 'logic': True},
    'ki_sets_apretados_ganados': {'display_name': 'KI: Sets Apretados Ganados', 'json_key': 'sets_apretados_ganados', 'type': 'direct', 'logic': True},
    'ki_pct_vic_sets_apretados': {'display_name': 'KI: Vic. Sets Apretados (%)', 'json_key': 'porcentaje_victorias_sets_apretados', 'type': 'direct', 'logic': True},
    'ki_remontadas_post_1er_set': {'display_name': 'KI: Remontadas (Tras Perder 1er Set)', 'json_key': 'partidos_remontados_tras_perder_1er_set', 'type': 'direct', 'logic': True},
    'ki_pct_remontadas_post_1er_set': {'display_name': 'KI: Remontadas (Tras Perder 1er Set) (%)', 'json_key': 'porcentaje_remontadas_tras_perder_1er_set', 'type': 'direct', 'logic': True},
    'ki_perdidos_post_ganar_1er_set': {'display_name': 'KI: Perdidos (Tras Ganar 1er Set)', 'json_key': 'partidos_perdidos_tras_ganar_1er_set', 'type': 'direct', 'logic': False},
    'ki_pct_perdidos_post_ganar_1er_set': {'display_name': 'KI: Perdidos (Tras Ganar 1er Set) (%)', 'json_key': 'porcentaje_derrotas_tras_ganar_1er_set', 'type': 'direct', 'logic': False},
    'ki_prom_dif_pts_sets_ganados': {'display_name': 'KI: Prom. Dif. Pts Sets Ganados', 'json_key': 'promedio_diferencial_puntos_sets_ganados', 'type': 'direct', 'logic': True},
    'ki_prom_dif_pts_sets_perdidos': {'display_name': 'KI: Prom. Dif. Pts Sets Perdidos', 'json_key': 'promedio_diferencial_puntos_sets_perdidos', 'type': 'direct', 'logic': False},
    'ki_pct_sets_gan_comodo': {'display_name': 'KI: Sets Ganados Cómodamente (%)', 'json_key': 'porcentaje_sets_ganados_comodamente', 'type': 'direct', 'logic': True},
    'ki_pct_sets_perd_estrep': {'display_name': 'KI: Sets Perdidos Estrepitosamente (%)', 'json_key': 'porcentaje_sets_perdidos_estrepitosamente', 'type': 'direct', 'logic': False},
    'ki_winrate_finales_orig': {'display_name': 'KI: Winrate Finales (Orig.) (%)', 'json_key': 'winrate_finales_original', 'type': 'direct', 'logic': True},
    'ki_finales_jugadas_orig': {'display_name': 'KI: Finales Jugadas (Orig.)', 'json_key': 'finales_jugadas_original', 'type': 'direct', 'logic': True},
    'ki_vic_rem_2_sets': {'display_name': 'KI: Vic. Remontando 2 Sets Abajo', 'json_key': 'victorias_remontando_2_sets_abajo_marcador', 'type': 'direct', 'logic': True},
    'ki_pct_vic_rem_2_sets': {'display_name': 'KI: Vic. Remontando 2 Sets Abajo (%)', 'json_key': 'porcentaje_partidos_remontando_2_sets_abajo', 'type': 'direct', 'logic': True},
    'ki_match_point_conv_proxy': {'display_name': 'KI: Match Point Conv. (Proxy) (%)', 'json_key': 'match_point_conversion_pct_proxy', 'type': 'direct', 'logic': True},
    'ki_tasa_conv_gr_final': {'display_name': 'KI: Tasa Conversión Grupo a Final (%)', 'json_key': 'tasa_conversion_grupo_a_final', 'type': 'direct', 'logic': True},
}

PREDICTIVIDAD_DINAMICA = {}
UMBRAL_EFECTIVIDAD = 55.0

# --- Funciones de Análisis (Copiadas de analisisv4.py y adaptadas) ---
# (Aquí van las funciones: cargar_predictividad_desde_db, get_stat_value_from_player_data,
#  comparar_estadisticas_detallado, generar_comparativa_texto, analizar_comparativa_jugadores)

def cargar_predictividad_desde_db(db_path):
    # (Esta función es la misma que ya tienes, no es necesario copiarla de nuevo aquí)
    # ...
    global PREDICTIVIDAD_DINAMICA
    PREDICTIVIDAD_DINAMICA = {}
    
    # Verificar si el archivo de la base de datos existe
    if not os.path.exists(db_path):
        print(f"Error crítico: El archivo de base de datos no se encontró en la ruta: {db_path}")
        return

    analisis_guardados_dfs_dict = cargar_ultimos_analisis_guardados(db_path, limit=1)

    if not analisis_guardados_dfs_dict:
        print("No se encontraron análisis de efectividad guardados en la DB.")
        return

    stat_name_cols_map = {
        'overround': 'Análisis', 'resumen_global': 'Estadística',
        'killer_instinct': 'Estadística (KI)', 'torneos': 'Estadística (Torneos)',
        'oponentes': 'Estadística (Riv/H2H)'
    }

    print(f"\nINFO: Usando análisis de efectividad base de fecha: {analisis_guardados_dfs_dict.get('fecha_analisis','N/A')}")

    for modulo_key, df_efectividad in analisis_guardados_dfs_dict.items():
        if modulo_key in stat_name_cols_map and isinstance(df_efectividad, pd.DataFrame) and not df_efectividad.empty:
            col_nombre_estadistica = stat_name_cols_map[modulo_key]
            
            if col_nombre_estadistica in df_efectividad.columns and 'General (%)' in df_efectividad.columns:
                for _, row in df_efectividad.iterrows():
                    nombre_stat = str(row[col_nombre_estadistica]).strip()
                    general_pct_val = row['General (%)']
                    if pd.notna(general_pct_val):
                        PREDICTIVIDAD_DINAMICA[nombre_stat] = float(general_pct_val)
    
    if PREDICTIVIDAD_DINAMICA:
        print(f"INFO: PREDICTIVIDAD_DINAMICA cargada con {len(PREDICTIVIDAD_DINAMICA)} entradas.")


def get_stat_value_from_player_data(player_section_data, stat_config_entry):
    if player_section_data is None: return None
    json_key = stat_config_entry['json_key']
    stat_type = stat_config_entry.get('type', 'direct')
    base_value = player_section_data.get(json_key)
    if base_value is None: return None

    if stat_type == 'direct': return base_value
    elif stat_type == 'special_calc': return stat_config_entry['calc_func'](base_value)
    elif stat_type == 'dict_subkey':
        sub_key = stat_config_entry['sub_key']
        current_val = base_value
        if isinstance(base_value, dict):
            if isinstance(sub_key, list):
                for part in sub_key:
                    current_val = current_val.get(part) if isinstance(current_val, dict) else None
                return current_val
            else:
                return base_value.get(sub_key)
        return None
    elif stat_type == 'categorical':
        return stat_config_entry['value_map'].get(base_value)
    return base_value


def comparar_estadisticas_detallado(stat_config, val_j1, val_j2):
    if val_j1 is None or val_j2 is None or pd.isna(val_j1) or pd.isna(val_j2): return "N/A"
    try:
        num_val_j1, num_val_j2 = float(val_j1), float(val_j2)
    except (ValueError, TypeError): return "Error de tipo"

    logic = stat_config.get('logic', True)
    if stat_config.get('json_key') in ['cambio_rating_promedio_por_derrota', 'promedio_diferencial_puntos_sets_perdidos']:
        logic = True
    
    if logic:
        if num_val_j1 > num_val_j2: return "Jugador 1"
        if num_val_j2 > num_val_j1: return "Jugador 2"
    else:
        if num_val_j1 < num_val_j2: return "Jugador 1"
        if num_val_j2 < num_val_j1: return "Jugador 2"
    return "Empate"


def generar_comparativa_texto(jugador1_nombre, jugador2_nombre, resumen_comparativo, umbral, pronostico_tuple):
    """
    Genera un texto de análisis completo, incluyendo puntuación ponderada,
    índice de confianza y alertas automáticas.
    """
    texto = f"Análisis Comparativo: {jugador1_nombre} vs {jugador2_nombre}\n"
    texto += "--------------------------------------------------\n\n"

    # --- 1. CLASIFICACIÓN DE ESTADÍSTICAS Y CÁLCULO DE SCORES ---
    ventajas_j1_alta, ventajas_j2_alta = [], []
    ventajas_j1_baja, ventajas_j2_baja = [], []
    stats_favor_j1, stats_favor_j2 = 0, 0
    stats_clave_favor_j1, stats_clave_favor_j2 = 0, 0
    score_ponderado_j1, score_ponderado_j2 = 0.0, 0.0
    
    sorted_resumen = sorted(resumen_comparativo.items(), key=lambda item: PREDICTIVIDAD_DINAMICA.get(item[0], 0.0), reverse=True)

    for stat_name, data in sorted_resumen:
        efectividad = PREDICTIVIDAD_DINAMICA.get(stat_name, 0.0)
        val_j1_str = f"{data['valor_j1']:.2f}" if isinstance(data['valor_j1'], float) else str(data['valor_j1'])
        val_j2_str = f"{data['valor_j2']:.2f}" if isinstance(data['valor_j2'], float) else str(data['valor_j2'])
        detalle = f"- {stat_name} (J1: {val_j1_str} vs J2: {val_j2_str} | Efec: {efectividad:.2f}%)"
        
        if data["superior"] == "Jugador 1":
            stats_favor_j1 += 1
            if efectividad >= umbral:
                ventajas_j1_alta.append(detalle)
                stats_clave_favor_j1 += 1
                score_ponderado_j1 += efectividad # Suma ponderada
            else:
                ventajas_j1_baja.append(detalle)
        elif data["superior"] == "Jugador 2":
            stats_favor_j2 += 1
            if efectividad >= umbral:
                ventajas_j2_alta.append(detalle)
                stats_clave_favor_j2 += 1
                score_ponderado_j2 += efectividad # Suma ponderada
            else:
                ventajas_j2_baja.append(detalle)

    # --- 2. GENERACIÓN DE SECCIONES DE ANÁLISIS ---
    texto += f"ESTADÍSTICAS CLAVE (Efectividad >= {umbral}%):\n"
    if ventajas_j1_alta: texto += f"  A favor de {jugador1_nombre}:\n" + '\n'.join(f"    {v}" for v in ventajas_j1_alta) + "\n"
    if ventajas_j2_alta: texto += f"  A favor de {jugador2_nombre}:\n" + '\n'.join(f"    {v}" for v in ventajas_j2_alta) + "\n"
    if not ventajas_j1_alta and not ventajas_j2_alta: texto += "  (Ninguna estadística clave para destacar)\n"
    
    texto += "\nOTRAS ESTADÍSTICAS:\n"
    if ventajas_j1_baja: texto += f"  A favor de {jugador1_nombre}:\n" + '\n'.join(f"    {v}" for v in ventajas_j1_baja) + "\n"
    if ventajas_j2_baja: texto += f"  A favor de {jugador2_nombre}:\n" + '\n'.join(f"    {v}" for v in ventajas_j2_baja) + "\n"
    if not ventajas_j1_baja and not ventajas_j2_baja: texto += "  (Ninguna otra estadística con un claro superior)\n"

    # --- 3. NUEVO: ANÁLISIS PONDERADO, CONFIANZA Y ALERTAS ---
    texto += "\n==================================================\n"
    texto += "=== ANÁLISIS DE PREDICCIÓN AVANZADO ===\n"
    texto += "==================================================\n"

    # --- Puntuación Ponderada y Conclusión ---
    ganador_ponderado = "Empate"
    if score_ponderado_j1 > score_ponderado_j2: ganador_ponderado = jugador1_nombre
    elif score_ponderado_j2 > score_ponderado_j1: ganador_ponderado = jugador2_nombre

    texto += "\n--- ANÁLISIS PONDERADO (STATS CLAVE) ---\n"
    texto += f"Score Ponderado {jugador1_nombre}: {score_ponderado_j1:.2f}\n"
    texto += f"Score Ponderado {jugador2_nombre}: {score_ponderado_j2:.2f}\n"
    texto += f"Ganador según Ponderación: {ganador_ponderado}\n"

    # --- Índice de Confianza ---
    total_score_ponderado = score_ponderado_j1 + score_ponderado_j2
    confianza_str = "N/A"
    confianza_level = "Indefinido"
    indice_confianza = 0

    if total_score_ponderado > 0:
        indice_confianza = abs(score_ponderado_j1 - score_ponderado_j2) / total_score_ponderado * 100
        confianza_str = f"{indice_confianza:.1f}%"
        if indice_confianza < 15: confianza_level = "BAJA (Partido muy reñido)"
        elif indice_confianza < 40: confianza_level = "MEDIA"
        else: confianza_level = "ALTA"
    
    texto += f"\nÍndice de Confianza del Pronóstico: {confianza_str} ({confianza_level})\n"

    # --- Alertas Automáticas ---
    texto += "\n--- ALERTAS DE PRONÓSTICO ---\n"
    alertas = []

    # Alerta de Contradicción
    ganador_general = "Empate"
    if stats_favor_j1 > stats_favor_j2: ganador_general = jugador1_nombre
    elif stats_favor_j2 > stats_favor_j1: ganador_general = jugador2_nombre
    
    ganador_clave_simple = "Empate"
    if stats_clave_favor_j1 > stats_clave_favor_j2: ganador_clave_simple = jugador1_nombre
    elif stats_clave_favor_j2 > stats_clave_favor_j1: ganador_clave_simple = jugador2_nombre

    if ganador_general != "Empate" and ganador_clave_simple != "Empate" and ganador_general != ganador_clave_simple:
        alertas.append(f"[!] CONTRADICCIÓN: El análisis general favorece a {ganador_general} pero el de stats clave a {ganador_clave_simple}.")

    # Alerta de Underdog Arriesgado
    try:
        odds_j1 = pronostico_tuple[15]
        odds_j2 = pronostico_tuple[16]
        odds_ganador_ponderado = odds_j1 if ganador_ponderado == jugador1_nombre else odds_j2
        if odds_ganador_ponderado > 2.0 and indice_confianza < 40:
             alertas.append(f"[!] RIESGO: Se pronostica un 'underdog' (Odds: {odds_ganador_ponderado:.2f}) con confianza {confianza_level}.")
    except (IndexError, TypeError):
        pass # No hacer nada si los datos de odds no están disponibles

    # Alerta de Confianza Baja
    if confianza_level.startswith("BAJA"):
        alertas.append("[!] PRECAUCIÓN: El margen estadístico es muy estrecho. Resultado impredecible.")
        
    if not alertas:
        texto += "  - Sin alertas significativas detectadas.\n"
    else:
        for alerta in alertas:
            texto += f"  {alerta}\n"
            
    texto += "\n==================================================\n"

    return texto.strip()

def analizar_comparativa_jugadores(datos_jugadores_dict, pronostico_tuple):
    """
    Analiza la comparativa y ahora pasa el pronostico_tuple completo
    a la función que genera el texto para poder usar las odds.
    """
    if not datos_jugadores_dict or len(datos_jugadores_dict) != 2:
        return "Error: Se requieren datos de dos jugadores."

    nombres = list(datos_jugadores_dict.keys())
    j1_nombre, j2_nombre = nombres[0], nombres[1]
    j1_stats, j2_stats = datos_jugadores_dict[j1_nombre], datos_jugadores_dict[j2_nombre]
    resumen_comparativo = {}

    modulos_a_comparar = {
        "resumen_global": STATS_CONFIG_RESUMEN_GLOBAL,
        "killer_instinct": STATS_CONFIG_KI
    }

    for seccion, stats_config in modulos_a_comparar.items():
        for stat_key, config_entry in stats_config.items():
            if not isinstance(config_entry, dict): continue
            
            val_j1 = get_stat_value_from_player_data(j1_stats.get(seccion), config_entry)
            val_j2 = get_stat_value_from_player_data(j2_stats.get(seccion), config_entry)
            
            superior = comparar_estadisticas_detallado(config_entry, val_j1, val_j2)

            if superior in ["Jugador 1", "Jugador 2"]:
                resumen_comparativo[config_entry['display_name']] = {
                    "valor_j1": val_j1 if val_j1 is not None else "N/A",
                    "valor_j2": val_j2 if val_j2 is not None else "N/A",
                    "superior": superior
                }
    
    if not resumen_comparativo:
        return f"No se pudieron comparar estadísticas para {j1_nombre} y {j2_nombre}."

    # Pasar el pronostico_tuple a la función que genera el texto
    return generar_comparativa_texto(j1_nombre, j2_nombre, resumen_comparativo, UMBRAL_EFECTIVIDAD, pronostico_tuple)
# --- Clase del Widget Interactivo ---

class AnalisisInteractivoWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Análisis Comparativo Interactivo")
        self.pronosticos_data_list = []

        # Cargar la predictividad una sola vez al iniciar el widget
        cargar_predictividad_desde_db(DB_NAME)
        if not PREDICTIVIDAD_DINAMICA:
            print("ADVERTENCIA CRÍTICA: No se cargó PREDICTIVIDAD_DINAMICA. El análisis estará incompleto.")
        
        # --- UI Setup ---
        main_layout = QHBoxLayout(self)

        # Panel izquierdo: Selección de Pronóstico
        left_panel = QVBoxLayout()
        left_panel.addWidget(QLabel("<b>Seleccionar Pronóstico</b>"))
        
        self.btn_actualizar = QPushButton("🔄 Actualizar Lista")
        self.btn_actualizar.clicked.connect(self._actualizar_datos)
        left_panel.addWidget(self.btn_actualizar)
        
        self.filtro_input = QLineEdit()
        self.filtro_input.setPlaceholderText("Buscar por jugador o fecha (YYYY-MM-DD)...")
        self.filtro_input.textChanged.connect(self._filtrar_lista_pronosticos)
        left_panel.addWidget(self.filtro_input)

        self.lista_pronosticos = QListWidget()
        self.lista_pronosticos.currentItemChanged.connect(self._on_pronostico_seleccionado)
        left_panel.addWidget(self.lista_pronosticos)

        # Panel derecho: Visualización del Análisis
        right_panel = QVBoxLayout()
        right_panel.addWidget(QLabel("<b>Análisis Comparativo Detallado</b>"))

        self.texto_analisis = QTextEdit()
        self.texto_analisis.setReadOnly(True)
        self.texto_analisis.setFontFamily("Courier") # Fuente monoespaciada para mejor alineación
        self.texto_analisis.setLineWrapMode(QTextEdit.NoWrap)
        right_panel.addWidget(self.texto_analisis)

        # Añadir paneles al layout principal
        left_widget = QWidget()
        left_widget.setLayout(left_panel)
        left_widget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)

        right_widget = QWidget()
        right_widget.setLayout(right_panel)
        right_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        main_layout.addWidget(left_widget, 1) # Proporción 1 para el panel izquierdo
        main_layout.addWidget(right_widget, 3) # Proporción 3 para el panel derecho (más ancho)

        # Cargar datos iniciales
        self.cargar_y_mostrar_pronosticos()

    def cargar_y_mostrar_pronosticos(self):
        """Carga todos los pronósticos desde la DB y los muestra en la lista."""
        self.pronosticos_data_list = cargar_pronosticos(DB_NAME)
        self.lista_pronosticos.clear()
        
        if not self.pronosticos_data_list:
            self.lista_pronosticos.addItem("No hay pronósticos en la base de datos.")
            return

        for pronostico_tuple in self.pronosticos_data_list:
            # pronostico_tuple[1] es fecha_creacion, [2] es j1, [3] es j2
            fecha = pronostico_tuple[1].split(" ")[0] # Tomar solo la parte de la fecha
            j1 = pronostico_tuple[2]
            j2 = pronostico_tuple[3]
            display_text = f"{fecha} - {j1} vs {j2}"
            
            item = QListWidgetItem(display_text)
            item.setData(Qt.UserRole, pronostico_tuple) # Guardar la tupla completa en el item
            self.lista_pronosticos.addItem(item)
            
    def _actualizar_datos(self):
        """
        Limpia la vista y recarga TODA la información necesaria:
        1. Los datos de efectividad (PREDICTIVIDAD_DINAMICA).
        2. La lista de pronósticos desde la base de datos.
        """
        print("INFO: Actualizando toda la información...")
        
        # 1. Limpiar la vista actual
        self.texto_analisis.clear()
        self.filtro_input.clear()
        
        # 2. RECARGAR LOS DATOS DE EFECTIVIDAD
        print("INFO: Recargando datos de efectividad...")
        cargar_predictividad_desde_db(DB_NAME)
        if not PREDICTIVIDAD_DINAMICA:
            print("ADVERTENCIA CRÍTICA: No se cargó PREDICTIVIDAD_DINAMICA en la actualización.")

        # 3. RECARGAR LA LISTA DE PRONÓSTICOS
        print("INFO: Recargando lista de pronósticos...")
        self.cargar_y_mostrar_pronosticos()
        
        print("INFO: Actualización completa.")
        
    def _preparar_datos_para_analisis(self, pronostico_tuple):
        """
        Toma una tupla de pronóstico de la DB y la convierte al formato
        que espera la función analizar_comparativa_jugadores.
        Esto reemplaza la necesidad de parsear un bloque de texto.
        """
        try:
            # Mapeo de índices a nombres de columna para claridad, basado en la tabla pronosticos
            columnas = {
                'id': 0, 'fecha_creacion': 1, 'jugador1': 2, 'jugador2': 3, 'calificacion_j1': 4,
                'calificacion_j2': 5, 'probabilidad_j1': 6, 'probabilidad_j2': 7, 'resumen_global': 8,
                'killer_instinct': 9, 'rachas': 10, 'torneos': 11, 'h2h': 12, 'common_opponents': 13,
                'ganador_pronosticado': 14, 'odds_jugador1': 15, 'odds_jugador2': 16, 'overround': 17,
                'resultado_registrado': 18, 'sets_resultado': 19, 'puntos_por_set_resultado': 20
            }
            
            def get_val(key):
                # Asegurarse de que el índice no esté fuera de rango
                idx = columnas.get(key)
                if idx is not None and idx < len(pronostico_tuple):
                    return pronostico_tuple[idx]
                return None
    
            j1_nombre = get_val('jugador1')
            j2_nombre = get_val('jugador2')
            
            # Parsear los JSON de las columnas
            resumen_global_json = get_val('resumen_global')
            killer_instinct_json = get_val('killer_instinct')
    
            resumen_global_data = json.loads(resumen_global_json) if resumen_global_json else {}
            killer_instinct_data = json.loads(killer_instinct_json) if killer_instinct_json else {}
    
            # Estructurar los datos por jugador
            datos_formateados = {
                j1_nombre: {
                    'nombre': j1_nombre,
                    'resumen_global': resumen_global_data.get(j1_nombre, {}),
                    'killer_instinct': killer_instinct_data.get(j1_nombre, {})
                },
                j2_nombre: {
                    'nombre': j2_nombre,
                    'resumen_global': resumen_global_data.get(j2_nombre, {}),
                    'killer_instinct': killer_instinct_data.get(j2_nombre, {})
                }
            }
            return datos_formateados
            
        except json.JSONDecodeError as e:
            print(f"Error fatal parseando JSON de la base de datos para el pronóstico: {e}")
            return None
        except Exception as e:
            print(f"Error inesperado al preparar datos para análisis: {e}")
            return None

    def _generar_cabecera_pronostico(self, pronostico_tuple):
        """Genera un string de texto con el resumen del pronóstico seleccionado."""
        
        # Mapeo de índices a nombres de columna para claridad, basado en la tabla pronosticos
        columnas = {
            'id': 0, 'fecha_creacion': 1, 'jugador1': 2, 'jugador2': 3, 'calificacion_j1': 4,
            'calificacion_j2': 5, 'probabilidad_j1': 6, 'probabilidad_j2': 7, 'resumen_global': 8,
            'killer_instinct': 9, 'rachas': 10, 'torneos': 11, 'h2h': 12, 'common_opponents': 13,
            'ganador_pronosticado': 14, 'odds_jugador1': 15, 'odds_jugador2': 16, 'overround': 17,
            'resultado_registrado': 18, 'sets_resultado': 19, 'puntos_por_set_resultado': 20
        }
        
        def get_val(key):
            return pronostico_tuple[columnas[key]]

        j1, j2 = get_val('jugador1'), get_val('jugador2')
        
        # Construcción del texto
        texto = "=== PRONÓSTICO DE PARTIDO ===\n\n"
        texto += f"Jugador 1: {j1}\n"
        texto += f"Jugador 2: {j2}\n"
        texto += f"Fecha del pronóstico: {get_val('fecha_creacion')}\n\n"

        texto += "--- CALIFICACIONES ---\n"
        texto += f"{j1}: {get_val('calificacion_j1'):.2f}\n"
        texto += f"{j2}: {get_val('calificacion_j2'):.2f}\n\n"

        texto += "--- PROBABILIDADES ---\n"
        texto += f"{j1}: {get_val('probabilidad_j1'):.1f}%\n"
        texto += f"{j2}: {get_val('probabilidad_j2'):.1f}%\n\n"

        texto += "--- DETALLES DE PREDICCIÓN ---\n"
        texto += f"Ganador Pronosticado: {get_val('ganador_pronosticado')}\n"
        texto += f"Odds {j1}: {get_val('odds_jugador1')}\n"
        texto += f"Odds {j2}: {get_val('odds_jugador2')}\n"
        
        overround_val = get_val('overround')
        if overround_val is not None:
            texto += f"Overround: {overround_val:.2f}%\n\n"
        else:
            texto += "\n"

        # Sección de resultado (solo si está disponible)
        resultado = get_val('resultado_registrado')
        if resultado:
            texto += "--- RESULTADO REGISTRADO DEL PARTIDO ---\n"
            # Determinar si el pronóstico fue acertado
            ganador_real = resultado.split(' (')[0]
            acierto = "Acertado" if ganador_real == get_val('ganador_pronosticado') else "Fallido"
            texto += f"Pronóstico: {acierto}\n"
            texto += f"Sets: {get_val('sets_resultado')}\n"
            texto += f"Puntos por Set: {get_val('puntos_por_set_resultado')}\n"
            
        return texto

    def _filtrar_lista_pronosticos(self, texto_filtro):
        """Oculta o muestra items en la lista según el texto del filtro."""
        texto_filtro = texto_filtro.lower()
        for i in range(self.lista_pronosticos.count()):
            item = self.lista_pronosticos.item(i)
            if texto_filtro in item.text().lower():
                item.setHidden(False)
            else:
                item.setHidden(True)

    def _on_pronostico_seleccionado(self, current_item, previous_item):
        """
        Se activa cuando el usuario selecciona un pronóstico de la lista.
        Ahora genera una cabecera y la une al análisis comparativo.
        """
        if current_item is None:
            self.texto_analisis.clear()
            return
            
        pronostico_tuple = current_item.data(Qt.UserRole)
        if pronostico_tuple is None:
            self.texto_analisis.setText("Error: No hay datos asociados a este pronóstico.")
            return

        # 1. Generar la cabecera con el resumen del pronóstico
        texto_cabecera = self._generar_cabecera_pronostico(pronostico_tuple)
        
        # 2. Preparar los datos para el análisis comparativo
        datos_para_analisis = self._preparar_datos_para_analisis(pronostico_tuple)
        
        if not datos_para_analisis:
            # Mostrar solo la cabecera si el análisis falla
            self.texto_analisis.setPlainText(texto_cabecera + "\n\nError al procesar los datos JSON para el análisis comparativo.")
            return

        # 3. Generar el texto del análisis comparativo, pasando ahora el pronostico_tuple completo
        analisis_texto = analizar_comparativa_jugadores(datos_para_analisis, pronostico_tuple)
        
        # 4. Unir ambos textos y mostrarlos
        texto_final = texto_cabecera + "\n\n" + analisis_texto
        self.texto_analisis.setPlainText(texto_final)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # Crear la ventana principal y añadir el widget
    main_window = QWidget()
    main_window.setWindowTitle("Panel de Análisis Interactivo de Pronósticos")
    main_window.setGeometry(100, 100, 1200, 700)
    
    layout = QVBoxLayout(main_window)
    analisis_widget = AnalisisInteractivoWidget()
    layout.addWidget(analisis_widget)
    
    main_window.show()
    sys.exit(app.exec_())
