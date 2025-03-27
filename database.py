from datetime import datetime
import pandas as pd
import numpy as np
from pathlib import Path
from modulos.config import DATABASE_PATH

def guardar_resultados(df_final):
    # Generar número de registro
    nuevo_registro = 1
    
    if df_final is None or df_final.empty:
        print("⚠️ Error: No hay datos para guardar")
        return 0
    
    try:  # <-- BLOQUE PRINCIPAL DE TRY
        nuevo_df = df_final.reset_index(names='Jugador').copy()
        nuevo_df['Registro_Nº'] = 1
        
        try:  # Sub-bloque para manejar FileNotFoundError
            existing = pd.read_excel(DATABASE_PATH)
            if 'Registro_Nº' in existing.columns:
                nuevo_registro = existing['Registro_Nº'].max() + 1
        except FileNotFoundError:
            existing = pd.DataFrame(columns=nuevo_df.columns)
        
        # =============================================
        # NUEVO: Redondear todos los float a 2 decimales
        # =============================================
        float_cols = nuevo_df.select_dtypes(include=['float64']).columns
        nuevo_df[float_cols] = nuevo_df[float_cols].round(2)
        
        # Asignar fecha y registro
        nuevo_df['Fecha'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        nuevo_df['Registro_Nº'] = nuevo_registro
        
        # Concatenar y guardar
        updated = pd.concat([existing, nuevo_df], ignore_index=True)
        updated = updated.astype({**nuevo_df.dtypes.to_dict(), 'Registro_Nº': 'int64'})
        updated = updated.dropna(axis=1, how='all')
        
        # Ordenar columnas
        cols = ['Registro_Nº', 'Fecha', 'Jugador'] + [c for c in updated.columns if c not in ['Registro_Nº', 'Fecha', 'Jugador']]
        updated = updated[cols]
        
        updated.to_excel(DATABASE_PATH, index=False)
        print(f"✅ Datos guardados en {DATABASE_PATH} | Registro: {nuevo_registro}")
        return nuevo_registro
    
    except Exception as e:
        print(f"❌ Error crítico al guardar: {str(e)}")
        return 0