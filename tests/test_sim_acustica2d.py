# HUELLA-EJECUTOR-SIM-ACUSTICA2D-20261021
"""Ejecutor directo del solver `sim/sim_acustica2d.py` — acustica-monotile.

`sim/sim_acustica2d.py` (626 l.) era el unico portador sin ejecutor **directo**:
lo ejecutaban el driver del enlace y los tests del enlace, pero nadie asertaba
su contrato. Es el mismo patron del driver antes de `8aac8e2`: un objeto que se
usa mucho y no se mide nunca en lo suyo. La diferencia importa — si `correr()`
deja de fallar cerrado ante una malla mal formada, el driver seguiria verde
porque el driver solo le pasa mallas buenas.

Contrato MEDIDO del objeto (no el supuesto):

  * `correr(L_a, modo, mascara=None) -> dict` (l.267) devuelve **41 claves**
    con `nu`, `T`, `T_media`, `T_desv_max`, `fase_error_max`, `K_min/max`,
    `identidad_inv_*`, etc. `ny = 1` si `modo == "C1a"` (1D) y `ny = nx` si no.
  * Las cinco guardas levantan **`SystemExit` cuyo `.code` es un str** (no un
    RC): malla ausente, forma de malla, malla no binaria, mascara que no casa
    con la malla, y malla demasiado corta para la sonda. Igual que
    `cargar_mascara` en el driver: falla cerrado, pero no por codigo.
  * El **nulo homogeneo** (`C1a`, `L=20a`, sin mascara) corre en **0.04 s** —
    no los ~13 s de la bateria 384² — y da `T_teorico = 1.0` con
    `T_media = 0.999673538683`, `T_desv_max = 5.144001050e-3`,
    `fase_error_max = 1.488056718e-3`. Es la unica corrida real de este test.
  * `cargar_mascara` transpone a **ejes del solver** (`.T`) y fuerza
    `float64` contiguo; la mascara bajo custodia es exactamente `{0.0, 1.0}`,
    asi que compararla es exacto (no hay aritmetica de coma flotante).

Desviaciones declaradas contra la orden que autorizo este acto (la orden no se
reescribe, se corrige con el numero delante):

  1. La orden pedia "caso con `T` conocido → tolerancia (`1e-12` muerde,
     `7.105e-15` no)". Esa escala es la del **driver** contra su crudo
     (diferencia entre hosts). Aqui no se reproduce un crudo: se asierta el
     **nulo** contra su valor teorico (`T_teorico = 1.0`), y la tolerancia que
     muerde es `1e-3` (el valor medido dista `3.26e-4` de 1.0). Copiar `1e-12`
     aqui seria asertar un numero que este objeto no produce.
  2. La rama **heterogenea** no se ejecuta en este archivo: el suelo de malla
     (`nx > sonda 16a + PML 20`) la deja en `320x320`, ~13 s por corrida. Se
     ejecuta de verdad en `test_driver_enlace.py` (corrida real `u1`). Aqui solo
     se mide su guarda de forma, que es barata y es la que puede fallar cerrada.
  3. El **modo desconocido no levanta** (medido: `correr(20.0, "ZZZ")` toma
     `ny = nx` y `T_teorico = sqrt(d1/d2)`, o sea monta un C1b silencioso). Es
     un hueco **del objeto**, no de este test: no se asierta (prohibirlo aqui
     seria asertar lo que el objeto no hace) y se declara para que el acta lo
     recoja. Medirlo cuesta 13 s, que este acto no paga.
  4. `main()` no se ejecuta: corre las 12 realizaciones (~2.5 min). Su unico
     `return` es `return 0` (l.622), ya declarado en el ejecutor del driver.

Falsadores probados (mutantes en copia de `sim/`, restaurado el original):

  * `K = np.full(..., K_C1)` -> `K_MAT` en la rama homogenea: cae por
    `K_min == K_C1` y, sobre todo, por `fase_error_max < UMBRAL_PRESTADO`
    (0.4393 medido contra 0.05 declarado; el nulo da 0.001488).
  * `ny = 1 if modo == "C1a" else nx` -> `ny = nx`: cae por `ny == 1`.
  * guarda de forma borrada -> cae por ausencia de `SystemExit`.
  * `.T` borrado en `cargar_mascara` -> cae por la comparacion exacta contra
    el `.npy` transpuesto (la forma no cambia, solo los ejes).
  * guarda de sonda borrada -> cae el caso de malla corta.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pytest

RAIZ = Path(__file__).resolve().parents[1]
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

from sim import sim_acustica2d as S  # noqa: E402

# --- nulo homogeneo medido (L=20a, C1a, sin mascara): 0.04 s, no 13 s -------
L_NULO = 20.0
NX_NULO = 320
NT_NULO = 2304
T_MEDIA_NULO = 0.9996735386830571
T_DESV_NULO = 0.005144001050197189
FASE_NULO = 0.0014880567178716664

TOL_TEORICO = 1e-3        # el valor medido dista 3.26e-4 de 1.0 (3x de margen)
TOL_DESV = 0.01           # el valor medido 5.144e-3 queda 1.94x por debajo

# claves que consumen el driver del enlace y el crudo publicado
CLAVES_CONSUMIDAS = (
    "modo", "L_a", "nx", "ny", "nt", "K_C1", "es_heterogeneo",
    "fraccion_mascara_union", "K_min", "K_max", "inv_eps_min", "inv_eps_max",
    "identidad_inv_eps_igual_a_K", "identidad_inv_mu_igual_a_uno",
    "nu", "T", "T_media", "T_teorico", "T_desv_max", "T_riz",
    "T_min", "T_max", "fase_error", "fase_error_max", "cola_sonda",
    "cola_dominio", "residuo_media_p", "pico_sonda",
)


@pytest.fixture(scope="module")
def nulo() -> dict:
    """La unica corrida real del archivo (0.04 s): el nulo homogeneo."""
    return S.correr(L_NULO, "C1a")


# --------------------------------------------------------------------------
# 1. El nulo homogeneo: la malla, el reparto constitutivo y la identidad
# --------------------------------------------------------------------------
def test_el_nulo_homogeneo_declara_su_malla(nulo: dict) -> None:
    assert nulo["modo"] == "C1a"
    assert nulo["L_a"] == L_NULO
    assert nulo["nx"] == NX_NULO, f"nx medido {nulo['nx']}, se esperaba {NX_NULO}"
    assert nulo["ny"] == 1, (
        f"C1a debe ser 1D (ny=1); ny={nulo['ny']} significa que el modo "
        "se monto como C1b"
    )
    assert nulo["nt"] == NT_NULO, f"nt medido {nulo['nt']}, se esperaba {NT_NULO}"


def test_el_nulo_es_homogeneo_y_no_tiene_fraccion_de_mascara(nulo: dict) -> None:
    assert nulo["es_heterogeneo"] is False
    assert nulo["fraccion_mascara_union"] is None, (
        "sin mascara no hay fraccion: None, no 0.0 (0.0 seria una mascara vacia)"
    )
    assert nulo["K_min"] == S.K_C1
    assert nulo["K_max"] == S.K_C1
    assert S.K_C1 == S.K_FONDO, "C1 es el medio de fondo: K_C1 == K_FONDO"


def test_el_nulo_respeta_la_identidad_constitutiva(nulo: dict) -> None:
    # El lazo exige inv_mu = 1.0 e inv_eps = K; el objeto lo exporta ademas como
    # booleano porque bajo `python3 -O` el assert interno desaparece.
    assert nulo["identidad_inv_eps_igual_a_K"] is True
    assert nulo["identidad_inv_mu_igual_a_uno"] is True
    assert nulo["inv_eps_min"] == S.K_C1
    assert nulo["inv_eps_max"] == S.K_C1


# --------------------------------------------------------------------------
# 2. La fisica del nulo: T = 1 dentro de la tolerancia declarada
# --------------------------------------------------------------------------
def test_el_nulo_da_t_teorico_uno_y_t_media_en_la_tolerancia(nulo: dict) -> None:
    assert nulo["T_teorico"] == 1.0, "C1a es 1D: la transmision teorica es 1"
    assert abs(nulo["T_media"] - 1.0) < TOL_TEORICO, (
        f"T_media medida {nulo['T_media']!r} contra 1.0; tolerancia {TOL_TEORICO} "
        f"(valor de referencia medido: {T_MEDIA_NULO!r})"
    )
    assert len(nulo["T"]) == len(nulo["nu"]), "T y nu van por el mismo eje de bins"
    assert all(np.isfinite(nulo["T"])), "T tiene no-finitos"
    assert nulo["T_min"] > 0.0, "una transmision no puede ser <= 0"


def test_el_nulo_no_discrepa_contra_el_umbral_declarado(nulo: dict) -> None:
    # El nulo es el control: si el nulo discrepara, el umbral no mide nada.
    assert nulo["T_desv_max"] < TOL_DESV, (
        f"T_desv_max {nulo['T_desv_max']!r} >= {TOL_DESV} "
        f"(valor de referencia medido: {T_DESV_NULO!r})"
    )
    assert nulo["fase_error_max"] < S.UMBRAL_PRESTADO, (
        f"fase_error_max {nulo['fase_error_max']!r} >= UMBRAL_PRESTADO "
        f"{S.UMBRAL_PRESTADO} (valor de referencia medido: {FASE_NULO!r})"
    )


def test_el_dict_trae_las_claves_que_el_crudo_consume(nulo: dict) -> None:
    faltan = [k for k in CLAVES_CONSUMIDAS if k not in nulo]
    assert not faltan, f"claves ausentes del dict de correr(): {faltan}"


# --------------------------------------------------------------------------
# 3. Las guardas de `correr()`: fallan cerrado con SystemExit(str)
# --------------------------------------------------------------------------
def test_mascara_que_no_casa_con_la_malla_falla_cerrado() -> None:
    with pytest.raises(SystemExit) as exc:
        S.correr(L_NULO, "C1b", np.zeros((4, 4)))
    assert isinstance(exc.value.code, str), (
        f"el contrato es SystemExit(str), no un RC: {exc.value.code!r}"
    )
    assert exc.value.code == (
        "mascara (4, 4) no casa con la malla (320, 320) de L=20a"
    ), exc.value.code


def test_malla_demasiado_corta_para_la_sonda_falla_cerrado() -> None:
    with pytest.raises(SystemExit) as exc:
        S.correr(4.0, "C1a")
    assert isinstance(exc.value.code, str), exc.value.code
    assert exc.value.code == (
        "malla L=4a demasiado corta para la sonda d=16a"
    ), exc.value.code


# --------------------------------------------------------------------------
# 4. Las guardas de `cargar_mascara()` contra una custodia temporal
# --------------------------------------------------------------------------
@pytest.fixture()
def custodia(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    monkeypatch.setattr(S, "GEO", tmp_path)
    (tmp_path / "u1").mkdir()
    return tmp_path


def test_mascara_ausente_bajo_custodia_falla_cerrado(custodia: Path) -> None:
    esperada = custodia / "u1" / "malla_u1_n64_k2.npy"
    with pytest.raises(SystemExit) as exc:
        S.cargar_mascara("u1", 64)
    assert isinstance(exc.value.code, str), exc.value.code
    assert exc.value.code == f"mascara ausente bajo custodia: {esperada}", exc.value.code


def test_mascara_de_forma_incorrecta_falla_cerrado(custodia: Path) -> None:
    np.save(custodia / "u1" / "malla_u1_n64_k2.npy", np.zeros((8, 8)))
    with pytest.raises(SystemExit) as exc:
        S.cargar_mascara("u1", 64)
    assert isinstance(exc.value.code, str), exc.value.code
    assert exc.value.code == (
        "malla_u1_n64_k2.npy: forma (8, 8), se esperaba (64, 64)"
    ), exc.value.code


def test_mascara_no_binaria_falla_cerrado(custodia: Path) -> None:
    np.save(custodia / "u1" / "malla_u1_n64_k2.npy", np.full((64, 64), 2.0))
    with pytest.raises(SystemExit) as exc:
        S.cargar_mascara("u1", 64)
    assert isinstance(exc.value.code, str), exc.value.code
    assert exc.value.code == "malla_u1_n64_k2.npy: la mascara no es binaria", (
        exc.value.code
    )


# --------------------------------------------------------------------------
# 5. La mascara real bajo custodia: transposicion a ejes del solver
# --------------------------------------------------------------------------
def test_cargar_mascara_transpone_a_ejes_del_solver() -> None:
    m = S.cargar_mascara("u1", 384)
    assert m.shape == (384, 384)
    assert m.dtype == np.float64
    assert m.flags["C_CONTIGUOUS"], "el solver exige mascara contigua"
    assert set(np.unique(m).tolist()) <= {0.0, 1.0}

    # Comparacion exacta: la mascara es binaria, no hay aritmetica de flotantes.
    cruda = np.load(
        RAIZ / "data" / "geometria_hat" / "u1" / "malla_u1_n384_k2.npy"
    ).astype(np.float64)
    assert not np.array_equal(cruda, cruda.T), (
        "la malla de custodia debe ser asimetrica: si fuera simetrica, la "
        "transposicion de cargar_mascara seria invisible y este test no mediria"
    )
    assert np.array_equal(m, cruda.T), (
        "cargar_mascara debe devolver la malla en ejes del solver (transpuesta)"
    )
