import seaborn as sns
import numpy as np
import shutil
import sys
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from modulos.config import FILE_PATH, ROUND_WEIGHTS, DATA_DIR, backup_dir
from modulos.data_cleaning import limpiar_porcentajes, determinar_resultado
from modulos.metrics import calcular_sets_ganados, procesar_tiebreaks
from modulos.analysis import analizar_jugadores, determinar_mejor_rendimiento
from modulos.database import guardar_resultados

# Agregar la carpeta raíz al path de Python
sys.path.append(str(Path(__file__).parent))


# ======================
# EJECUCIÓN PRINCIPAL (ACTUALIZADA)
# ======================
if __name__ == "__main__":
    try:
        # 1. Cargar y procesar datos
        xls = pd.ExcelFile(FILE_PATH)
        jugadores = xls.sheet_names[:2]
        data = {}  # Definir data dentro del bloque principal

        # Cargar y validar datos
        if not jugadores:
            raise ValueError("❌ No hay hojas válidas en el Excel")

        for jugador in jugadores:
            try:
                df = xls.parse(jugador)
                df = limpiar_porcentajes(df)
                
        # Aplicar la función modificada (pasa el nombre del jugador)
                df[['Sets_Ganados', 'Puntos_Ganados', 'Puntos_Perdidos', 'Historial_Sets']] = df.apply(
                    lambda x: calcular_sets_ganados(x, jugador), 
                    axis=1
                )


                # Validación de columnas
                required_cols = ['Rd', 'Rk', 'vRk', 'Jugadores', 'Score', 
                                'DR', 'A%', 'DF%', '1stIn', '1st%', '2nd%',
                                'BPSvd_Salvados', 'BPSvd_Totales']
                missing = [col for col in required_cols if col not in df.columns]
                if missing:
                    raise ValueError(f"Columnas faltantes en {jugador}: {', '.join(missing)}")
                
                # Procesamiento
                df['W o L'] = df.apply(lambda x: determinar_resultado(x, jugador), axis=1)
                df[['Tiebreaks_Ganados', 'Tiebreaks_Perdidos']] = df.apply(procesar_tiebreaks, axis=1, result_type='expand')
                df['Rd_Weight'] = df['Rd'].map(ROUND_WEIGHTS).fillna(1)
                df['BPSvd%'] = np.where(df['BPSvd_Totales'] > 0, (df['BPSvd_Salvados'] / df['BPSvd_Totales']) * 100, 0)
                
                data[jugador] = df
                
            except Exception as e:
                print(f"❌ Error procesando {jugador}: {str(e)}")
                continue

        # Validación EXTRA
        if not data:
            raise ValueError("❌ No se procesaron datos de ningún jugador")
        
        df_analisis = analizar_jugadores(data)
        if df_analisis.empty:
            raise ValueError("❌ El análisis no generó métricas")
        
        df_final = determinar_mejor_rendimiento(df_analisis)
        if df_final is None or df_final.empty:
            raise ValueError("❌ No hay puntuaciones calculadas")
        
        n_registro = guardar_resultados(df_final)
        
        # 3. Copia de seguridad
        backup_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy(FILE_PATH, backup_dir / f"Registro{n_registro:02d}.xlsx")
        print(f"✅ Copia de seguridad creada: Registro{n_registro:02d}.xlsx")

        # 4. Visualización
        print("\n=== RESULTADOS FINALES ===")
        print(df_final[['Puntuación', '%_Victorias', 'BPSvd%']])
        
        df_final[['%_Victorias', 'Rendimiento_Fases_Avanzadas']].plot(
            kind='bar', 
            title='Comparativa de Rendimiento', 
            figsize=(10, 6)
        )
        plt.ylabel('Porcentaje')
        plt.tight_layout()
        plt.show()
        
        # NUEVO: Gráfico de Recuperación vs Puntuación
        # ==============================================
        plt.figure(figsize=(10, 6))
        sns.regplot(
            x=df_final['%_Recuperacion_Sets'], 
            y=df_final['Puntuación'],
            scatter_kws={'alpha':0.7, 'color':'#2ecc71'},
            line_kws={'color':'#e74c3c', 'linestyle':'--'}
        )
        plt.title('Impacto de la Recuperación en Sets en la Puntuación Final', pad=20)
        plt.xlabel('% de Recuperación después de Perder un Set')
        plt.ylabel('Puntuación Final')
        plt.grid(alpha=0.3)
        plt.tight_layout()
        plt.show()

    except Exception as e:
        print(f"🚨 Error crítico: {str(e)}")
