from py_rpautom.python_utils import processo_existente

from src.utils.pom import acceder_pagina_login, entrar_sitio_itau


def test_acceder_pagina_login(setup_navegador):
    assert setup_navegador['status'] == 'done'

    resultado_acceder_pagina_login = acceder_pagina_login()

    assert resultado_acceder_pagina_login['status'] == 'done'



def test_entrar_sitio_itau_con_chrome(teardown_navegador):
    resultado_test_entrar_sitio_itau = entrar_sitio_itau(False)

    assert processo_existente('chrome') is True

    assert resultado_test_entrar_sitio_itau == {
        'status': 'done',
        'reason': 'Función procesada',
        'data': True
    }
