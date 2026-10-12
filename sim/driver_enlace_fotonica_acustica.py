#!/usr/bin/env python3 -B
"""BATERIA DEL ENLACE fotonica-monotile -> acustica-monotile (Paso 3 del protocolo).

UNIVERSO DECLARADO (se imprime antes de toda cifra)
  Objeto:  T(nu) del solver acustico `sim/sim_acustica2d.py` (Paso 3: mapeo
           constitutivo K(x,y) desde mascara binaria) a L = 24.0 a, modo C1b,
           con la mascara binaria bajo custodia en `data/geometria_hat/`.
  Motor:   este driver + numpy; el solver es el instrumento.
  Unidad:  1 valor de T por bin de frecuencia; 29 bins; 1 realizacion = 1 corrida.
  Ventana: nu in [0.15, 0.55] c_s/a (29 bins), la del pre-registro.

PRE-DECLARADO (antes de ver una sola cifra)
  sigma_U2 con ddof = 1 (cuasi-desviacion de las 5 realizaciones U2). El par de
  control ddof = 0 se imprime AL LADO; ninguno se elige despues de ver la salida.
  Piso del ruido: 0.005523 (contrato del Paso 3). El valor medido en el crudo C1
  (commit d5a7548) es 0.00552322568652841; se imprimen los DOS.
  Veredicto por bin:
      DeltaT(nu) = |T_U1(nu) - media_T_U2(nu)| - (3*sigma_U2(nu) + 0.005523)
      DeltaT > 0  -> DISCREPA (por encima del piso)
      DeltaT <= 0 -> NULO (no distinguible del piso)
  Control de convencion: se corre ADEMAS el juego completo con las mascaras SIN
  transponer (declarado). El solver transpone al cargar (`cargar_mascara`), porque
  el vecino `malla_hat.py` indexa fila = y, columna = x y este solver indexa
  eje 0 = x, eje 1 = y. El juego sin transponer NO es un veredicto: es el control
  de que la convencion de ejes no es un no-op.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np

AQUI = Path(__file__).resolve().parent
if str(AQUI) not in sys.path:
    sys.path.insert(0, str(AQUI))

import sim_acustica2d as S  # noqa: E402  (el instrumento que se pone a prueba)

L_A = 24.0
MODO = "C1b"
N = 384
REALIZACIONES = (
    "u1",
    "u2_semilla_101",
    "u2_semilla_102",
    "u2_semilla_103",
    "u2_semilla_104",
    "u2_semilla_105",
)
DDQF = 1                              # pre-declarado
FACTOR = 3.0                          # pre-declarado (3 sigma)
PISO_CONTRATO = 0.005523              # pre-declarado (contrato del Paso 3)
PISO_MEDIDO = 0.00552322568652841     # medido en el crudo C1 (d5a7548); par de control
CRUDO_C1 = "crudo_C1_acustica_20261012T072953Z.json"
CRUDO_GEO_U1 = "crudo.json"           # el del vecino, bajo la custodia del Paso 1/2


def t_utc() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def crudo_json(p: Path) -> dict | None:
    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else None


def abre(m: dict, camino: str, por_defecto=None):
    """Lee una llave anidada sin inventarla: ausente -> por_defecto."""
    x = m
    for k in camino.split("."):
        if isinstance(x, dict) and k in x:
            x = x[k]
        else:
            return por_defecto
    return x


def corre(real: str, transponer: bool) -> dict:
    """Una corrida. `transponer=True` usa la capacidad nueva del solver."""
    if transponer:
        m = S.cargar_mascara(real, N)
    else:
        nombre = "u1" if real == "u1" else "u2"
        crudo = np.load(S.GEO / real / f"malla_{nombre}_n{N}_k2.npy")
        m = np.ascontiguousarray(crudo, dtype=np.float64)
    t0 = time.time()
    r = S.correr(L_A, MODO, mascara=m)
    r["_segundos"] = round(time.time() - t0, 2)
    r["_transpuesta"] = bool(transponer)
    return r


def vector(rs: list[dict]) -> np.ndarray:
    return np.vstack([np.asarray(r["T"], dtype=np.float64) for r in rs])


def veredicto(T_U1: np.ndarray, U2: np.ndarray, piso: float, ddof: int) -> dict:
    media = U2.mean(axis=0)
    desv = U2.std(axis=0, ddof=ddof)
    umbral = FACTOR * desv + piso
    delta = np.abs(T_U1 - media) - umbral
    return {
        "media_T_U2": media,
        "sigma_U2": desv,
        "umbral": umbral,
        "delta_T": delta,
        "n_discrepa": int((delta > 0.0).sum()),
        "n_bins": int(delta.size),
        "rango_T_U2": U2.max(axis=0) - U2.min(axis=0),
    }


def main() -> int:
    t_ini = t_utc()
    print("=" * 72)
    print("BATERIA DEL ENLACE ACUSTICA  ·  Paso 3  ·  K(x,y) desde mascara binaria")
    print("=" * 72)
    print(
        "UNIVERSO DECLARADO: T(nu) del solver sim/sim_acustica2d.py (blob "
        "4de2c841e0d6e6b2757c371ef5cca1e4661b646b, commit f29879b) a L = 24.0 a, "
        "modo C1b, mascara de data/geometria_hat/ (commit b498fcf). "
        "MOTOR = este driver + numpy. UNIDAD = valor de T por bin (29 bins). "
        f"VENTANA = reloj UTC de arriba (t_utc_inicio = {t_ini})."
    )
    print(
        f"DECLARADO ANTES DE MEDIR: sigma con ddof = {DDQF} (control al lado: "
        f"ddof = 0) · factor = {FACTOR:g} · piso del contrato = {PISO_CONTRATO} "
        f"· piso medido en C1 = {PISO_MEDIDO}"
    )
    print(f"SOLVER: {Path(S.__file__).resolve()}")

    # ---- el par de denominadores del llenado (declarado, NO adjudicado) ----
    u1_geo = crudo_json(S.GEO / "u1" / CRUDO_GEO_U1)
    if u1_geo is None:
        print("LLENADO: crudo geometrico u1 ausente; el par no se puede imprimir.")
    else:
        print(
            "LLENADO (dos denominadores, se imprimen los dos): "
            f"suma_areas = {abre(u1_geo, 'fraccion_de_llenado.U1', 'ausente')} "
            f"(analitico) · cobertura_union_U1 = "
            f"{abre(u1_geo, 'fraccion_de_llenado.cobertura_union_U1', 'ausente')} "
            f"(celdas cubiertas) · media de la mascara binaria = "
            f"{abre(u1_geo, 'u1.cobertura', 'ausente')}"
        )
        print(
            "ESCALA (declarado, NO adjudicado): celda = "
            f"{abre(u1_geo, 'celda', 'ausente')} unidades del vecino · "
            f"lado de la ventana = celda * 384 · ventana del solver = 24 a con "
            "dx = 0.0625 a; no hay conversion declarada entre 'unidad' y 'a': "
            "el mapeo disponible es celda a celda sobre la ventana completa."
        )

    # ---- corridas declaradas ----
    print("-" * 72)
    print("CORRIDAS DECLARADAS (mascara transpuesta al cargar: convencion del solver)")
    runs: list[dict] = []
    for real in REALIZACIONES:
        r = corre(real, True)
        runs.append(r)
        print(
            f"  {real:<18} {r['_segundos']:>6.2f} s  nx={r['nx']} ny={r['ny']} "
            f"hetero={r['es_heterogeneo']} f_mascara={r['fraccion_mascara_union']} "
            f"K in [{r['K_min']}, {r['K_max']}] inv_eps in "
            f"[{r['inv_eps_min']}, {r['inv_eps_max']}] "
            f"id_eps={r['identidad_inv_eps_igual_a_K']} "
            f"id_mu={r['identidad_inv_mu_igual_a_uno']}"
        )

    nu = np.asarray(runs[0]["nu"], dtype=np.float64)
    nu_iguales = all(bool(np.array_equal(nu, np.asarray(r["nu"]))) for r in runs)
    print(f"CONTROL: las {len(runs)} rejillas de nu son identicas -> {nu_iguales}")

    T_U1 = np.asarray(runs[0]["T"], dtype=np.float64)
    U2 = vector(runs[1:])
    v1 = veredicto(T_U1, U2, PISO_CONTRATO, DDQF)
    v0 = veredicto(T_U1, U2, PISO_CONTRATO, 0)
    vm = veredicto(T_U1, U2, PISO_MEDIDO, DDQF)

    print("-" * 72)
    print("VECTOR DE VEREDICTOS  DeltaT(nu) = |T_U1 - media_T_U2| - (3 sigma_U2 + 0.005523)")
    print(f"{'nu':>8} {'T_U1':>12} {'media_U2':>12} {'sigma_U2':>11} {'umbral':>11} {'DeltaT':>12}  veredicto")
    for i, n_i in enumerate(nu):
        d = v1["delta_T"][i]
        print(
            f"{n_i:>8.4f} {T_U1[i]:>12.8f} {v1['media_T_U2'][i]:>12.8f} "
            f"{v1['sigma_U2'][i]:>11.4e} {v1['umbral'][i]:>11.4e} {d:>12.6e}  "
            f"{'DISCREPA' if d > 0.0 else 'NULO'}"
        )

    print("-" * 72)
    print(
        f"RESUMEN (declarado): bins = {v1['n_bins']} · DISCREPA = {v1['n_discrepa']} · "
        f"NULO = {v1['n_bins'] - v1['n_discrepa']} · DeltaT_max = "
        f"{float(v1['delta_T'].max()):.6e} en nu = {nu[int(v1['delta_T'].argmax())]:.4f} · "
        f"DeltaT_min = {float(v1['delta_T'].min()):.6e} en nu = "
        f"{nu[int(v1['delta_T'].argmin())]:.4f}"
    )
    print(
        "PAR DE CONTROL (no se elige despues de ver la salida): "
        f"ddof = 0 -> DISCREPA = {v0['n_discrepa']} · "
        f"piso medido {PISO_MEDIDO} -> DISCREPA = {vm['n_discrepa']} · "
        f"rango de U2 (max - min, piso declarado) max = "
        f"{float(v1['rango_T_U2'].max()):.6e} en nu = "
        f"{nu[int(v1['rango_T_U2'].argmax())]:.4f}"
    )

    # ---- control de convencion: mascaras SIN transponer ----
    print("-" * 72)
    print("CONTROL DE CONVENCION (sin transponer; NO es veredicto, es el control)")
    ctrl: list[dict] = []
    for real in REALIZACIONES:
        r = corre(real, False)
        ctrl.append(r)
        print(f"  {real:<18} {r['_segundos']:>6.2f} s  f_mascara={r['fraccion_mascara_union']}")
    T_U1_c = np.asarray(ctrl[0]["T"], dtype=np.float64)
    U2_c = vector(ctrl[1:])
    vc = veredicto(T_U1_c, U2_c, PISO_CONTRATO, DDQF)
    ident_con = bool(np.array_equal(T_U1, T_U1_c))
    print(
        f"  T_U1 transpuesta == T_U1 sin transponer -> {ident_con} (la convencion "
        f"NO es un no-op si es False)"
    )
    print(f"  Control sin transponer: DISCREPA = {vc['n_discrepa']} de {vc['n_bins']}")

    crudo_c1 = crudo_json(S.CRUDOS / CRUDO_C1)
    piso_c1 = abre(crudo_c1, "PISO_DE_RUIDO_riz_T_max", None) if crudo_c1 else None
    print(
        f"CONTROL DEL PISO: piso declarado en el crudo C1 = {piso_c1} "
        f"(contrato del Paso 3 = {PISO_CONTRATO})"
    )

    t_fin = t_utc()
    print(f"t_utc_inicio = {t_ini}   t_utc_fin = {t_fin}")

    salida = {
        "instrumento": "sim/driver_enlace_fotonica_acustica.py",
        "acto": "Paso 3 del enlace fotonica-monotile -> acustica-monotile",
        "UNIVERSO DECLARADO": (
            "T(nu) del solver sim/sim_acustica2d.py (blob "
            "4de2c841e0d6e6b2757c371ef5cca1e4661b646b, commit f29879b) a L = 24.0 a, "
            "modo C1b, mascara de data/geometria_hat/ (commit b498fcf)"
        ),
        "motor": "driver + numpy; el solver es el instrumento",
        "unidad": "valor de T por bin (29 bins); 1 realizacion = 1 corrida",
        "t_utc_inicio": t_ini,
        "t_utc_fin": t_fin,
        "declarado_antes_de_medir": {
            "ddof_sigma": DDQF,
            "factor": FACTOR,
            "piso_contrato": PISO_CONTRATO,
            "piso_medido_C1": PISO_MEDIDO,
            "regla": "DeltaT(nu) = |T_U1(nu) - media_T_U2(nu)| - (factor*sigma_U2(nu) + piso)",
        },
        "solver": str(Path(S.__file__).resolve()),
        "L_a": L_A,
        "modo": MODO,
        "n": N,
        "realizaciones": list(REALIZACIONES),
        "nu": nu.tolist(),
        "nu_iguales_en_todas_las_corridas": nu_iguales,
        "T_U1": T_U1.tolist(),
        "T_U2": U2.tolist(),
        "media_T_U2": v1["media_T_U2"].tolist(),
        "sigma_U2_ddof1": v1["sigma_U2"].tolist(),
        "sigma_U2_ddof0": v0["sigma_U2"].tolist(),
        "umbral": v1["umbral"].tolist(),
        "delta_T": v1["delta_T"].tolist(),
        "veredicto_por_bin": ["DISCREPA" if d > 0.0 else "NULO" for d in v1["delta_T"]],
        "n_discrepa": v1["n_discrepa"],
        "n_nulo": v1["n_bins"] - v1["n_discrepa"],
        "delta_T_max": float(v1["delta_T"].max()),
        "delta_T_max_nu": float(nu[int(v1["delta_T"].argmax())]),
        "delta_T_min": float(v1["delta_T"].min()),
        "delta_T_min_nu": float(nu[int(v1["delta_T"].argmin())]),
        "control_ddof0_n_discrepa": v0["n_discrepa"],
        "control_piso_medido_n_discrepa": vm["n_discrepa"],
        "rango_T_U2_max": float(v1["rango_T_U2"].max()),
        "rango_T_U2_max_nu": float(nu[int(v1["rango_T_U2"].argmax())]),
        "control_convencion": {
            "descripcion": (
                "juego completo con las mascaras SIN transponer; NO es veredicto, es "
                "el control de que la convencion de ejes no es un no-op"
            ),
            "T_U1": T_U1_c.tolist(),
            "T_U2": U2_c.tolist(),
            "delta_T": vc["delta_T"].tolist(),
            "n_discrepa": vc["n_discrepa"],
            "T_U1_identico_al_declarado": ident_con,
        },
        "corridas": [
            {
                "realizacion": real,
                "transpuesta": r["_transpuesta"],
                "segundos": r["_segundos"],
                "nx": r["nx"],
                "ny": r["ny"],
                "nt": r["nt"],
                "es_heterogeneo": r["es_heterogeneo"],
                "fraccion_mascara_union": r["fraccion_mascara_union"],
                "K_min": r["K_min"],
                "K_max": r["K_max"],
                "inv_eps_min": r["inv_eps_min"],
                "inv_eps_max": r["inv_eps_max"],
                "identidad_inv_eps_igual_a_K": r["identidad_inv_eps_igual_a_K"],
                "identidad_inv_mu_igual_a_uno": r["identidad_inv_mu_igual_a_uno"],
                "T": r["T"],
                "T_media": r["T_media"],
                "fase_error_max": r["fase_error_max"],
                "cola_final": r["cola_final"],
            }
            for real, r in zip(REALIZACIONES, runs)
        ],
        "control_convencion_corridas": [
            {
                "realizacion": real,
                "transpuesta": r["_transpuesta"],
                "segundos": r["_segundos"],
                "fraccion_mascara_union": r["fraccion_mascara_union"],
            }
            for real, r in zip(REALIZACIONES, ctrl)
        ],
        "piso_declarado_en_el_crudo_C1": piso_c1,
        "llenado_dos_denominadores": (
            None
            if u1_geo is None
            else {
                "suma_areas_analitico": abre(u1_geo, "fraccion_de_llenado.U1"),
                "cobertura_union_U1": abre(u1_geo, "fraccion_de_llenado.cobertura_union_U1"),
                "media_mascara_binaria": abre(u1_geo, "u1.cobertura"),
                "nota": "se imprimen los dos; no se adjudica ni se repara el vecino",
            }
        ),
        "escala_declarada": (
            None if u1_geo is None else {"celda_unidades_vecino": abre(u1_geo, "celda")}
        ),
    }

    etiqueta = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    S.CRUDOS.mkdir(parents=True, exist_ok=True)
    base = S.CRUDOS / f"crudo_ENLACE_ACUSTICA_FOTONICA_{etiqueta}"
    (base.with_suffix(".json")).write_text(
        json.dumps(salida, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(f"CRUDO: {base.with_suffix('.json')}")
    print(f"t_utc_fin = {t_fin}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
