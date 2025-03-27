from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import numpy as np
from pathlib import Path
from modulos.config import ROUND_WEIGHTS
from modulos.metrics import calcular_dificultad_rivales, parse_score

# ======================
# ANÁLISIS COMPARATIVO
# ======================
def analizar_jugadores(data):
    if not data:  # Si no hay datos de entrada
        print("⚠️ Error: No hay datos para analizar")
        return pd.DataFrame()  # Retorna DataFrame vacío

    resultados = {}
    for jugador, df in data.items():
        # Calcular dificultad de rivales PARA CADA JUGADOR
        vrk_series = pd.to_numeric(df['vRk'], errors='coerce')
        
        stats = {
            # Métricas básicas
            'Partidos_Ganados': df['W o L'].eq('W').sum(),
            'Partidos_Perdidos': len(df) - df['W o L'].eq('W').sum(),
            '%_Victorias': round(df['W o L'].eq('W').mean() * 100, 2),
            
            # Análisis de sets
            'Sets/Participado': df['Sets_Ganados'].mean(),
            '%_Sets_Ganados': (df['Sets_Ganados'].sum() / df['Score'].apply(lambda x: len(parse_score(x))).sum()) * 100,
            
            # Tiebreaks
            'Tiebreaks_Ganados': df['Tiebreaks_Ganados'].sum(),
            'Tiebreaks_Perdidos': df['Tiebreaks_Perdidos'].sum(),
            '%_Tiebreaks': round((df['Tiebreaks_Ganados'].sum() / (df['Tiebreaks_Ganados'].sum() + df['Tiebreaks_Perdidos'].sum())) * 100, 2) if (df['Tiebreaks_Ganados'].sum() + df['Tiebreaks_Perdidos'].sum()) > 0 else 0,
            
            # Rendimiento en rondas
            'Rendimiento_Fases_Avanzadas': round(np.average(df['W o L'].eq('W').astype(int), weights=df['Rd_Weight']) * 100, 2),
            
            # Métricas de servicio
            'DR': df['DR'].mean(),
            'Ace%': df['A%'].mean(),
            'Doble_Falta%': df['DF%'].mean(),
            '1stIn%': df['1stIn'].mean(),
            '1stWon%': df['1st%'].mean(),
            '2ndWon%': df['2nd%'].mean(),
            
            # Break Points
            'BPSvd_Salvados': df['BPSvd_Salvados'].sum(),
            'BPSvd_Totales': df['BPSvd_Totales'].sum(),
            'BPSvd%': round((df['BPSvd_Salvados'].sum() / df['BPSvd_Totales'].sum()) * 100, 2) if df['BPSvd_Totales'].sum() > 0 else 0,
            'BPSvd/Participado': df['BPSvd_Totales'].mean(),
            
            # Dificultad de rivales
            'Dificultad_Rivales': calcular_dificultad_rivales(vrk_series),
        }
        
        # Promedio de puntos ganados por set
        puntos_ganados = [p for sublist in df['Puntos_Ganados'] for p in sublist]
        avg_puntos_ganados = np.nanmean(puntos_ganados) if puntos_ganados else 0
        
        # Puntos en sets perdidos (efectividad bajo presión)
        avg_puntos_perdidos = np.mean([p for sublist in df['Puntos_Perdidos'] for p in sublist])
        
        # Tasa de recuperación (ganar set después de perder uno)
        recuperacion = 0
        historial_total = [s for sublist in df['Historial_Sets'] for s in sublist]
        num_sets_perdidos = historial_total.count('L')
        recuperacion = 0
        
        for i in range(1, len(historial_total)):
            if historial_total[i-1] == 'L' and historial_total[i] == 'W':
                recuperacion += 1
        tasa_recuperacion = (recuperacion / num_sets_perdidos) * 100 if num_sets_perdidos > 0 else 0
        
        stats.update({
            'Avg_Puntos_Ganados': round(avg_puntos_ganados, 2),
            'Avg_Puntos_Perdidos': round(avg_puntos_perdidos, 2),
            '%_Recuperacion_Sets': round(tasa_recuperacion, 2)
        })

        resultados[jugador] = stats
    
    return pd.DataFrame(resultados).T

# En analysis.py, modificar los pesos:
def determinar_mejor_rendimiento(df_analisis):
    scaler = MinMaxScaler()
    
    if len(df_analisis) < 2:
        print("⚠️ Advertencia: Insuficientes datos para análisis avanzado")
        df_analisis['Puntuación'] = 0
        return df_analisis.sort_values('Puntuación', ascending=False)

    metrics = df_analisis[[
        '%_Victorias', 'Rendimiento_Fases_Avanzadas', 'Dificultad_Rivales',
        '%_Tiebreaks', 'BPSvd%', 'BPSvd/Participado', '%_Recuperacion_Sets'
    ]]
    
    df_scaled = pd.DataFrame(scaler.fit_transform(metrics), 
                            columns=metrics.columns, 
                            index=metrics.index)
    
    pesos = [0.10, 0.15, 0.25, 0.10, 0.10, 0.15, 0.10]
    df_analisis['Puntuación'] = df_scaled.dot(pd.Series(pesos, index=df_scaled.columns))

    # =====================================================
    # Segmentación Dinámica (Elimina la versión con bins fijos)
    # =====================================================
    q33 = df_analisis['%_Recuperacion_Sets'].quantile(0.33)
    q66 = df_analisis['%_Recuperacion_Sets'].quantile(0.66)
    
    bins = [0, q33, q66, 100]
    labels = [f'Baja (<{int(q33)}%)', f'Media ({int(q33)}-{int(q66)}%)', f'Alta (>={int(q66)}%)']
    
    df_analisis['Nivel_Recuperacion'] = pd.cut(
        df_analisis['%_Recuperacion_Sets'],
        bins=bins,
        labels=labels,
        include_lowest=True
    )
    
    stats_segmentacion = df_analisis.groupby(
        'Nivel_Recuperacion', 
        observed=False
    )['Puntuación'].agg(['mean', 'std']).fillna(0)

    print("\n=== DATOS ANALIZADOS ===")
    print(df_analisis)
    print("Número de registros:", len(df_analisis))

    # =====================================================
    # Cálculo de Correlaciones (con indentación correcta)
    # =====================================================
    try:
        numeric_cols = df_analisis.select_dtypes(include=[np.number]).columns.drop('Puntuación', errors='ignore')
        numeric_cols = numeric_cols[df_analisis[numeric_cols].nunique() > 1]
        
        if len(numeric_cols) > 0:
            correlaciones = df_analisis[numeric_cols].corrwith(df_analisis['Puntuación'])
            print("\n🔍 Correlación con la Puntuación Final:")
            print(correlaciones.sort_values(ascending=False).round(2))
        else:
            print("ℹ️ No hay suficientes datos para calcular correlaciones.")
            
    except Exception as e:
        print(f"❌ Error en correlaciones: {str(e)}")
    
    return df_analisis.sort_values('Puntuación', ascending=False)