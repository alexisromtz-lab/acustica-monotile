#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SOLVER ACUSTICO 2D (CASO B: K VARIABLE, RHO=1)
"""acustica-monotile · acto C1 · solver acustico 2D (p, vx, vy) + piso de ruido.

HUELLA DEL CONTRATO
  `# SOLVER ACUSTICO 2D (CASO B: K VARIABLE, RHO=1)` escrita una sola vez sobre
  la semilla vacia `e69de29bb2d1d6434b8b29ae775ad8c2e48c5391` (commit `fc82307`),
  tras PRE-VUELO A2.1 RC 0 sobre esa misma tupla.

UNIVERSO DECLARADO (se imprime antes de toda cifra)
  unidades normalizadas a = 1, c_s = 1, rho_0 = 1, K_0 = 1; frecuencia reducida
  nu = omega a / (2 pi c_s); malla Yee 2D (p, vx, vy) con dx = dy = a/16;
  Courant S = c_s dt/dx = 0.5 (limite 2D 1/sqrt(2) = 0.7071); capa absorbente PML
  de campo partido de 20 celdas por borde, sigma(u) = sigma_max u^3 con
  u = (d-i)/d, sigma_max = -(orden+1) c ln(R0)/(2 d), R0 = 1e-6, d = 1.25 a;
  fuente = pulso gaussiano sigma = 0.5 a/c_s, t0 = 3 sigma, termino BLANDO PUNTUAL
  en la ecuacion de p en (i = 2a, j central); sondas en columnas de posicion
  ABSOLUTA d = 8a y d = 16a sobre la fila central (al crecer L el dominio solo se
  alarga hacia la derecha); ventana de medida nu en [0.15, 0.55] (el borde bajo lo
  fija que la sonda cercana quede a >= 1 lambda); T_total = 72 a/c_s, Nt = 2304
  pasos, dnu = 1/T_total; doble precision; motor numpy; unidad de conteo = celda;
  medio HOMOGENEO (K = 1, rho = 1 -> c_s = 1): en C1 NO hay objeto.

EL MAPA DUAL (pre-registro de esta casa, §2, Caso B, ratificado por el dueno)
  EM (Yee TM)                        ACUSTICA                        mapa
  dEz/dt = (1/eps)(dx Hy - dy Hx)    dp/dt  = -K (dx vx + dy vy)     Ez = p
  dHx/dt = -(1/mu) dy Ez             dvx/dt = -(1/rho) dx p          Hx = +vy/alfa
  dHy/dt = +(1/mu) dx Ez             dvy/dt = -(1/rho) dy p          Hy = -vx/alfa
  Consistencia: alfa = mu/rho y eps alfa = 1/K. Con alfa = mu/rho = 1 queda
  eps = 1/K, mu = rho, v = (-Hy, Hx).

POR QUE EL LAZO ES LITERALMENTE EL DE MAXWELL 2D TM
  Sustituyendo Hy = -vx y Hx = +vy en las tres actualizaciones del vecino, con
  eps = 1/K (o sea inv_eps = K) y mu = rho = 1:
    vx = ax_v vx - bx_v INV_MU dx p        (el signo menos cae solo de Hy = -vx)
    vy = ay_v vy - by_v INV_MU dy p
    px = ax_e px - bx_e inv_eps dx vx      (el menos sale de hy = -vx)
    py = ay_e py - by_e inv_eps dy vy
  Son las mismas operaciones, en el mismo orden y con los mismos coeficientes de
  PML que el vecino. Los unicos cambios son de nombre: ez -> p (con su particion
  px + py), hy -> -vx, hx -> +vy. INV_MU = 1.0 entra explicito en las dos
  actualizaciones de velocidad (x * 1.0 es bit-exacto en IEEE-754: no mueve un
  solo bit).

QUE MIDE C1 (dos sub-corridas, ambas a L = 24a y L = 36a)
  Dominio HOMOGENEO K = 1 con la misma malla, paso, PML, fuente y sondas. No hay
  objeto. Entrega:
    A(L, nu)  = |FFT(sonda)| / |S(omega)|   con |S| = exp(-sigma^2 omega^2 / 2)
    T(nu)     = A(16a)/A(8a)   TRANSMITANCIA entre las dos sondas de la MISMA
                corrida (ley 2D: sqrt(8/16) = 0.7071 · en 1D: 1.0000)
    riz       = max_nu |ln T - media_nu ln T|  -> PISO DE RUIDO del instrumento
    delta     = max_nu |ln A(36a) - ln A(24a)| -> deriva espuria con L
    cola      = max|sonda|(t >= 24 a/c_s) / pico          -> piso de reflexion
    cola_dom  = max_dominio|p|(t >= 42 a/c_s) / pico      -> residuo fuera de las
                sondas, medido cuando el pulso primario YA salio del dominio
                (t >= 1.17 x 36 a/c_s). Su celda, su paso n y el maximo final se
                exportan para LOCALIZARLO.
  ESCALA DE A: A no lleva la constante del pulso (sigma sqrt(2 pi)) ni la amplitud
  emitida; su escala ABSOLUTA no esta calibrada. Todas las predicciones usan
  cociente entre sondas, diferencia de logaritmos o fase -> inmunes al factor
  constante y a la forma de |S| que se use.
  Por que la planitud se mide sobre T y NO sobre A: en 2D la onda cilindrica
  impone a A un descenso sistematico ~ nu^(-1/2); su desviacion de la media vale
  ~0.32 y NO es ruido del instrumento, es la ley del objeto. Medir la planitud
  sobre A seria ROJO POR CONSTRUCCION en cualquier instrumento correcto. El
  cociente entre las DOS sondas de la MISMA corrida cancela la normalizacion de la
  fuente y la tendencia geometrica, y deja lo unico que le importa a una medida de
  decaimiento: el rizo.
  C1a = cuasi-1D (ny=1, PML SOLO en x, onda plana): aqui vive la dispersion
  numerica, comparable EXACTA con la formula de Yee, y el piso de reflexion mas
  afilado. C1b = 2D real (ny=nx, PML en los cuatro bordes, fuente puntual): aqui
  viven el reparto cilindrico y la dependencia espuria con L en la geometria que
  el objeto va a usar.
  Complemento ANALITICO de la malla de Yee (mismo estencil):
    sin(omega dt/2) = S sin(k dx/2)   ->  v_p = omega/k  ->  error de fase.
  El error de fase MEDIDO sale de la diferencia de fase entre las dos sondas
  (k = fase / delta_d) con la convencion de rama declarada: m se elige una sola
  vez en el primer punto de la ventana.

SELLOS Y PRESTAMOS (leer antes de citar cualquier VERDE de este crudo)
  Las cuatro predicciones Q1..Q4 y el umbral 0.05 son de la CASA VECINA
  (`fotonica-monotile/PREREGISTRO_INSTRUMENTO_FDTD_20261012.md` §3/§6) y NO estan
  selladas en esta casa. Se imprimen rotuladas como ANALOGO PRESTADO: el sello de
  acustica (pre-registro §8) pide el NULO en medio homogeneo, o sea el PISO DE
  RUIDO, y ese piso es la cifra `riz` de aqui. Un VERDE prestado no es un sello.
  Negativo declarado (pre-registro §7.3): `inv_eps = 1.0/eps = K` es bit-exacto
  solo para los K recíprocos exactos (1.0 y 0.25). Para un K arbitrario no lo es;
  el crudo imprime la comprobacion de esa identidad en la malla de C1.

REGLA DURA
  Un decaimiento solo cuenta POR ENCIMA de este piso. Si C1 no es plano se para y
  se repara el instrumento ANTES de medir el objeto.

Uso:
  python3 -B sim/sim_acustica2d.py
  python3 -B sim/sim_acustica2d.py --json

CAPACIDAD NUEVA (Paso 3 del enlace fotonica-monotile -> acustica-monotile)
  `correr(L_a, modo, mascara=None)`. Con `mascara` binaria (n, n) cargada de la
  custodia (`data/geometria_hat/<realizacion>/malla_{u1,u2}_n<N>_k2.npy`, commit
  b498fcf) el modulo local pasa a ser K(x,y) = K_fondo + (K_mat - K_fondo) m(x,y)
  con K_fondo = 1.0 y K_mat = 0.25, y el resto del reparto intacto: eps = 1/K,
  inv_mu = 1.0 en toda la malla. La mascara se TRANSPONE al cargarla (el vecino
  indexa fila = y, columna = x; este solver indexa eje 0 = x, eje 1 = y) y el
  crudo imprime el par de control de esa convencion.
  Con `mascara=None` el solver es el de C1 y no se movio un bit: el nulo del
  instrumento no cambia al ganar la capacidad (se comprueba re-corriendo C1b a
  L = 24a contra el crudo commit `d5a7548`).
"""
from __future__ import annotations

import hashlib
import json
import math
import sys
import time
from pathlib import Path

import numpy as np

# ------------------------------------------------------------------ declarado
C = 1.0
A = 1.0
DX = A / 16.0
DY = DX
S = 0.5                      # Courant = c_s dt / dx
DT = S * DX / C
PML_CELDAS = 20
PML_ORDEN = 3
PML_R0 = 1.0e-6
SIGMA = 0.5
T0 = 3.0 * SIGMA
I_FUENTE = int(round(2.0 * A / DX))
D_SONDAS = (8.0 * A, 16.0 * A)
L_LISTA = (24.0 * A, 36.0 * A)
MODOS = ("C1a", "C1b")
NU_MIN = 0.15
NU_MAX = 0.55
T_TOTAL = 72.0
FACTOR_Q4 = 3.0
T_COLA_MIN = 24.0
T_COLA_DOM = 42.0

# --- reparto constitutivo congelado (pre-registro §3, Caso B) ---
RHO = 1.0
K_FONDO = 1.0
K_MAT = 0.25                 # NO se usa en C1: C1 es homogeneo (nulo). Declarado.
INV_MU = 1.0                 # mu = rho = 1 fijo (pre-registro §4: no hay arreglo inv_mu)
K_C1 = K_FONDO               # C1 = medio HOMOGENEO, sin objeto
UMBRAL_PRESTADO = 0.05       # PRESTADO de la casa vecina; NO sellado en esta casa

AQUI = Path(__file__).resolve().parent
CRUDOS = AQUI.parent / "crudos"
GEO = AQUI.parent / "data" / "geometria_hat"     # custodia del enlace (Paso 1/2)
REALIZACIONES = (
    "u1",
    "u2_semilla_101",
    "u2_semilla_102",
    "u2_semilla_103",
    "u2_semilla_104",
    "u2_semilla_105",
)

UNIVERSO = (
    "unidades normalizadas a=1, c_s=1, rho_0=1, K_0=1; nu = omega a/(2 pi c_s); "
    f"malla Yee (p,vx,vy) dx=dy=a/16 ({DX:g}); Courant S={S} (limite 2D "
    f"{1/math.sqrt(2):.4f}); PML campo partido {PML_CELDAS} celdas/borde, "
    f"sigma_max = -(orden+1)c ln(R0)/(2d) con orden={PML_ORDEN}, R0={PML_R0:g}, "
    f"d={PML_CELDAS * DX:g} a; fuente = pulso gaussiano sigma={SIGMA} a/c_s, t0={T0} a/c_s, "
    f"termino blando puntual en la ecuacion de p en (i={I_FUENTE}, j=central); sondas en "
    f"posicion ABSOLUTA d={D_SONDAS[0]:g}a y d={D_SONDAS[1]:g}a; L en "
    f"{L_LISTA[0]:g}a y {L_LISTA[1]:g}a; ventana nu en [{NU_MIN}, {NU_MAX}] (el borde "
    f"bajo lo fija que la sonda cercana quede a >= 1 lambda: 1/{NU_MIN} = "
    f"{1.0/NU_MIN:.2f} a); T_total={T_TOTAL} a/c_s, Nt={int(round(T_TOTAL/DT))}, "
    f"dnu={1.0/T_TOTAL:.4f}; umbral de planitud = {UMBRAL_PRESTADO} sobre T = "
    "A(16a)/A(8a) de la MISMA corrida (PRESTADO de la casa vecina, NO sellado aqui); "
    f"cola de sonda desde t >= {T_COLA_MIN:g} a/c_s y residuo de dominio desde "
    f"t >= {T_COLA_DOM:g} a/c_s medido SOLO en el interior fisico (celdas de la PML "
    "excluidas: ahi el maximo es la onda incidente entrando al absorbente, no un "
    "residuo); doble precision; medio HOMOGENEO K=1, rho=1 -> c_s=1 (NO hay objeto "
    "en C1); motor numpy; unidad de conteo = celda; dos sub-corridas: C1a = cuasi-1D "
    "(ny=1, PML solo en x, onda plana -> aqui vive la dispersion numerica, comparable "
    "EXACTA con la formula de Yee) y C1b = 2D real (ny=nx, PML en los cuatro bordes, "
    "fuente puntual -> aqui viven el reparto cilindrico y la dependencia espuria con L)"
)


def t_utc() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


# ------------------------------------------------------------------ instrumento
def perfil_sigma(n: int, celdas: int) -> np.ndarray:
    """Conductividad de la PML por nodo: sigma = sigma_max u^orden, u = (d-i)/d."""
    celdas = min(celdas, n // 2)
    s = np.zeros(n, dtype=np.float64)
    if celdas <= 0:
        return s
    d = celdas * DX
    smax = -(PML_ORDEN + 1) * C * math.log(PML_R0) / (2.0 * d)
    for k in range(celdas):
        u = (celdas - k) / float(celdas)
        s[k] = smax * u ** PML_ORDEN
        s[n - 1 - k] = s[k]
    return s


def coef_pml(sig: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Diferencia exponencial: a = exp(-sigma dt), b = (1-a)/sigma (b -> dt si sigma=0)."""
    a = np.exp(-sig * DT)
    b = np.where(sig > 0.0, (1.0 - a) / np.where(sig > 0.0, sig, 1.0), DT)
    return a, b


def fuente(t: float) -> float:
    return math.exp(-((t - T0) ** 2) / (2.0 * SIGMA ** 2))


def espectro_fuente(nu: np.ndarray) -> np.ndarray:
    om = 2.0 * math.pi * nu
    return np.exp(-(SIGMA ** 2) * om ** 2 / 2.0)


def yee_error_fase(nu: np.ndarray) -> np.ndarray:
    """(1/dt)^2 sin^2(omega dt/2) = (1/dx)^2 [sin^2(kx dx/2)+sin^2(ky dy/2)]
    sobre el eje: sin(k dx/2) = sin(omega dt/2)/S ; v_p = omega/k."""
    om = 2.0 * math.pi * nu
    arg = np.sin(om * DT / 2.0) / S
    arg = np.clip(arg, -1.0, 1.0)
    k = 2.0 * np.arcsin(arg) / DX
    vp = np.divide(om, k, out=np.ones_like(om), where=(k > 0))
    return vp / C - 1.0


# MAPEO CONSTITUTIVO CASO B: HETEROGENEIDAD K(x,y) DESDE MASCARA BINARIA
# (Paso 3 del protocolo de enlace fotonica-monotile -> acustica-monotile.)
# La mascara binaria m(x,y) vive bajo custodia en data/geometria_hat/ (Paso 1/2,
# commit b498fcf) con su CUSTODIA_SHA256.txt; el mapeo es el del reparto
# congelado (§3/§4, Caso B) y NO toca el resto de la actualizacion:
#     K(x,y) = K_fondo + (K_mat - K_fondo) * m(x,y)    K_fondo=1.0  K_mat=0.25
#     eps = 1/K        inv_eps = 1/eps        inv_mu = 1.0 en toda la malla
# Con K en {1.0, 0.25} los dos reciprocos son EXACTOS (1/1.0 y 1/0.25), luego la
# identidad inv_eps == K es bit-exacta (negativo declarado, §7.3: vale para K
# reciproco exacto, no para un K arbitrario).
# CONVENCION DE EJES (declarada; medida en el vecino `malla_hat.py:513-544`):
#   rasterizar() devuelve union[i, j] con i = indice de y (filas, de py) y j =
#   indice de x (columnas, de px), porque meshgrid(xs, ys) pone la fila en y y
#   los margenes i0/i1 salen de py con j0/j1 de px. Este solver indexa K[i, j]
#   con i = x (eje 0) y j = y (eje 1). Luego m se TRANSPONE al cargar.
#   Control en el crudo: union.T != union. La transposicion NO es un no-op: no
#   se puede elegir la convencion sin declararla.
def cargar_mascara(realizacion: str, n: int) -> np.ndarray:
    """Mascara binaria bajo custodia -> float (n, n) ya en ejes del solver."""
    nombre = "u1" if realizacion == "u1" else "u2"
    ruta = GEO / realizacion / f"malla_{nombre}_n{n}_k2.npy"
    if not ruta.is_file():
        raise SystemExit(f"mascara ausente bajo custodia: {ruta}")
    m = np.load(ruta)
    if m.shape != (n, n):
        raise SystemExit(f"{ruta.name}: forma {m.shape}, se esperaba ({n}, {n})")
    if not bool(np.all((m == 0) | (m == 1))):
        raise SystemExit(f"{ruta.name}: la mascara no es binaria")
    return np.ascontiguousarray(m.T, dtype=np.float64)


def correr(L_a: float, modo: str, mascara: np.ndarray | None = None) -> dict:
    nx = int(round(L_a / DX))
    ny = 1 if modo == "C1a" else nx
    if mascara is None:
        K = np.full((nx, ny), K_C1, dtype=np.float64)  # C1: homogeneo (nulo)
        es_heterogeneo = False
        fraccion_mascara = None
    else:
        # heterogeneidad K(x,y): ver el bloque "mapeo constitutivo" de arriba
        m = np.asarray(mascara, dtype=np.float64)
        if m.shape != (nx, ny):
            raise SystemExit(
                f"mascara {m.shape} no casa con la malla ({nx}, {ny}) de L={L_a:g}a"
            )
        K = K_FONDO + (K_MAT - K_FONDO) * m
        es_heterogeneo = True
        fraccion_mascara = float(m.mean())
    eps = 1.0 / K                                  # UNICO arreglo constitutivo
    inv_eps = 1.0 / eps                            # = K por la via del codigo
    inv_mu = np.full((nx, ny), INV_MU, dtype=np.float64)   # mu = rho = 1 fijo
    identidad_inv_eps = bool(np.all(inv_eps == K))
    identidad_inv_mu = bool(np.all(inv_mu == INV_MU))

    # GUARDA DEL LAZO: el mapeo exige inv_mu = 1.0 fijo e inv_eps = K. Un gate sin
    # assert detras informa, no protege: si el reparto constitutivo se moviera, C1
    # seguiria imprimiendo cifras y el crudo saldria "verde" por el motivo
    # equivocado. Se declara que bajo python3 -O este assert desaparece: por eso la
    # comprobacion se exporta ademas como identidad_inv_eps_igual_a_K.
    assert (INV_MU == 1.0 and identidad_inv_eps and identidad_inv_mu), (
        "el lazo exige inv_mu = 1.0 en toda la malla e inv_eps = K "
        "(Caso B, pre-registro §4)"
    )
    nt = int(round(T_TOTAL / DT))
    jc = ny // 2
    idx = [I_FUENTE + int(round(d / DX)) for d in D_SONDAS]
    if idx[-1] >= nx - PML_CELDAS:
        raise SystemExit(
            f"malla L={L_a:g}a demasiado corta para la sonda d={D_SONDAS[-1]:g}a"
        )
    # --- PML de campo partido: sigma solo en los ejes que absorben ---
    sx = perfil_sigma(nx, PML_CELDAS)
    sy = np.zeros(ny) if ny == 1 else perfil_sigma(ny, PML_CELDAS)
    ax_e, bx_e = coef_pml(sx)
    ay_e, by_e = coef_pml(sy)
    ax_v, bx_v = coef_pml(0.5 * (sx[:-1] + sx[1:]))   # vx en (i+1/2, j)
    ay_v, by_v = coef_pml(0.5 * (sy[:-1] + sy[1:]))   # vy en (i, j+1/2)
    px = np.zeros((nx, ny))
    py = np.zeros((nx, ny))
    vx = np.zeros((nx, ny))
    vy = np.zeros((nx, ny))
    s = [np.zeros(nt + 1), np.zeros(nt + 1)]
    cola_dominio = 0.0
    cola_ubi = (-1, -1)
    cola_n = -1
    n_cola = int(round(T_COLA_MIN / DT))
    n_cola_dom = int(round(T_COLA_DOM / DT))
    pml_x = PML_CELDAS if nx > 2 * PML_CELDAS else 0
    pml_y = PML_CELDAS if ny > 2 * PML_CELDAS else 0
    vista = (slice(pml_x, nx - pml_x), slice(pml_y, ny - pml_y))
    t0 = time.time()
    for n in range(nt + 1):
        t = n * DT
        p = px + py
        vx[:-1, :] = (ax_v[:, None] * vx[:-1, :]
                      - bx_v[:, None] * INV_MU * (p[1:, :] - p[:-1, :]) / DX)
        vy[:, :-1] = (ay_v[None, :] * vy[:, :-1]
                      - by_v[None, :] * INV_MU * (p[:, 1:] - p[:, :-1]) / DY)
        if ny == 1:
            px[1:, 0] = (ax_e[1:] * px[1:, 0]
                         - bx_e[1:] * inv_eps[1:, 0] * (vx[1:, 0] - vx[:-1, 0]) / DX)
        else:
            px[1:, 1:] = (ax_e[1:, None] * px[1:, 1:]
                          - bx_e[1:, None] * inv_eps[1:, 1:]
                          * ((vx[1:, 1:] - vx[:-1, 1:]) / DX))
            # CORREGIDO v3: el termino en y usaba vy[:, :-1] (fila completa) y
            # rompia la forma (nx-1,ny-1) contra (nx,ny-1); el vecino usa hx[1:, :-1].
            py[1:, 1:] = (ay_e[None, 1:] * py[1:, 1:]
                          - by_e[None, 1:] * inv_eps[1:, 1:]
                          * ((vy[1:, 1:] - vy[1:, :-1]) / DY))
        px[I_FUENTE, jc] += fuente(t)
        p = px + py
        s[0][n] = p[idx[0], jc]
        s[1][n] = p[idx[1], jc]
        if n >= n_cola_dom:
            vi, vj = np.unravel_index(int(np.argmax(np.abs(p[vista]))), p[vista].shape)
            v = float(np.abs(p[pml_x + vi, pml_y + vj]))
            if v > cola_dominio:
                cola_dominio = v
                cola_ubi = (int(pml_x + vi), int(pml_y + vj))
                cola_n = int(n)
    transcurrido = time.time() - t0
    fi, fj = np.unravel_index(int(np.argmax(np.abs(p[vista]))), p[vista].shape)
    i_fin, j_fin = int(pml_x + fi), int(pml_y + fj)
    fin_abs = float(np.abs(p[i_fin, j_fin]))

    frec = np.fft.rfftfreq(nt + 1, DT)                    # unidades c_s/a = nu
    fft = [np.fft.rfft(x) * DT for x in s]
    sel = (frec >= NU_MIN) & (frec <= NU_MAX)
    nu = frec[sel]
    sf = espectro_fuente(nu)
    Amp = [np.abs(fft[i][sel]) / sf for i in (0, 1)]
    lnA = [np.log(np.maximum(Amp[i], 1e-300)) for i in (0, 1)]

    # --- fase medida entre las dos sondas (convencion de rama declarada) ---
    dd = D_SONDAS[1] - D_SONDAS[0]
    om = 2.0 * math.pi * nu
    # La sonda es una senal REAL; el rfft de una onda que viaja en +x cumple
    # phi(x) = -k x. Se toma el desfase como phi(8a) - phi(16a) = +k dd, para que
    # k crezca con nu; la rama m se fija UNA vez en el primer punto de la ventana.
    ang = np.unwrap(np.angle(fft[0][sel] * np.conj(fft[1][sel])))
    mm = float(np.round((om[0] / C * dd - ang[0]) / (2.0 * math.pi)))
    k = (ang + 2.0 * math.pi * mm) / dd
    fase_err = np.divide(
        om, k * C, out=np.ones_like(om), where=(np.abs(k) > 1e-12)
    ) - 1.0

    pico2 = float(np.abs(s[1]).max())
    cola_sonda = float(np.abs(s[1][n_cola:]).max()) / pico2 if pico2 > 0 else float("nan")
    cola_dom = cola_dominio / pico2 if pico2 > 0 else float("nan")
    cola_fin = fin_abs / pico2 if pico2 > 0 else float("nan")
    media_int = float(np.mean(p[vista])) / pico2 if pico2 > 0 else float("nan")
    T_teorico = 1.0 if modo == "C1a" else math.sqrt(D_SONDAS[0] / D_SONDAS[1])
    T = Amp[1] / np.maximum(Amp[0], 1e-300)
    ln_T = np.log(T)

    return {
        "modo": modo,
        "L_a": L_a,
        "nx": nx,
        "ny": ny,
        "nt": nt,
        "K_C1": K_C1,
        "es_heterogeneo": es_heterogeneo,
        "fraccion_mascara_union": fraccion_mascara,
        "K_min": float(K.min()),
        "K_max": float(K.max()),
        "inv_eps_min": float(inv_eps.min()),
        "inv_eps_max": float(inv_eps.max()),
        "identidad_inv_eps_igual_a_K": identidad_inv_eps,
        "identidad_inv_mu_igual_a_uno": identidad_inv_mu,
        "segundos_corrida": round(transcurrido, 2),
        "nu": nu.tolist(),
        "A_d_1": Amp[0].tolist(),
        "A_d_2": Amp[1].tolist(),
        "lnA_d_1": lnA[0].tolist(),
        "lnA_d_2": lnA[1].tolist(),
        "T": T.tolist(),
        "T_media": float(np.mean(T)),
        "T_teorico": T_teorico,
        "T_desv_max": float(np.abs(T - T_teorico).max()),
        "T_riz": float(np.abs(ln_T - ln_T.mean()).max()),
        "T_min": float(T.min()),
        "T_max": float(T.max()),
        "riz_d_1": float(np.abs(lnA[0] - lnA[0].mean()).max()),
        "riz_d_2": float(np.abs(lnA[1] - lnA[1].mean()).max()),
        "fase_error": fase_err.tolist(),
        "fase_error_max": float(np.abs(fase_err).max()),
        "rama_m": mm,
        "cola_sonda": cola_sonda,
        "cola_dominio": cola_dom,
        "cola_dominio_celda": [int(cola_ubi[0]), int(cola_ubi[1])],
        "cola_dominio_paso": cola_n,
        "cola_dominio_t": (cola_n * DT) if cola_n >= 0 else float("nan"),
        "cola_final_celda": [int(i_fin), int(j_fin)],
        "cola_final": cola_fin,
        "residuo_media_p": media_int,
        "pico_sonda": pico2,
    }


def sha16(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()[:16]


def main() -> int:
    nus = np.linspace(NU_MIN, NU_MAX, 512)
    yee_max = float(np.abs(yee_error_fase(nus)).max())
    salida = {
        "instrumento": "acustica-monotile/sim/sim_acustica2d.py",
        "acto": "C1 · piso de ruido del instrumento (homogeneo K=1, rho=1, c_s=1)",
        "mapa": "Caso B: eps = 1/K, mu = rho = 1, alfa = 1, v = (-Hy, Hx)",
        "UNIVERSO DECLARADO": UNIVERSO,
        "t_utc_inicio": t_utc(),
        "umbral_planitud_prestado": UMBRAL_PRESTADO,
        "origen_del_umbral": (
            "PRESTADO de fotonica-monotile/PREREGISTRO_INSTRUMENTO_FDTD_20261012.md "
            "§3/§6; NO sellado en esta casa"
        ),
        "ventana_nu": [NU_MIN, NU_MAX],
        "sondas_a": [d / A for d in D_SONDAS],
        "modos": list(MODOS),
        "L_a": [l / A for l in L_LISTA],
        "yee_error_fase_max_ventana": yee_max,
        "factor_q4": FACTOR_Q4,
        "reparto_constitutivo": {
            "rho_0": RHO, "K_0": K_FONDO, "c_s_0": math.sqrt(K_FONDO / RHO),
            "Z_0": math.sqrt(RHO * K_FONDO),
            "K_mat_declarado_no_usado": K_MAT,
            "eps_mat_declarado_no_usado": 1.0 / K_MAT,
            "c_s_mat_declarado_no_usado": math.sqrt(K_MAT / RHO),
            "Z_mat_declarado_no_usado": math.sqrt(RHO * K_MAT),
            "inv_mu_fijo": INV_MU,
        },
        "corridas": [],
    }
    for modo in MODOS:
        for L in L_LISTA:
            salida["corridas"].append(correr(L, modo))

    por = {(c["modo"], c["L_a"]): c for c in salida["corridas"]}
    deltas = {}
    for modo in MODOS:
        a = np.array(por[(modo, L_LISTA[0])]["lnA_d_2"])
        b = np.array(por[(modo, L_LISTA[1])]["lnA_d_2"])
        deltas[modo] = float(np.abs(b - a).max())
    salida["delta_lnA_36_vs_24"] = deltas
    riz_T = {m: max(por[(m, L)]["T_riz"] for L in L_LISTA) for m in MODOS}
    salida["riz_T_por_modo"] = riz_T
    salida["PISO_DE_RUIDO_riz_T_max"] = float(max(riz_T.values()))
    salida["PISO_DE_RUIDO_riz_lnA_max"] = float(
        max(max(c["riz_d_1"], c["riz_d_2"]) for c in salida["corridas"])
    )
    salida["riz_lnA_diagnostico"] = [
        {"modo": c["modo"], "L_a": c["L_a"],
         "riz_d_1": c["riz_d_1"], "riz_d_2": c["riz_d_2"]}
        for c in salida["corridas"]
    ]
    desv = {m: max(por[(m, L)]["T_desv_max"] for L in L_LISTA) for m in MODOS}
    salida["T_desv_max_por_modo"] = desv
    fase_max = max(por[("C1a", L)]["fase_error_max"] for L in L_LISTA)
    salida["fase_error_max_C1a"] = fase_max
    salida["ANALOGO_PRESTADO_Q1_riz_T_ok"] = bool(max(riz_T.values()) <= UMBRAL_PRESTADO)
    salida["ANALOGO_PRESTADO_Q2_delta_ok"] = bool(max(deltas.values()) <= UMBRAL_PRESTADO)
    salida["ANALOGO_PRESTADO_Q3_T_ok"] = bool(max(desv.values()) <= UMBRAL_PRESTADO)
    salida["ANALOGO_PRESTADO_Q4_fase_ok"] = bool(fase_max <= FACTOR_Q4 * yee_max)
    salida["identidad_inv_eps_en_todas_las_corridas"] = bool(
        all(c["identidad_inv_eps_igual_a_K"] for c in salida["corridas"])
    )
    salida["t_utc_fin"] = t_utc()
    salida["sha16_script"] = sha16(Path(__file__).resolve())

    etiqueta = salida["t_utc_inicio"].replace("-", "").replace(":", "")
    CRUDOS.mkdir(parents=True, exist_ok=True)
    pj = CRUDOS / f"crudo_C1_acustica_{etiqueta}.json"
    pj.write_text(json.dumps(salida, indent=1, ensure_ascii=False), encoding="utf-8")
    salida["ruta_crudo_json"] = str(pj)
    salida["sha16_crudo_json"] = sha16(pj)

    Ln = []
    Ln.append("UNIVERSO DECLARADO: " + salida["UNIVERSO DECLARADO"])
    Ln.append(f"instrumento: {salida['instrumento']} · sha16 {salida['sha16_script']}")
    Ln.append(f"mapa: {salida['mapa']}")
    Ln.append(f"t_utc: {salida['t_utc_inicio']} -> {salida['t_utc_fin']}")
    Ln.append(
        f"umbral de planitud: {UMBRAL_PRESTADO} · origen: {salida['origen_del_umbral']}"
    )
    Ln.append(f"factor Q4: {FACTOR_Q4}")
    r = salida["reparto_constitutivo"]
    Ln.append(
        f"reparto congelado: rho_0={r['rho_0']:g} K_0={r['K_0']:g} c_s_0={r['c_s_0']:g} "
        f"Z_0={r['Z_0']:g} · inclusion declarada (no usada en C1): K_mat="
        f"{r['K_mat_declarado_no_usado']:g} eps_mat={r['eps_mat_declarado_no_usado']:g} "
        f"c_s_mat={r['c_s_mat_declarado_no_usado']:g} Z_mat="
        f"{r['Z_mat_declarado_no_usado']:g} · INV_MU={r['inv_mu_fijo']:g} fijo"
    )
    Ln.append("")
    Ln.append("---- C1 · homogeneo K = 1 (NO hay objeto) ----")
    for c in salida["corridas"]:
        Ln.append(
            f"{c['modo']} · L = {c['L_a']:g}a · malla {c['nx']}x{c['ny']} · "
            f"{c['nt']} pasos · {c['segundos_corrida']} s"
        )
        Ln.append(
            f"   T(nu) = A({D_SONDAS[1]/A:g}a)/A({D_SONDAS[0]/A:g}a) = "
            f"{c['T_media']:.6f}  (teorico {c['T_teorico']:.6f}, desv max "
            f"{c['T_desv_max']:.6f}, rango {c['T_min']:.6f}..{c['T_max']:.6f})"
        )
        Ln.append(
            f"   riz de T = {c['T_riz']:.6f}   [diagnostico] riz de ln A(d="
            f"{D_SONDAS[0]/A:g}a) = {c['riz_d_1']:.6f} · riz de ln A(d="
            f"{D_SONDAS[1]/A:g}a) = {c['riz_d_2']:.6f}"
        )
        Ln.append(
            f"   fase: error max = {c['fase_error_max']:.6e}  ·  rama m = {c['rama_m']:.0f}"
        )
        Ln.append(
            f"   cola de sonda (t >= {T_COLA_MIN:g} a/c_s) = {c['cola_sonda']:.3e}  ·  "
            f"residuo de dominio interior (t >= {T_COLA_DOM:g} a/c_s) = "
            f"{c['cola_dominio']:.3e}"
        )
        Ln.append(
            f"   residuo localizado: celda {tuple(c['cola_dominio_celda'])} en n = "
            f"{c['cola_dominio_paso']} (t = {c['cola_dominio_t']:.2f} a/c_s) · maximo "
            f"final = {c['cola_final']:.3e} en celda {tuple(c['cola_final_celda'])} "
            f"(x respecto a la fuente = "
            f"{(c['cola_final_celda'][0] - I_FUENTE) * DX / A:+.2f} a) · media "
            f"espacial de p en el interior = {c['residuo_media_p']:+.3e}"
        )
    Ln.append("")
    for modo in MODOS:
        Ln.append(
            f"delta({modo}) = max_nu |ln A(36a) - ln A(24a)| = {deltas[modo]:.6f}"
        )
    Ln.append(
        f"complemento analitico Yee: error de fase max en la ventana = {yee_max:.6e}"
    )
    Ln.append("")
    Ln.append(f"PISO DE RUIDO MEDIDO: riz(T) max = {salida['PISO_DE_RUIDO_riz_T_max']:.6f}"
              f"  ·  riz(ln A) max (diagnostico, NO es piso: lleva la ley 2D) = "
              f"{salida['PISO_DE_RUIDO_riz_lnA_max']:.6f}")
    Ln.append("")
    Ln.append("---- ANALOGO PRESTADO de la casa vecina (§6 de su pre-registro) ----")
    Ln.append("     NO son sellos de esta casa: el sello de acustica pide el NULO")
    Ln.append("     (piso de ruido) y ese piso es la cifra riz(T) de arriba.")
    Ln.append(
        f"Q1 riz(T) <= {UMBRAL_PRESTADO} en C1a y C1b: "
        f"{'VERDE' if salida['ANALOGO_PRESTADO_Q1_riz_T_ok'] else 'ROJO'}"
        f"  [C1a {riz_T['C1a']:.6f} · C1b {riz_T['C1b']:.6f}]"
    )
    Ln.append(
        f"Q2 delta <= {UMBRAL_PRESTADO}: "
        f"{'VERDE' if salida['ANALOGO_PRESTADO_Q2_delta_ok'] else 'ROJO'}"
    )
    Ln.append(
        f"Q3 T (2D 0.7071 · 1D 1.0000) +- {UMBRAL_PRESTADO}: "
        f"{'VERDE' if salida['ANALOGO_PRESTADO_Q3_T_ok'] else 'ROJO'}"
    )
    Ln.append(
        f"Q4 fase medida {fase_max:.3e} <= {FACTOR_Q4:g} x Yee {yee_max:.3e}"
        f" = {FACTOR_Q4 * yee_max:.3e}: "
        f"{'VERDE' if salida['ANALOGO_PRESTADO_Q4_fase_ok'] else 'ROJO'}"
    )
    Ln.append("")
    Ln.append(
        f"identidad inv_eps == K en la malla de C1 (K=1): "
        f"{salida['identidad_inv_eps_en_todas_las_corridas']}  "
        f"[pre-registro §7.3: bit-exacta solo para K reciproco exacto]"
    )
    Ln.append("")
    Ln.append("---- ventana: nu · A_C1a(8a) · A_C1a(16a) · A_C1b(8a) · A_C1b(16a) ----")
    ref = por[("C1a", L_LISTA[0])]
    for i in range(len(ref["nu"])):
        Ln.append(
            f"  {ref['nu'][i]:.4f}  {ref['A_d_1'][i]:.6e}  {ref['A_d_2'][i]:.6e}  "
            f"{por[('C1b', L_LISTA[0])]['A_d_1'][i]:.6e}  "
            f"{por[('C1b', L_LISTA[0])]['A_d_2'][i]:.6e}"
        )
    texto = "\n".join(Ln) + "\n"
    pt = CRUDOS / f"crudo_C1_acustica_{etiqueta}.txt"
    pt.write_text(texto, encoding="utf-8")
    print(texto, end="")
    if "--json" in sys.argv:
        print(json.dumps(salida, indent=1, ensure_ascii=False))
    print(f"crudo json: {pj} · sha16 {salida['sha16_crudo_json']}")
    print(f"crudo txt : {pt} · sha16 {sha16(pt)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
