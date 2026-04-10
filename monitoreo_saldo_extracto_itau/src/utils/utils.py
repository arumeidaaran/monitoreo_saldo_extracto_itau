from py_rpautom.python_utils import processo_existente


def validar_webdriver(modo: str, nome_webdriver: str):
    resultado = {
        'status': 'done',
        'reason': '',
        'data': None
    }

    try:
        if not isinstance(modo, str):
            raise ValueError('Parametro modo necesita ser str')

        if (
            modo.upper() != 'ACTIVO' and
            modo.upper() != 'DESACTIVO'
        ):
            raise ValueError('Modo de ejecución no existe')

        if not isinstance(nome_webdriver, str):
            raise ValueError('Parametro modo necesita ser str')

        if (
            nome_webdriver.upper() != 'CHROMEDRIVER' and
            nome_webdriver.upper() != 'EDGEDRIVER' and
            nome_webdriver.upper() != 'GECKODRIVER'
        ):
            raise ValueError('Nome de webdriver no válido')

        esta_activo = modo.upper() == 'ACTIVO'

        resultado['data'] = processo_existente(
            nome_webdriver.lower()
        ) == esta_activo
        resultado['reason'] = 'Función procesada'
    except Exception as error:
        resultado['status'] = 'undone'

        if resultado['reason'] == '':
            resultado['reason'] = str(error)

    return resultado
