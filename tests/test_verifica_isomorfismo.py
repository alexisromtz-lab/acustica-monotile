# HUELLA-EJECUTOR-VERIFICA-ISOMORFISMO-20261020
"""Ejecutor del instrumento del isomorfismo — acustica-monotile.

`sim/verifica_isomorfismo.py` (196 l.) decidia solo, y nadie lo ejecutaba: el
censo `censo_numpy_dependencia_20261020.py` lo dejaba fuera de los portadores
ejecutados. Habia foto de su rojo historico (`crudos/isomorfismo_20261012T070415Z.json`,
medido por `tests/test_cifras_publicadas.py`), pero una foto del crudo **no**
es ejecutar el veredicto: se puede conservar el rojo y a la vez tener un
instrumento que ya no sabe ponerse rojo.

Este test abre el instrumento y **exige los tres veredictos que declara**:
el `RC=0` con datos reales y, sobre filas sinteticas, el `RC=2` (control
positivo muerto) y el `RC=3` (caso ratificado no exacto). Un test que solo
mide el caso feliz no distingue un verificador de un adorno.

Desviaciones medidas contra la orden que autorizo este acto (la orden no se
reescribe, se corrige con el numero delante):

  1. RUTA: la orden apuntaba a un `sim/tests/test_verifica_isomorfismo.py` del
     corpus de custodia. Ese corpus no tiene `sim/tests/` y su CI no corre
     pytest: el ejecutor vive donde vive el objeto
     (`acustica-monotile/tests/`), o no ejecuta nada.
  2. MALFORMADO: la orden esperaba `RC 2` para una entrada malformada. El
     contrato real del objeto es `ValueError` en `alfa_de_fila` y en
     `residuo_del_mapeo` (falla cerrado por excepcion, no por codigo de salida).
     El test exige el contrato medido, no el previsto.

Falsadores declarados (lo que pone rojo a este test):

  1. numpy ausente -> este modulo lo importa en su cabecera: la coleccion
     levanta `ModuleNotFoundError` y el test no empieza. Ya medido en vivo en
     `39551443489` (rama desechable sin la linea de numpy en el manifiesto).
  2. el caso `B_ratificado` deja de ser exacto (residuo != 0) -> test 1 cae.
  3. el control positivo deja de discriminar (su maximo pasa a 0) -> test 2,
     y el `VERDE` del test 6 se convierte en `RC=2`: la casa prefiere
     declararse rota antes que firmar un verde vacio.
  4. la rama `elif ctrl_max <= 0.0` se borra o cambia de codigo -> test 7 cae
     (el instrumento ya no sabe decir `RC=2`).
  5. el defecto del control se extiende a las tres ecuaciones -> test 2 cae:
     el control planta el defecto en `p` y solo en `p`, y eso es medible.
  6. `rel()` devuelve 0.0 en vez de `None` con denominador nulo -> test 5 cae
     (un no-medido disfrazado de cero es el verde falso que este instrumento
     declara no querer).
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parents[1]
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

from sim import verifica_isomorfismo as instrumento  # noqa: E402

FILAS_ESPERADAS = 12          # 3 medios x (1 ratificada + 2 invertidas) + 3 controles
MEDIOS = ("uniforme (rho=1, K=1)", "densimetrico (rho 1->4, K=1)", "modulo (rho=1, K 1->0.25)")
CONTROL = 0.3333333333333333  # 1.5 - 1: el unico defecto que el control planta


def _filas():
    return instrumento.corre()


def _por_asignacion(filas, asignacion):
    return [f for f in filas if f["asignacion"] == asignacion]


def _main(monkeypatch, tmp_path, capsys, filas=None):
    """Corre `main()` en un cwd desechable: el instrumento escribe `crudos/`."""
    if filas is not None:
        monkeypatch.setattr(instrumento, "corre", lambda: filas)
    monkeypatch.chdir(tmp_path)
    rc = instrumento.main()
    return rc, capsys.readouterr().out


def _sello(tmp_path):
    crudos = sorted((tmp_path / "crudos").glob("isomorfismo_*.json"))
    assert len(crudos) == 1, crudos
    return json.loads(crudos[0].read_text(encoding="utf-8"))


def test_el_caso_ratificado_es_exacto_en_los_tres_medios_y_las_tres_ecuaciones():
    """La fila B es identidad de los lados derechos: residuo exactamente 0.0."""
    filas = _por_asignacion(_filas(), "B_ratificado")
    assert [f["medio"] for f in filas] == list(MEDIOS)
    for f in filas:
        assert (f["p"], f["vx"], f["vy"]) == (0.0, 0.0, 0.0), f


def test_el_control_positivo_discrimina_y_localiza_el_defecto_en_una_ecuacion():
    """El control planta 1.5 en eps: el mapeo deja de ser exacto SOLO en `p`."""
    control = _por_asignacion(_filas(), "B_control_x1.5")
    assert len(control) == 3
    for f in control:
        assert f["p"] == CONTROL, f
        assert f["vx"] == 0.0 and f["vy"] == 0.0, f


def test_el_contrato_invertido_solo_cae_donde_el_medio_no_es_homogeneo():
    """En el medio homogeneo las tres asignaciones coinciden: por eso no decide."""
    filas = _filas()
    homogeneo = [f for f in filas
                 if f["medio"] == MEDIOS[0] and f["asignacion"] != "B_control_x1.5"]
    assert len(homogeneo) == 3
    for f in homogeneo:
        assert (f["p"], f["vx"], f["vy"]) == (0.0, 0.0, 0.0), f

    invertido_alfa1 = [f for f in filas
                       if f["fila"] == "A_invertido_alfa1" and f["medio"] != MEDIOS[0]]
    assert len(invertido_alfa1) == 2
    for f in invertido_alfa1:
        assert f["p"] > 0.0, f


def test_el_defecto_del_mapeo_invertido_no_depende_del_medio():
    """El contrato A falla por el MAPEO, no por la inclusion: mismo 0.75 en los dos."""
    invertido_alfa1 = [f for f in _filas()
                       if f["fila"] == "A_invertido_alfa1" and f["medio"] != MEDIOS[0]]
    assert invertido_alfa1[0]["p"] == invertido_alfa1[1]["p"], invertido_alfa1

    invertido_eps_mu = [f for f in _filas()
                        if f["fila"] == "A_invertido_alfa_eps_mu" and f["medio"] != MEDIOS[0]]
    assert invertido_eps_mu[0]["p"] != invertido_eps_mu[1]["p"], invertido_eps_mu


def test_un_no_medido_no_es_un_cero():
    """Denominador nulo -> None. Un cero que cuadra consigo mismo es un verde falso."""
    np = instrumento.np
    assert instrumento.rel(np.ones((2, 2)), np.zeros((2, 2))) is None
    assert instrumento.rel(np.zeros((2, 2)), np.ones((2, 2))) == 1.0
    assert instrumento.fmt(None) == "NO_MEDIDO"
    assert instrumento.fmt(0.0) == "0.000000e+00"


def test_el_verde_es_derivado_y_su_rc_impreso_coincide_con_el_sellado(monkeypatch, tmp_path, capsys):
    """RC 0: la prosa impresa no puede contradecir al sello que el mismo crudo escribe."""
    rc, salida = _main(monkeypatch, tmp_path, capsys)

    assert rc == 0
    assert "VEREDICTO=VERDE" in salida
    assert "RC=0" in salida
    assert "CASO_B_exacto_en_los_tres_medios_y_las_tres_ecuaciones = True" in salida
    assert "MEDIO_HOMOGENEO_todo_cero = True" in salida

    sello = _sello(tmp_path)
    assert sello["rc"] == rc
    assert sello["veredicto"] == "VERDE"
    assert sello["B_todo_cero"] is True
    assert sello["homogeneo_todo_cero"] is True
    assert sello["control_positivo_max"] == CONTROL
    assert sello["n"] == instrumento.N
    assert len(sello["filas"]) == FILAS_ESPERADAS
    for f in sello["filas"]:
        assert set(f) == {"p", "vx", "vy", "medio", "fila", "asignacion"}, f


def test_un_control_muerto_declara_rc_2(monkeypatch, tmp_path, capsys):
    """La orden: el test debe EXIGIR el RC 2. Control muerto => el instrumento se declara roto."""
    filas = [dict(f) for f in _filas()]
    for f in filas:
        if f["asignacion"] == "B_control_x1.5":
            f["p"] = f["vx"] = f["vy"] = 0.0

    rc, salida = _main(monkeypatch, tmp_path, capsys, filas)

    assert rc == 2
    assert "ROJO: el control positivo no discrimina => el instrumento no mide" in salida
    assert "VEREDICTO=VERDE" not in salida
    sello = _sello(tmp_path)
    assert sello["rc"] == rc == 2
    assert sello["control_positivo_max"] == 0.0


def test_un_caso_ratificado_torcido_declara_rc_3(monkeypatch, tmp_path, capsys):
    """El otro rojo publicado: el control discrimina pero B deja de ser exacto."""
    filas = [dict(f) for f in _filas()]
    filas[0]["p"] = 1e-9

    rc, salida = _main(monkeypatch, tmp_path, capsys, filas)

    assert rc == 3
    assert "ROJO: el caso ratificado B no es exacto" in salida
    sello = _sello(tmp_path)
    assert sello["rc"] == rc == 3


def test_entrada_malformada_falla_cerrado():
    """Contrato medido: ValueError, no un codigo de salida inventado por la orden."""
    with pytest.raises(ValueError):
        instrumento.alfa_de_fila("fila_inexistente", None, None)

    _, rho, K, _ = instrumento.medios(4)[0]
    with pytest.raises(ValueError):
        instrumento.residuo_del_mapeo(rho, K, "asignacion_inexistente", 1.0)


def test_las_filas_declaran_su_alfa_y_no_lo_heredan():
    """El defecto historico (07:04:15Z): la fila B recibio el alfa de la fila A."""
    assert instrumento.alfa_de_fila("B_ratificado", None, None) == 1.0
    assert instrumento.alfa_de_fila("A_invertido_alfa1", None, None) == 1.0

    np = instrumento.np
    rho = np.full((4, 4), 4.0)
    K = np.ones((4, 4))
    alfa = instrumento.alfa_de_fila("A_invertido_alfa_eps_mu", rho, K)
    assert bool(np.all(alfa == 0.25)), alfa
