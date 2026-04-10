# Nome: ItauAutomacao
from py_rpautom.python_utils import coletar_pid, finalizar_processo
from py_rpautom.web_utils import iniciar_navegador

from utils.utils import validar_webdriver

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
