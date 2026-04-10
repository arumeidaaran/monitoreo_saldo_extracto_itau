import utils # type: ignore

def test_validar_webdriver_con_modo_activo_y_chromedriver():
    resultado_validar_webdriver =  utils.utils.validar_webdriver(
        modo='activo',
        nome_webdriver='chromedriver',
    )

    assert resultado_validar_webdriver['data'] == True
