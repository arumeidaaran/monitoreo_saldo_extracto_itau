from py_rpautom.python_utils import processo_existente

from monitoreo_saldo_extracto_itau import entrar_sitio_itau


def test_entrar_sitio_itau_con_chrome():
    resultado_test_entrar_sitio_itau = entrar_sitio_itau()

    assert resultado_test_entrar_sitio_itau == {
        'status': 'done',
        'reason': 'Función procesada',
        'data': True
    }
    assert processo_existente('chrome') == True
