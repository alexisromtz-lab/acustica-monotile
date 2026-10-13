# WHITEPAPER — ESQUELETO Y BORRADOR DE SECCIONES

- **Título de trabajo:** *Bounds on Wave Transport in Aperiodic Hat Monotile Tilings: A Bit-Reproducible Dual Acoustic-Photonic FDTD Benchmark*
- **Fecha de escritura:** 2026-10-13 (UTC).
- **Casa que escribe:** `acustica-monotile` (rama `main`, HEAD `92abcfc`).
- **Acto:** `Frente 2 del ARC 5 — esqueleto del whitepaper corto (4 a 6 páginas)`.
- **Estado:** `ESQUELETO · BORRADOR DE SECCIONES · NO ENVIADO`.
- **Extensión objetivo:** 4 a 6 páginas a dos columnas (aprox. 2 400 a 3 600 palabras de cuerpo).
- **Formato elegido:** Markdown como fuente de trabajo + plantilla LaTeX a **dos columnas** (bloque en §VIII). La elección se declara: Markdown para pre-registro y revisión, LaTeX para el PDF indexable.

**UNIVERSO DECLARADO:** los artefactos sellados de `alexisromtz-lab/acustica-monotile` (HEAD de trabajo `92abcfc`) y de `alexisromtz-lab/fotonica-monotile` (reposo absoluto `14bc745`), en su versión depositada `v0.1.0`.
**MOTOR:** lectura de artefactos, **sin re-ejecución**. Las cifras del enlace se leen del crudo `crudos/crudo_ENLACE_ACUSTICA_FOTONICA_20261012T204809Z.json`; las del instrumento fotónico, del `PREREGISTRO_INSTRUMENTO_FDTD_20261012.md` y de los crudos de `crudos/`.
**UNIDAD:** valor por bin (29 bins) para el vector; celda para el conteo de malla; 1 realización = 1 corrida.
**VENTANA:** la de cada crudo, impresa en su cabecera.

> **REGLA DE ESTE ESQUELETO.** Ninguna cifra de este archivo se deriva de nuevo: cada una se cita con su artefacto, su unidad y su ventana. Lo que **no** está medido aparece marcado `PENDIENTE DECLARADO` con su condición de entrada. Se **declara**; no se adjudica.
>
> **Nota de edición (regla dura del entorno):** este archivo no contiene signos monetarios. Las fórmulas usan los delimitadores `\( \)` y `\[ \]`, nunca el par de signos de dólar, por la regla de sustitución vigente.

---

## 0. Cómo se usa este archivo

1. **§I a §VI** son los seis bloques del paper. Cada uno trae: objetivo, material medido, y qué falta.
2. **§VII** es la tabla de trazabilidad: figura, valor, instrumento, artefacto, ventana. Ninguna cifra entra al paper sin renglón aquí.
3. **§VIII** trae la plantilla LaTeX y los comandos.
4. Marca `PENDIENTE DECLARADO` = no medido, con condición de entrada escrita. **No se rellena con prosa.**

### 0.1 Comandos ya ejecutados para este frente (registro)

**Topics de GitHub** (motor `gh 2.96.0`, cuenta `alexisromtz-lab`; ventana medida `2026-10-13T04:56:17Z` a `04:56:23Z`; verificados por relectura, `n = 6` en cada repositorio):

```sh
gh repo edit alexisromtz-lab/acustica-monotile \
  --add-topic fdtd --add-topic acoustics --add-topic einstein-monotile \
  --add-topic aperiodic-tiling --add-topic reproducible-research --add-topic wave-propagation

gh repo edit alexisromtz-lab/fotonica-monotile \
  --add-topic fdtd --add-topic photonics --add-topic einstein-monotile \
  --add-topic electromagnetics --add-topic reproducible-research --add-topic bandgap-analysis

# relectura (la escritura se verifica leyendo, nunca con el mensaje de exito)
gh api repos/alexisromtz-lab/acustica-monotile/topics --jq '.names|join(",")'
gh api repos/alexisromtz-lab/fotonica-monotile/topics --jq '.names|join(",")'
```

Medido: `acustica-monotile` = `acoustics,aperiodic-tiling,fdtd,einstein-monotile,reproducible-research,wave-propagation` · `fotonica-monotile` = `bandgap-analysis,einstein-monotile,electromagnetics,fdtd,photonics,reproducible-research`.

### 0.2 Pre-vuelo A2.1 de este archivo (turno 1)

```sh
bash /Users/marlene/platino-labs/tools/gate_pre_escritura.sh \
  /Users/marlene/acustica-monotile/WHITEPAPER_ESQUELETO_20261013.md \
  AUSENTE WHITEPAPER-ESQUELETO-MONOTILE-20261013 0
```

Medido a `2026-10-13T05:09:42Z`: `RC = 10` (`COLISION: ... no existe`). Lectura declarada: para una **creación**, el gate autoriza **por ausencia** — `RC = 10` es la prueba de que la fila **no** existe todavía, y `RC = 11` sería la colisión. `RC = 0` es inalcanzable antes de crear y antes de registrar (ver §III.3).

---

## I. Introducción y Problema

- **Objetivo.** Plantear si la aperiodicidad **determinista** (sin desorden estocástico) produce transporte anómalo, o si la dispersión observada se explica por el **empaquetamiento estadístico** de las realizaciones.
- **El objeto.** El monotilo de Hat (Smith y colaboradores): tesela única que cubre el plano de forma aperiódica, sin desorden aleatorio. Contrasta con el desorden estocástico clásico: aquí no hay distribuciones, hay una regla.
- **La conjetura a batir.** Que la aperiodicidad pura abra una firma de transporte distinguible en transmisión.
- **Estado medido al escribir.**
  - En el lado fotónico, el acto de contraste sellado (`crudos/crudo_acto3_20261012T205230Z.json`, `t_utc = 2026-10-12T20:52:30Z`, `acto = 3.2`, `rc = 0`) devuelve `NEGATIVO / NULO SOSTENIDO`: la hipótesis **queda refutada en ese régimen de contraste**. Se publica como **resultado, no como fracaso**.
  - Criterio declarado en el propio crudo: `k_sigma = 3.0`, `riz_T_C1 = 0.05`, `bins_consecutivos = 3`.
  - Reparto medido del criterio: **28 de 29** bins cumplen la banda; **1** no. El que no cumple es el **borde inferior** de la ventana, con `T_U1 = 1.993564`, media `T_U2 = 0.408862`, `sigma_U2 = 0.265708`, `|diferencia| = 1.584702` contra `banda = 0.847124`.
  - El propio crudo marca ese bin: `cumple = [True, False x 28]`, `rachas = [[0, 0]]`, `racha_mas_larga = 1`. Como el criterio exige **3 bins consecutivos** y hay **1**, el veredicto sellado **se sostiene**.
  - En el lado acústico del enlace bilateral, el vector oficial da **7 `DISCREPA` / 22 `NULO`** sobre **29** bins (ver §IV).
- **Tesis del paper (una sola frase, a cerrar en redacción).** El transporte en el monotilo de Hat, a este contraste, **no** se distingue del que produce un empaquetamiento aperiodizado equivalente: lo que manda es la dispersión de la realización, no una anomalía de transporte.
- **Qué falta.** Cita bibliográfica externa del monotilo de Hat y del estado del arte en transporte en teselados aperiódicos. `PENDIENTE DECLARADO`: no hay bibliografía medida dentro de estos dos repositorios; se incorpora **sólo** con verificación externa previa.
- **Presupuesto:** 0.75 página.

---

## II. Formulación Numérica y Complejo Dual

- **Objetivo.** Fijar el complejo de dos solucionadores sobre la **misma geometría**, para que la comparación entre polarizaciones físicas (acústica y electromagnética) sea un cambio de operador con el objeto geométrico controlado.

### II.1 Instrumento fotónico (la pieza fuente)

Declarado en `PREREGISTRO_INSTRUMENTO_FDTD_20261012.md`, sellado a `T_UTC 2026-10-12T05:49Z`:

| Pieza | Valor declarado |
|---|---|
| Esquema | Yee 2D, polarización TM (`Ez`, `Hx`, `Hy`) |
| Paso de malla | `dx = dy = a/16` |
| Número de Courant | `S = 0.5` (estabilidad 2D) |
| Frontera absorbente | esponja de 20 celdas por borde, perfil `borde^3`, `alfa = 0.30` |
| Fuente | gaussiana, `sigma = 0.5 a/c`, retardo `t0 = 3 sigma` |
| Sondas | absolutas en `d = 8a` y `d = 16a` |
| Ventana de frecuencias | `nu` en `[0.15, 0.55]` c/a |
| Sub-corridas | **C1a** cuasi-1D (`ny = 1`, esponja sólo en x) y **C1b** 2D real (`ny = nx`, esponja en los cuatro bordes) |

### II.2 Instrumento acústico (el consumo del enlace)

Universo del crudo del enlace: `T(nu)` del solver `sim/sim_acustica2d.py` (blob `4de2c841e0d6e6b2757c371ef5cca1e4661b646b`, commit `f29879b`) a `L = 24.0 a`, modo `C1b`, con máscara de `data/geometria_hat/` (commit `b498fcf`), **más** el mismo `T(nu)` sin máscara (control nulo homogéneo).

Parámetros medidos del crudo: `n = 384`, `nt/nx/ny = 2304/384/384`, `modo = C1b`, `L_a = 24.0`, realizaciones `u1` + `u2_semilla_{101..105}`.

### II.3 Acoplamiento: la convención es un objeto, no un detalle

La máscara se **transpone al cargar** (el vecino `malla_hat.py` indexa fila = `y`, columna = `x`; este solver indexa eje 0 = `x`, eje 1 = `y`). Medido en el control de convención del crudo: con la máscara transpuesta, `T_U1 identico = False` y el reparto pasa a **11/29 `DISCREPA`** frente a los **7/29** oficiales. La convención **sí mueve el vector**: no es un no-op.

### II.4 Invariantes que el solver imprime

En las **6** corridas declaradas: `es_heterogeneo = True`, `identidad_inv_eps_igual_a_K = True`, `identidad_inv_mu_igual_a_uno = True`, `K` en `[0.25, 1.0]`, `inv_eps` en `[0.25, 1.0]`. El contraste constitutivo es `eps_mat 4` sobre `eps_0 1`.

- **Qué falta (declarado).** La **condición de frontera del solver acústico** no se re-deriva en este esqueleto: se lee de `sim/sim_acustica2d.py` al redactar y se declara su naturaleza exacta (la pieza fotónica usa esponja; **no** se afirma que la acústica use PML). `PENDIENTE DECLARADO`.
- **Qué falta (declarado).** El orden de convergencia espacial del solver acústico: `PENDIENTE DECLARADO` (ver §III.4).
- **Presupuesto:** 1 página (incluye una tabla de parámetros y una figura de la malla).

---

## III. Protocolo de Reproducibilidad A2.1

- **Objetivo.** Que la reproducibilidad sea **propiedad medida**, no reclamo: pre-registro cerrado antes de mirar la salida, control de no-regresión bit a bit, y declaración explícita de lo que el arnés **no** puede certificar.

### III.1 Pre-registro cerrado

El instrumento fotónico se declaró **antes** de correrlo: `PREREGISTRO_INSTRUMENTO_FDTD_20261012.md`, sellado a `T_UTC 2026-10-12T05:49Z`, con cuatro criterios y su umbral (l.195–198). Veredicto medido del acto 1, gen 6:

| Criterio | Umbral | Veredicto | Valores impresos |
|---|---|---|---|
| Q1 | `riz <= 0.05` en C1a y C1b | VERDE | `[C1a 0.005394 · C1b 0.005523]` |
| Q2 | `delta = max_nu abs(ln A(36a) − ln A(24a)) <= 0.05` | VERDE | `[0.004548 · 0.006001]` |
| Q3 | `A(16a)/A(8a) = 0.7071 ± 0.05` en C1b; `1.000` en C1a | VERDE | `[C1a/24a 0.999907 · C1a/36a 1.000055 · C1b/24a 0.707449 · C1b/36a 0.707223]` |
| Q4 | `max abs(error de fase medido) <= 3 · max abs(error de Yee)` | VERDE | `fase medida 1.405e-03 <= 3 x Yee 1.463133e-03 = 4.389e-03` (rama `m = 1`) |

Con Q1..Q4 en verde, la condición de entrada al acto 2 del pre-registro queda **cumplida** (habilitado, no corrido). En el lado acústico, el pre-registro equivalente es `PREREGISTRO_ACUSTICA_MONOTILE_20261012.md` (blob `075a05b425e182cf9f5a54edbc86af60e9e13f85`).

### III.2 Regresión C1 bit a bit

Sección de control instrumental **dentro** del acta de cierre (§4), no un archivo aparte. El camino **sin** máscara (`C1b`, `L = 24.0 a`) se compara contra el crudo `C1` sellado, sobre los **29** bins. Ventana de la corrida sellada: `2026-10-12T21:33:50Z` a `21:33:54Z`.

| Prueba | Medida |
|---|---|
| `filas` / `fila_match` | 4 / 1 |
| `len_ref` / `len_new` | 29 / 29 |
| `array_equal` | **True** |
| `max_abs_dif` | **0.0** (bit a bit) |
| `T_media` | 0.707449275919397 |
| `T_teorico` (`sqrt(0.5)`) | 0.7071067811865476 |
| `T_riz` | 0.0055232256865284102 |
| `piso_medido_C1` del crudo | 0.00552322568652841 |
| `es_heterogeneo` | **False** |
| `fraccion_mascara_union` | `None` |
| `nt / nx / ny` | 2304 / 384 / 384 |

Lectura: `T_riz` **es exactamente** el `piso_medido_C1` del propio instrumento en su configuración homogénea. El piso **no** es un número heredado por prosa: es la cifra de ruido del instrumento. Y el camino sin máscara **no cambió un bit**.

**Trampa de metro declarada y cerrada.** La cifra `0.004258596071401777` **no** es un `riz`: su casa medida es `T_desv_max` / `T_desv_max_por_modo`, la **desviación máxima de `T`**, otra cantidad. Llamarla «riz máximo» era un defecto de **nombre**, no de cifra.

### III.3 El arnés de pre-escritura A2.1 y su límite medido

`tools/gate_pre_escritura.sh TARGET BLOB_PRE HUELLA [LINEAS_PRE]`, con tupla de destino obligatoria (orden sin los cuatro parámetros = rechazo por defecto de contrato). Códigos: `0` pre-vuelo OK · `10` el objeto no existe · `11` la huella ya habita en el destino (colisión: la fila **ya está escrita**) · `12` blob distinto al contrato (árbol en movimiento) · `13` estado sucio en git · `14` el destino no vive en un árbol git (fail-closed) · `15` líneas distintas al contrato · `20` tupla incompleta.

**Límite medido y declarado:** `RC = 0` exige **existe + blob del contrato + árbol limpio en ese camino**. Para una **creación** es inalcanzable antes de crear y antes de registrar. Consecuencia operativa: en creación, el gate autoriza **por ausencia** (`RC = 10` es la prueba de que la fila no existe; `RC = 11` sería la colisión). Medido en este archivo: `RC = 10` a `2026-10-13T05:09:42Z`.

### III.4 Escalera de mallas y orden `p = 2`

- **Declarado:** el esquema Yee es de **orden 2** en espacio; paso `dx = dy = a/16`; Courant `S = 0.5`. Es **declaración de esquema**, no medición de orden.
- **Medido (dos peldaños de consistencia):** Q2 y Q3 de §III.1, sobre dos distancias de sonda (`8a`, `16a`) y dos ventanas de decaimiento (`24a`, `36a`). Los cuatro números salen en verde con margen amplio.
- **`PENDIENTE DECLARADO` (tercer peldaño).** Medir el orden efectivo con una malla más fina: paso `dx' = a/32`, `S = 0.5`, las mismas sondas, y calcular `p = log2(razón de errores)`. **No ejecutado, no medido.** No se escribe un `p` medido sin esa corrida.

### III.5 Regla de cifras (D22) aplicada al propio paper

Ninguna cifra entra al texto sin **denominador declarado** y **comando que la respalde**. Un nombre con dos denominadores se imprime **el par**: no se elige y no se promedia. Consecuencia ya pagada: el **`1.7 %` queda PURGADO** del registro (ver §IV.4).

- **Presupuesto:** 1 página.

---

## IV. Resultados Experimentales

- **Objetivo.** Reportar el vector bilateral y, sobre todo, **de qué está hecho su umbral**.

### IV.1 Vector oficial del enlace

Regla pre-declarada, leída del crudo (no re-tecleada):

\[ \Delta T(\nu) = | T_{U1}(\nu) - \overline{T_{U2}}(\nu) | - (\, 3.0 \cdot \sigma_{U2}(\nu) + \text{piso} \,) \]

con `ddof_sigma = 1`, `factor = 3.0`, `piso_contrato = 0.005523`, `piso_medido_C1 = 0.00552322568652841`. Regla por bin: `DeltaT > 0` da `DISCREPA`; `DeltaT <= 0` da `NULO`.

Rejilla: `n_bins = 29`, de `nu = 0.1527114967462039` a `nu = 0.5414316702819957` c/a; `nu_iguales_en_todas_las_corridas = True` (la rejilla **no** es una variable del contraste).

| clase | n |
|---|---|
| `DISCREPA` | **7** |
| `NULO` | **22** |
| total | 29 |

Clases presentes medidas: `['DISCREPA', 'NULO']`. **No hay tercera clase.**

### IV.2 Los 7 bins `DISCREPA`

| i | nu | DeltaT |
|---|---|---|
| 0 | 0.152711 | 7.119200e-01 |
| 1 | 0.166594 | 7.589031e-01 |
| 3 | 0.194360 | 8.292833e-01 |
| 7 | 0.249892 | 1.041554e-01 |
| 14 | 0.347072 | 5.113464e-03 |
| 16 | 0.374837 | 3.497564e-01 |
| 24 | 0.485900 | 1.569740e+00 |

Extremos del vector: `delta_T_max = 1.5697403560585752` en `nu = 0.48590021691973967` (bin 24, `DISCREPA`); `delta_T_min = -3.805628370974314` en `nu = 0.5414316702819957` (bin 28, `NULO`), con `abs(delta_T_min) = 3.805628e+00` y `rango_T_U2_max = 3.4677075111160995` **en el mismo bin**. El bin del mínimo **no** es el del máximo, y caen en extremos opuestos del veredicto: **el vector no es monótono en `nu`**. Se imprime el par; **no** se elige cuál describe el enlace.

### IV.3 De qué está hecho el umbral (el resultado que ordena el paper)

| cantidad | min | max |
|---|---|---|
| `sigma_U2_ddof1` (29 valores) | 1.073493e+00 | 1.440030e+00 |
| `umbral = 3 sigma_U2 + piso` | 3.275710e-01 | 4.325612e+00 |
| aportación del piso | — | `piso / umbral_max = 1.27687e-03` |
| aportación de `3 sigma_U2` | 0.983139 | 0.998723 |
| `piso` | 0.00552322568652841 | 0.00552322568652841 |

**Lectura declarada.** Un `NULO` significa «cae por debajo de `3 sigma_U2 + piso`», **no** «los dos universos coinciden». Los 22 `NULO` **no** son prueba de física compartida: son compatibilidad con un denominador **dominado por la dispersión estadística del empaquetamiento**. El nulo es una **cota acotada a su propio denominador**. Se **declara**; no se recalibra.

### IV.4 Dos denominadores separados (D22) — **no se funden**

| objeto | vía | valor |
|---|---|---|
| **A** — delta de rasterizado en U1 | `suma_areas_analitico` | 0.4038327588420457 |
| **A** — delta de rasterizado en U1 | `cobertura_union_U1` (media de la máscara binaria) | 0.4036797417534722 |
| **A** — delta | — | **1.530e-04** |
| **B** — salto de cobertura U1 a U2 | U1 | 0.4036797417534722 |
| **B** — salto de cobertura U1 a U2 | U2 (`101..105`) | 0.3824734157986111 a 0.3850843641493056 |
| **B** — salto | — | **aprox. 0.02 (2 pp)** |

Los dos números de **A** son **verdaderos** y miden **objetos distintos** (suma de áreas de la geometría contra promedio de celdas de la máscara binaria): son **hermanos, no fusionables**. **A** y **B** tampoco se suman. Un porcentaje único que los mezcle reintroduce el defecto: **el `1.7 %` queda PURGADO del registro**.

### IV.5 Controles del crudo (leídos del mismo crudo, no re-ejecutados)

| control | valor | lectura |
|---|---|---|
| `control_ddof0_n_discrepa` | **8** | con `ddof = 0` el reparto cambia de 7 a 8 |
| `control_piso_medido_n_discrepa` | **7** | con el piso **medido** en vez del de contrato: igual |
| `control_convencion` (máscara transpuesta) | `T_U1 identico = False` | 11/29 `DISCREPA` — la convención **sí** mueve el vector |
| `nu_iguales_en_todas_las_corridas` | `True` | la rejilla no es una variable del contraste |

El control `ddof` da **8** contra el oficial **7**: los dos se imprimen; **no se adjudica** cuál es el bueno. Se declara que el reparto depende del estimador de `sigma_U2`, y que `ddof = 1` se fijó **antes** de medir.

### IV.6 Fracción de máscara por realización

| realización | `fraccion_mascara_union` |
|---|---|
| `u1` | 0.4036797417534722 |
| `u2_semilla_101` | 0.3824734157986111 |
| `u2_semilla_102` | 0.3850843641493056 |
| `u2_semilla_103` | 0.3834771050347222 |
| `u2_semilla_104` | 0.3846367730034722 |
| `u2_semilla_105` | 0.38299560546875 |

### IV.7 Evidencia de que manda el empaquetamiento

Cadena medida, sin causalidad añadida: el umbral lo domina `3 sigma_U2` (aporte `0.983139` a `0.998723`); el piso aporta `1.27687e-03`; los `NULO` son compatibilidad con ese denominador; y la única realización geométricamente distinta (`u1`) es la que produce las discrepancias de borde. **Enunciado admitido estrictamente:** *«Correlacionadas con Delta f aprox. 2 pp y no adjudicables exclusivamente a orden aperiódico»*.

**Toda afirmación causal del tipo «artefacto por solape» queda PURGADA.** En este repositorio **no hay sonda instrumental** que la mida, y una causa sin sonda es una hipótesis escrita con ropa de resultado.

- **Qué falta (declarado).** Figuras: (a) `T_U1` contra media `T_U2` con banda `3 sigma`, sobre los 29 bins; (b) `DeltaT` contra `nu` con las 7 marcas; (c) descomposición del umbral (piso contra `3 sigma`). Todas se generan **desde el crudo sellado**; `PENDIENTE DECLARADO` hasta generar los artefactos de figura con su propio comando.
- **Presupuesto:** 1.5 páginas.

---

## V. Discusión y Senderos Futuros

- **Objetivo.** Decir qué **no** cierra este resultado, qué defectos quedan declarados, y con qué condición de entrada se abrirían.

### V.1 Errata de plantilla (fechada, sin editar la fila vieja)

El pre-registro acústico §7.7.a nombra la plantilla `fdtd2m_tm.py`. **El nombre real es `fdtd2d_tm.py`** (blob `0d7820a8ea566e403e9528f30945a4a04ff9cbc4`). El error está en el nombre citado, **no** en el blob ni en la medición. Va en **apéndice fechado**; la fila vieja **no se edita**.

### V.2 Defectos declarados y **no** reparados

- **Ruta de lectura de la escala.** El driver del enlace lee la escala declarada desde una clave **raíz** que no existe, y por eso el crudo imprime `escala_declarada = {'celda_unidades_vecino': None}`. La clave **sí existe**, anidada: en `data/geometria_hat/u1/crudo.json`, `u1.celda = 0.45782072127145995` y `u1.lado = 175.80315696824061` (`n_centroides = 3603`). Es **defecto de camino de lectura, no de dato**. Repararlo exige **driver nuevo + corrida nueva + crudo nuevo**: el crudo de `20:48:09Z` **no se reescribe**.
- **Advertencia para replicaciones externas de `v0.1.0`.** No debe leerse un factor de conversión de la raíz del crudo de `u1`; el mapeo del enlace es **celda a celda sobre la ventana completa**, y la equivalencia `unidad ↔ a` **no está declarada**.
- **Aliasing de borde (declarado, sin adjudicar).** `3603` teselas sobre `59525` celdas activas dan aprox. **16.5 celdas por tesela**; en `nu` en `[0.15, 0.20]`, `lambda = c_s / nu` cae en aprox. `5.0a` a `6.6a`. La relación entre esta escala y el salto de cobertura se **declara**; no se adjudica.
- **Hipótesis falsable de causalidad en baja frecuencia.** El vínculo entre la discrepancia espectral en `nu` en `{0.1527, 0.1666, 0.1944}` y el salto de permitividad efectiva `<K>` entra **formalmente como hipótesis declarada, NO adjudicada**, pendiente de **igualación estricta de relleno** o de **prueba analítica de medio efectivo**. No es un resultado: es una pregunta con condiciones de cierre escritas.
- **Reparto bajo `ddof = 0`.** 8 contra 7: se imprime el par, no se adjudica.

### V.3 Pendientes con condición de entrada

| pendiente | condición de entrada | estado |
|---|---|---|
| `U2_ac` (§7.8) | `abs(T_U1 − media_T_U2) > 3 sigma_U2 + 0.005523` en `[0.15, 0.55]` | **evaluable del crudo congelado, sin corridas nuevas.** Re-derivado: **7/22**, que **coincide** con `n_discrepa`/`n_nulo`; el control `ddof = 0` re-deriva **8** y coincide con `control_ddof0_n_discrepa = 8` |
| contraste `C2` | una corrida nueva de medio **homogéneo** con `K = 0.25`, `R = -1/3`, `T_amp = 2/3` | **no derivable de lo congelado.** Medido: `reparto_constitutivo.K_mat_declarado_no_usado = 0.25` — **declarado y no usado** — y las **4** corridas son homogéneas con `K_0 = 1.0`. **No se ejecuta.** |
| tercer peldaño de malla | `dx' = a/32`, `S = 0.5`, mismas sondas, `p = log2(razón de errores)` | **no ejecutado, no medido** |

### V.4 Senderos futuros (declarados, no recorridos)

- **Cambio de Objeto.** Cuasicristales de Penrose y teselados octogonales Ammann-Beenker: evaluar si una aperiodicidad con simetrías rotacionales prohibidas de 5 u 8 pliegues **abate** el ruido de dispersión transversal. Cambia el objeto, conserva el operador.
- **Cambio de Operador.** Resonadores puntuales en los **vértices** del monotilo Hat: el mecanismo pasa de **interferencia destructiva por aperiodicidad pura** a **apertura de bandgap por hibridación resonante local**. Esto constituye un **objeto físico nuevo**, con su propia formulación analítica y su pre-registro independiente. Detalle en `CIERRE_SENDERO_FUTURO_Y_ERRATA_DOCUMENTADA_20261013.md`.
- **Erratas de malla en la literatura previa.** `PENDIENTE DECLARADO`: el apartado se redacta **sólo** con fuentes externas verificadas una por una y clasificadas (`COINCIDE` / `DIVERGE` / `PRESTADO` / `AJENO`). No hay bibliografía medida dentro de estos repositorios, y no se inventa una para llenar la sección.
- **Presupuesto:** 1 página.

---

## VI. Disponibilidad de Datos

### VI.1 Snapshots congelados

| Paquete | DOI | Concepto | ZIP (bytes) | md5 |
|---|---|---|---|---|
| `acustica-monotile` | `10.5281/zenodo.23329941` | `10.5281/zenodo.23329940` | 475297 | `1514aeb95afb134418a2af8e81018379` |
| `fotonica-monotile` | `10.5281/zenodo.23329943` | `10.5281/zenodo.23329942` | 124629 | `479546ff0d10d7b6acd7f15b2738844b` |

Metadatos de ambos registros, medidos: `state = published`, revisión `3`, `version = '0.1.0'`, `publication_date = 2026-10-12`, `access = open`, `type = software`, licencia `mit-license`, creador `Roman Martinez, Jose Alexis`.

### VI.2 Repositorios

| Repositorio | Visibilidad | HEAD al escribir | Topics (n = 6) |
|---|---|---|---|
| `alexisromtz-lab/acustica-monotile` | público | `92abcfc` (1 commit posterior a la marca `v0.1.0` = `0b39c72`, hash remoto completo `0b39c7264d9f4412e0f3c8e8c3e0e9b49ca2d0fb`) | `acoustics`, `aperiodic-tiling`, `fdtd`, `einstein-monotile`, `reproducible-research`, `wave-propagation` |
| `alexisromtz-lab/fotonica-monotile` | público | `14bc745` (**reposo absoluto**: HEAD = remoto = marca) | `bandgap-analysis`, `einstein-monotile`, `electromagnetics`, `fdtd`, `photonics`, `reproducible-research` |

Integración continua de depósito: el *webhook* de Zenodo está **encendido** en ambos repositorios. Se declara como **acto de panel humano**, no automatizable desde la API.

### VI.3 Reproducción

```sh
# instrumento fotónico (pieza C1: Q1..Q4) y acto de contraste
python3 fdtd2d_tm.py --json
python3 inyector_diel.py --correr      # escribe un crudo NUEVO con hora UTC; no sobrescribe el sellado

# enlace (mascara + control nulo) sobre el solver acustico
python3 -B sim/driver_enlace_fotonica_acustica.py
```

Los tres scripts del vecino se resuelven desde su propio directorio; el driver del enlace **no toma argumentos** y escribe un crudo nuevo en `crudos/`. Ninguna corrida sobrescribe un crudo sellado.

**Nota de alcance para el paper.** El sello de depósito cubre paquetes **de código** (ZIP con su DOI). Un paper citado desde esos registros necesita además su **PDF con estructura de artículo** para ser indexable por los índices de literatura. Este esqueleto existe para cerrar ese hueco, no para reemplazar los depósitos.

- **Presupuesto:** 0.5 página.

---

## VII. Trazabilidad: cada cifra con su artefacto

**Regla:** ninguna cifra entra al paper sin renglón aquí. Si falta el artefacto, la cifra sale del texto.

| # | Cifra | Valor | Instrumento / artefacto | Ventana |
|---|---|---|---|---|
| 1 | Reparto del veredicto | 7 `DISCREPA` / 22 `NULO` / 29 bins | `crudos/crudo_ENLACE_ACUSTICA_FOTONICA_20261012T204809Z.json` (26278 B, 1018 l) | `2026-10-12T20:47:13Z` → `20:48:09Z` |
| 2 | Regla pre-declarada | `ddof = 1`, `factor = 3.0`, `piso_contrato = 0.005523` | mismo crudo, bloque `declarado_antes_de_medir` | idem |
| 3 | Piso del umbral | `0.00552322568652841` | mismo crudo (`piso_medido_C1`) | idem |
| 4 | Aporte del piso | `1.27687e-03` del umbral máximo | acta de cierre §9.2 (re-derivación del crudo congelado) | `2026-10-13` (lectura) |
| 5 | Aporte de `3 sigma_U2` | `0.983139` a `0.998723` | acta de cierre §9.2 | idem |
| 6 | Control `ddof = 0` | 8 | crudo, `control_ddof0_n_discrepa` | idem |
| 7 | Control de convención | `T_U1 identico = False` ⇒ 11/29 | crudo, `control_convencion` | idem |
| 8 | Delta de rasterizado (objeto A) | `1.530e-04` | acta de cierre §3.1 | idem |
| 9 | Salto de cobertura (objeto B) | aprox. 2 pp | acta de cierre §3.2 | idem |
| 10 | C1 bit a bit | `array_equal = True`, `max_abs_dif = 0.0` | acta de cierre §4 | `2026-10-12T21:33:50Z` → `21:33:54Z` |
| 11 | `T_riz` = piso medido | `0.0055232256865284102` | acta de cierre §4 | idem |
| 12 | Criterios Q1..Q4 | VERDE, 4 de 4 | `PREREGISTRO_INSTRUMENTO_FDTD_20261012.md` (sellado `2026-10-12T05:49Z`) | `2026-10-12T05:49Z` |
| 13 | Acto 3.2 | `NEGATIVO / NULO SOSTENIDO`, 28/29 en banda, `racha_mas_larga = 1` | `crudos/crudo_acto3_20261012T205230Z.json` (vecino `fotonica-monotile`) | `2026-10-12T20:52:30Z` |
| 14 | Alias de instrumentos | `malla_hat.py` 910 l `914a8666f1d13ddf` · `fdtd2d_tm.py` 501 l `56a8d5f896b9cfea` · `inyector_diel.py` 767 l `01ffcf31c040368d` | `shasum -a 256` sobre disco | `2026-10-13` |
| 15 | Alias acústicos | solver 626 l `49c429e5cbedc4d0` (blob `4de2c841…`) · driver 352 l `0a896230fa53d108` (blob `a0ab6ac8…`) · verificador 196 l `10011010c00dc8d3` | `shasum -a 256` + `git hash-object` | `2026-10-13` |
| 16 | DOIs y md5 de los ZIP | ver §VI.1 | API de Zenodo (`/api/records/{id}`) | `2026-10-13` |
| 17 | Topics y visibilidad | ver §VI.2 | `gh api repos/{owner}/{repo}/topics` (relectura) | `2026-10-13T04:56:17Z` → `04:56:23Z` |

**Dos motores de identidad, declarados:** `sha256[0:16]` (medido con `shasum` sobre el archivo en disco) y **blob SHA-1** de git (`git hash-object`, el que citan las actas). **No son el mismo metro** y no se intercambian.

---

## VIII. Plantilla LaTeX (dos columnas) y comandos

### VIII.1 Plantilla

```latex
\documentclass[twocolumn,10pt]{article}
\usepackage{amsmath,amssymb}
\usepackage{graphicx}
\usepackage{booktabs}
\usepackage[hidelinks]{hyperref}
\usepackage[margin=1.9cm]{geometry}

\title{Bounds on Wave Transport in Aperiodic Hat Monotile Tilings:\\
A Bit-Reproducible Dual Acoustic--Photonic FDTD Benchmark}
\author{Jose Alexis Roman Martinez}
\date{2026-10-13}

\begin{document}
\maketitle

\begin{abstract}
... 150 a 200 palabras: objeto, protocolo, veredicto (7 de 29 bins por encima del
umbral), y de que esta hecho el umbral (\textbackslash 3 sigma U2, no el piso).
\end{abstract}

\section{Introduccion y problema}
\section{Formulacion numerica y complejo dual}
\section{Protocolo de reproducibilidad}
\section{Resultados}
\section{Discusion y senderos futuros}
\section{Disponibilidad de datos}

\bibliographystyle{plain}
\bibliography{referencias}
\end{document}
```

Las fórmulas van entre `\( \)` o `\[ \]` (nunca con el par de signos de dólar, por la regla de sustitución de este entorno).

### VIII.2 Comandos de construcción y de cierre

```sh
# compilacion (mismo camino que el paper hermano sfqed-paper)
tectonic main.tex            # produce main.pdf

# verificacion del esqueleto (nunca por lectura del mensaje de exito)
wc -l WHITEPAPER_ESQUELETO_20261013.md
wc -c WHITEPAPER_ESQUELETO_20261013.md
shasum -a 256 WHITEPAPER_ESQUELETO_20261013.md | cut -c1-16
grep -c '^#+ ' WHITEPAPER_ESQUELETO_20261013.md    # cabezas, nivel 1 a 3
grep -c '^## ' WHITEPAPER_ESQUELETO_20261013.md    # cabezas, nivel 2 a 3
```

**Cierre del arnés (turno 2)** tras registrar el archivo:

```sh
bash /Users/marlene/platino-labs/tools/gate_pre_escritura.sh \
  /Users/marlene/acustica-monotile/WHITEPAPER_ESQUELETO_20261013.md \
  <BLOB_POST> <HUELLA> <LINEAS_POST>
```

### VIII.3 Reparto de páginas (objetivo 4 a 6)

| Sección | Páginas |
|---|---|
| I. Introducción y problema | 0.75 |
| II. Formulación numérica y complejo dual | 1.00 |
| III. Protocolo de reproducibilidad | 1.00 |
| IV. Resultados experimentales | 1.50 |
| V. Discusión y senderos futuros | 1.00 |
| VI. Disponibilidad de datos | 0.50 |
| **total** | **5.75** |

---

## IX. Estado

**ESTADO: ESQUELETO ESCRITO · SEIS SECCIONES BORRADOR · TRAZABILIDAD DE 17 FILAS · PLANTILLA LATEX DOS COLUMNAS INCLUIDA · CERO CIFRAS NUEVAS · PENDIENTES DECLARADOS CON CONDICION DE ENTRADA.**
