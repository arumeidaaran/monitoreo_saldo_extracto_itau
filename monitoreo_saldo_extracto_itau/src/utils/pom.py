from py_rpautom.python_utils import coletar_pid, finalizar_processo
from py_rpautom.web_utils import clicar_elemento, escrever_em_elemento, iniciar_navegador, limpar_campo, selecionar_elemento

from utils.utils import validar_webdriver

XPATH = 'xpath'
CSS_SELECTOR = 'css_selector'

_list_opcion_login = ['CPF', 'AGENCY-ACCOUNT']

def entrar_sitio_itau():
    resultado = {
        'status': '',
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
            options=(('--start-maximized'),)
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


def resolver_login(valor_opcion: str, credenciales: dict[str, str]):
    resultado = {
        'status': '',
        'reason': '',
        'data': None
    }

    try:
        accederPaginaLogin()
        elegirOpcionSeleccion(valor_opcion)

        resultado_hacerLogin = hacerLogin(valor_opcion, credenciales)
        if resultado_hacerLogin['status'] == 'undone':
            raise RuntimeError(resultado_hacerLogin['reason'])

        resultado['status'] = 'done'
        resultado['reason'] = 'Función procesada'
    except Exception as error:
        resultado['status'] = 'undone'
        resultado['reason'] = str(error)

    return resultado


def accederPaginaLogin():
    resultado = {
        'status': '',
        'reason': '',
        'data': None
    }

    try:
        buttonAccederCuentaElementoSelector = (
            'form ~ button[aria-label="Mais acessos"]'
        )
        resultado_clicar_elemento = clicar_elemento(
            seletor=buttonAccederCuentaElementoSelector,
            tipo_elemento=CSS_SELECTOR,
        )

        if (not resultado_clicar_elemento):
            resultado['reason'] = (
                'Elemento de login no localizado. '
                'Es posible que la página esté en modo móvil'
            )

            raise RuntimeError(resultado['reason'])

        resultado['data'] = resultado_clicar_elemento
        resultado['status'] = 'done'
        resultado['reason'] = 'Función procesada'
    except Exception as error:
        resultado['status'] = 'undone'
        resultado['reason'] = str(error)

    return resultado


def elegirOpcionSeleccion(valor_opcion):
    resultado = {
        'status': '',
        'reason': '',
        'data': None
    }

    try:
        if not valor_opcion in _list_opcion_login:
            raise ValueError('Valor incorrecto para valor_opcion')

        select_opciones_aceso_selector = '#idl-more-access-select-login'
        resultado_select_elemento = selecionar_elemento(
            seletor=select_opciones_aceso_selector,
            valor=valor_opcion,
            tipo_elemento=CSS_SELECTOR,
        )
        if (not resultado_select_elemento):
            resultado['reason'] = 'Elemento de select no localizado'
            raise RuntimeError(resultado['reason'])

        resultado['status'] = 'done'
        resultado['reason'] = ''
    except Exception as error:
        resultado['status'] = 'undone'
        resultado['reason'] = str(error)


    return resultado


def hacerLogin(valor_opcion: str, credenciales: dict[str, str]):
    resultado = {
        'status': '',
        'reason': '',
        'data': None
    }

    try:
        if not valor_opcion in _list_opcion_login:
            raise ValueError('Valor incorrecto para valor_opcion')

        match str(valor_opcion).upper():
            case 'CPF':
                if not credenciales.get('CPF'):
                    raise ValueError('credenciales no contiene CPF')

                resultado_login_por_CPF = login_por_CPF(credenciales)
                if resultado_login_por_CPF['status'] == 'undone':
                    raise RuntimeError(resultado_login_por_CPF['reason'])

            case 'AGENCY-ACCOUNT':
                if not credenciales.get('AGENCIA'):
                    raise ValueError('credenciales no contiene agencia')

                if not credenciales.get('cuenta'):
                    raise ValueError('credenciales no contiene cuenta')

                resultado_login_por_agencia_cuenta = login_por_agencia_cuenta(
                    credenciales
                )
                if resultado_login_por_agencia_cuenta['status'] == 'undone':
                    raise RuntimeError(
                        resultado_login_por_agencia_cuenta['reason']
                    )

            case _:
                ...

        resultado['status'] = 'done'
        resultado['reason'] = ''
    except Exception as error:
        resultado['status'] = 'undone'
        resultado['reason'] = str(error)

    return resultado


def login_por_agencia_cuenta(credenciales: dict[str, str]):
    resultado = {
        'status': '',
        'reason': '',
        'data': None
    }

    try:
        input_agencia_selector = 'input[id="idl-more-access-input-agency"]'
        limpar_campo(
            seletor=input_agencia_selector,
            tipo_elemento=CSS_SELECTOR,
        )
        escrever_em_elemento(
            seletor=input_agencia_selector,
            texto=credenciales.get('agencia'),
            tipo_elemento=CSS_SELECTOR,
        )

        input_ceunta_selector = 'input[id="idl-more-access-input-account"]'
        limpar_campo(
            seletor=input_ceunta_selector,
            tipo_elemento=CSS_SELECTOR,
        )
        escrever_em_elemento(
            seletor=input_ceunta_selector,
            texto=credenciales.get('cuenta'),
            tipo_elemento=CSS_SELECTOR,
        )

        button_acesar_en_login_selector = 'button[aria-label="Acessar"]'
        button_acesar_en_login = clicar_elemento(
            seletor=button_acesar_en_login_selector,
            tipo_elemento=CSS_SELECTOR,
        )
        if (not button_acesar_en_login):
            resultado['reason'] = (
                'Botón de acesar cuenta no localizado'
            )

            raise RuntimeError(resultado['reason'])

        resultado['data'] = button_acesar_en_login
        resultado['status'] = 'done'
        resultado['reason'] = ''
    except Exception as error:
        resultado['status'] = 'undone'
        resultado['reason'] = str(error)

    return resultado


def login_por_CPF(credenciales: dict[str, str]):
    resultado = {
        'status': '',
        'reason': '',
        'data': None
    }

    try:
        input_CPF_selector = 'input[id="idl-more-access-input-cpf"]'
        limpar_campo(
            seletor=input_CPF_selector,
            tipo_elemento=CSS_SELECTOR,
        )
        escrever_em_elemento(
            seletor=input_CPF_selector,
            texto=credenciales.get('CPF'),
            tipo_elemento=CSS_SELECTOR,
        )

        button_acesar_en_login_selector = 'button[aria-label="Acessar"]'
        button_acesar_en_login = clicar_elemento(
            seletor=button_acesar_en_login_selector,
            tipo_elemento=CSS_SELECTOR,
        )
        if (not button_acesar_en_login):
            resultado['reason'] = (
                'Elemento de butón acessar em '
                'pantalla de login no localizado.'
            )

            raise RuntimeError(resultado['reason'])

        resultado['data'] = button_acesar_en_login
        resultado['status'] = 'done'
        resultado['reason'] = ''
    except Exception as error:
        resultado['status'] = 'undone'
        resultado['reason'] = str(error)

    return resultado

