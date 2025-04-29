# Guía y Plantilla para Análisis Comparativo de Jugadores de Tenis de Mesa

---

## 1. Objetivos del Análisis

- Comparar el rendimiento histórico de dos jugadores en torneos.
- Identificar patrones, fortalezas y debilidades.
- Estimar probabilidades de victoria en un hipotético enfrentamiento.
- Generar insights accionables (ej: estrategias, rivales a evitar).

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
| Volatilidad (σ)       | Desviación estándar del delta (mide inconsistencia).   |
| Eficacia en Finales   | % de victorias en etapas decisivas (finales, semis).  |

### B. Desempeño contra Rivales

| Variable              | Descripción                                           |
|-----------------------|-------------------------------------------------------|
| Win Rate vs. [Rival]  | % de victorias contra oponentes específicos.          |
| Delta Promedio        | Cambio promedio en rating al enfrentarlos.            |

### C. Tendencias Temporales

- Rating a lo largo del tiempo (mejoras/descensos).
- Rachas de victorias/derrotas.
- Resultados en ligas específicas (ej: bajo rendimiento en ligas altas).

---

## 4. Proceso de Análisis

1. **Recopilación de Datos:** Organizar torneos, resultados y ratings en tablas.
2. **Cálculo de Variables Clave:** 
    - Win Rate total y por liga.
    - Volatilidad (σ) del delta.
    - Eficacia contra rivales comunes.
3. **Identificación de Patrones:**
    - Debilidades contra rivales específicos.
    - Consistencia en etapas clave (ej: finales).
4. **Estimación de Probabilidades:**
    - Usar historial directo (si existe).
    - Comparar desempeño en ligas similares.
    - Considerar volatilidad y rating actual.

---

## 5. Comparación Directa

Cuadro resumen comparando todas las estadísticas, patrones y probabilidades disponibles y analizadas.

| Variable                 | Jugador A        | Jugador B        |
|--------------------------|------------------|------------------|
| Rating Promedio          | 430-470          | 440-480          |
| Win Rate (450-500)       | 45%              | 58%              |
| Volatilidad (σ delta)    | Alta (18.7)      | Moderada (10.2)  |
| Eficacia vs [Rival Común]| 39%              | 63%              |
| ...                      | ...              | ...              |

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

## 7. Índice de Confianza en la Predicción (ICP)

### Instrucciones y Fórmula Mejorada para el ICP

**Objetivo:** Calcular un índice (entre 0 y 1) que refleje la confianza en la predicción de que un jugador (el "favorito del análisis") ganará el partido directo contra el rival, basándose en su historial directo y su rendimiento contra rivales comunes.

#### **Pasos para el cálculo:**

1. **Definir Jugadores y Periodo:**
    - Identifica claramente al **Jugador (Favorito Pronosticado)** y al **Jugador (Rival)**.
    - Define el **periodo de tiempo** de los datos a analizar (ej. últimos 6 meses, temporada actual).

2. **Calcular $W_{directos}$ (Win Rate Directo del Favorito):**
    - Reúne todos los partidos jugados **entre el Jugador Favorito y el Rival** en el periodo definido.
    - Calcula la tasa de victorias del Favorito en esos enfrentamientos:
        $$
        W_{directos} = \frac{\text{Victorias del Favorito}}{\text{Total de partidos directos}}
        $$

3. **Identificar Rivales Comunes:**
    - Haz una lista de todos los **oponentes únicos** contra los que jugó cada jugador.
    - Encuentra la **intersección** de ambas listas (los "rivales comunes").

4. **Calcular Win Rate del Favorito vs CADA Rival Común:**
    - Para **cada rival común**:
        - Busca todos los partidos del **Favorito contra ese rival común**.
        - Calcula la tasa de victorias del Favorito contra ese oponente:
            $$
            WinRate_{Favorito,RivalComún} = \frac{\text{Victorias del Favorito vs Rival Común}}{\text{Total partidos Favorito vs Rival Común}}
            $$
        - *Nota: Si no hay partidos del Favorito contra un rival común, excluye a ese rival del promedio.*

5. **Calcular $W_{comunes}$ (Win Rate Promedio del Favorito vs Rivales Comunes):**
    - **Promedio simple:**  
        $$
        W_{comunes,simple} = \frac{\sum WinRate_{Favorito,RivalComún}}{\text{Número de rivales comunes considerados}}
        $$
    - **Promedio ponderado (opcional):**  
        $$
        W_{comunes,ponderado} = \frac{\sum (\text{Cantidad de partidos Favorito vs Rival Común} \times WinRate_{Favorito,RivalComún})}{\text{Total de partidos contra rivales comunes}}
        $$

6. **Seleccionar Pesos ($w_1, w_2$):**
    - Asegúrate que $w_1 + w_2 = 1$.
    - **Valores sugeridos:** $w_1 = 0.55$ (directo), $w_2 = 0.45$ (comunes).

7. **Calcular ICP Final:**
    - Usa la fórmula de promedio ponderado:
        $$
        ICP = (w_1 \times W_{directos}) + (w_2 \times W_{comunes})
        $$

    - Se recomienda reportar ambos resultados:
        - ICP con $W_{comunes,simple}$
        - ICP con $W_{comunes,ponderado}$

8. **Interpretación:**
    - **0.0 - 0.4:** Confianza Baja
    - **0.4 - 0.7:** Confianza Media
    - **0.7 - 1.0:** Confianza Alta
    - Explica brevemente el resultado, los valores de cada componente y la cantidad de datos usados.

---

## 8. Conclusión

- Determina si hay un favorito leve o claro (según datos), y matiza según el ICP.
- **Índice de Confianza en la Predicción (ICP): [ ]** (_baja/media/alta_).
- _Recomendación: ..._

---

## 9. Formato de Entrega

- Markdown estructurado con el nombre de:  
  `Analisis_Comparativo_Jugador_Analizado_1_vs_Jugador_Analizado_2.md`

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