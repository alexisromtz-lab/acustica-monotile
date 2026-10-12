#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Instrumento del isomorfismo: acustica 2D (p, vx, vy)  <->  FDTD TM 2D (Ez, Hx, Hy).

UNIVERSO DECLARADO: un modo de Fourier de 32x32 celdas, tres medios, tres
asignaciones constitutivas y un control positivo.
MOTOR : numpy (np.roll + diferencia hacia adelante). NO se avanza el tiempo.
UNIDAD: residuo relativo max|a-b| / max|b| por ecuacion (p, vx, vy).
VENTANA: T_UTC impresa por este mismo crudo.

Por que no se avanza el tiempo: el isomorfismo es una propiedad de las
ECUACIONES (identidad de los lados derechos), no del esquema. Un paso temporal
anade el error de Yee y mezcla el defecto del MAPEO con el defecto del METRO.

Caso congelado por este instrumento: B  (eps = 1/K, mu = rho, alfa = mu/rho = 1).
Contrato refutado: A  (eps = rho, mu = 1/K)  -- el que etiquetaba
"densimetrico" a una variacion de eps con mu fijo.
"""
import json
import os
import sys
import time

import numpy as np

N = 32
BLOB_SEMILLA = "e69de29bb2d1d6434b8b29ae775ad8c2e48c5391"


def t_utc():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def campos(n):
    i = np.arange(n)[:, None]
    j = np.arange(n)[None, :]
    p = np.sin(2.0 * np.pi * i / n) * np.cos(2.0 * np.pi * j / n)
    vx = np.cos(2.0 * np.pi * i / n) + 0.0 * j
    vy = 0.0 * i + np.sin(2.0 * np.pi * j / n)
    return p, vx, vy


def dxp(f):
    return np.roll(f, -1, axis=0) - f


def dyp(f):
    return np.roll(f, -1, axis=1) - f


def rel(a, b):
    """Residuo relativo. Devuelve None si el denominador es nulo: un no-medido
    no es un cero (un cero que cuadra consigo mismo es un verde falso)."""
    d = float(np.abs(b).max())
    if d == 0.0:
        return None
    return float(np.abs(a - b).max() / d)


def residuo_del_mapeo(rho, K, asignacion, alfa):
    """Residuo de las TRES ecuaciones, para una asignacion y un alfa dados."""
    if asignacion == "B_ratificado":
        eps, mu = 1.0 / K, rho
    elif asignacion == "B_control_x1.5":
        eps, mu = 1.5 / K, rho          # control positivo: el mapeo ya no es exacto
    elif asignacion == "A_invertido":
        eps, mu = rho, 1.0 / K
    else:
        raise ValueError(asignacion)

    p, vx, vy = campos(rho.shape[0])
    Ez = p
    Hy = -vx / alfa
    Hx = +vy / alfa

    dEz = (1.0 / eps) * (dxp(Hy) - dyp(Hx))
    dHx = -(1.0 / mu) * dyp(Ez)
    dHy = +(1.0 / mu) * dxp(Ez)

    dp = -K * (dxp(vx) + dyp(vy))
    dvx = -(1.0 / rho) * dxp(p)
    dvy = -(1.0 / rho) * dyp(p)

    return {"p": rel(dEz, dp), "vx": rel(-dHy / alfa, dvx), "vy": rel(+dHx / alfa, dvy)}


def medios(n):
    i = np.arange(n)[:, None]
    z = np.zeros((1, n))
    uno = np.ones((n, n))
    rho_den = np.where(i < n // 2, 4.0, 1.0) + z        # inclusion densa: sin solver (inv_mu = 0)
    K_mod = np.where(i < n // 2, 0.25, 1.0) + z         # inclusion blanda: la via ratificada
    return [
        ("uniforme (rho=1, K=1)", uno, uno, 1.0),
        ("densimetrico (rho 1->4, K=1)", rho_den, uno, 1.0),
        ("modulo (rho=1, K 1->0.25)", uno, K_mod, 1.0),
    ]


def corre():
    filas = []
    for nombre, rho, K, alfa in medios(N):
        for etiqueta, asignacion in (("B_ratificado", "B_ratificado"),
                                     ("A_invertido_alfa1", "A_invertido"),
                                     ("A_invertido_alfa_eps_mu", "A_invertido")):
            a = alfa if etiqueta == "A_invertido_alfa1" else (1.0 / K) / rho
            r = residuo_del_mapeo(rho, K, asignacion, a)
            r.update({"medio": nombre, "fila": etiqueta, "asignacion": asignacion})
            filas.append(r)
        r = residuo_del_mapeo(rho, K, "B_control_x1.5", 1.0)
        r.update({"medio": nombre, "fila": "CONTROL_positivo_B_x1.5", "asignacion": "B_control_x1.5"})
        filas.append(r)
    return filas


def fmt(v):
    return "NO_MEDIDO" if v is None else ("%.6e" % v)


def main():
    t0 = t_utc()
    filas = corre()

    ceros_B = [f for f in filas if f["asignacion"] == "B_ratificado"]
    todos_B = [f["p"] for f in ceros_B] + [f["vx"] for f in ceros_B] + [f["vy"] for f in ceros_B]
    B_todo_cero = all((x is not None and x == 0.0) for x in todos_B)

    ctrl = [f[k] for f in filas if f["asignacion"] == "B_control_x1.5" for k in ("p", "vx", "vy")]
    ctrl_min = min(ctrl)

    homogeneo = [f for f in filas if f["medio"].startswith("uniforme")]
    hom_todo_cero = all((f[k] is not None and f[k] == 0.0) for f in homogeneo for k in ("p", "vx", "vy"))

    if B_todo_cero and ctrl_min > 0.0:
        veredicto = "VERDE"
        rc = 0
    elif ctrl_min <= 0.0:
        veredicto = "ROJO: el control positivo no discrimina => el instrumento no mide"
        rc = 2
    else:
        veredicto = "ROJO: el caso ratificado B no es exacto"
        rc = 3

    lineas = []
    lineas.append("T_UTC=%s" % t0)
    lineas.append("UNIVERSO DECLARADO: 1 modo de Fourier de %dx%d celdas, %d filas = 3 medios x "
                  "(B_ratificado + 2 filas del contrato invertido) + 3 controles positivos; "
                  "MOTOR = numpy np.roll sin avanzar el tiempo; UNIDAD = residuo relativo por "
                  "ecuacion (p, vx, vy); VENTANA = T_UTC de arriba." % (N, N, len(filas)))
    lineas.append("SEMILLA del instrumento = %s" % BLOB_SEMILLA)
    lineas.append("medio | fila | res_p | res_vx | res_vy")
    for f in filas:
        lineas.append("%-32s | %-22s | %s | %s | %s"
                      % (f["medio"], f["fila"], fmt(f["p"]), fmt(f["vx"]), fmt(f["vy"])))
    lineas.append("CASO_B_exacto_en_los_tres_medios_y_las_tres_ecuaciones = %s" % B_todo_cero)
    lineas.append("CONTROL_POSITIVO_min = %s  (>0 exige que el instrumento discrimine)" % fmt(ctrl_min))
    lineas.append("MEDIO_HOMOGENEO_todo_cero = %s  (por eso el medio homogeneo NO decide: "
                  "las tres asignaciones coinciden)" % hom_todo_cero)
    lineas.append("VEREDICTO=%s" % veredicto)
    lineas.append("RC=%d" % rc)
    texto = "\n".join(lineas) + "\n"

    out = "crudos"
    os.makedirs(out, exist_ok=True)
    sello = t0.replace(":", "").replace("-", "")
    with open(os.path.join(out, "isomorfismo_%s.txt" % sello), "w", encoding="utf-8") as fh:
        fh.write(texto)
    with open(os.path.join(out, "isomorfismo_%s.json" % sello), "w", encoding="utf-8") as fh:
        json.dump({"t_utc": t0, "n": N, "semilla": BLOB_SEMILLA, "filas": filas,
                   "B_todo_cero": B_todo_cero, "control_positivo_min": ctrl_min,
                   "homogeneo_todo_cero": hom_todo_cero, "veredicto": veredicto, "rc": rc},
                  fh, ensure_ascii=False, indent=2)

    sys.stdout.write(texto)
    return rc


if __name__ == "__main__":
    sys.exit(main())
