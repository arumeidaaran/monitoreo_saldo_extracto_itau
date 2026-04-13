from src.utils.utils import validar_webdriver


def test_validar_webdriver_con_modo_activo_y_chromedriver(setup_navegador):
    assert setup_navegador['status'] == 'done'

    resultado_validar_webdriver = validar_webdriver(
        modo='activo',
        nome_webdriver='chromedriver',
    )

    assert resultado_validar_webdriver['data'] is True
