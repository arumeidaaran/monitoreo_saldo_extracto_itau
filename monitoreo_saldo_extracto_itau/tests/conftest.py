from py_rpautom.python_utils import coletar_pid, finalizar_processo
from py_rpautom.web_utils import encerrar_navegador
from pytest import fixture

from src.utils.pom import entrar_sitio_itau


def _encerrar_navegador_silenciosamente():
    try:
        encerrar_navegador()
    except Exception:
        # Some tests open the browser conditionally,
        #   so teardown should be safe.
        pass

    # try:
    #     resultado_coletar_pid = coletar_pid('chromedriver')
    #     for processo in resultado_coletar_pid:
    #         finalizar_processo(processo['pid'])
    # except Exception:
    #     pass


@fixture
def setup_navegador():
    resultado = entrar_sitio_itau(False)
    try:
        yield resultado
    finally:
        _encerrar_navegador_silenciosamente()


@fixture
def teardown_navegador():
    try:
        yield
    finally:
        _encerrar_navegador_silenciosamente()
