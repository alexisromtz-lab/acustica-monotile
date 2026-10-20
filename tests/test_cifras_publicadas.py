# HUELLA-ACUSTICA-TEST-CIFRAS-20261020
"""Cada cifra que este README publica tiene portador en un crudo sellado.

Molde portado desde `fotonica-monotile/tests/test_cifras_publicadas.py`
(`HUELLA-FOTONICA-TEST-CIFRAS-20261020`): misma estructura, otro dominio
fisico y otro crudo. No vuelve a correr el solver (6 corridas de 384^2 x 2304
pasos mas 4 de la casa C1): mide procedencia e identidad, que es exactamente
lo que un crudo sellado permite medir sin repetir la fisica.

Los falsadores, uno por cada forma de mentir de una cifra:

  1. una cifra de seis o mas decimales en el README sin hoja numerica que la
     respalde dentro de su propio redondeo ni formula derivada declarada;
  2. un crudo editado a mano: `media_T_U2`, `sigma_U2_*`, `umbral`, `delta_T`
     o `veredicto_por_bin` dejan de cumplir las identidades que el propio
     crudo declara;
  3. un veredicto movido: `22 de 29` deja de ser el numero derivado, o los
     controles (`ddof = 0` -> 8, piso medido -> 7, ejes -> 11) dejan de
     reproducirse;
  4. un piso cambiado de sitio: el umbral nominal usa el contrato
     pre-declarado (`0.005523`), no el piso medido; el medido entra como par
     de control y no mueve el veredicto (`control_piso_medido_n_discrepa`);
  5. un instrumento (`sim/*.py`) tocado sin volver a sellar su `sha16`, su
     blob o su numero de lineas;
  6. un rojo borrado del escaparate (`RC=2` del isomorfismo) o un verde
     vacio: `B_todo_cero` deja de derivarse de sus filas.

No hay red y no hay tolerancias elegidas a mano: cada cifra se compara con su
propio redondeo (media unidad del ultimo digito publicado) y cada identidad
con el residuo que la cruda declara, salvo las que el propio crudo sella con
residuo cero, que se exigen exactas.
"""

from __future__ import annotations

import hashlib
import json
import math
import re
import statistics
from pathlib import Path
from typing import Any, Iterable, Iterator

RAIZ = Path(__file__).resolve().parents[1]
GEOMETRIA = RAIZ / "data" / "geometria_hat"
README = RAIZ / "README.md"
CITATION = RAIZ / "CITATION.cff"
ZENODO = RAIZ / ".zenodo.json"

NOMBRE_ENLACE = "crudos/crudo_ENLACE_ACUSTICA_FOTONICA_20261012T204809Z.json"
NOMBRE_C1 = "crudos/crudo_C1_acustica_20261012T072953Z.json"
NOMBRE_ISO_ROJO = "crudos/isomorfismo_20261012T070415Z.json"
NOMBRE_ISO_VERDE = "crudos/isomorfismo_20261012T070744Z.json"
NOMBRE_GEO_U1 = "data/geometria_hat/u1/crudo.json"
NOMBRES_GEO_U2 = tuple(
    f"data/geometria_hat/u2_semilla_{s}/crudo.json" for s in range(101, 106)
)

DOI_VERSION = "10.5281/zenodo.23329941"
DOI_CONCEPTO = "10.5281/zenodo.23329940"

# Una cifra "publicada" es la que se escribe con seis decimales o mas; las de
# menos digitos son redondeos de prosa y no reclaman portador seis-decimal.
PATRON_CIFRA = re.compile(r"-?\d+\.\d{6,}(?:[eE][-+]?\d+)?")
PATRON_VERSION_CFF = re.compile(r'^version:\s*"?([0-9][^"\n]*?)"?\s*$', re.MULTILINE)
PATRON_VERSION_JSON = re.compile(r'"version"\s*:\s*"([^"]+)"')
PATRON_TITULO_CFF = re.compile(r'^title:\s*"(.+)"\s*$', re.MULTILINE)
PATRON_TITULO_JSON = re.compile(r'"title"\s*:\s*"([^"]+)"')

REL = 1e-15
_CACHE: dict[str, Any] = {}


def _texto(rel: str) -> str:
    ruta = RAIZ / rel
    assert ruta.is_file(), f"artefacto ausente: {rel}"
    return ruta.read_text(encoding="utf-8")


def _json(rel: str) -> Any:
    if rel not in _CACHE:
        _CACHE[rel] = json.loads(_texto(rel))
    return _CACHE[rel]


def _sha16(rel: str) -> str:
    return hashlib.sha256((RAIZ / rel).read_bytes()).hexdigest()[:16]


def _lineas(rel: str) -> int:
    return len(_texto(rel).splitlines())


def _blob(rel: str) -> str:
    """git blob SHA-1 reconstruido sin invocar git (identidad de procedencia)."""
    cuerpo = (RAIZ / rel).read_bytes()
    return hashlib.sha1(b"blob %d\0" % len(cuerpo) + cuerpo).hexdigest()


def _readme() -> str:
    return _texto("README.md")


# ---------------------------------------------------------------- universo ---


def test_universo_declarado_29_bins_monotonos() -> None:
    d = _json(NOMBRE_ENLACE)
    nu = d["nu"]
    assert len(nu) == 29
    assert nu[0] == 0.1527114967462039
    assert nu[-1] == 0.5414316702819957
    assert all(a < b for a, b in zip(nu, nu[1:])), "la rejilla no es monotona"
    assert len(set(nu)) == 29
    assert d["nu_iguales_en_todas_las_corridas"] is True
    # El crudo del enlace no publica la rejilla por corrida (solo el booleano de
    # arriba); la rejilla si viaja suelta en las 4 corridas de la casa C1, que
    # comparten ventana con el enlace. Eso se puede medir, y se mide.
    c1 = _json(NOMBRE_C1)
    assert len(c1["corridas"]) == 4
    for corrida in c1["corridas"]:
        assert corrida["nu"] == nu, f"rejilla C1 distinta en {corrida['modo']} L={corrida['L_a']}"
    assert "**29 bins**" in _readme()


def test_las_seis_corridas_son_heterogeneas_y_declaran_su_K() -> None:
    d = _json(NOMBRE_ENLACE)
    esperadas = ["u1"] + [f"u2_semilla_{s}" for s in range(101, 106)]
    assert d["realizaciones"] == esperadas
    assert [c["realizacion"] for c in d["corridas"]] == esperadas
    assert len(d["corridas"]) == 6
    assert d["n"] == 384 and d["L_a"] == 24.0 and d["modo"] == "C1b"
    for corrida in d["corridas"]:
        assert corrida["es_heterogeneo"] is True
        assert corrida["K_min"] == 0.25 and corrida["K_max"] == 1.0
        assert corrida["inv_eps_min"] == 0.25 and corrida["inv_eps_max"] == 1.0
        assert corrida["identidad_inv_eps_igual_a_K"] is True
        assert corrida["identidad_inv_mu_igual_a_uno"] is True
        assert corrida["transpuesta"] is True
        assert (corrida["nx"], corrida["ny"], corrida["nt"]) == (384, 384, 2304)


# ------------------------------------------------------------- identidades ---


def test_media_T_U2_es_la_media_de_las_cinco_semillas() -> None:
    d = _json(NOMBRE_ENLACE)
    U2, media = d["T_U2"], d["media_T_U2"]
    assert len(U2) == 5 and all(len(columna) == 29 for columna in U2)
    assert d["corridas"][0]["T"] == d["T_U1"]
    for k in range(5):
        assert d["corridas"][k + 1]["T"] == U2[k]
    for i in range(29):
        esperado = statistics.fmean([U2[j][i] for j in range(5)])
        assert math.isclose(media[i], esperado, rel_tol=0.0, abs_tol=REL), i


def test_sigma_es_la_desviacion_muestral_ddof1() -> None:
    d = _json(NOMBRE_ENLACE)
    U2, s1 = d["T_U2"], d["sigma_U2_ddof1"]
    assert d["declarado_antes_de_medir"]["ddof_sigma"] == 1
    for i in range(29):
        columna = [U2[j][i] for j in range(5)]
        assert math.isclose(s1[i], statistics.stdev(columna), rel_tol=0.0, abs_tol=REL), i
        assert not math.isclose(
            s1[i], statistics.pstdev(columna), rel_tol=0.0, abs_tol=1e-3
        ), f"bin {i}: ddof = 1 indistinguible de ddof = 0"


def test_el_par_de_control_ddof0_es_la_poblacional() -> None:
    d = _json(NOMBRE_ENLACE)
    U2, s0 = d["T_U2"], d["sigma_U2_ddof0"]
    for i in range(29):
        columna = [U2[j][i] for j in range(5)]
        assert math.isclose(s0[i], statistics.pstdev(columna), rel_tol=0.0, abs_tol=REL), i
    assert s0 != d["sigma_U2_ddof1"]


def test_el_umbral_usa_el_piso_del_contrato() -> None:
    """Errata 9.6: el nominal usa el contrato; el medido es par de control."""
    d = _json(NOMBRE_ENLACE)
    f = d["declarado_antes_de_medir"]
    s, u = d["sigma_U2_ddof1"], d["umbral"]
    assert f["factor"] == 3.0
    assert f["piso_contrato"] == 0.005523
    assert f["piso_medido_C1"] == 0.00552322568652841
    assert round(f["piso_medido_C1"], 6) == f["piso_contrato"], (
        "el contrato debe ser el redondeo a 6 decimales del piso medido"
    )
    for i in range(29):
        assert u[i] == 3.0 * s[i] + f["piso_contrato"], (
            f"bin {i}: el umbral no usa el piso del contrato"
        )
    residuo = max(abs(u[i] - (3.0 * s[i] + f["piso_medido_C1"])) for i in range(29))
    assert math.isclose(
        residuo, 2.2568652857657412e-07, rel_tol=0.0, abs_tol=1e-20
    ), "la distancia entre el piso del contrato y el medido cambio"
    txt = _readme()
    assert "3 · sigma_U2(nu) + 0.005523)" in txt, "el eje del veredicto no publica el contrato"
    assert "### 9.6" in txt, "la errata 9.6 debe declarar cual piso manda"
    assert "**es exactamente** el" not in txt, "la frase retirada por 9.6 sigue en el README"


def test_delta_T_es_la_resta_absoluta_menos_el_umbral() -> None:
    d = _json(NOMBRE_ENLACE)
    U1, media, u, dt = d["T_U1"], d["media_T_U2"], d["umbral"], d["delta_T"]
    for i in range(29):
        assert dt[i] == abs(U1[i] - media[i]) - u[i], i


def test_veredicto_por_bin_es_el_signo_de_delta_T() -> None:
    d = _json(NOMBRE_ENLACE)
    dt, ver = d["delta_T"], d["veredicto_por_bin"]
    assert set(ver) == {"DISCREPA", "NULO"}
    assert len(ver) == 29
    for i, (x, v) in enumerate(zip(dt, ver)):
        assert (x > 0) == (v == "DISCREPA"), i
    assert d["n_discrepa"] == sum(1 for x in dt if x > 0)
    assert d["n_nulo"] == sum(1 for x in dt if x <= 0)
    assert d["n_discrepa"] + d["n_nulo"] == 29
    assert d["n_discrepa"] == 7 and d["n_nulo"] == 22


def test_el_veredicto_publicado_es_7_discrepa_22_nulo() -> None:
    txt = _readme()
    assert "22 de 29" in txt
    assert "7 `DISCREPA` / 22 `NULO`" in txt
    zen = json.loads((RAIZ / ".zenodo.json").read_text(encoding="utf-8"))
    assert "7 DISCREPA / 22 NULO" in zen["description"]
    assert "7 DISCREPA y 22 NULO" in (RAIZ / "CITATION.cff").read_text(encoding="utf-8")


def test_extremos_de_delta_T_publicados() -> None:
    d = _json(NOMBRE_ENLACE)
    dt, nu = d["delta_T"], d["nu"]
    assert d["delta_T_max"] == max(dt) == 1.5697403560585752
    assert d["delta_T_max_nu"] == nu[dt.index(max(dt))] == 0.48590021691973967
    assert d["delta_T_min"] == min(dt) == -3.805628370974314
    assert d["delta_T_min_nu"] == nu[dt.index(min(dt))] == 0.5414316702819957
    txt = _readme()
    for cifra in ("1.5697403560585752", "-3.805628370974314", "0.4859002169197397"):
        assert cifra in txt, cifra


def test_rango_T_U2_max_y_su_bin() -> None:
    d = _json(NOMBRE_ENLACE)
    U2, nu = d["T_U2"], d["nu"]
    rango = [
        max(columna[i] for columna in U2) - min(columna[i] for columna in U2)
        for i in range(29)
    ]
    assert d["rango_T_U2_max"] == max(rango) == 3.4677075111160995
    assert d["rango_T_U2_max_nu"] == nu[rango.index(max(rango))]
    assert d["rango_T_U2_max_nu"] == d["delta_T_min_nu"], (
        "el rango maximo y el delta_T minimo deben caer en el mismo bin"
    )
    assert "3.4677075111160995" in _readme()


def test_sigma_y_umbral_publicados_a_12_decimales() -> None:
    d = _json(NOMBRE_ENLACE)
    s, u = d["sigma_U2_ddof1"], d["umbral"]
    publicadas = {
        "0.107349341659": min(s),
        "1.440029667278": max(s),
        "0.327571024978": min(u),
        "4.325612001835": max(u),
    }
    txt = _readme()
    for cifra, valor in publicadas.items():
        assert f"{valor:.12f}" == cifra, (cifra, valor)
        assert cifra in txt, cifra


def test_reparto_del_nulo_publicado() -> None:
    d = _json(NOMBRE_ENLACE)
    f = d["declarado_antes_de_medir"]
    s, u = d["sigma_U2_ddof1"], d["umbral"]
    reparto = [3.0 * s[i] / u[i] for i in range(29)]
    assert f"{min(reparto):.12f}" == "0.983139534395"
    assert f"{max(reparto):.12f}" == "0.998723186454"
    assert f"{f['piso_medido_C1'] / max(u):.12e}" == "1.276865720778e-03"
    assert f"{f['piso_contrato'] / max(u):.12e}" != "1.276865720778e-03", (
        "esa cifra solo sale con el piso medido: no es intercambiable"
    )
    txt = _readme()
    for cifra in ("0.983139534395", "0.998723186454", "1.276865720778e-03"):
        assert cifra in txt, cifra


def test_control_ddof0_reproduce_el_8_publicado() -> None:
    d = _json(NOMBRE_ENLACE)
    f = d["declarado_antes_de_medir"]
    U1, media, s0 = d["T_U1"], d["media_T_U2"], d["sigma_U2_ddof0"]
    n0 = sum(
        1
        for i in range(29)
        if abs(U1[i] - media[i]) - (f["factor"] * s0[i] + f["piso_contrato"]) > 0
    )
    assert n0 == d["control_ddof0_n_discrepa"] == 8
    assert "**8** `DISCREPA`" in _readme()


def test_control_del_piso_medido_no_mueve_el_veredicto() -> None:
    d = _json(NOMBRE_ENLACE)
    f = d["declarado_antes_de_medir"]
    U1, media, s1 = d["T_U1"], d["media_T_U2"], d["sigma_U2_ddof1"]
    nm = sum(
        1
        for i in range(29)
        if abs(U1[i] - media[i]) - (f["factor"] * s1[i] + f["piso_medido_C1"]) > 0
    )
    assert nm == d["control_piso_medido_n_discrepa"] == 7 == d["n_discrepa"]
    assert "**7** `DISCREPA`" in _readme()


def test_control_de_convencion_no_es_un_no_op() -> None:
    d = _json(NOMBRE_ENLACE)
    cc = d["control_convencion"]
    assert len(cc["delta_T"]) == 29
    assert sum(1 for x in cc["delta_T"] if x > 0) == cc["n_discrepa"] == 11
    assert cc["T_U1_identico_al_declarado"] is False
    assert cc["T_U1"] != d["T_U1"], "el control de ejes debe mover la medicion"
    assert "NO es veredicto" in cc["descripcion"]
    assert "**11** `DISCREPA`" in _readme()


def test_llenado_dos_denominadores_no_fusionables() -> None:
    d = _json(NOMBRE_ENLACE)
    ll = d["llenado_dos_denominadores"]
    assert ll["cobertura_union_U1"] == ll["media_mascara_binaria"] == 0.4036797417534722
    assert ll["suma_areas_analitico"] == 0.4038327588420457
    assert ll["suma_areas_analitico"] != ll["cobertura_union_U1"]
    g = _json(NOMBRE_GEO_U1)
    assert g["u1"]["suma_areas"] == ll["suma_areas_analitico"]
    assert g["u1"]["cobertura"] == ll["cobertura_union_U1"]
    assert g["fraccion_de_llenado"]["cobertura_union_U1"] == ll["cobertura_union_U1"]
    u1 = next(c for c in d["corridas"] if c["realizacion"] == "u1")
    assert u1["fraccion_mascara_union"] == ll["media_mascara_binaria"]


def test_custodia_de_la_geometria_verifica() -> None:
    custodia = GEOMETRIA / "CUSTODIA_SHA256.txt"
    entradas = [
        linea.split()
        for linea in custodia.read_text(encoding="utf-8").splitlines()
        if linea.strip()
    ]
    assert len(entradas) == 18
    for sha, rel in entradas:
        assert hashlib.sha256((GEOMETRIA / rel).read_bytes()).hexdigest() == sha, rel
    u1 = {sha for sha, rel in entradas if rel.endswith("malla_u1_n384_k2.npy")}
    u2 = [sha for sha, rel in entradas if rel.endswith("malla_u2_n384_k2.npy")]
    assert len(u1) == 1, "la mascara U1 debe ser la misma en las 6 carpetas"
    assert len(u2) == 6 and len(set(u2)) == 5, "U2 debe variar con la semilla"


# ----------------------------------------------------------- procedencia ---


def test_instrumentos_por_hash_de_archivo_y_blob_git() -> None:
    publicados = {
        "sim/sim_acustica2d.py": (
            626,
            "49c429e5cbedc4d0",
            "4de2c841e0d6e6b2757c371ef5cca1e4661b646b",
        ),
        "sim/driver_enlace_fotonica_acustica.py": (
            352,
            "0a896230fa53d108",
            "a0ab6ac8b3b14ef42d0b5fad4f9db281a301c6f6",
        ),
        "sim/verifica_isomorfismo.py": (196, "10011010c00dc8d3", None),
    }
    txt = _readme()
    for rel, (n, sha16, blob) in publicados.items():
        assert _lineas(rel) == n, rel
        assert _sha16(rel) == sha16, rel
        assert sha16 in txt, rel
        if blob is not None:
            assert _blob(rel) == blob, rel
            assert blob in txt, rel
    assert _blob("ACTA_DE_CIERRE_DEL_ENLACE_ACUSTICA_FOTONICA_20261012.md") == (
        "c10d5efba6920a192f890b75fc48effdf1c97054"
    )
    assert _blob("PREREGISTRO_ACUSTICA_MONOTILE_20261012.md") == (
        "075a05b425e182cf9f5a54edbc86af60e9e13f85"
    )
    enlace = _json(NOMBRE_ENLACE)
    assert _blob("sim/sim_acustica2d.py") in enlace["UNIVERSO DECLARADO"]


def test_piso_de_ruido_es_el_riz_T_max_de_C1() -> None:
    c1 = _json(NOMBRE_C1)
    assert c1["PISO_DE_RUIDO_riz_T_max"] == c1["riz_T_por_modo"]["C1b"]
    assert (
        c1["PISO_DE_RUIDO_riz_T_max"]
        == max(c1["riz_T_por_modo"].values())
        == 0.00552322568652841
    )
    for modo in ("C1a", "C1b"):
        assert c1["riz_T_por_modo"][modo] == max(
            r["T_riz"] for r in c1["corridas"] if r["modo"] == modo
        )
        assert c1["T_desv_max_por_modo"][modo] == max(
            r["T_desv_max"] for r in c1["corridas"] if r["modo"] == modo
        )
    assert c1["T_desv_max_por_modo"]["C1b"] == 0.004258596071401777
    assert all(r["T_riz"] != 0.004258596071401777 for r in c1["corridas"]), (
        "0.004258596071401777 es una desviacion maxima de T, no un riz"
    )
    enlace = _json(NOMBRE_ENLACE)
    assert (
        enlace["declarado_antes_de_medir"]["piso_medido_C1"]
        == c1["PISO_DE_RUIDO_riz_T_max"]
    )
    assert enlace["piso_declarado_en_el_crudo_C1"] == c1["PISO_DE_RUIDO_riz_T_max"]
    assert c1["sha16_script"] == "84721caf685985b3"
    assert c1["sha16_script"] != _sha16("sim/sim_acustica2d.py"), (
        "el crudo C1 sella el solver anterior al mapeo K(x,y); el actual debe diferir"
    )
    assert c1["fase_error_max_C1a"] <= c1["factor_q4"] * c1["yee_error_fase_max_ventana"]
    assert all(
        c1[k] is True
        for k in (
            "ANALOGO_PRESTADO_Q1_riz_T_ok",
            "ANALOGO_PRESTADO_Q2_delta_ok",
            "ANALOGO_PRESTADO_Q3_T_ok",
            "ANALOGO_PRESTADO_Q4_fase_ok",
        )
    )


def test_el_umbral_de_planitud_es_prestado_y_declarado() -> None:
    c1 = _json(NOMBRE_C1)
    assert c1["umbral_planitud_prestado"] == 0.05
    assert "PRESTADO" in c1["origen_del_umbral"]
    assert "NO sellado" in c1["origen_del_umbral"]
    assert c1["identidad_inv_eps_en_todas_las_corridas"] is True


def test_contraste_C2_no_es_derivable_de_lo_congelado() -> None:
    c1 = _json(NOMBRE_C1)
    reparto = c1["reparto_constitutivo"]
    assert reparto["K_mat_declarado_no_usado"] == 0.25
    assert reparto["K_0"] == 1.0 and reparto["inv_mu_fijo"] == 1.0
    assert len(c1["corridas"]) == 4
    assert all(r["K_C1"] == 1.0 for r in c1["corridas"]), (
        "si aparece una corrida con K != 1, C2 deja de estar pendiente"
    )
    txt = _readme()
    assert "### 9.3" in txt and "No se ejecuta" in txt


def test_el_isomorfismo_rojo_se_conserva() -> None:
    rojo = _json(NOMBRE_ISO_ROJO)
    assert rojo["rc"] == 2
    assert "control positivo no discrimina" in rojo["veredicto"]
    assert rojo["B_todo_cero"] is False
    assert len(rojo["filas"]) == 12
    control = [f for f in rojo["filas"] if f["fila"] == "CONTROL_positivo_B_x1.5"]
    assert len(control) == 3, "un control positivo por medio"
    firmas = {(f["p"], f["vx"], f["vy"]) for f in control}
    assert len(firmas) == 1, (
        "el control positivo varia con el medio: ya no es el rojo sellado"
    )
    assert control[0]["p"] == 0.3333333333333333
    assert control[0]["p"] * 1.5 != control[0]["p"], "el factor x1.5 no se aplica al control"
    assert "`RC=2`" in _readme()


def test_el_isomorfismo_verde_no_es_un_cero_vacio() -> None:
    verde = _json(NOMBRE_ISO_VERDE)
    assert verde["rc"] == 0 and verde["veredicto"] == "VERDE"
    ratificados = [f for f in verde["filas"] if f["asignacion"] == "B_ratificado"]
    homogenos = [
        f
        for f in verde["filas"]
        if f["medio"].startswith("uniforme") and f["fila"] != "CONTROL_positivo_B_x1.5"
    ]
    assert len(ratificados) == 3 and len(homogenos) == 3
    assert verde["B_todo_cero"] is all(f["p"] == 0.0 for f in ratificados)
    assert all(f["p"] == 0.0 and f["vx"] == 0.0 and f["vy"] == 0.0 for f in homogenos)
    assert verde["homogeneo_todo_cero"] is True
    assert verde["B_todo_cero"] is True
    # el unico no-cero del bloque homogeneo es el control positivo, por diseno
    assert verde["control_positivo_max"] == 0.3333333333333333
    control = [f for f in verde["filas"] if f["fila"] == "CONTROL_positivo_B_x1.5"]
    assert {f["p"] for f in control} == {0.3333333333333333}
    rojo = _json(NOMBRE_ISO_ROJO)
    assert verde["semilla"] == rojo["semilla"]


def test_cita_doi_version_y_concepto() -> None:
    txt = _readme()
    assert DOI_VERSION in txt and DOI_CONCEPTO in txt
    cff = CITATION.read_text(encoding="utf-8")
    zen = ZENODO.read_text(encoding="utf-8")
    version_cff = PATRON_VERSION_CFF.search(cff)
    version_zen = PATRON_VERSION_JSON.search(zen)
    assert version_cff is not None and version_zen is not None
    assert version_cff.group(1).strip() == "0.1.0"
    assert version_cff.group(1).strip() == version_zen.group(1)
    assert version_cff.group(1).strip() != "1.2.0", "cff-version no es la version del paquete"
    titulo_cff = PATRON_TITULO_CFF.search(cff)
    titulo_zen = PATRON_TITULO_JSON.search(zen)
    assert titulo_cff is not None and titulo_zen is not None
    assert titulo_cff.group(1) == titulo_zen.group(1)


# -------------------------------------------- el barrido de las cifras ----


def _numeros(objeto: Any) -> Iterator[float]:
    if isinstance(objeto, dict):
        for valor in objeto.values():
            yield from _numeros(valor)
    elif isinstance(objeto, list):
        for valor in objeto:
            yield from _numeros(valor)
    elif isinstance(objeto, bool):
        return
    elif isinstance(objeto, (int, float)):
        yield float(objeto)


def _corpus_numerico() -> list[float]:
    rutas = (
        NOMBRE_ENLACE,
        NOMBRE_C1,
        NOMBRE_ISO_ROJO,
        NOMBRE_ISO_VERDE,
        NOMBRE_GEO_U1,
    ) + NOMBRES_GEO_U2
    numeros: list[float] = []
    for rel in rutas:
        numeros.extend(_numeros(_json(rel)))
    return numeros


def _derivados() -> Iterable[float]:
    """Cifras que el crudo no sella sueltas sino como formula declarada."""
    d = _json(NOMBRE_ENLACE)
    f = d["declarado_antes_de_medir"]
    s, u = d["sigma_U2_ddof1"], d["umbral"]
    yield f["piso_medido_C1"] / max(u)
    yield f["piso_contrato"] / max(u)
    for i in range(29):
        yield f["factor"] * s[i] / u[i]
        yield abs(u[i] - (f["factor"] * s[i] + f["piso_medido_C1"]))
        yield abs(u[i] - (f["factor"] * s[i] + f["piso_contrato"]))


def _decimales(cifra: str) -> int:
    m = re.match(r"-?(\d+)\.(\d+)(?:[eE](-?\d+))?$", cifra)
    assert m is not None, cifra
    return len(m.group(2)) - int(m.group(3) or 0)


def _tiene_portador(cifra: str, portadores: list[float]) -> bool:
    valor = float(cifra)
    quantum = 10.0 ** -_decimales(cifra)
    return any(abs(valor - portador) < quantum + 1e-18 for portador in portadores)


def test_ninguna_cifra_de_seis_decimales_queda_sin_portador() -> None:
    publicadas = sorted(set(PATRON_CIFRA.findall(_readme())))
    assert len(publicadas) >= 20, "el barrido no puede ser vacuo"
    for ancla in ("0.327571024978", "0.4036797417534722", "3.4677075111160995"):
        assert ancla in publicadas, ancla
    portadores = _corpus_numerico() + list(_derivados())
    huerfanas = [c for c in publicadas if not _tiene_portador(c, portadores)]
    assert huerfanas == [], f"cifras sin portador en ningun crudo: {huerfanas}"
