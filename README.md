<!-- HUELLA-README-ACUSTICA-MONOTILE-20261013 -->

# acustica-monotile — Enlace fotónica → acústica sobre la geometría Monotile Hat

[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.23329941-blue)](https://doi.org/10.5281/zenodo.23329941)
[![Licencia: MIT](https://img.shields.io/badge/licencia-MIT-green)](LICENSE)
[![Motor](https://img.shields.io/badge/motor-Python%203.14%20%C2%B7%20numpy%202.4.6-blue)](crudos/crudo_ENLACE_ACUSTICA_FOTONICA_20261012T204809Z.json)
[![Control C1 bit a bit](https://img.shields.io/badge/C1%20bit--a--bit-PASA-brightgreen)](ACTA_DE_CIERRE_DEL_ENLACE_ACUSTICA_FOTONICA_20261012.md)
[![Orden del esquema Yee](https://img.shields.io/badge/Yee-p%20%3D%202-blueviolet)](WHITEPAPER_ESQUELETO_20261013.md)

**Gancho.** Solver acústico 2D que evalúa el transporte de ondas y las cotas de *bandgap* sobre
el monotilo aperiódico de Hat, y que **publica un resultado negativo como resultado, no como
fracaso**: sobre **29 bins** de frecuencia, el vector `T(nu)` con la máscara del monotilo **no**
se separa de su control nulo homogéneo en **22 de 29** bins, y el nulo es una **cota**
(`3 · sigma_U2 + piso`), no una igualdad. Cada cifra de este README viaja con su artefacto
sellado, y cada tabla dice con qué comando se obtiene.

*Dual 2D Yee-FDTD solver evaluating wave transport and bandgap bounds on the aperiodic
Einstein Hat monotile. Null-bounded verdict over 29 frequency bins, sealed raw artifacts, and a
bit-to-bit non-regression control.*

**Nota sobre las insignias.** Cada insignia cita su artefacto, y dos de ellas declaran su
límite. La de **motor** cita el campo de firma del crudo sellado (`python3 -B` + numpy 2.4.6
sobre Python 3.14.7): es lo **medido**, no una promesa de compatibilidad con otras versiones. La
de **orden del esquema** (`p = 2`) es el orden **declarado** del esquema Yee en
`WHITEPAPER_ESQUELETO_20261013.md` §III, **no** una escalera de convergencia medida: en este
repositorio no existe ninguna corrida que refine la malla y mida el exponente. Se escribe
`p = 2`, nunca `p = 2.0001`.


Instrumentos y crudos del **Paso 3 del enlace**: la malla dieléctrica del monotilo
Hat, generada en el repositorio vecino `fotonica-monotile`, se rasteriza a una
**máscara binaria** y se inyecta como heterogeneidad constitutiva `K(x, y)` en un
solver acústico 2D. El vector de transmisión `T(nu)` de la geometría **con**
máscara se compara contra el mismo solver **sin** máscara (control nulo homogéneo).

Este repositorio publica **un resultado negativo como resultado**, no como fracaso.

---

## Inicio rápido (15 s)

Sin dependencias: el bloque de abajo usa sólo la biblioteca estándar de Python (`json`). No
requiere numpy, no escribe nada y **re-deriva el veredicto desde el crudo sellado**.

```sh
git clone https://github.com/alexisromtz-lab/acustica-monotile.git
cd acustica-monotile
python3 -B - <<'PY'
import json
d = json.load(open('crudos/crudo_ENLACE_ACUSTICA_FOTONICA_20261012T204809Z.json'))
f = d['declarado_antes_de_medir']          # la regla, escrita ANTES de ver una cifra
dd = [abs(a - b) - (f['factor'] * s + f['piso_medido_C1'])
      for a, b, s in zip(d['T_U1'], d['media_T_U2'], d['sigma_U2_ddof1'])]
print('DISCREPA=%d  NULO=%d  bins=%d'
      % (sum(x > 0 for x in dd), sum(x <= 0 for x in dd), len(dd)))
PY
```

Salida observada (`python3 -B`, 2026-10-13) — reproduce el veredicto sellado:

```text
DISCREPA=7  NULO=22  bins=29
```

El mismo bloque, extendido con `print(d['n_discrepa'], d['n_nulo'])`, imprime `7 22`: **el
veredicto re-derivado coincide con los campos del propio crudo**
(`derivado_igual_al_campo=True`), y las clases presentes son exactamente `DISCREPA` y `NULO`.

**Reproducción completa** (la corrida real del enlace, no la lectura del crudo):

```sh
python3 -B sim/driver_enlace_fotonica_acustica.py
```

El driver **no toma argumentos**; resuelve `sim/` por `__file__` y escribe un crudo **nuevo**,
etiquetado con la hora UTC de la corrida, en `crudos/` — es decir, **no sobrescribe el crudo
sellado**. Requiere numpy, y no es una corrida de segundos.

---

## Resultados medidos

Tabla metrológica, descompuesta. **Universo declarado: el crudo sellado**
`crudos/crudo_ENLACE_ACUSTICA_FOTONICA_20261012T204809Z.json` (26 278 B, commit `03edabb`),
ventana `2026-10-12T20:47:13Z → 20:48:09Z`, unidad = **valor de `T` por bin** (29 bins; 1
realización = 1 corrida), 6 corridas, todas heterogéneas, con `K ∈ [0.25, 1.00]`. El veredicto
asentado está en §1; esta tabla lo **descompone**, no lo repite.

| Cantidad | Valor medido | Cómo se obtiene |
| --- | --- | --- |
| Vector oficial | **29 bins**, `nu = 0.1527114967462039 → 0.5414316702819957` (c/a) | `len(d['nu'])`, `d['nu'][0]`, `d['nu'][-1]` |
| Veredicto | **7 `DISCREPA` / 22 `NULO`** | re-derivado `= 7/22` **y** campo `n_discrepa/n_nulo = 7/22` |
| `delta_T` máximo | `1.5697403560585752` en `nu = 0.4859002169197397` | `max(d['delta_T'])` |
| `delta_T` mínimo (el más negativo) | `-3.805628370974314` en `nu = 0.5414316702819957` | `min(d['delta_T'])` |
| Rango de `T_U2` en ese mismo bin | `rango_T_U2_max = 3.4677075111160995` | se **imprimen los dos**; ninguno se elige ni se adjudica |
| `sigma_U2` (`ddof = 1`) | `[0.107349341659, 1.440029667278]` | `min/max(d['sigma_U2_ddof1'])` |
| Banda del nulo | `[0.327571024978, 4.325612001835]` = `3 · sigma_U2 + 0.00552322568652841` | `min/max(d['umbral'])` |
| Reparto del nulo | `3 sigma_U2 / banda ∈ [0.983139534395, 0.998723186454]` · `piso / banda_max = 1.276865720778e-03` | `3*s/u` y `piso/max(umbral)` bin a bin |
| Llenado: **dos denominadores, no fusionables** | `suma_areas_analitico = 0.4038327588420457` · `cobertura_union_U1 = 0.4036797417534722 = media_mascara_binaria` | `d['llenado_dos_denominadores']`; no se elige |
| Control de convención (`ddof = 0`) | **8** `DISCREPA` | `control_ddof0_n_discrepa` |
| Control del piso (`piso_medido_C1`) | **7** `DISCREPA` | `control_piso_medido_n_discrepa` (igual que el nominal: el piso no cambia el veredicto) |
| Control de ejes (máscaras sin transponer) | **11** `DISCREPA` | `control_convencion['n_discrepa']` — mide que la convención **no es un no-op**; **no es un veredicto** |
| `nu` idéntico en todas las corridas | `True` | `nu_iguales_en_todas_las_corridas` |
| No-regresión **C1 bit a bit** | `array_equal = True` · `max_abs_dif = 0.0` sobre los 29 bins | acta de cierre §4 (l.150–151) |

Lectura del reparto, **dentro de lo medido**: el nulo es una cota acotada a su propio
denominador (`3 sigma_U2 + piso`) y está dominada por `3 sigma_U2`, que aporta de
`0.983139534395` a `0.998723186454` de la banda; el piso instrumental aporta
`1.276865720778e-03` de la banda máxima. Lo que **no** dice: que exista un mecanismo de
transporte. Eso queda declarado abajo, sin adjudicar.

Nota de no-deriva: §9.2 imprime la misma participación **a 6 decimales** (`[0.983139,
0.998723]`) y el mismo piso normalizado (`1.27687e-03`). Son las **mismas** cifras con otra
anchura de impresión, no dos mediciones: `0.983139534395` truncado a 6 decimales es `0.983139`
y redondeado es `0.983140`.

---

## Cómo citar (BibTeX)

```bibtex
@software{roman_martinez_acustica_monotile_2026,
  author    = {Roman Martinez, Jose Alexis},
  title     = {acustica-monotile: enlace experimental fotónica → acústica sobre la geometría Monotile Hat (Paso 3)},
  year      = {2026},
  version   = {0.1.0},
  publisher = {Zenodo},
  doi       = {10.5281/zenodo.23329941},
  url       = {https://doi.org/10.5281/zenodo.23329941},
  license   = {MIT},
  keywords  = {monotile Hat, aperiodicidad, FDTD, metrología A2.1, enlace fotónica-acústica, no-regresión bit a bit}
}
```

**No se declara ORCID**: el propio `CITATION.cff` lo dice — no existe ninguno en este
ecosistema, y el bloque de arriba no lleva ese campo. El formulario canónico de cita es
`CITATION.cff` (esquema CFF 1.2.0); los metadatos de depósito viven en `.zenodo.json`. El DOI de
la **versión** es el de la insignia; el del **concepto** (todas las versiones) es
`10.5281/zenodo.23329940`.

---

## 1. Veredicto asentado

| Campo | Valor medido |
| --- | --- |
| Vector oficial | **29 bins**, `nu = 0.152711 … 0.541432` (c/a) |
| Veredicto | **7 `DISCREPA` / 22 `NULO`** |
| Crudo sellado | `crudos/crudo_ENLACE_ACUSTICA_FOTONICA_20261012T204809Z.json` (26 278 B) |
| Ventana de medición (UTC) | `2026-10-12T20:47:13Z` → `2026-10-12T20:48:09Z` |
| Eje del veredicto | `DeltaT(nu) = abs(T_U1(nu) − media_T_U2(nu)) − (3 · sigma_U2(nu) + 0.005523)` |
| Regla por bin | `DeltaT > 0` ⇒ `DISCREPA` · `DeltaT ≤ 0` ⇒ `NULO` |
| Firma del motor | `python3 -B` + numpy 2.4.6 (Python 3.14.7) |
| Acta de cierre | `ACTA_DE_CIERRE_DEL_ENLACE_ACUSTICA_FOTONICA_20261012.md` |

El veredicto **no se re-deriva aquí**: se lee del campo `n_discrepa` / `n_nulo` del
crudo sellado (medido: `n_discrepa = 7`, `n_nulo = 22`).

---

## 2. Instrumentos

| Pieza | Rol | Líneas | `sha256[0:16]` (medido 2026-10-13) |
| --- | --- | --- | --- |
| `sim/sim_acustica2d.py` | el instrumento: solver acústico 2D, `T(nu)` | 626 | `49c429e5cbedc4d0` |
| `sim/driver_enlace_fotonica_acustica.py` | batería del enlace (máscara + control nulo) | 352 | `0a896230fa53d108` |
| `sim/verifica_isomorfismo.py` | verificación del isomorfismo de malla | 196 | `10011010c00dc8d3` |

Blobs citados por el acta (motor distinto: `git hash-object`, SHA-1):
solver `4de2c841e0d6e6b2757c371ef5cca1e4661b646b` (commit `f29879b`) ·
driver `a0ab6ac8b3b14ef42d0b5fad4f9db281a301c6f6` · geometría (commit `b498fcf`).

---

## 3. Reproducción

```sh
python3 -B sim/driver_enlace_fotonica_acustica.py
```

Desde la raíz del repositorio. El driver **no toma argumentos**; resuelve `sim/` por
`__file__` y escribe un crudo **nuevo**, etiquetado con la hora UTC de la corrida, en
`crudos/` — es decir, **no sobrescribe el crudo sellado**. El crudo del enlace lleva:

- **UNIVERSO DECLARADO** impreso antes de toda cifra (objeto · motor · unidad · ventana);
- **PRE-DECLARADO** antes de ver una sola cifra: `sigma_U2` con `ddof = 1`, **con el par
  de control `ddof = 0` impreso al lado** (ninguno se elige después de ver la salida);
- control de convención: el juego completo se corre **además** con las máscaras sin
  transponer. Ese juego **no es un veredicto**: mide que la convención de ejes no es un
  no-op.

La corrida viene del **Paso 3** del protocolo; su pre-registro es
`PREREGISTRO_ACUSTICA_MONOTILE_20261012.md`.

---

## 4. Control de no-regresión C1 (bit a bit)

Sección de control instrumental del acta (§4), no un archivo aparte. El camino **sin
máscara** (`C1b`, `L = 24.0 a`) se compara contra el crudo `C1` sellado
`crudos/crudo_C1_acustica_20261012T072953Z.json`, sobre los **29 bins**:

| Medida | Valor |
| --- | --- |
| `array_equal` | **`True`** |
| `max_abs_dif` | **`0.0`** (bit a bit) |
| `piso_medido_C1` del crudo `C1` | `0.00552322568652841` |
| `T_riz` usado en el umbral del enlace | `0.0055232256865284102` |

El piso **no es un número heredado por prosa**: `T_riz` **es exactamente** el
`piso_medido_C1` del propio instrumento en su configuración homogénea. (Nota de nombre,
ya pagada: la cifra `0.004258596071401777` **no** es un `riz` — su casa medida es
`T_desv_max` / `T_desv_max_por_modo`, la **desviación máxima de `T`**, otra cantidad.)

---

## 5. Qué **no** se afirma (declarado, no adjudicado)

- **Dos denominadores del llenado, separados y no fusionables**: `suma_areas`
  (analítico) · `cobertura_union_U1` (celdas cubiertas) · media de la máscara binaria.
  Se imprimen **los dos**; no se elige.
- **Escala / lectura de `celda`**: no hay conversión declarada entre «unidad» y `a`;
  el mapeo disponible es **celda a celda sobre la ventana completa**. Defecto de ruta de
  lectura **declarado**.
- **Hipótesis sin adjudicar**: la causalidad en baja frecuencia y el rol del *aliasing*
  de borde. Quedan como hipótesis, no como resultado.
- **Cuatro cortes ratificados** aplicados a la redacción del acta (§5), sin archivo aparte.

---

## 6. Custodia de la geometría

`data/geometria_hat/CUSTODIA_SHA256.txt` fija las sumas de la malla binaria del vecino:

- `data/geometria_hat/u1/` — `crudo.json`, `malla_u1_n384_k2.npy`, `malla_u2_n384_k2.npy`
- `data/geometria_hat/u2_semilla_{101..105}/` — 5 realizaciones U2 (mismo par de mallas)

La máscara se transpone **al cargar** (convención del solver: el vecino `malla_hat.py`
indexa fila = `y`, columna = `x`; este solver indexa eje 0 = `x`, eje 1 = `y`).

---

## 7. Estructura del repositorio

```
ACTA_DE_CIERRE_DEL_ENLACE_ACUSTICA_FOTONICA_20261012.md   acta de cierre (fuente de este README)
PREREGISTRO_ACUSTICA_MONOTILE_20261012.md                 pre-registro del Paso 3
crudos/                                                    crudos sellados (.json + .txt)
data/geometria_hat/                                        malla bajo custodia (u1, u2_semilla_101..105)
sim/                                                       solver, driver del enlace, verificador
```

---

## 8. Cita y licencia

- **Cita**: ver `CITATION.cff` (esquema CFF 1.2.0). Metadatos de archivo: `.zenodo.json`.
- **Licencia**: **MIT** — texto en `LICENSE`. Se declara la elección: el paquete admitía
  MIT o Apache-2.0, y se toma la primera.

Repositorio hermano: [`alexisromtz-lab/fotonica-monotile`](https://github.com/alexisromtz-lab/fotonica-monotile)
(origen de la geometría y de la malla dieléctrica).

---

## 9. Fe de erratas e incidencias conocidas

Esta sección es **aditiva**. El acta de cierre
(`ACTA_DE_CIERRE_DEL_ENLACE_ACUSTICA_FOTONICA_20261012.md`, blob `c10d5efba6920a192f890b75fc48effdf1c97054`)
y el preregistro (`PREREGISTRO_ACUSTICA_MONOTILE_20261012.md`, blob `075a05b425e182cf9f5a54edbc86af60e9e13f85`)
son **inmutables** y **no** se editan: lo que sigue es la fe de erratas del paquete.

### 9.1 Errata de plantilla (preregistro, adenda 7.7.a)

El preregistro §7.7.a nombra la plantilla `fdtd2m_tm.py`. **El nombre real es
`fdtd2d_tm.py`** (blob `0d7820a8ea566e403e9528f30945a4a04ff9cbc4`, repositorio hermano
`alexisromtz-lab/fotonica-monotile`). El error está en el nombre citado, no en el blob
ni en la medición.

### 9.2 Valor complementario re-derivado del crudo congelado (sin corridas nuevas)

El criterio del preregistro §7.8 se re-deriva **únicamente** del crudo ya congelado
(`crudos/crudo_ENLACE_ACUSTICA_FOTONICA_20261012T204809Z.json`, commit `03edabb`), sin
reejecutar el solucionador y sin disparar el arnés de pre-escritura: el resultado es
**7 `DISCREPA` / 22 `NULO`**, que **coincide** con los campos `n_discrepa` / `n_nulo`
del propio crudo; el control de convención `ddof = 0` re-deriva **8** y coincide con
`control_ddof0_n_discrepa = 8`.

Descomposición del umbral (medida sobre el mismo crudo): la aportación del piso es
`piso / umbral_max = 1.27687e-03` y la de `3 sigma_U2` cae en `[0.983139, 0.998723]`
=> **el nulo es una cota acotada a su propio denominador** (`3 sigma_U2 + piso`),
dominada por la fluctuación estadística del empaquetamiento aleatorio, no por el piso
instrumental. Se **declara**; no se adjudica.

### 9.3 Contraste `C2`: declarado, **no** derivable de lo congelado

`C2` exige un medio **homogéneo** con `K: 1 -> 0.25`. Medido en el crudo
`crudos/crudo_C1_acustica_20261012T072953Z.json` (commit `d5a7548`): el campo
`reparto_constitutivo` trae `K_mat_declarado_no_usado = 0.25` — **declarado y no
usado** — y las **4** corridas son todas homogéneas con `K_0 = 1.0`. No existe en Git
ninguna corrida con `K != 1` => **`C2` no se puede derivar**: queda **pendiente
declarado** con su condición de entrada (una corrida nueva de medio homogéneo con
`K = 0.25`, `R = -1/3`, `T_amp = 2/3`). **No se ejecuta.**

### 9.4 Advertencia de uso del arnés: camino de lectura de `celda`

El driver del enlace lee la escala declarada de la malla bajo custodia desde una clave
**raíz** que no existe en el crudo de `u1`; por eso el crudo del enlace imprime
`escala_declarada = {'celda_unidades_vecino': None}`. La clave real está **anidada**: en
`data/geometria_hat/u1/crudo.json`, `u1.celda = 0.45782072127145995` y
`u1.lado = 175.80315696824061`.

**Advertencia para replicaciones externas de `v0.1.0`**: no debe leerse un factor de
conversión de la raíz del crudo de `u1`; el mapeo del enlace es **celda a celda sobre la
ventana completa**, y la equivalencia `unidad <-> a` **no está declarada**. Esta sección
**extiende** lo ya dicho en §5 de este README; no lo repite ni lo corrige. El código de
`sim/` **no se modifica** en `v0.1.0`: el acta sellada certifica el árbol bajo el control
C1 bit a bit.

### 9.5 Sendero futuro declarado

El veredicto cierra **este** enlace, no el transporte en aperiodicidad. Se declaran dos
vías: **Cambio de Objeto** (cuasicristales de Penrose y teselados octogonales
Ammann-Beenker, evaluando si una aperiodicidad con simetrías rotacionales prohibidas de
5 u 8 pliegues abate el ruido de dispersión transversal) y **Cambio de Operador**
(resonadores puntuales en los vértices del Hat monotile; el mecanismo pasa de
interferencia destructiva por aperiodicidad pura a apertura de bandgap por hibridación
resonante local, lo que constituye un **objeto físico nuevo** con su propia formulación
analítica y pre-registro independiente). Detalle en
`CIERRE_SENDERO_FUTURO_Y_ERRATA_DOCUMENTADA_20261013.md`.
