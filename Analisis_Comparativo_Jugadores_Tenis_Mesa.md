# Análisis Comparativo de Jugadores de Tenis de Mesa

## 1. Objetivos del Análisis

- Comparar el rendimiento histórico de **Strelec A** (Jugador 1) y **Uhlar R** (Jugador 2) en torneos.
- Identificar patrones, fortalezas y debilidades.
- Estimar probabilidades de victoria en un hipotético enfrentamiento directo.
- Generar insights accionables.

---

## 2. Recopilación de Datos

Ambos jugadores cuentan con un historial detallado de partidos en ligas 600-700 y 700-800, incluyendo finales, fases de grupo y enfrentamientos contra rivales comunes. Los datos incluyen fechas, rating inicial/final, deltas de rating, resultados por sets y rivales.

---

## 3. Cálculo de Variables Clave

### A. Estadísticas Generales

| Variable                      | Strelec A (Jugador 1) | Uhlar R (Jugador 2) |
|-------------------------------|-----------------------|---------------------|
| **Rating Promedio**           | 650–731               | 687–781             |
| **Rango de Rating**           | 622–731               | 687–781             |
| **Win Rate Total (%)**        | 60%                   | 62%                 |
| **Win Rate Liga 700-800**     | 36%                   | 48%                 |
| **Win Rate Liga 600-700**     | 70%                   | 74%                 |
| **Volatilidad (σ delta)**     | 10.7                  | 12.4                |
| **Eficacia en Finales**       | 47% (8/17 finales)    | 59% (10/17 finales) |

**Notas:**
- Los ratings y win rates son aproximados, calculados a partir de los resultados listados por torneo.
- La volatilidad se estima como la desviación estándar de los deltas por partido.

---

### B. Desempeño contra Rivales Comunes

#### Principales rivales comunes: Koczy R, Schwan Ja, Pavliska M, Chovanec P, Skacelik R, Jokiel P, Krupnik L jr.

| Rival         | J1: Win Rate / Delta Prom. | J2: Win Rate / Delta Prom. |
|---------------|---------------------------|----------------------------|
| Koczy R       | 38% / -0.4                | 57% / +2.6                 |
| Schwan Ja     | 67% / +2.0                | 50% / +0.8                 |
| Pavliska M    | 33% / -2.0                | 42% / -1.2                 |
| Chovanec P    | 0% / -9.5                 | 50% / -0.1                 |
| Skacelik R    | 60% / +4.0                | 35% / -3.2                 |
| Jokiel P      | 25% / -5.8                | 44% / -0.2                 |
| Krupnik L jr. | 66% / +2.5                | 62% / +2.1                 |

---

### C. Tendencias Temporales

- **Ambos muestran crecimiento en rating con altibajos; Uhlar R tiene mayor rating de pico y menor caída prolongada.**
- **Strelec A** destaca en ligas 600-700, pero sufre en 700-800 (win rate bajo y caídas de rating).
- **Uhlar R** es más consistente en 700-800 aunque tiene rachas negativas en fases finales de algunos torneos.
- **Rachas de victorias:** Ambos han tenido rachas de 4+ victorias consecutivas en ligas medias.
- **Rendimiento en finales:** Uhlar R es más eficaz.

---

## 4. Identificación de Patrones

- **Strelec A**: Fuerte en fases de grupo, baja eficacia en finales y contra rivales de rating similar o mayor. Mayor volatilidad en ligas altas.
- **Uhlar R**: Mejor adaptación a ligas altas, mejor eficacia en finales, más victorias contra rivales comunes clave.

---

## 5. Comparación Directa (Resumen)

| Variable                      | Strelec A (J1)         | Uhlar R (J2)          |
|-------------------------------|------------------------|-----------------------|
| Rating Promedio               | 650–731                | 687–781               |
| Win Rate Total                | 60%                    | 62%                   |
| Win Rate Liga 700-800         | 36%                    | 48%                   |
| Volatilidad (σ delta)         | 10.7                    | 12.4                  |
| Eficacia en Finales           | 47%                     | 59%                   |
| Win Rate vs. Koczy R          | 38%                     | 57%                   |
| Win Rate vs. Pavliska M       | 33%                     | 42%                   |
| Win Rate vs. Krupnik L jr.    | 66%                     | 62%                   |
| Tendencia Últimos Torneos     | Descendente             | Estable/Ascendente    |

---

## 6. Estimación de Enfrentamiento Directo

**Probabilidades de Victoria (estimadas):**
- **Strelec A:** 43%
- **Uhlar R:** 57%

**Resultado más probable:**  
- **3-2 a favor de Uhlar R** (partido cerrado, ventaja ligera para Uhlar por rating y eficacia en finales).

---

## 7. Índice de Confianza en la Predicción (ICP)

**Cálculo:**
- **Partidos directos**: 1 (victoria de Uhlar R el 27 Feb 2025, 3-1 y 3-0) → P_directos = 2/2 = 1.0
- **Win rate directos (favorito):** 2/2 = 1.0
- **Partidos contra rivales comunes**: 7 principales rivales (ver tabla)
- **Concordancia resultados comunes**: 5/7 (Uhlar R mejor en 5 de 7 comparaciones) = 0.71
- **Peso correctivo (\(\alpha\))**: 0.5

\[
ICP = (1.0 \times 1.0) + 0.5 \times (1.0 \times 0.71) = 1.0 + 0.355 = 1.36
\]

**Interpretación:**  
- **ICP ≈ 1.36** (alta confianza)  
- _Motivo: Hay partidos directos recientes, concordancia en rivales comunes y consistencia general en los datos._

---

## 8. Conclusión

- **Uhlar R** es el favorito claro, especialmente en ligas altas y finales, con mejor desempeño directo y ante rivales comunes.
- **Índice de Confianza en la Predicción (ICP): 1.36** (alta).
- **Recomendación:** Apostar a favor de Uhlar R en partidos importantes; Strelec A es competitivo pero menos confiable en etapas decisivas y ante rivales fuertes.

---

## 9. Formato de Entrega

_Estructurado en Markdown, tablas comparativas y justificación de cada paso y conclusión. Para análisis futuros, actualizar los datos con nuevos torneos y recalcular métricas clave._
