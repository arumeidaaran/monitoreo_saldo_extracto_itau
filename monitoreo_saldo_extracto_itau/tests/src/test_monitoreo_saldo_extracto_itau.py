from monitoreo_saldo_extracto_itau import entrar_sitio_itau

def test_entrar_sitio_itau():
    resultado_test_entrar_sitio_itau = entrar_sitio_itau()

    assert resultado_test_entrar_sitio_itau == {
        'status': 'done',
        'reason': f'Función procesada',
        'data': None
    }

