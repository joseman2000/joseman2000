# La Tetería del Invernadero — Propuesta de diseño (Paso 2)

Estado: **PROPUESTA, pendiente de aprobación**. Todos los números salen de
`teteria/tools/sim*.py` (jugador codicioso: compra lo de mejor amortización,
~4 clics/s, sin contar el progreso offline). Son ajustables desde un único
fichero de configuración (`balance.js`) cuando se implemente.

---

## 1. Recurso y fórmulas base

| Concepto | Fórmula | Justificación |
|---|---|---|
| Recurso | **Hojas de té** | — |
| Clic | `1 × multClic + 1% de la PPS` (el 1% se desbloquea con una mejora) | El clic importa al principio y no se vuelve inútil al final. |
| Coste edificio | `coste_base × 1.15^n` (factor por edificio, 1.15 por defecto) | Estándar del género: crecimiento exponencial suave, cada compra se nota. |
| PPS | `Σ (n_i × pps_base_i × mejoras_i) × (1 + 0.01 × logros) × pasivas × modo` | Los multiplicadores se agrupan por capas; dentro de cada capa suman, entre capas multiplican, para que nada se dispare. |
| Mejoras de edificio | ×2 al tener 1, 10, 25, 50 y 100 unidades | Objetivos visibles; dan ritmo a la partida. |
| Logros | +1 % de producción global cada uno | Pequeño pero acumulable (~40 logros → +40 %). |

### Edificios (los 4 primeros entran en el Hito 1)

| # | Cozy | Marchito | Coste base | PPS base |
|---|---|---|---|---|
| 1 | Maceta de menta | Maceta reseca | 15 | 0.1 |
| 2 | Regadera | Regadera oxidada | 100 | 1 |
| 3 | Bancal de manzanilla | Bancal de ortigas | 1.1 K | 8 |
| 4 | Tetera de cobre | Tetera agrietada | 12 K | 47 |
| 5 | Invernadero de cristal | Invernadero roto | 130 K | 260 |
| 6 | Salón de té | Salón vacío | 1.4 M | 1 400 |
| 7 | Destilería de aromas | Alambique de hiel | 20 M | 7 800 |
| 8 | Árbol madre | Árbol hueco | 330 M | 44 000 |

Cada escalón cuesta ~10× más y produce ~6× más: el edificio nuevo siempre es
mejor por unidad, pero el anterior sigue siendo rentable un buen rato.

---

## 2. Renacer y Semillas

- **Semillas ganadas** = `floor( sqrt( hojas_totales_de_la_partida / 1 000 000 ) )`
  - 1 M → 1 · 25 M → 5 · 100 M → 10 · 10 000 M → 100.
  - La raíz da el rendimiento decreciente: el doble de Semillas exige el cuádruple de hojas.
- **El botón Renacer aparece** al alcanzar 1 M de hojas (≈ 40 min en la 1.ª partida),
  pero la UI recomienda esperar a ≥ 5 Semillas (≈ 95 min). Eso es el "medio-final".
- **Las Semillas se gastan** (no dan bono por tenerlas). Así el Marchitar es una
  decisión real: ahorrar o mejorar.

### Pasivas permanentes (coste = base × 1.5^nivel)

| Pasiva | Efecto por nivel | Coste base |
|---|---|---|
| Raíces profundas | +30 % de producción (suma) | 3 |
| Manos cálidas | +100 % de potencia de clic | 2 |
| Brote temprano | Empiezas con 10·nivel macetas y la mejora de 1 unidad | 5 |
| Siesta larga | Offline: +2 h de tope y +10 % de eficiencia | 4 |
| Memoria del jardín | Conservas la mejora ×2 de "1 unidad" de todos los edificios | 25 (único) |

**Por qué el coste ×1.5:** en la simulación, un bono lineal por Semilla hacía
que las partidas se aceleraran sin fin (la partida 20 daba 10¹⁰ Semillas). Con
coste geométrico, el multiplicador crece con el logaritmo de las Semillas y las
partidas se mantienen en 1–2,5 h.

---

## 3. El Marchitar

- **Coste: 150 Semillas** (se gastan). Como a la vez vas comprando pasivas,
  hace falta haber ganado ~250 en total → **unos 10 Renaceres**.
- **Multiplicadores de una partida Marchita**: producción **×2** y Semillas **×2**.
  - El ×2 nominal parece poco, pero los edificios se compran antes y el efecto se
    acumula. Resultado simulado en Semillas frente a cozy (misma duración):

| Cómo juegas la Marchita | Producción perdida por corrupción | Semillas vs. cozy |
|---|---|---|
| Bien (atento) | ~10 % | **×5,5** |
| Normal | ~25 % | **×4** |
| Mal / AFK | ~50 % | ×2 |

  Cae dentro del objetivo ×3–×5, y jugar mal sigue compensando un poco (no frustra).
  Con ×2,5 nominal salía ×6–×8: demasiado.

### Corrupción (valores iniciales)

| Parámetro | Valor | Motivo |
|---|---|---|
| Frecuencia | 1 evento cada 60–90 s (aleatorio) | ~1 decisión por minuto: activo pero no agobiante. |
| Simultáneos | máx. 1 los primeros 15 min, luego 2 | Aprendes la mecánica antes de tener que priorizar. |
| Objetivo | un tipo de edificio que tengas, con más peso cuanto más produce | Así hay que elegir qué salvar. |
| Aviso | **12 s** de "marchitándose": el edificio parpadea, su icono se oscurece + sonido de crujido | Tiempo de sobra para reaccionar sin mirar la pantalla fija. |
| Purificar a tiempo | **mantener pulsado 1,5 s**, sin coste; enfriamiento global de 8 s | Acción física clara; el enfriamiento crea prioridades cuando hay 2. |
| Si fallas | El edificio **deja de producir** y además **consume** hojas = 50 % de lo que produciría | Penalización visible pero limitada a un edificio. |
| Contagio | Tras 45 s corrompido, el edificio siguiente de la lista empieza su aviso | Castiga ignorar, no un fallo puntual. |
| Purificar un corrompido | mantener 3 s + coste = 30 s de tu PPS total | Siempre recuperable, nunca un callejón sin salida. |

**Mejoras de automatización (con un precio):**
- *Espantapájaros de ceniza*: purifica solo 1 aviso cada 40 s, pero −10 % de producción.
- *Campana de bronce*: +6 s de aviso, pero los eventos llegan un 15 % más a menudo.
- *Raíz negra*: los corrompidos no contagian, pero el bono de Semillas baja de ×2 a ×1,8.

### ⚠️ Decisión que necesito: corrupción con la pestaña cerrada / offline

**Recomiendo la opción A:**

- **A — Pausa total (recomendada).** Con la pestaña oculta o cerrada no aparece ni
  avanza ninguna corrupción. Lo que ya estaba corrompido sigue sin producir pero
  no contagia ni consume. La producción offline de una partida Marchita se cobra
  **sin el ×2** (eficiencia offline normal). Al volver hay 20 s de gracia antes del
  siguiente evento.
  *Por qué:* no castiga por cerrar el navegador, y quitar el ×2 offline evita que
  lo óptimo sea cerrar la pestaña. El modo Marchito premia la atención, offline no
  hay atención que premiar.
- B — Tope de daño: offline la corrupción sigue, pero con un máximo de 1 edificio
  corrompido y sin contagio; el ×2 se mantiene. Más "realista", pero vuelves y te
  encuentras un castigo que no pudiste evitar.
- C — Sin offline: una partida Marchita no genera nada fuera de la pestaña. Simple
  pero muy duro con el móvil.

**Offline en modo cozy:** 50 % de la PPS, tope de 8 h (ampliable con *Siesta larga*).

---

## 4. Tabla de ritmo esperado (simulado, juego activo, sin offline)

| Partida | Duración | Semillas ganadas | Total acumulado | Tiempo jugado acumulado | Renacer disponible desde |
|---|---|---|---|---|---|
| 1 | 95 min | 5 | 5 | 1,6 h | min 38 |
| 2 | 72 min | 5 | 10 | 2,8 h | min 29 |
| 3 | 58 min | 5 | 15 | 3,7 h | min 23 |
| 5 | 79 min | 11 | 33 | 6,1 h | min 19 |
| 7 | 95 min | 24 | 73 | 9,1 h | min 15 |
| 9 | 131 min | 54 | 163 | 13,1 h | min 12 |
| **10** | 154 min | 81 | **244 → Marchitar** | **~16 h** | min 10 |

- **Primer Renacer:** se puede a los ~40 min; lo razonable, a los ~95 min.
- **Hasta el Marchitar:** ~10 Renaceres, ~16 h de juego activo (bastante menos
  contando el progreso offline; con 8 h offline al 50 % por noche, unos 3–4 días).
- **Partida Marchita típica:** 45–90 min, y da 90–170 Semillas en lugar de 23–41
  (×4 jugando normal). Así el Marchitar se nota como un salto, no como un +10 %.

---

## 5. Técnica y forma de trabajar

- HTML + CSS + JavaScript sin dependencias (módulos ES); el Hito 6 añade un build
  estático listo para publicar (GitHub Pages / itch.io).
- Bucle a 10 ticks/s con delta de tiempo real; números grandes con formato
  (1,2 K / 3,4 M…), suficiente hasta 1e300 con `Number`.
- Guardado en `localStorage` cada 10 s y al cerrar, con versión de esquema y
  exportar/importar en texto.
- El código vive en `teteria/` (este repo es el de tu perfil de GitHub).

### Hito 1 — criterio de "hecho" comprobable
1. Abrir `teteria/index.html` muestra la tetera; clicar suma hojas.
2. 4 edificios comprables; el precio sube ×1.15 por unidad y la PPS se acumula en tiempo real.
3. ≥ 6 mejoras (clic y ×2 por edificio) que solo aparecen al cumplir su requisito.
4. Recargar la página conserva el estado (guardado automático + botón de borrar partida).
5. Test automático (Node) de las fórmulas de coste, PPS y guardado/carga: pasa.
