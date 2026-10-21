# HUELLA-EJECUTOR-SIM-ACUSTICA-20261020
"""Ejecutor del instrumento — acustica-monotile.

`sim/sim_acustica2d.py` importa numpy y produce las cifras que el README
publica, pero hasta hoy ningun test ni ningun paso del aparato lo abria: el
censo `censo_numpy_dependencia_20261020.py` lo clasifico `SIN_EJECUTOR`
(3 portadores, 0 ejecutados). Un import que nadie ejecuta no puede fallar, y
por tanto no era una dependencia: era una suposicion.

Este test abre el instrumento, corre una de sus funciones — la dispersion
numerica del esquema Yee sobre el eje (`yee_error_fase`), el piso del que
cuelga todo el reparto de la casa — y **asierte sobre su salida**.

Falsador declarado (lo que hace rojo a este test):

  1. numpy ausente del entorno -> `from sim import sim_acustica2d` levanta
     `ModuleNotFoundError` en la coleccion: el test no puede ni empezar.
     Es la prueba de que el import es real y no decorativo.
  2. `yee_error_fase` devuelve ceros (regresion a `np.zeros_like`) -> la
     dispersion deja de tener signo fisico y el test 1 cae.
  3. el error de fase crece con `nu` en el signo contrario (esquema mal
     cableado) -> el test 2 cae.
  4. numpy 1.x activo -> el test 4 cae: el manifiesto declara `numpy>=2.0,<3.0`
     y los alias retirados en 2.0 no se pueden usar de tapadillo.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

from sim import sim_acustica2d as instrumento  # noqa: E402

NU = [0.15, 0.25, 0.35, 0.45, 0.55]


def _nu():
    """El instrumento toma un ndarray: se le da el suyo, sin importar numpy aqui.

    El test no importa numpy a proposito: si lo hiciera, seria portador del
    paquete y el `ModuleNotFoundError` del falsador quedaria escondido detras
    de su propio import.
    """
    return instrumento.np.array(NU, dtype=float)


def _error():
    return [float(x) for x in instrumento.yee_error_fase(_nu())]


def test_el_error_de_fase_tiene_el_signo_del_esquema_yee():
    """Con S = 0.5 sobre el eje, k >= omega/c: v_p = omega/k <= c, luego error <= 0."""
    err = _error()
    assert len(err) == len(NU)
    assert all(e <= 0.0 for e in err), err
    assert all(e < 0.0 for e in err), err


def test_la_medida_no_es_vacia_y_crece_con_la_frecuencia():
    """Un `zeros_like` pasaria el test 1; aqui no: magnitud > 0 y monotona."""
    err = _error()
    magnitudes = [abs(e) for e in err]
    assert max(magnitudes) > 0.0
    assert all(b > a for a, b in zip(magnitudes, magnitudes[1:])), magnitudes


def test_dos_llamadas_devuelven_los_mismos_bits():
    """Sin aleatoriedad ni estado global: la cifra es reproducible."""
    assert _error() == _error()


def test_numpy_cargado_cumple_el_piso_declarado():
    """El manifiesto declara numpy>=2.0,<3.0: un 1.x aqui seria un manifiesto mentiroso."""
    version = instrumento.np.__version__
    assert re.fullmatch(r"\d+\.\d+\.\d+.*", version), version
    assert int(version.split(".")[0]) >= 2, version
