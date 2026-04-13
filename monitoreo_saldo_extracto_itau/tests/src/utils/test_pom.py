from py_rpautom.python_utils import processo_existente

from src.utils.pom import entrar_sitio_itau


def test_entrar_sitio_itau_con_chrome():
    resultado_test_entrar_sitio_itau = entrar_sitio_itau(False)

    assert resultado_test_entrar_sitio_itau == {
        'status': 'done',
        'reason': 'Función procesada',
        'data': True
    }
    assert processo_existente('chrome') == True
