# Nome: ItauAutomacao
from py_rpautom.web_utils import iniciar_navegador
from py_rpautom.python_utils import processo_existente, finalizar_processo, coletar_pid


def entrar_sitio_itau():
    resultado = {
        'status': 'done',
        'reason': '',
        'data': None
    }

    try:
        resutlado_validar_webdriver = validar_webdriver(
            'activo',
            'chromedriver'
        )

        if resutlado_validar_webdriver['data']:
            resultado_coletar_pid = coletar_pid('chromedriver')
            [
                finalizar_processo(processo['pid'])
                for processo in resultado_coletar_pid
            ]

        resultado_iniciar_navegador = iniciar_navegador(
            url='https://itau.com.br',
            nome_navegador='chrome',
            # options=(('--start-maximized'),)
        )

        if resultado_iniciar_navegador == False:
            resultado['reason'] = 'Error al ejecutar iniciar_navegador'
            raise RuntimeError(resultado['reason'])

        resultado['data'] = resultado_iniciar_navegador
        resultado['reason'] = 'Función procesada'
    except Exception as error:
        resultado['status'] = 'undone'

        if resultado['reason'] == '':
            resultado['reason'] = str(error)

    return resultado


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

