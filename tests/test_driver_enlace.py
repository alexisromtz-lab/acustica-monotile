# HUELLA-EJECUTOR-DRIVER-ENLACE-20261020
# HUELLA-EJECUTOR-DRIVER-ENLACE-BORDE-EXACTO-20261021
# HUELLA-EJECUTOR-DRIVER-ENLACE-TOLERANCIA-REPRODUCIBLE-20261021
"""Ejecutor del driver del enlace fotonica -> acustica — acustica-monotile.

`sim/driver_enlace_fotonica_acustica.py` (352 l.) era el ultimo inerte de
`acustica-monotile`: el censo `censo_numpy_dependencia_20261020.py` lo contaba
como portador de numpy y no lo veia ejecutado por nadie. Su bateria completa
(6 realizaciones x 2 convenciones, 12 corridas del solver) si se corrio alguna
vez — su crudo esta conservado — pero una foto del crudo no ejecuta el veredicto.

Contrato MEDIDO del objeto (no el supuesto):

  * `main()` devuelve **0 siempre**: su unico `return` es `return 0` (l.348).
    El driver no tiene rama roja. Lo que emite es un veredicto *impreso y
    guardado* (`DISCREPA`/`NULO` por bin), no un codigo de salida.
  * Un par ausente no produce un RC: `sim_acustica2d.cargar_mascara` levanta
    `SystemExit` cuyo `.code` es un **str** con el mensaje de custodia
    (`mascara ausente bajo custodia: ...`). Falla cerrado, pero no por codigo.
  * Una corrida `corre('u1', True)` reproduce el `T_U1` publicado **bit a bit**
    (max|dT| medido = 0.0 contra el crudo del 2026-10-12).

Desviaciones declaradas contra la orden que autorizo este acto (la orden no se
reescribe, se corrige con el numero delante):

  1. RUTA: la orden apuntaba a `platino-labs/sim/tests/`, que no existe y no
     corre pytest. El ejecutor vive donde vive el objeto y donde hay pytest:
     `acustica-monotile/tests/`. La medicion de acoplamiento (D13) da **cero
     copias**: `platino-labs/sim/` no tiene `verifica_isomorfismo.py` ni este
     driver; no hay fork ni dependencia cross-repo que declarar.
  2. `RC != 0` EN EL CASO SIN PAR: la orden pedia un codigo distinto de cero.
     El contrato medido no tiene codigos: `main()` firma 0 y el par ausente
     levanta `SystemExit` con `.code` de tipo str. Se exige el contrato medido.
  3. COSTO: la bateria completa cuesta 12 corridas x ~13 s = ~2.5 min. El
     ejecutor NO la repite en cada push: corre **una** corrida real (la del
     `T_U1` publicado) y el resto del contrato se ejecuta sobre funciones puras
     y con `corre` inyectado, que es donde vive la decision.

Falsadores declarados (lo que pone rojo a este test):

  1. numpy ausente -> este modulo lo importa en su cabecera y el driver lo
     necesita para correr: la coleccion levanta `ModuleNotFoundError`.
  2. la desigualdad del veredicto deja de ser estricta (`delta >= 0` en vez de
     `delta > 0`) -> cae `test_el_borde_exacto_mata_la_desigualdad_no_estricta`.
     ERRATA MEDIDA: la primera version de este ejecutor declaraba que el caso
     frontera de `test_veredicto_se_apaga_con_un_control_que_no_discrimina`
     ya cubria este mutante, y era falso: con cinco copias desplazadas `sigma`
     sale -5.55e-17 y `delta` cae en -5.55e-17, negativo tambien para `>= 0.0`,
     asi que el mutante sobrevivia con 11 verdes. El borde solo muerde donde
     `delta` es 0.0 **exacto**, y eso exige `T` constante y piso 0.
  3. el veredicto se apaga con un control que no discrimina (todos los bins
     `NULO`) -> test 4 cae.
  4. el solver cambia y `T_U1` deja de reproducir el crudo -> test 7 cae.
  5. la convencion de ejes se vuelve un no-op (el solver deja de transponer)
     -> test 8 cae.
  6. `main()` deja de firmar 0 o deja de escribir el crudo -> test 10 cae.
  7. el flag `T_U1_identico_al_declarado` se cablea a constante -> test 11 cae.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pytest

RAIZ = Path(__file__).resolve().parents[1]
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

from sim import driver_enlace_fotonica_acustica as driver  # noqa: E402

CRUDOS = RAIZ / "crudos"
CRUDO_ENLACE = CRUDOS / "crudo_ENLACE_ACUSTICA_FOTONICA_20261012T204809Z.json"
CRUDO_C1 = CRUDOS / "crudo_C1_acustica_20261012T072953Z.json"
BINS = 29

# Reproduccion del crudo publicado entre maquinas: macOS/arm64 da 0.0 y el
# runner Linux dio 7.105e-15 (run 39556291717). 1e-12 queda nueve ordenes por
# debajo del bin mas fino (5.113e-3) y no puede mover un veredicto.
TOL_REPRODUCCION = 1e-12


def _enlace() -> dict:
    return json.loads(CRUDO_ENLACE.read_text(encoding="utf-8"))


def _nu_sintetico() -> np.ndarray:
    return np.linspace(0.15, 0.55, BINS)


def _T_sintetico() -> np.ndarray:
    nu = _nu_sintetico()
    return 1.0 + 0.5 * nu + 0.01 * np.sin(20.0 * nu)


def _realizacion(nu: np.ndarray, T: np.ndarray, transpuesta: bool) -> dict:
    """Corrida falsa con la forma exacta que `main()` consume.

    `nu` y `T` van como listas: `S.correr` real las devuelve serializables y
    `main()` las pasa crudas a `json.dumps` (medido: con ndarray levanta
    `TypeError: Object of type ndarray is not JSON serializable`).
    """
    T = np.asarray(T, dtype=np.float64)
    return {
        "nu": np.asarray(nu, dtype=np.float64).tolist(),
        "T": T.tolist(),
        "T_media": float(np.mean(T)),
        "nt": 2304,
        "nx": 384,
        "ny": 384,
        "es_heterogeneo": True,
        "fraccion_mascara_union": 0.4036797417534722,
        "K_min": 0.25,
        "K_max": 1.0,
        "inv_eps_min": 0.25,
        "inv_eps_max": 1.0,
        "identidad_inv_eps_igual_a_K": True,
        "identidad_inv_mu_igual_a_uno": True,
        "fase_error_max": 0.5,
        "cola_final": 0.5,
        "_segundos": 0.0,
        "_transpuesta": bool(transpuesta),
    }


# ------------------------------------------------- pre-declarado (medido) ---


def test_constantes_predeclaradas_no_se_mueven() -> None:
    assert driver.N == 384
    assert driver.L_A == 24.0
    assert driver.MODO == "C1b"
    assert driver.DDQF == 1
    assert driver.FACTOR == 3.0
    assert driver.PISO_CONTRATO == 0.005523
    assert driver.PISO_MEDIDO == 0.00552322568652841
    assert len(driver.REALIZACIONES) == 6
    assert driver.REALIZACIONES[0] == "u1"
    assert len(driver.REALIZACIONES[1:]) == 5


def test_el_piso_medido_es_el_del_crudo_C1() -> None:
    c1 = json.loads(CRUDO_C1.read_text(encoding="utf-8"))
    assert c1["PISO_DE_RUIDO_riz_T_max"] == driver.PISO_MEDIDO
    assert driver.PISO_MEDIDO > driver.PISO_CONTRATO


# ------------------------------------------- el veredicto (la decision) ---


def test_veredicto_reproduce_la_bateria_publicada() -> None:
    e = _enlace()
    T_U1 = np.asarray(e["T_U1"], dtype=np.float64)
    U2 = np.asarray(e["T_U2"], dtype=np.float64)
    assert T_U1.size == BINS and U2.shape == (5, BINS)

    v1 = driver.veredicto(T_U1, U2, driver.PISO_CONTRATO, driver.DDQF)
    v0 = driver.veredicto(T_U1, U2, driver.PISO_CONTRATO, 0)
    vm = driver.veredicto(T_U1, U2, driver.PISO_MEDIDO, driver.DDQF)

    assert v1["n_bins"] == BINS
    assert v1["n_discrepa"] == e["n_discrepa"] == 7
    assert v0["n_discrepa"] == e["control_ddof0_n_discrepa"] == 8
    assert vm["n_discrepa"] == e["control_piso_medido_n_discrepa"] == 7
    assert np.array_equal(v1["delta_T"], np.asarray(e["delta_T"], dtype=np.float64))
    assert float(v1["delta_T"].max()) == e["delta_T_max"]
    assert float(v1["delta_T"].min()) == e["delta_T_min"]


def test_veredicto_se_apaga_con_un_control_que_no_discrimina() -> None:
    T = _T_sintetico()
    muerto = np.vstack([T.copy() for _ in range(5)])
    v = driver.veredicto(T, muerto, driver.PISO_CONTRATO, driver.DDQF)
    assert v["n_discrepa"] == 0, "un U2 identico a U1 tiene que dar NULO en todo bin"
    assert np.all(np.abs(v["sigma_U2"]) < 1e-15), (
        "sigma de cinco copias no es exactamente 0.0: numpy deja un artefacto de "
        "signo del orden de -5.55e-17; se mide con tolerancia, no con igualdad"
    )
    assert np.all(np.abs(v["delta_T"] + driver.PISO_CONTRATO) < 1e-15)

    vivo = np.vstack([T + 2.0 * driver.PISO_CONTRATO for _ in range(5)])
    v2 = driver.veredicto(T, vivo, driver.PISO_CONTRATO, driver.DDQF)
    assert v2["n_discrepa"] == BINS, "un sesgo comun mayor que el piso tiene que DISCREPAR"

    frontera = np.vstack([T + driver.PISO_CONTRATO for _ in range(5)])
    v3 = driver.veredicto(T, frontera, driver.PISO_CONTRATO, driver.DDQF)
    assert np.all(np.abs(v3["delta_T"]) < 1e-15), (
        "el borde no cae en 0.0 exacto: cae en -5.55e-17 por el artefacto de sigma; "
        "se mide con tolerancia y la decision NO cambia de lado"
    )
    assert np.all(v3["delta_T"] <= 0.0)
    assert v3["n_discrepa"] == 0, "DeltaT = 0 no es DISCREPA: la desigualdad es estricta"


def test_el_borde_exacto_mata_la_desigualdad_no_estricta() -> None:
    """El borde donde `delta` cae en `0.0` exacto, sin redondeo de la media.

    El caso frontera del test anterior desplaza las cinco copias de `U2` por el
    piso, y ahi la media deja un artefacto: `sigma` sale -5.55e-17 y `delta`
    cae en -5.55e-17, negativo tambien bajo `>= 0.0`. Con `T` constante y piso 0
    no hay desplazamiento que redondear: `U2 - media` es 0.0 exacto, `sigma` es
    0.0 exacto y `delta` es 0.0 exacto. Es el unico punto donde `> 0.0` y
    `>= 0.0` dan distinto, y por eso el unico que mata el mutante.
    """
    constante = np.full(BINS, 1.0)
    U2 = np.vstack([constante.copy() for _ in range(5)])

    v = driver.veredicto(constante, U2, 0.0, driver.DDQF)
    assert np.all(v["sigma_U2"] == 0.0)
    assert np.all(v["delta_T"] == 0.0), (
        "el borde tiene que ser 0.0 exacto: %r no es el punto donde la "
        "desigualdad estricta se distingue de la no estricta"
        % (sorted(set(v["delta_T"].tolist()))[:3],)
    )
    assert v["n_bins"] == BINS
    assert v["n_discrepa"] == 0, (
        "DeltaT = 0.0 exacto no es DISCREPA: si aqui DISCREPA, la desigualdad "
        "se volvio no estricta y los 29 bins del borde firman de mas"
    )


def test_vector_apila_una_fila_por_realizacion() -> None:
    rs = [_realizacion(_nu_sintetico(), _T_sintetico() + k, True) for k in range(5)]
    U2 = driver.vector(rs)
    assert U2.shape == (5, BINS)
    assert np.array_equal(U2[3], rs[3]["T"])


def test_abre_no_inventa_llaves() -> None:
    m = {"a": {"b": 7}}
    assert driver.abre(m, "a.b") == 7
    assert driver.abre(m, "a.c", "ausente") == "ausente"
    assert driver.abre(m, "x.y") is None
    assert driver.abre({"a": 3}, "a.b", "ausente") == "ausente"


# ----------------------------------------- el solver, corrido de verdad ---


def test_corre_u1_reproduce_el_crudo_dentro_de_la_tolerancia_declarada() -> None:
    """Reproduccion del crudo publicado, con la tolerancia declarada y defendida.

    ERRATA MEDIDA en CI (`39556291717`, runner Linux): la version anterior
    aserto `np.array_equal` — "bit a bit" — y paso en macOS/arm64 con
    max|dT| = 0.0, pero en el runner dio max|dT| = 7.105e-15. El "bit a bit"
    no era propiedad del objeto: era propiedad de esta maquina. La suma de
    float64 cambia de orden con el BLAS y el kernel, y el crudo se imprimio con
    otra de esas sumas.

    Lo que si es propiedad del objeto y se puede exigir en cualquier maquina:
    la reproduccion cae orders de magnitud por debajo de la resolucion del
    veredicto. `TOL_REPRODUCCION` se declara y se defiende contra esa
    resolucion: el bin mas cercano a cero del crudo esta a 5.113e-3, el piso a
    5.523e-3, y la tolerancia es 1e-12 — nueve ordenes por debajo del bin mas
    fino. No puede mover un solo veredicto.
    """
    e = _enlace()
    r = driver.corre("u1", True)
    T = np.asarray(r["T"], dtype=np.float64)
    publicado = np.asarray(e["T_U1"], dtype=np.float64)
    desvio = float(np.max(np.abs(T - publicado)))

    assert TOL_REPRODUCCION * 1e9 < driver.PISO_CONTRATO
    assert TOL_REPRODUCCION < float(np.min(np.abs(np.asarray(e["delta_T"]))))
    assert desvio <= TOL_REPRODUCCION, (
        "el solver dejo de reproducir la corrida publicada: max|dT| = %r sobre "
        "una tolerancia declarada de %r (macOS/arm64 midio 0.0; el runner Linux "
        "de 39556291717 midio 7.105e-15)" % (desvio, TOL_REPRODUCCION)
    )

    assert r["nt"] == 2304
    assert r["es_heterogeneo"] is True
    assert r["identidad_inv_eps_igual_a_K"] is True
    assert r["identidad_inv_mu_igual_a_uno"] is True
    assert abs(r["T_media"] - e["corridas"][0]["T_media"]) <= TOL_REPRODUCCION
    assert r["K_min"] == e["corridas"][0]["K_min"] == 0.25
    assert r["K_max"] == e["corridas"][0]["K_max"] == 1.0


def test_la_convencion_de_ejes_no_es_un_no_op() -> None:
    cargada = driver.S.cargar_mascara("u1", driver.N)
    cruda = np.ascontiguousarray(
        np.load(driver.S.GEO / "u1" / "malla_u1_n384_k2.npy"), dtype=np.float64
    )
    assert cargada.shape == (driver.N, driver.N)
    assert not np.array_equal(cargada, cruda)
    assert np.array_equal(cargada, cruda.T)


def test_par_ausente_falla_cerrado_sin_rc() -> None:
    with pytest.raises(SystemExit) as exc:
        driver.corre("no_existe", True)
    assert isinstance(exc.value.code, str)
    assert "mascara ausente bajo custodia" in exc.value.code


# -------------------------------------------- main(), con corre inyectado ---


def _monta_crudos(tmp_path: Path) -> Path:
    destino = tmp_path / "crudos"
    destino.mkdir(parents=True, exist_ok=True)
    (destino / driver.CRUDO_C1).write_text(
        CRUDO_C1.read_text(encoding="utf-8"), encoding="utf-8"
    )
    return destino


def test_main_firma_cero_y_escribe_el_crudo(tmp_path, monkeypatch) -> None:
    destino = _monta_crudos(tmp_path)
    monkeypatch.setattr(driver.S, "CRUDOS", destino)

    nu = _nu_sintetico()
    T = _T_sintetico()
    inyectado = {"transpuesta": T, "sin_transponer": T + 1.0}

    def corre_falso(real: str, transponer: bool) -> dict:
        return _realizacion(nu, inyectado["transpuesta" if transponer else "sin_transponer"], transponer)

    monkeypatch.setattr(driver, "corre", corre_falso)

    rc = driver.main()
    assert rc == 0

    escritos = sorted(p for p in destino.glob("crudo_ENLACE_ACUSTICA_FOTONICA_*.json"))
    assert len(escritos) == 1, escritos
    d = json.loads(escritos[0].read_text(encoding="utf-8"))

    assert d["realizaciones"] == list(driver.REALIZACIONES)
    assert d["n"] == driver.N and d["modo"] == driver.MODO and d["L_a"] == driver.L_A
    assert d["nu_iguales_en_todas_las_corridas"] is True
    assert d["piso_declarado_en_el_crudo_C1"] == driver.PISO_MEDIDO
    assert d["declarado_antes_de_medir"]["piso_contrato"] == driver.PISO_CONTRATO
    assert d["declarado_antes_de_medir"]["factor"] == driver.FACTOR

    U2 = np.vstack([T for _ in range(5)])
    esperado = driver.veredicto(T, U2, driver.PISO_CONTRATO, driver.DDQF)
    assert d["n_discrepa"] == esperado["n_discrepa"]
    assert d["n_nulo"] + d["n_discrepa"] == BINS
    assert d["control_convencion"]["T_U1_identico_al_declarado"] is False


def test_el_flag_de_convencion_discrimina(tmp_path, monkeypatch) -> None:
    destino = _monta_crudos(tmp_path)
    monkeypatch.setattr(driver.S, "CRUDOS", destino)

    nu = _nu_sintetico()
    T = _T_sintetico()

    def corre_igual(real: str, transponer: bool) -> dict:
        return _realizacion(nu, T, transponer)

    monkeypatch.setattr(driver, "corre", corre_igual)
    assert driver.main() == 0
    escritos = sorted(destino.glob("crudo_ENLACE_ACUSTICA_FOTONICA_*.json"))
    d = json.loads(escritos[-1].read_text(encoding="utf-8"))
    assert d["control_convencion"]["T_U1_identico_al_declarado"] is True
