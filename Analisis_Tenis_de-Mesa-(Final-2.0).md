# Guía y Plantilla para Análisis Comparativo de Jugadores de Tenis de Mesa

---

## 1. Objetivos del Análisis

- Comparar el rendimiento histórico de dos jugadores en torneos.
- Identificar patrones, fortalezas y debilidades.
- Estimar probabilidades de victoria en un hipotético enfrentamiento.
- Generar insights accionables (ej: estrategias, rivales a evitar).
- Garantizar y Forzar el analisis del Jugador 1 y Jugador 2 por separado, para asi garantizar y mejorar el analisis del historial de cada uno, en pocas palabra analisa y evalua primero el historiar del jugador 1 y luego haz lo mismo con el jugador 2
---

## 2. Datos Requeridos

Para cada jugador, se necesita (esta información se encuentra en los archivos de texto adjuntados):

- **Historial de Torneos:**
  - Fechas, nombres de torneos y ligas (ej: *A14, league 450-500*).
  - Resultados de partidos (sets y puntos por set).
  - Rating inicial/final en cada torneo.
  - Delta (cambio en el rating por partido y torneo).
  - Rivales comunes: Jugadores a los que ambos se hayan enfrentado.

---

## 3. Variables Clave a Analizar

### A. Estadísticas Generales

| Variable              | Descripción                                           |
|-----------------------|-------------------------------------------------------|
| Rating Promedio       | Rango de rating del jugador en el período.            |
| Win Rate Total        | % de partidos ganados en todas las ligas.             |
| Win Rate por Liga     | % de victorias en rangos específicos (ej: 450-500).   |
| Volatilidad (s)       | Desviación estándar del delta (mide inconsistencia).   |
| Eficacia en Finales   | % de victorias en etapas decisivas (finales, semis).  |

### B. Desempeño contra Rivales

| Variable              | Descripción                                           |
|-----------------------|-------------------------------------------------------|
| Win Rate vs. [Rival]  | % de victorias contra oponentes específicos.          |
| Delta Promedio        | Cambio promedio en rating al enfrentarlos.            |

### C. Tendencias Temporales

- Rating a lo largo del tiempo (mejoras/descensos).
- Rachas de victorias/derrotas.
- Mejor racha positiva	+30.9	+34
- Peor racha negativa
- Resultados en ligas específicas (ej: bajo rendimiento en ligas altas).

---

## 4. Proceso de Análisis

1. **Recopilación de Datos:** Organizar torneos, resultados y ratings en tablas.

2. **Cálculo de Variables Clave:** 
    - Win Rate total y por liga.
    - Volatilidad (s) del delta.
    - Eficacia contra rivales comunes.

3. **Identificación de Patrones:**
    - Debilidades contra rivales específicos.
    - Consistencia en etapas clave (ej: finales).

4. **Ajustes Basados en Lecciones de Predicciones Fallidas**
   
   Antes de emitir la estimación de probabilidades y la predicción final, aplicar los siguientes criterios de ajuste (alertas):

   - **Consistencia (Volatilidad):**
     - Dar mayor peso a la estabilidad del jugador (menor volatilidad) especialmente cuando las diferencias de win rate o rating son pequeñas.
     - Si el jugador con mejor rating/promedio es mucho más volátil, considerar que la ventaja puede estar sobreestimada.
   
   - **Predicciones Ajustadas (51-49%, 55-45%):**
     - Si la predicción es muy ajustada, considerar el enfrentamiento como de pronóstico reservado.
     - Revisar si alguno de los jugadores es más consistente: favorecer levemente al más estable.
   
   - **Historial Directo y Volatilidad:**
     - Si el H2H (head-to-head) es parejo pero uno es mucho más estable, dar preferencia al consistente.
     - Si el H2H favorable corresponde a partidos antiguos o en periodos de alta volatilidad, ponderar menos ese dato.
   
   - **Momentum vs. Nivel Base:**
     - No sobrevalorar el momentum corto si el rival tiene mejor rendimiento a largo plazo y mayor estabilidad.
   
   - **Dependencia del Rango de Liga:**
     - Si el alto win rate de un jugador se da en ligas más bajas, y sufre mucho en ligas superiores (donde enfrenta al rival), ajustar a la baja su probabilidad real.

   - **Factores No Cuantificables:**
     - Reconocer que siempre habrá upsets y variables fuera del modelo (estilo de juego, día, mentalidad, lesiones, etc.). No confiar ciegamente en diferencias pequeñas de probabilidad.

---

5. **Estimación de Probabilidades (Ajustada):**
   - Aplicar todos los criterios anteriores para ajustar la predicción matemática original.
   - Si la predicción ajustada cambia el favorito, explicar el porqué (consistencia, H2H contextualizado, etc.).
   - Ejemplo de tabla y explicación.

---

## 5. Comparación Directa

Ejemplo Cuadro resumen comparando todas las estadísticas, patrones y probabilidades disponibles y analizadas.

## 6. Comparación Directa (Garantizar formato numerico y porcentajes donde corresponda cumplinedo con el formato del siguiente cuadro de ejemplo)

| Variable                   | **Horak D**             | **Darin K**                |
|----------------------------|-------------------------|----------------------------|
| Rating promedio            | 552                     | 574                        |
| Rango de rating            | 524-579                 | 513-629                    |
| Win Rate Total             | 56%                     | 59%                        |
| Win Rate (500-550)         | 70%                     | 76%                        |
| Win Rate (550-600)         | 53%                     | 59%                        |
| Win Rate (600-700)         | 0% (pocas muestras)     | 47%                        |
| **Volatilidad (s delta)**  | 8.2 (estable)           | 13.8 (más inestable)       |
| **Momentum actual**        | Ligera baja reciente    | Subida estable             |
| **Finales ganadas (%)**    | 44%                     | 53%                        |
| **3er puesto (%)**         | 50%                     | 47%                        |
| **Rivales Top (>700)**     | win 10% (Derrotas frecuentes)|win 15% (Derrotas frecuentes)|
| **Rivales Medios (<700)**  | win 40% Equilibrado     | win 45% Ligera ventaja             |
| **Tendencia**              | Descendente             | Estable/ligero descenso en 800+ |
| **Rachas**                 | Altamente variable      | Consistente                |
| Vs Prokupek Ja             | 40% win, -Δ             | 30% win, -Δ                |
| Vs Belovsky Jo             | 58% win, +Δ             | 43% win, ≈Δ                |
| Delta promedio vs Rivales  | +0.5                    | -0.5                       |
| Evolución rating 2025      | ↑ hasta mar, ↓          | ↑ hasta feb, ↓             |
---

## 6. Estimación de Enfrentamiento Directo

Probabilidades de Victoria Basadas en:
- Historial directo
- Win Rate en ligas equivalentes
- Volatilidad (jugadores inconsistentes son menos predecibles)
- Generar la probabilidad de ganar en porcentaje de cada jugador si llegaran a tener un cara a cara

**Predicción de Sets/Puntos:**
- Sets más probables (ej: 3-1, 3-2)
- Puntos totales estimados (basados en promedio de puntos por set)

Ejemplo:
- **Probabilidad de victoria:**  
  - Jugador 1: [ ]%  
  - Jugador 2: [ ]%
- **Resultado más probable:** [ ]

---

## 7. Concluciones Basado en rendimiento, forma y momentum de cada jugador

---

## 8. Formato de Entrega

- Markdown estructurado con el nombre de:  
  `Analisis_Comparativo_Nombre_Jugador_1_vs_Nombre_Jugador_2.md

---

## Anexo: Instrucciones para Identificación y Conteo Correcto de Partidos

### Estructura de los Historiales

- **Cada bloque de torneo** comienza con una línea que indica la fecha, el nombre del torneo y la liga.
- **Dentro de cada torneo**, hay una subsección encabezada por la palabra `"Opponent"`.
- **Debajo de "Opponent"**, aparece una lista de líneas, cada una correspondiente a **un partido** jugado por el jugador analizado en ese torneo.

### Formato de cada línea de partido

```
[Hora] [Etapa] [Nombre del oponente] [?] [Rating del oponente] [Resultado] [Puntuación por set] [Delta]
Ejemplo:
02:30  gr  Fojt P  ?  724  1 : 3  14-16 8-11 11-5 8-11  -6.3
```

### Principio Fundamental para el Conteo

- **Cada línea bajo "Opponent" corresponde exactamente a UN partido individual.**
- **Para obtener el total de partidos jugados por el jugador en el historial:**
  - Sumar el número total de líneas bajo todas las secciones "Opponent" en todos los torneos.
- **Para identificar partidos contra un rival específico:**
  - Contar todas las líneas donde el nombre del oponente coincide exactamente con el rival buscado.
- **Para cualquier estadística o análisis avanzado (win rate por liga, progresión, rendimiento en finales, etc.):**
  - SIEMPRE utilizar la información de torneo, liga y etapa proveniente del encabezado de cada bloque y de cada línea de partido.
  - Agrupar, segmentar o filtrar según liga, rango, torneo, etapa o periodo cuando el análisis lo requiera.

---

_Seguir estrictamente estas instrucciones garantiza un conteo preciso de partidos y análisis avanzados con segmentación correcta por torneo, liga o etapa._
