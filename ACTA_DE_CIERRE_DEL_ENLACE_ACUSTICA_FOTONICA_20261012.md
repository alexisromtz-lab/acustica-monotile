# ACTA DE CIERRE DEL ENLACE FOTONICA-MONOTILE -> ACUSTICA-MONOTILE

- **Fecha de escritura:** 2026-10-12 (UTC).
- **Casa que escribe:** `acustica-monotile` (rama `main`).
- **Acto:** `Paso 3 del enlace fotonica-monotile -> acustica-monotile`.
- **Instrumento:** `sim/driver_enlace_fotonica_acustica.py` (352 l, blob `a0ab6ac8b3b14ef42d0b5fad4f9db281a301c6f6`).
- **Solver (el metro):** `sim/sim_acustica2d.py` (626 l, blob `4de2c841e0d6e6b2757c371ef5cca1e4661b646b`, commit `f29879b`).
- **Crudo del acto:** `crudos/crudo_ENLACE_ACUSTICA_FOTONICA_20261012T204809Z.json` (26278 B, 1018 l).
- **Ventana de la corrida:** `t_utc_inicio = 2026-10-12T20:47:13Z` · `t_utc_fin = 2026-10-12T20:48:09Z`.

**UNIVERSO DECLARADO:** el `T(nu)` del solver `sim/sim_acustica2d.py` (blob `4de2c841e0d6e6b2757c371ef5cca1e4661b646b`, commit `f29879b`) a `L = 24.0 a`, modo `C1b`, con mascara de `data/geometria_hat/` (commit `b498fcf`), mas el mismo `T(nu)` sin mascara (control C1 nulo).
**MOTOR:** `python3 -B` + numpy 2.4.6 (Python 3.14.7); el solver es el instrumento.
**UNIDAD:** valor de `T` por bin (29 bins); `1 realizacion = 1 corrida`.
**VENTANA:** reloj UTC declarado en cada figura.

---

## 1. Vector oficial del enlace

Regla pre-declarada (`declarado_antes_de_medir`, leida del crudo, no re-tecleada):

    DeltaT(nu) = | T_U1(nu) - media_T_U2(nu) | - ( factor * sigma_U2(nu) + piso )
    ddof_sigma = 1
    factor     = 3.0
    piso_contrato      = 0.005523
    piso_medido_C1     = 0.00552322568652841

### 1.1 Rejilla de nu (29 bins)

    0.152711, 0.166594, 0.180477, 0.194360, 0.208243, 0.222126, 0.236009,
    0.249892, 0.263774, 0.277657, 0.291540, 0.305423, 0.319306, 0.333189,
    0.347072, 0.360954, 0.374837, 0.388720, 0.402603, 0.416486, 0.430369,
    0.444252, 0.458134, 0.472017, 0.485900, 0.499783, 0.513666, 0.527549,
    0.541432

`n_bins = 29` · `nu0 = 0.152711` · `nu28 = 0.541432` · `nu_iguales_en_todas_las_corridas = True`.

### 1.2 Reparto del veredicto

| clase | n |
|---|---|
| `DISCREPA` | **7** |
| `NULO` | **22** |
| total | 29 |

`n_discrepa = 7` · `n_nulo = 22`. Clases presentes medidas: `['DISCREPA', 'NULO']` — no hay tercera clase.

### 1.3 Los 7 bins DISCREPA

| i | nu | DeltaT |
|---|---|---|
| 0 | 0.152711 | 7.119200e-01 |
| 1 | 0.166594 | 7.589031e-01 |
| 3 | 0.194360 | 8.292833e-01 |
| 7 | 0.249892 | 1.041554e-01 |
| 14 | 0.347072 | 5.113464e-03 |
| 16 | 0.374837 | 3.497564e-01 |
| 24 | 0.485900 | 1.569740e+00 |

### 1.4 Extremos del vector

- `delta_T_max = 1.5697403560585752` en `nu = 0.48590021691973967` (bin 24, DISCREPA).
- `delta_T_min = -3.805628370974314` en `nu = 0.5414316702819957` (bin 28, NULO).
- `|delta_T_min| = 3.805628e+00`.
- `rango_T_U2_max = 3.4677075111160995` en `nu = 0.5414316702819957`.

Observacion: el bin del minimo **no** es el bin del maximo y los dos caen en extremos opuestos del veredicto — el vector **no** es monotono en nu.

### 1.5 Denominador del umbral (punto 1 del analisis del dueño)

El umbral no lo manda el piso: lo manda `3 sigma_U2`.

| cantidad | min | max |
|---|---|---|
| `sigma_U2_ddof1` (29 valores) | 1.073493e+00 | 1.440030e+00 |
| `umbral = 3 sigma_U2 + piso` | 3.275710e-01 | 4.325612e+00 |
| `piso` | 0.00552322568652841 | 0.00552322568652841 |

Lectura declarada: un `NULO` significa «cae por debajo de `3 sigma_U2 + piso`», **no** «los dos universos coinciden». Los 22 `NULO` **no** son prueba de fisica compartida: son compatibilidad con un denominador dominado por la dispersion de U2.

---

## 2. Controles del crudo (leidos del mismo crudo, no re-ejecutados)

| control | valor | lectura |
|---|---|---|
| `control_ddof0_n_discrepa` | 8 | con `ddof = 0` el reparto cambia de 7 a 8 |
| `control_piso_medido_n_discrepa` | 7 | con el piso **medido** en vez del de contrato: 7 (igual) |
| `control_convencion` (`T_U1` transpuesta vs sin transponer) | `T_U1` identico = **False** | 11/29 DISCREPA — la convencion de la mascara **si mueve** el vector |
| `nu_iguales_en_todas_las_corridas` | True | la rejilla no es una variable del contraste |

El control `ddof` da **8** vs el oficial **7**: los dos se imprimen; **no se adjudica** cual es el bueno — se declara que el reparto depende del estimador de `sigma_U2`, y que `ddof = 1` se fijo **antes** de medir.

### 2.1 Fraccion de mascara medida por realizacion

| realizacion | `fraccion_mascara_union` |
|---|---|
| `u1` | 0.4036797417534722 |
| `u2_semilla_101` | 0.3824734157986111 |
| `u2_semilla_102` | 0.3850843641493056 |
| `u2_semilla_103` | 0.3834771050347222 |
| `u2_semilla_104` | 0.3846367730034722 |
| `u2_semilla_105` | 0.38299560546875 |

En las 6 corridas declaradas: `es_heterogeneo = True`, `identidad_inv_eps_igual_a_K = True`, `identidad_inv_mu_igual_a_uno = True`, `K` en `[0.25, 1.0]`, `inv_eps` en `[0.25, 1.0]`.

---

## 3. Denominadores separados (D22) — **no se funden**

**Regla:** un nombre con dos denominadores se imprime **el par**; no se elige y no se promedia. **El `1.7 %` queda PURGADO del registro**: no es una cifra, es una razon entre dos objetos de distinta clase.

### 3.1 Objeto A — delta de rasterizado en U1

| via | valor |
|---|---|
| `suma_areas_analitico` (analitica, ratificada por el dueño) | 0.4038327588420457 |
| `cobertura_union_U1` (media de la mascara binaria) | 0.4036797417534722 |
| **delta** | **1.530e-04** |

Los dos numeros son **verdaderos** y miden **objetos distintos**: el area suma de la geometria contra el promedio de celdas de la mascara binaria. Se declaran **hermanos, no fusionables**.

### 3.2 Objeto B — salto de cobertura U1 hacia U2

| objeto | rango |
|---|---|
| U1 | 0.4036797417534722 |
| U2 (`101..105`) | [0.3824734157986111, 0.3850843641493056] |
| **salto** | **aprox. 0.02 (2 pp)** |

**El salto U1 a U2 y el delta de rasterizado NO son el mismo objeto** y **no se suman**. Un porcentaje unico que los mezcle reintroduce el defecto que el `1.7 %` cometia.

Nota del propio crudo, citada: *«se imprimen los dos; no se adjudica ni se repara el vecino»*.

---

## 4. Seccion de calibracion instrumental: control de no-regresion C1 bit a bit

Esta seccion es un **control instrumental dentro de la misma acta** (no un archivo aparte): sin ella, «el enlace no movio el solver» seria una afirmacion, no una medicion.

**UNIVERSO DECLARADO:** el `T(nu)` `C1b` a `L = 24.0` del solver (1 modulo) contra el `T(nu)` `C1b`/`24.0` del crudo `crudos/crudo_C1_acustica_20261012T072953Z.json` (1 archivo).
**MOTOR:** `python3 -B` + numpy.
**UNIDAD:** valor de `T` (29 bins).
**VENTANA:** corrida sellada `2026-10-12T21:33:50Z` -> `2026-10-12T21:33:54Z`.

| prueba | medida |
|---|---|
| `filas_4` / `fila_match` | 4 / 1 |
| `len_ref` / `len_new` | 29 / 29 |
| `array_equal` | **True** |
| `max_abs_dif` | **0.0** (bit a bit) |
| `T_media` | 0.707449275919397 |
| `T_teorico` (`sqrt(0.5)`) | 0.7071067811865476 |
| `T_riz` | 0.0055232256865284102 |
| `piso_medido_C1` del crudo | 0.00552322568652841 |
| `es_heterogeneo` | **False** |
| `fraccion_mascara_union` | `None` |
| `identidad_inv_eps_igual_a_K` | True |
| `identidad_inv_mu_igual_a_uno` | True |
| `nt` / `nx` / `ny` | 2304 / 384 / 384 |

**Resultado:** `array_equal = True` y `max_abs_dif = 0.0` sobre los 29 bins — el camino sin mascara **no cambio un bit** respecto del crudo `C1` de `d5a7548`. Y `T_riz = 0.0055232256865284102` **es exactamente** el `piso_medido_C1` que el crudo del enlace usa en su umbral: el piso **no** es un numero heredado por prosa, es la cifra de ruido del propio instrumento en su configuracion homogenea.

### 4.1 Trampa de metro declarada (y cerrada)

La cifra `0.004258596071401777` **no** es un `riz`: su casa medida es `corridas[2]/T_desv_max` y `T_desv_max_por_modo/C1b` — es la **desviacion maxima de `T`**, otra cantidad. Llamarla «riz max» era un defecto de **nombre**, no de cifra. El piso de ruido tiene una sola casa: `T_riz`. (Y `r['T']` es el **vector de 29 bins**, no el campo 3D: intentar reacomodarlo da `ValueError: cannot reshape array of size 29 into shape (2304,384,384)`.)

---

## 5. Los cuatro cortes ratificados

1. **Punto 2, en redaccion numerada.** Se admite **estrictamente** como: *«Correlacionadas con Delta f aprox. 2 pp y no adjudicables exclusivamente a orden aperiodico»*. **Toda afirmacion causal del tipo «artefacto por solape» queda PURGADA**: en este repositorio **no hay sonda instrumental** que la mida, y una causa sin sonda es una hipotesis escrita con ropa de resultado.
2. **Separacion de denominadores (D22).** El `1.7 %` **purgado**. Se registran como objetos independientes y no fusionables: el delta de rasterizado en U1 (`0.4038327588420457` vs `0.4036797417534722` -> `1.530e-04`) y el salto de cobertura U1 a U2 (`0.40368` vs `[0.38247, 0.38508]`, aprox. 2 pp). Ver §3.
3. **Causalidad en baja frecuencia como hipotesis falsable.** El vinculo entre la discrepancia espectral en `nu` en `{0.1527, 0.1666, 0.1944}` y el salto de permitividad efectiva `<K>` entra **formalmente como hipotesis declarada, NO adjudicada**, pendiente de **igualacion estricta de relleno** o de **prueba analitica de medio efectivo**. No es un resultado del acta: es una pregunta con condiciones de cierre escritas.
4. **Registro de paridad bit a bit C1.** La prueba de no-regresion se incorpora como **seccion de control instrumental dentro de esta misma acta** (§4), sin archivo aparte.

---

## 6. Declaraciones sin adjudicar

- **El denominador del contraste es `3 sigma_U2`, no el piso.** `umbral` recorre `3.275710e-01` a `4.325612e+00` mientras `piso = 0.00552322568652841`. Consecuencia declarada: **los 22 `NULO` no son evidencia de fisica compartida**; son compatibilidad con un denominador dominado por la dispersion de U2. Se **declara**, no se recalibra.
- **Defecto de instrumento, declarado y NO reparado.** `escala_declarada` en el crudo trae `{'celda_unidades_vecino': None}`: el driver leyo la escala en una clave de raiz que no existe. La clave **si existe**, anidada: `u1.celda = 0.45782072127145995` y `u1.lado = 175.80315696824061` en `data/geometria_hat/u1/crudo.json` (`n_centroides = 3603`). Es **defecto de camino de lectura, no de dato**. Repararlo exige **driver nuevo + corrida nueva + crudo nuevo**: el crudo de `20:48:09Z` **no se reescribe**.
- **Aliasing de borde, declarado sin adjudicar.** 3603 teselas sobre 59525 celdas activas dan aprox. 16.5 celdas por tesela; en la ventana `nu` en `[0.15, 0.20]`, `lambda = c_s / nu` cae en aprox. `5.0a` a `6.6a`. La relacion entre esta escala y el salto de cobertura se **declara**; no se adjudica.
- **`rango_T_U2_max`** (`3.4677075111160995` en `nu = 0.5414316702819957`) y **`delta_T_min`** (`-3.805628370974314`, mismo bin) coexisten en el extremo alto de la rejilla: se imprime el par, **no** se elige cual describe el enlace.

---

## 7. Pendientes declarados (fuera de esta acta)

- **Errata de plantilla:** el preregistro `PREREGISTRO_ACUSTICA_MONOTILE_20261012.md` §7.7.a nombra la plantilla `fdtd2m_tm.py`; el nombre real es `fdtd2d_tm.py` (blob `0d7820a8ea566e403e9528f30945a4a04ff9cbc4`). Va en **apendice fechado**, nunca editando la fila vieja.
- **Ejecucion de U2_ac (§7.8):** `abs(T_U1 - media_T_U2) > 3 sigma_U2 + 0.005523` en `[0.15, 0.55]` — evaluable desde el crudo existente, **sin corridas nuevas**.
- **Contraste C2:** `K: 1 -> 0.25`, `R = -1/3`, `T_amp = 2/3` contra el techo nativo `riz(T) <= 0.010` y la regla del `0.55 %`.
- **Camino de lectura de `celda`** en `abre(...)` del driver (deberia ser `u1.celda` / `lado`).

---

## 8. Cierre

El enlace **fotonica-monotile -> acustica-monotile** queda cerrado con: un vector oficial de **29 bins** (**7 `DISCREPA` / 22 `NULO`**), **dos denominadores separados y no fusionables**, un **control de no-regresion C1 bit a bit** (`array_equal = True`, `max_abs_dif = 0.0`), y **cuatro cortes ratificados** aplicados a la redaccion. Lo que **no** esta medido queda **declarado como hipotesis**: la causalidad en baja frecuencia, el rol del aliasing de borde, y el reparto bajo `ddof = 0`.

**ESTADO: CERRADO · 7 DISCREPA / 22 NULO · C1 BIT A BIT (max_abs_dif = 0.0) · DOS DENOMINADORES SEPARADOS · HIPOTESIS DECLARADAS SIN ADJUDICAR.**
