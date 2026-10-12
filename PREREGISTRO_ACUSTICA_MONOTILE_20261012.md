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
