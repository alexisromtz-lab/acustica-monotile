# CIERRE DEL ENLACE ACUSTICA-MONOTILE — SENDERO FUTURO DECLARADO Y ERRATA DOCUMENTADA

UNIVERSO DECLARADO: el arbol `~/acustica-monotile` en `HEAD = 0b39c72` y las piezas
que este documento cita; MOTOR = `git hash-object` · `wc -l` · `wc -c` · `git log`
· `python3 -B` (numpy 2.4.6, Python 3.14.7); UNIDAD = linea · byte · blob · bin ·
corrida; VENTANA = reloj UTC `2026-10-13T02:15:31Z` -> `2026-10-13T02:47:00Z`.
Este documento es **aditivo y autonomo**: **no** edita el acta sellada, **no** toca
una sola linea de `sim/`, y **no** reabre la verificacion de integridad del arbol.

---

## 0. Que cierra este documento (y que NO toca)

Cierra la **documentacion** del enlace `fotonica-monotile -> acustica-monotile` una
vez asentado su veredicto (`7 DISCREPA` / `22 NULO`, acta `6a1fc1b`), y declara el
**sendero futuro** de este frente. Los cuatro pendientes que el acta dejo fuera
(acta §7) entran aqui como **notas tecnicas y erratas de documentacion**, no como
reejecuciones.

Lo que este documento **no** hace, por orden expresa del dueno:

- **no** modifica `sim/sim_acustica2d.py`, `sim/driver_enlace_fotonica_acustica.py`
  ni `sim/verifica_isomorfismo.py`;
- **no** reabre el arnes A2.1 sobre el experimento cerrado;
- **no** edita `ACTA_DE_CIERRE_DEL_ENLACE_ACUSTICA_FOTONICA_20261012.md` (inmutable:
  una hipotesis nueva es un **documento nuevo**, nunca una edicion del acta);
- **no** corre el solucionador. Todo valor complementario de §2 se deriva de los
  **crudos ya congelados en Git**.

### 0.1 Declaracion de reconciliacion (declarar, no adjudicar)

La orden dice «deja el arbol intacto en `6a1fc1b`». Medido hoy: `HEAD = 0b39c72`,
**exactamente un commit por encima** de `6a1fc1b5788e4809ce269ce2b1aa75c40aeda392`.
El commit de mas es `chore(empaque): metadatos de publicacion (README, CITATION.cff,
.zenodo.json, LICENSE MIT, .gitignore)` -> `5 files changed, 234 insertions(+)`.

Los cuatro blobs certificados por el acta siguen **byte a byte identicos** en disco y
en `HEAD`:

| pieza | blob | lineas / bytes |
|---|---|---|
| `ACTA_DE_CIERRE_DEL_ENLACE_ACUSTICA_FOTONICA_20261012.md` | `c10d5efba6920a192f890b75fc48effdf1c97054` | 201 / 12171 |
| `sim/sim_acustica2d.py` | `4de2c841e0d6e6b2757c371ef5cca1e4661b646b` | 626 / 29468 |
| `sim/driver_enlace_fotonica_acustica.py` | `a0ab6ac8b3b14ef42d0b5fad4f9db281a301c6f6` | 352 / 14531 |
| `PREREGISTRO_ACUSTICA_MONOTILE_20261012.md` | `075a05b425e182cf9f5a54edbc86af60e9e13f85` | 261 / 18503 |

=> **el contenido certificado esta intacto**; lo que hay encima es una **capa de
documentacion** (README, cita, licencia, metadatos de archivo). Se declara el desfase
de la referencia de la orden; **no se adjudica** quien lo movio, y **no se revierte**:
el acto correcto es **parchear el `README.md` existente**, que es lo que hace §3.

---

## 1. Los cuatro pendientes del acta §7 y su tratamiento

| # | pendiente (acta §7) | tratamiento en este cierre | donde vive |
|---|---|---|---|
| 1 | Errata de plantilla: el preregistro §7.7.a nombra `fdtd2m_tm.py` | **errata documentada**; el acta y el preregistro **no se editan** (append-only) | `README.md` §9.1 y §2.1 aqui |
| 2 | Ejecucion de `U2_ac` (§7.8) | **ya evaluada**: es el vector oficial. Se **re-deriva** del crudo congelado y se descompone su umbral | §2.1 aqui · `README.md` §9.2 |
| 3 | Contraste `C2` (`K: 1 -> 0.25`) | **no derivable** de los crudos congelados (medido, §2.3). Queda **declarado pendiente** con su condicion de entrada; **no se corre** | §2.3 aqui · `README.md` §9.3 |
| 4 | Camino de lectura de `celda` en `abre(...)` | **advertencia de uso del arnes** para replicaciones externas de `v0.1.0` | `README.md` §9.4 (extiende §5 del README, no la duplica) |

---

## 2. Valores complementarios derivados de los crudos congelados (sin corridas nuevas)

### 2.1 `U2_ac` es el vector oficial: re-derivado, no re-ejecutado

UNIVERSO DECLARADO: las 29 filas del crudo
`crudos/crudo_ENLACE_ACUSTICA_FOTONICA_20261012T204809Z.json` (26278 B, commit
`03edabb`); MOTOR = `python3 -B` leyendo las claves `T_U1`, `media_T_U2`,
`sigma_U2_ddof1`, `sigma_U2_ddof0`, `piso_declarado_en_el_crudo_C1`,
`declarado_antes_de_medir.factor`; UNIDAD = bin; VENTANA = `2026-10-13T02:44Z`.

Criterio (el que §7.8 define, sin bajarlo despues de ver la salida):

```
abs( T_U1(nu) - media_T_U2(nu) )  >  factor * sigma_U2(nu)  +  piso
factor = 3.0   piso = 0.00552322568652841
```

Resultado de la re-derivacion: **`DISCREPA = 7` · `NULO = 22`**, y la comparacion
contra los campos `n_discrepa` / `n_nulo` del propio crudo da **coincide = `True`**.
El control de convencion `ddof = 0` re-derivado da **`DISCREPA = 8`**, y coincide con
`control_ddof0_n_discrepa = 8` del crudo.

Los 7 bins `DISCREPA` (indice, `nu`, `DeltaT`):

| i | nu (c/a) | DeltaT |
|---|---|---|
| 0 | 0.152711 | 7.119198e-01 |
| 1 | 0.166594 | 7.589029e-01 |
| 3 | 0.194360 | 8.292831e-01 |
| 7 | 0.249892 | 1.041552e-01 |
| 14 | 0.347072 | 5.113238e-03 |
| 16 | 0.374837 | 3.497561e-01 |
| 24 | 0.485900 | 1.569740e+00 |

**Ninguna corrida nueva. Ningun disparo del arnes A2.1 por este §2.1.**

### 2.2 El nulo es una cota de **su propio denominador**

El mismo crudo permite descomponer el umbral fila a fila. Medido (misma VENTANA):

- aportacion del piso: `piso / umbral_max = 1.27687e-03`;
- aportacion de `3 · sigma_U2`: `3 sigma_U2 / umbral` en `[0.983139, 0.998723]`.

=> el umbral esta dominado por **la fluctuacion estadistica del empaquetamiento
aleatorio** (>= 98.31 % de su propio valor), no por el piso instrumental
(<= 0.128 %). La lectura correcta del `NULO` es por tanto la que el dueno fijo:

> el nulo **no** es una refutacion metafisica del transporte en aperiodicidad, sino una
> **cota acotada a su propio denominador** (`3 sigma_U2 + piso`), donde domina la
> fluctuacion estadistica del empaquetamiento aleatorio.

Esto **no** rebaja el veredicto: lo **acota**. Un nulo cuyo denominador es la
dispersion de 5 realizaciones barajadas mide **que esta estructura no se separa del
desorden**, no **que no haya transporte**.

### 2.3 Contraste `C2` — declarado, **no** derivable de lo congelado (medido)

`C2` pide un medio **homogeneo** con `K: 1 -> 0.25` (`R = -1/3`, `T_amp = 2/3`,
aritmetica declarada) contra el techo nativo `riz(T) <= 0.010` y la regla del
`0.55 %`.

Medido en el crudo congelado `crudos/crudo_C1_acustica_20261012T072953Z.json`
(commit `d5a7548`), campo `reparto_constitutivo`:

```
rho_0 = 1.0   K_0 = 1.0   c_s_0 = 1.0   Z_0 = 1.0
K_mat_declarado_no_usado = 0.25     <-- declarado y NO USADO
eps_mat_declarado_no_usado = 4.0    c_s_mat_declarado_no_usado = 0.5
Z_mat_declarado_no_usado = 0.5      inv_mu_fijo = 1.0
```

y las **4** corridas del crudo (`L=24 C1a`, `L=36 C1a`, `L=24 C1b`, `L=36 C1b`) son
todas **homogeneas con `K_0 = 1.0`**. Ninguna tiene `K != 1`.

=> **`C2` NO se puede derivar de los crudos congelados**: exigiria una corrida de
medio homogeneo con `K = 0.25` que **no existe** en Git. Se registra **declarado**
con su condicion de entrada y **no se ejecuta** (orden: no correr el solucionador,
no disparar A2.1). Traducir `K_mat_declarado_no_usado` a un valor medido seria
**tomar el mapa por el territorio**: el propio crudo dice `no_usado`.

---

## 3. Sendero futuro declarado

El veredicto cierra **este** enlace (geometria Monotile Hat con aperiodicidad pura,
`rho = 1`, `inv_mu = 1`). No cierra el transporte en aperiodicidad. El sendero que se
declara tiene **dos vias**, y la segunda **no es una variante de este experimento**.

### Via 1 — Cambio de Objeto (mismo operador, distinto muro)

Trasladar el solucionador y el metro a **cuasicristales de Penrose** o **teselados
octogonales (Ammann-Beenker)**. Se evalua si una **aperiodicidad con simetrias
rotacionales prohibidas (5 u 8 pliegues)** abate el **ruido de dispersion
transversal** frente al **ensamble desordenado** que aqui domina el denominador.

Punto de apoyo medido en este cierre: el denominador del umbral es hoy
`3 sigma_U2 + piso` con `3 sigma_U2 / umbral >= 0.983139`, es decir **el muro que
freno el enlace es la dispersion del barajado**, no el piso. Via 1 ataca
directamente ese termino.

Se declara lo que Via 1 **no** aporta: **mismo operador, mismo instrumento, mismos
metros**; si el objeto cambia, el pre-registro de la ventana `nu`, del numero de
realizaciones y del umbral debe **re-sellarse antes de la primera cifra**, con la
misma doctrina (`declarar antes de medir`).

### Via 2 — Cambio de Operador (mismo objeto, nueva fisica)

Incorporar **resonadores puntuales en los vertices del Hat monotile**. El mecanismo
fisico deja de ser **interferencia destructiva por aperiodicidad pura** y pasa a ser
**apertura de bandgap por hibridacion resonante local**.

> Esto constituye un **objeto fisico nuevo** y exigira su propia formulacion
> analitica y pre-registro independiente.

Consecuencias que se declaran desde ya, sin medirlas:

- Via 2 **no** hereda el veredicto de este enlace: otro operador es **otra ecuacion**;
- Via 2 **no** puede reutilizar el techo nativo `riz(T) <= 0.010` sin re-medirlo,
  porque un resonador introduce **perdidas y fase propia** que el solver actual no
  contiene;
- Via 2 **si** puede reutilizar la **geometria bajo custodia**
  (`data/geometria_hat/`, commit `b498fcf`) y el linaje del solver documentado en
  el preregistro §7.7.a.2 (`v1 cad029a -> v2 b9038c5 -> v3 bb1177b`), que es el
  activo transferible de este frente.

### 3.1 Por que las dos vias no se funden

| | Via 1 | Via 2 |
|---|---|---|
| objeto (muro) | **cambia** (Penrose / Ammann-Beenker) | **no cambia** (Hat) |
| operador (fisica) | **no cambia** (Helmholtz, `inv_mu = 1`) | **cambia** (resonadores) |
| que se mide | el mismo metro sobre otro muro | otro metro sobre el mismo muro |
| veredicto heredado | no (re-sellar ventana y umbral) | no (otra ecuacion) |

Fundirlas seria el defecto que este frente ya pago una vez: **sumar cifras de distinta
clase en una sola fila**.

---

## 4. Incidencia de arnes (documentacion de herramienta)

El arnes A2.1 (`tools/gate_pre_escritura.sh`, 80 lineas) evalua la presencia del
objetivo **antes** que el estado de git, y por eso un destino **ausente** corta con
`RC 10` sin consultar nunca su `BLOB_PRE`. En este ciclo el `RC 13` (estado sucio)
se diagnostico antes de la comprobacion de presencia.

- `RC` observados en este ciclo: **`10`** pre-escritura sobre destino **ausente** ·
  **`0`** pre-escritura sobre destino **existente y limpio** · **`11`** post-escritura
  (huella presente: cero escrituras).
- **Guardian canonico declarado: el invariante de blob (`git hash-object`) pre/post**,
  no la comprobacion de huella por linea (que perdio su salto de linea final via
  `tr -d '\n'`).
- La comprobacion de huella debe apuntar al **objeto cabecera** del texto nuevo, nunca
  a un token desnudo: un token suelto puede habitar en el destino por otra mano y
  producir una colision falsa.

Se **declara**; no se repara aqui, y no se reabre el arnes sobre el experimento cerrado.

---

## 5. Bitacora de este documento

- **Pre-vuelo A2.1 sobre este destino (ausente)**: `TARGET =
  CIERRE_SENDERO_FUTURO_Y_ERRATA_DOCUMENTADA_20261013.md` => `RC 10` (`COLISION: ...
  no existe.`), que es el **pre-estado esperado** de un destino nuevo.
- **Pre-vuelo A2.1 sobre el `README.md`**: `BLOB_PRE = 949c4e014f93dc0a49c4609106
  db92146b107304`, `LINEAS_PRE = 132`, huella `## 9. Fe de erratas e incidencias
  conocidas` (ausente hoy: `grep -cF` = `0`) => **`RC 0`**.
- Escritura unica y aditiva en los dos destinos. Post-verificacion (lineas, bytes,
  blob, `^#+`, signos monetarios) en el cuerpo del commit.
- **Cero signos monetarios** en el texto escrito; el acta sellada y el preregistro
  quedan **sin editar**, y los cuatro blobs certificados de §0.1 siguen byte a byte
  identicos.
