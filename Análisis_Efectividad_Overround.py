import pandas as pd
import math
import sqlite3

DB_NAME = "data/historial_jugadores.db"

def cargar_partidos(db_path=DB_NAME):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
        'SELECT jugador1, jugador2, odds_jugador1, odds_jugador2, overround, sets_resultado, calificacion_j1, calificacion_j2 FROM pronosticos'
    )
    data = cursor.fetchall()
    conn.close()
    columns = [
        "jugador1", "jugador2", "odds_jugador1", "odds_jugador2", "overround",
        "sets_resultado", "calificacion_j1", "calificacion_j2"
    ]
    return pd.DataFrame(data, columns=columns)

def determinar_ganador_real(sets_resultado, jugador1, jugador2):
    if not sets_resultado or ':' not in sets_resultado:
        return None
    try:
        sets_j1, sets_j2 = map(int, sets_resultado.split(':'))
        if sets_j1 > sets_j2:
            return jugador1
        elif sets_j2 > sets_j1:
            return jugador2
        else:
            return None
    except Exception:
        return None

def get_overround_bucket(overround_value, step_size):
    if overround_value is None or pd.isna(overround_value):
        return None
    try:
        ov = float(overround_value)
        if ov <= 0: return None
        bucket_id = math.floor((ov - 0.01) / step_size)
        lower_bound = bucket_id * step_size + 0.01
        upper_bound = bucket_id * step_size + step_size
        return f"{lower_bound:.2f}-{upper_bound:.2f}"
    except:
        return None

# ... (resto del código igual)

def analizar_favorito_odds_vs_overround(db_path=DB_NAME, overround_step=0.5):
    df = cargar_partidos(db_path)
    df = df.dropna(subset=["jugador1", "jugador2", "odds_jugador1", "odds_jugador2", "overround", "sets_resultado", "calificacion_j1", "calificacion_j2"])

    # Determinar favorito por odds
    df["favorito"] = df.apply(lambda row: row["jugador1"] if row["odds_jugador1"] < row["odds_jugador2"] else row["jugador2"], axis=1)
    df["cuota_favorito"] = df.apply(lambda row: row["odds_jugador1"] if row["favorito"] == row["jugador1"] else row["odds_jugador2"], axis=1)
    df["calif_favorito"] = df.apply(lambda row: row["calificacion_j1"] if row["favorito"] == row["jugador1"] else row["calificacion_j2"], axis=1)
    df["calif_no_favorito"] = df.apply(lambda row: row["calificacion_j2"] if row["favorito"] == row["jugador1"] else row["calificacion_j1"], axis=1)
    df["favorito_mayor_calif"] = df["calif_favorito"] > df["calif_no_favorito"]
    df["favorito_menor_calif"] = df["calif_favorito"] < df["calif_no_favorito"]

    # Ganador real
    df["ganador_real"] = df.apply(lambda row: determinar_ganador_real(row["sets_resultado"], row["jugador1"], row["jugador2"]), axis=1)
    df["favorito_gana"] = df["ganador_real"] == df["favorito"]
    df["favorito_mayor_calif_gana"] = df["favorito_gana"] & df["favorito_mayor_calif"]
    df["favorito_menor_calif_gana"] = df["favorito_gana"] & df["favorito_menor_calif"]

    # Overround bucket
    df["overround_bucket"] = df["overround"].apply(lambda o: get_overround_bucket(o, overround_step))
    df = df.dropna(subset=["overround_bucket"])

    # Usando .agg para evitar warnings y ser más eficiente
    resumen = df.groupby("overround_bucket").agg(
        Nº_partidos=('favorito_gana', 'count'),
        Acierto_favorito_pct=('favorito_gana', lambda x: 100 * x.sum() / len(x) if len(x) else None),
        Nº_fav_mayor_calif=('favorito_mayor_calif', 'sum'),
        Acierto_fav_mayor_calif_pct=('favorito_mayor_calif_gana', lambda x: 100 * x.sum() / x.count() if x.count() else None),
        Nº_fav_menor_calif=('favorito_menor_calif', 'sum'),
        Acierto_fav_menor_calif_pct=('favorito_menor_calif_gana', lambda x: 100 * x.sum() / x.count() if x.count() else None),
        Cuota_media_favorito=('cuota_favorito', 'mean'),
    ).reset_index()

    # Renombrar columnas para presentación
    resumen = resumen.rename(columns={
        "Nº_partidos": "Nº partidos",
        "Acierto_favorito_pct": "Acierto favorito (%)",
        "Nº_fav_mayor_calif": "Nº fav. mayor calif",
        "Acierto_fav_mayor_calif_pct": "Acierto favorito mayor calif (%)",
        "Nº_fav_menor_calif": "Nº fav. menor calif",
        "Acierto_fav_menor_calif_pct": "Acierto favorito menor calif (%)",
        "Cuota_media_favorito": "Cuota media favorito"
    })

    # Redondear para mejor presentación
    for col in ["Acierto favorito (%)", "Acierto favorito mayor calif (%)", "Acierto favorito menor calif (%)", "Cuota media favorito"]:
        resumen[col] = resumen[col].round(2)

    return resumen

if __name__ == "__main__":
    paso = 0.05
    print(f"Análisis objetivo con paso de overround: {paso}\n")
    df = analizar_favorito_odds_vs_overround(overround_step=paso)
    print(df)