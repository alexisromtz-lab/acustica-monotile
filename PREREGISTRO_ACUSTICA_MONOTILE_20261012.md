# PRE-REGISTRO METROLÓGICO: ACÚSTICA 2D Y CRISTALES FONÓNICOS DE MÓDULO (K)

- Casa: `/Users/marlene/acustica-monotile` · rama `main`.
- Autoriza: el dueño, 2026-10-12 (orden ratificada; verbatim en §1).
- Estado: **SELLADO ANTES de la primera corrida del solver acústico de esta casa**.
- Escritura: una sola vez, sobre la semilla vacía
  `e69de29bb2d1d6434b8b29ae775ad8c2e48c5391`, tras certificar PRE-VUELO RC 0 sobre
  esta misma tupla. La primera línea de arriba es la huella del contrato: si ya
  estuviera escrita, este acto no se habría ejecutado (A2.1, RC 11).
- Nota de transcripción: la notación del dueño se cita y se transcribe a ASCII
  (`eps`, `mu`, `rho`, `alfa`, `K`). Se declara la transcripción; no se cita como
  si fuera el objeto.

## 0 · UNIVERSO DECLARADO de este documento

UNIVERSO DECLARADO: **este archivo** (unidad: línea), más los crudos y artefactos
que cita por nombre completo. MOTOR: `bash` + `python3` + `numpy` (el instrumento
del §6 no avanza el tiempo). VENTANA: la hora UTC impresa en cada cierre. Toda
cifra de conteo de este documento caduca al escribirse: **su hora es parte de la
cifra**.

## 1 · La decisión física ratificada (verbatim del dueño)

> «La medición con contraste discrimina lo que el medio homogéneo enmascaraba: el
> mapeo exacto es el Caso B (eps = 1/K, mu = rho, alfa = 1) con v = (-Hy, Hx).
> Haber intentado llamar "densimétrico" a una variación en eps mientras mu = 1
> estaba fijo en el solver era una contradicción física directa.»

Rama ratificada: **(1) Cristal de Módulo/Compresibilidad: K variable, rho = 1
uniforme.**

## 2 · El mapa dual exacto (Caso B)

Par de sistemas, celda por celda, sin avanzar el tiempo:

| EM (Yee TM)                        | ACÚSTICA                          | mapa          |
|------------------------------------|-----------------------------------|---------------|
| dEz/dt = (1/eps) (dx Hy - dy Hx)   | dp/dt  = -K (dx vx + dy vy)       | Ez = p        |
| dHx/dt = -(1/mu) dy Ez             | dvx/dt = -(1/rho) dx p            | Hx = +vy/alfa |
| dHy/dt = +(1/mu) dx Ez             | dvy/dt = -(1/rho) dy p            | Hy = -vx/alfa |

Las tres condiciones de consistencia:

1. `dvx/dt`: `dvx/dt = -alfa dHy/dt = -(alfa/mu) dx p` ⇒ **alfa = mu/rho**.
2. `dvy/dt`: idéntico con signo opuesto ⇒ la misma **alfa = mu/rho**.
3. `dp/dt`: `(1/eps)(dxp Hy - dyp Hx) = -(1/(eps alfa)) (dx vx + dy vy)` ⇒
   **eps alfa = 1/K**.

Con **alfa = mu/rho = 1** (que es lo que exige rho = 1, mu = 1) queda:

    eps = 1/K      mu = rho      alfa = 1      v = (-Hy, Hx)

## 3 · Reparto constitutivo congelado

- **Fondo**: rho_0 = 1.0, K_0 = 1.0 ⇒ mu_0 = 1.0, eps_0 = 1.0 ⇒ c_s,0 = 1.0.
- **Inclusión**: rho = 1.0, K_mat = 0.25 ⇒ mu = 1.0, eps_mat = 4.0 ⇒ c_s = 0.5.
- Contraste: c_s,0 / c_s = **2**; índice acústico n = **2**.
- Impedancia: Z = sqrt(rho K) = sqrt(mu / eps) ⇒ Z_0 = 1.0 y Z_mat = 0.5. La
  inclusión es **más lenta y menos impedante**: es un dispersor, no una inclusión
  adaptada. Se declara aquí porque decide qué debe verse en el campo dispersado.

## 4 · Mapeo en código: cero modificaciones al solver

- `eps` es el **único** arreglo que hay que tocar: `eps = 1/K` da, por la vía del
  código, `inv_eps = 1.0/eps = K` ⇒ **el módulo elástico local entra exactamente
  como el multiplicador de la actualización de E**.
- `mu = rho = 1` ⇒ **no hace falta ningún arreglo `inv_mu`**.
- Antecedente medido en la casa vecina (solo lectura), hoy:

  UNIVERSO DECLARADO: los archivos `.py` de `/Users/marlene/fotonica-monotile`;
  MOTOR = `find` + `grep -c` + `wc -l` + `git hash-object`; UNIDAD = línea;
  VENTANA = **T_UTC=2026-10-12T07:08:10Z**.

  | archivo        | líneas | ocurrencias `inv_eps` | ocurrencias `inv_mu` | blob                                       |
  |----------------|--------|-----------------------|----------------------|--------------------------------------------|
  | `fdtd2d_tm.py` | 472    | **4**                 | **0**                | `0d7820a8ea566e403e9528f30945a4a04ff9cbc4` |

  Contexto: línea 189 `eps = np.ones((nx, ny))` (C1, sin objeto); línea 190
  `inv_eps = 1.0 / eps`; usos en 232, 235 y 238. **`inv_mu` no aparece**: la
  permeabilidad está fijada en 1 y un cristal **densimétrico** no es expresable en
  ese código.

## 5 · La corrección: por qué «densimétrico» era una contradicción física directa

El contrato invertido **A** (eps = rho, mu = 1/K, alfa = (1/K)/rho) no es una
variante del mismo mapeo: **falla O(1) en cuanto hay contraste** (§6), y la
palabra «densimétrico» describía una variación de `eps` con `mu` fijo, es decir un
objeto que ni el mapeo correcto ni el código del solver podían alojar. La lectura
inversa no era una preferencia de notación: era **física falsa**, y por eso el
medio homogéneo —donde las tres asignaciones coinciden— no podía delatarla (§7).

## 6 · Cifras de la corrección (comando, unidad y hora)

UNIVERSO DECLARADO: un modo de Fourier de 32x32 celdas, 12 filas = 3 medios x
(B_ratificado + 2 filas del contrato invertido) + 3 controles positivos.
MOTOR: `python3 -B sim/verifica_isomorfismo.py` (numpy, `np.roll`, sin avanzar el
tiempo). UNIDAD: residuo relativo `max|a-b| / max|b|` **por ecuación**.
VENTANA: **T_UTC=2026-10-12T07:07:44Z** · crudo
`crudos/isomorfismo_20261012T070744Z.txt` · instrumento
`sim/verifica_isomorfismo.py` blob `7781289318130c9dcecbed0a2faabe2ec7b5453d`.

| medio (contraste)                  | fila                    | res_p         | res_vx        | res_vy        |
|------------------------------------|-------------------------|---------------|---------------|---------------|
| uniforme (rho=1, K=1)              | B_ratificado            | 0.000000e+00  | 0.000000e+00  | 0.000000e+00  |
| uniforme                           | A_invertido_alfa1       | 0.000000e+00  | 0.000000e+00  | 0.000000e+00  |
| uniforme                           | A_invertido_alfa_eps_mu | 0.000000e+00  | 0.000000e+00  | 0.000000e+00  |
| uniforme                           | CONTROL_positivo_B_x1.5 | 3.333333e-01  | 0.000000e+00  | 0.000000e+00  |
| densimétrico (rho 1->4, K=1)       | B_ratificado            | 0.000000e+00  | 0.000000e+00  | 0.000000e+00  |
| densimétrico                       | A_invertido_alfa1       | 7.500000e-01  | 7.500000e-01  | 7.500000e-01  |
| densimétrico                       | A_invertido_alfa_eps_mu | 7.688746e+00  | 3.750000e+00  | 3.750000e+00  |
| densimétrico                       | CONTROL_positivo_B_x1.5 | 3.333333e-01  | 0.000000e+00  | 0.000000e+00  |
| módulo (rho=1, K 1->0.25)          | B_ratificado            | 0.000000e+00  | 0.000000e+00  | 0.000000e+00  |
| módulo                             | A_invertido_alfa1       | 7.500000e-01  | 7.500000e-01  | 7.500000e-01  |
| módulo                             | A_invertido_alfa_eps_mu | 1.922187e+00  | 9.375000e-01  | 9.375000e-01  |
| módulo                             | CONTROL_positivo_B_x1.5 | 3.333333e-01  | 0.000000e+00  | 0.000000e+00  |

Cierre del instrumento en esa corrida: `CASO_B_exacto_en_los_tres_medios_y_las_tres_ecuaciones = True` ·
`CONTROL_POSITIVO_max = 3.333333e-01` · `MEDIO_HOMOGENEO_todo_cero = True` ·
`VEREDICTO=VERDE` · `RC=0`.

Lectura: el Caso B es **exacto** (cero de máquina) en los tres medios y en las
tres ecuaciones **mientras hay contraste**; el contrato invertido falla O(1); y el
único medio donde los tres coinciden es el homogéneo.

## 7 · Negativos declarados (lo que este sello NO dice)

1. **No se avanza el tiempo.** El isomorfismo sellado es de las **ecuaciones**.
   La equivalencia numérica bajo el esquema (error de Yee, PML, fronteras) **no**
   queda sellada aquí.
2. **El medio homogéneo no discrimina**: en `uniforme` las tres asignaciones dan
   0.000000e+00. Una validación en medio homogéneo no puede decidir el reparto
   eps/mu, y ese es el defecto que este sello repara.
3. **`eps = 1/K` es bit-exacto sólo para los K usados** (1.0 y 0.25, recíprocos
   exactos). Para un K arbitrario, `1.0/(1.0/K)` no es K: se declara antes de
   usarlo.
4. **La fila A es un contrato refutado**, no «el otro mapeo correcto».
5. **Foto previa conservada.** La primera versión del instrumento salió ROJO
   (`RC=2`) por dos defectos **de ella misma** —le pasaba a la fila B el alfa de
   la fila A, y tomaba el `min` del control positivo cuando el control planta el
   defecto en una sola ecuación— y su crudo se conserva sin borrar:
   `crudos/isomorfismo_20261012T070415Z.txt` (`RC=2`). Sin esa foto, el ROJO no
   se podría volver a medir.
6. **Control negativo del instrumento**: con `alfa` corrido 1e-7 sobre el medio
   uniforme el residuo es 1e-7 ⇒ los ceros de la tabla son ceros, no un
   instrumento muerto.
7. **Nada del solver acústico queda sellado**: `sim_acustica2d.py` **no existe
   todavía** en esta casa.
8. **Este documento no se parchea**: sólo recibe apéndices fechados.

## 8 · Acto siguiente y condición de entrada

Acto: versionar `sim/sim_acustica2d.py` con el mismo patrón de semilla + gate
(A2.1), con `eps = 1/K` como **único** arreglo constitutivo, y correr el acto C1
acústico análogo (nulo en medio homogéneo: piso de ruido con contraste).

Condición de entrada: el Caso B reproducido en casa por el instrumento
**co-locado** (§6, verde) — cumplida.

## 9 · Bitácora de este archivo

- PRE-VUELO A2.1 sobre esta tupla: RC 0 (blob previo
  `e69de29bb2d1d6434b8b29ae775ad8c2e48c5391`, líneas previas 0).
- Escritura única. Post-verificación (líneas, bytes y blob) en el pie del commit.

## §7.7.a Adenda de Retractación y Asiento de Solver (2026-10-12T16:38:42Z)

UNIVERSO DECLARADO: el árbol `~/acustica-monotile` en `HEAD = d5a7548` y las piezas que esta adenda cita; MOTOR = `git hash-object` · `wc -l` · `wc -c` · `git log` · `python3 -B sim/sim_acustica2d.py`; UNIDAD = línea · byte · blob · corrida; VENTANA = reloj UTC de esta cabecera. **No se edita ni se borra ninguna línea anterior** (§7.8): esta adenda sólo agrega.

### §7.7.a.1 Retractación de la fila 7 de §7

La fila 7 de §7 dice: «**Nada del solver acústico queda sellado**: `sim_acustica2d.py` **no existe todavía** en esta casa.» Queda **RETRACTADA por hecho del disco**, sin tocarla: era verdadera hasta la semilla y falsa desde `cad029a`. La línea original se conserva intacta, como su contrato manda.

- Semilla: `fc82307` = `fc823076b00b27efb38961146a62cec586039598` (`init: anclar semilla vacia sim_acustica2d.py`), blob `e69de29bb2d1d6434b8b29ae775ad8c2e48c5391`, 0 líneas / 0 bytes. Gate de esa escritura: RC 0 a las `2026-10-12T07:21:49Z`.

### §7.7.a.2 Linaje del solver y el defecto que sólo la corrida cazó

| rev | commit | blob (16 hex) | líneas | bytes | qué cambió |
|---|---|---|---|---|---|
| v1 | `cad029a` | `8fc9222ec74efcd2` | 542 | 24944 | primera versión: lazo Maxwell 2D TM literal, `inv_eps = K`, `inv_mu = 1` fijo |
| v2 | `b9038c5` | `7ba083989a467f13` | 549 | 25371 | fuera la línea muerta `A1 = float(np.float64(0.0)) * 0.0` y la clave `_marcador`; entra la guarda del lazo |
| v3 | `bb1177b` | `c7688c7dbdeccd49` | 551 | 25538 | **indexación del término en y**: `vy[:, :-1]` → `vy[1:, :-1]` |

- Guarda del lazo (v2), literal: `assert INV_MU == 1.0 and bool(np.all(inv_eps == K))`.
- El defecto de v2 **no era legible en reposo**: la corrida murió con `ValueError: operands could not be broadcast together with shapes (383,383) (384,383)`. El vecino `fdtd2m_tm.py` (blob `0d7820a8ea566e40`) usa `hx[1:, :-1]` en esa línea.
- Gate de la reparación v2→v3: `BLOB_PRE = 7ba083989a467f133a3930f0bed6fc3f8a0f4ab7`, `LINEAS_PRE = 549`, huella `vy[1:, 1:] - vy[1:, :-1]` ⇒ RC 0 a las `2026-10-12T07:29:41Z`.
- Control independiente de que v3 es la forma **consistente** y no un parche que sólo compila: el error de fase medido queda a `0.96`× y `1.05`× del error analítico de dispersión de Yee en la ventana (`1.463133e-03`, `FACTOR_Q4 = 3.0`).

### §7.7.a.3 Piso de ruido de C1, medido

UNIVERSO DECLARADO: las 4 corridas de un crudo; MOTOR = `python3 -B sim/sim_acustica2d.py` (numpy, `np.fft`); UNIDAD = rizado de transmitancia adimensional; VENTANA = `2026-10-12T07:29:53Z` → `2026-10-12T07:30:19Z` (26.374 s de reloj).

| corrida | malla | s | T_media | T_teorico | T_riz | cola_sonda | fase_max |
|---|---|---|---|---|---|---|---|
| C1a 24a | 384x1 | 0.05 | 0.9999071789731048 | 1.0 | 0.005394204639334759 | 0.002784078634789628 | 0.0014045811674006092 |
| C1a 36a | 576x1 | 0.05 | 1.0000553614091023 | 1.0 | 0.004896082438906549 | 0.0026356556228717205 | 0.0013902681561519525 |
| C1b 24a | 384x384 | 6.8 | 0.707449275919397 | 0.7071067811865476 | 0.00552322568652841 | 0.022825810366877947 | 0.001535299592816397 |
| C1b 36a | 576x576 | 19.17 | 0.7072226761898761 | 0.7071067811865476 | 0.0044667919095235376 | 0.022825810375721022 | 0.0015219279413155595 |

- **Piso nativo medido**: `PISO_DE_RUIDO_riz_T_max = 0.00552322568652841` (0.55 %). `identidad_inv_eps_en_todas_las_corridas = True` en las cuatro configuraciones.
- `T_media` reproduce `1.000000` (C1a) y `sqrt(8/16) = 0.7071068` (C1b) hasta la tercera cifra: la sonda a distancia absoluta `16a` no cambia con `L` (`pico_sonda` idéntico por modo).
- `riz(lnA) = 0.384547 / 0.384425` **no es ruido**: es la ley cilíndrica `r^(-1/2)` leída en `r_2 = 2 r_1` (teórico `1/sqrt(2) = 0.7071068`; medido `0.707449 / 0.707223`). En `ln A` el factor entra como offset constante y el rizado de `T` lo cancela ⇒ **diagnóstico, no piso**.
- Crudo: `crudos/crudo_C1_acustica_20261012T072953Z.json` y `.txt`, sha16 `f8bf85b2370e4d50` / `f21aec4d0229dbc5`, commit `d5a75488d2b8c5f601f7a6c1d4be7d6c22cc4b18`; `sha16_script = 84721caf685985b3`.
- **Abierto, sin adjudicar** (ningún umbral de este crudo lo cubre): `cola_dominio` de C1b crece con el dominio (`7.727917669443574e-03` en 24a → `3.292129244455513e-02` en 36a) y el máximo final de C1b 36a cae en la celda `(552, 48)` = `+32.50 a` del manantial, borde externo de la PML. Se declara, no se adjudica.

### §7.7.a.4 Techo nativo (primero de esta casa)

- `riz(T) <= 0.010` — techo de rizado admisible para este instrumento, declarado sobre el piso medido. Aritmética declarada: `0.010 / 0.00552322568652841 = 1.8105`× (la orden lo enunció como «factor 2× sobre 0.0055»; el factor exacto sobre el piso medido es 1.81×, y así se sella).
- Regla que viaja con él: un contraste posterior de `K` heterogéneo **sólo** cuenta si su variación respecto al fondo **supera 0.55 %**.
- `ANALOGO_PRESTADO_Q1..Q4` (umbral `0.05`, `FACTOR_Q4 = 3.0`) siguen siendo **prestados de `fotonica-monotile`**: referencia provisional, **no** sellos de esta casa. El único sello nativo es el techo de arriba.

### §7.7.a.5 Bitácora de esta adenda

- Gate A2.1 sobre esta tupla: `TARGET` = este archivo, `BLOB_PRE = 5753f973608d41d60e5d269275e5b06891ce97bf`, `LINEAS_PRE = 163`, huella `Adenda de Retractación y Asiento de Solver` (la cabecera sin su nivel markdown) ⇒ **RC 0** a las `16:13:50Z`.
- Escritura única y aditiva; §0–§9 intactos. Post-verificación (líneas, bytes, blob, `^#+`, `§7`) en el cuerpo del commit.
