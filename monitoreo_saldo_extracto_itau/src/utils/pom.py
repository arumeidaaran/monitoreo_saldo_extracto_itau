from time import sleep

from py_rpautom.python_utils import coletar_pid, finalizar_processo
from py_rpautom.web_utils import (
    aguardar_elemento,
    clicar_elemento,
    coletar_atributo,
    escrever_em_elemento,
    extrair_texto,
    iniciar_navegador,
    limpar_campo,
    maximizar_janela,
    selecionar_elemento,
)

from utils.utils import validar_webdriver


XPATH = 'xpath'
CSS_SELECTOR = 'css_selector'

_list_opcion_login = ['CPF', 'AGENCY-ACCOUNT']


def acceder_elemento_menu_saldo_e_extrato():
    resultado = {
        'status': '',
        'reason': '',
        'data': None
    }

    try:
        esperar_loading(salir = True, tiempoLimite = 30)

        resultado_validar_menu_principal = validar_menu_principal()
        if resultado_validar_menu_principal['status'] == 'undone':
            resultado['reason'] = (
                'No apareció el menu principal.'
            )

            raise SystemError(resultado['reason'])

        resultado_acceder_menu_principal = acceder_menu_principal()
        if resultado_acceder_menu_principal['status'] == 'undone':
            resultado['reason'] = (
                'No fue posible hacer clic en el menu principal.'
            )

            raise SystemError(resultado['reason'])

        link_saldo_e_extrato_selector = (
            '(//li[@class="titulo "])[1]/following-sibling::li/'
            'a[contains(text(), "saldo e extrato")]'
        )
        link_saldo_e_extrato = aguardar_elemento(
            identificador=link_saldo_e_extrato_selector,
            tipo_elemento=XPATH,
            tempo=10,
        )
        if not link_saldo_e_extrato:
            resultado['reason'] = (
                'No apareció el elemento de menu Saldo e Extrato'
            )

            raise SystemError(resultado['reason'])

        clicar_elemento(
            seletor=link_saldo_e_extrato_selector,
            tipo_elemento=XPATH,
        )

        resultado['data'] = True
        resultado['status'] = 'done'
        resultado['reason'] = 'Función procesada'
    except Exception as error:
        resultado['status'] = 'undone'
        resultado['reason'] = str(error)

    return resultado


def acceder_menu_principal():
    resultado = {
        'status': '',
        'reason': '',
        'data': None
    }

    try:
        nav_menu_principal_selector = (
            '(//nav[@class="menu left"]//a)[1]/span'
        )

        resultado_nav_menu_principal = clicar_elemento(
            seletor=nav_menu_principal_selector,
            tipo_elemento=XPATH,
        )
        if not resultado_nav_menu_principal:
            resultado['reason'] = (
                'Error al intentar acceder el menu principal'
            )

            raise SystemError(resultado['reason'])

        resultado['status'] = 'done'
        resultado['reason'] = 'Función procesada'
    except Exception as error:
        resultado['status'] = 'undone'
        resultado['reason'] = str(error)

    return resultado


def aprobar_cookies() :
    result = {
        'status': '',
        'reason': '',
        'data': None,
    }

    try:
        elemento_raiz_selector = (
            'itau-cookie-consent-banner[segment="varejo"]'
        )
        elemento_escondido_selector = (
            'button[id="itau-cookie-consent-banner-accept-cookies-btn"]'
        )

        aceptar_cookies_button = aguardar_elemento(
            identificador=elemento_escondido_selector,
            tipo_elemento=CSS_SELECTOR,
            elemento_shadowroot=elemento_raiz_selector,
            tipo_elemento_shadowroot=CSS_SELECTOR,
            tempo=1,
        )

        if not aceptar_cookies_button:
            raise RuntimeError(
                'No se pudo encontrar el botón de aprobación de cookies.'
            )

        clicar_elemento(
            seletor=elemento_escondido_selector,
            tipo_elemento=CSS_SELECTOR,
            elemento_shadowroot=elemento_raiz_selector,
            tipo_elemento_shadowroot=CSS_SELECTOR,
        )

        result['status'] = 'done'
        result['reason'] = 'função processada'
    except Exception as error:
        result['status'] = 'undone'
        result['reason'] = str(error)
    
    return result


def validar_menu_principal():
    resultado = {
        'status': '',
        'reason': '',
        'data': None
    }

    try:
        nav_menu_principal_selector = (
            '(//nav[@class="menu left"]//a)[1]/span'
        )

        nav_menu_principal = aguardar_elemento(
            identificador=nav_menu_principal_selector,
            tipo_elemento=XPATH,
        )
        if not nav_menu_principal:
            resultado['reason'] = "No apareció el menu principal"

            raise SystemError(resultado['reason'])

        resultado['status'] = 'done'
        resultado['reason'] = 'Función procesada'
    except Exception as error:
        resultado['status'] = 'undone'
        resultado['reason'] = str(error)

    return resultado


def acceder_pagina_login():
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


def colectar_campo_valor_extrato():
    resultado = {
        'status': '',
        'reason': '',
        'data': None
    }

    try:
        paragrafo_valor_saldo_selector = 'p[id="saldo"]'
        paragrafo_valor_saldo = aguardar_elemento(
            identificador=paragrafo_valor_saldo_selector,
            tipo_elemento=CSS_SELECTOR,
        )        
        if paragrafo_valor_saldo == '':
            resultado['reason'] = (
                'No apareció el valor de dinero de la cuenta '
                'en la pantalla principal'
            )

            raise SystemError(resultado['reason'])

        paragrafo_valor_saldo_texto = extrair_texto(
            seletor=paragrafo_valor_saldo_selector,
            tipo_elemento=CSS_SELECTOR,
        )

        resultado['data'] = (
            paragrafo_valor_saldo_texto.replace('R$', '').strip()
        )
        resultado['status'] = 'done'
        resultado['reason'] = 'Función procesado'
    except Exception as error:
        resultado['status'] = 'undone'
        resultado['reason'] = str(error)

    return resultado


def elegir_opcion_seleccion(valor_opcion):
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


def entrar_sitio_itau(pantalla_intera: bool):
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
        )

        if pantalla_intera:
            maximizar_janela()

        if resultado_iniciar_navegador == False:
            resultado['reason'] = 'Error al ejecutar iniciar_navegador'
            raise RuntimeError(resultado['reason'])

        resultado['data'] = resultado_iniciar_navegador
        resultado['status'] = 'done'
        resultado['reason'] = 'Función procesada'
    except Exception as error:
        resultado['status'] = 'undone'

        if resultado['reason'] == '':
            resultado['reason'] = str(error)

    return resultado


def esperar_loading(salir = True, tiempoLimite = 60):
    resultado = {
        'status': '',
        'reason': '',
        'data': None
    }

    try:
        elemento_carregando_selector = '//*[@*="Carregando" or @*="carregando"]'
        contaje = 0
        validar_elemento_carregando = salir
        while (
            (validar_elemento_carregando == salir) and
            (contaje < tiempoLimite)
        ):
            validar_elemento_carregando = aguardar_elemento(
                identificador=elemento_carregando_selector,
                tempo=1,
                tipo_elemento=XPATH,
            )

            contaje = contaje + 1

        if (contaje == tiempoLimite):
            resultado['reason'] = 'Se acabó el tiempo esperando loading'

            raise SystemError(resultado['reason'])

        resultado['status'] = 'done'
        resultado['reason'] = 'Función procesada'
    except Exception as error:
        resultado['status'] = 'undone'
        resultado['reason'] = str(error)

    return resultado


def habilitar_campo_valor_extrato():
    resultado = {
        'status': '',
        'reason': '',
        'data': None
    }
    try:
        button_extrato_da_conta_selector = (
            'button[id="saldo-extrato-card-accordion"]'
        )

        button_extrato_da_conta_ = aguardar_elemento(
            identificador=button_extrato_da_conta_selector,
            tipo_elemento=CSS_SELECTOR,
        )
        if not button_extrato_da_conta_:
            resultado['reason'] = (
                'No apareció el campo de dinero de la cuenta'
            )

            raise SystemError(resultado['reason'])

        clicar_elemento(
            seletor=button_extrato_da_conta_selector,
            tipo_elemento=CSS_SELECTOR,
        )

        esperar_loading(salir = True, tiempoLimite = 30)

        paragrafo_valor_saldo_selector = 'p[id="saldo"]'
        paragrafo_valor_saldo = aguardar_elemento(
            identificador=paragrafo_valor_saldo_selector,
            tipo_elemento=CSS_SELECTOR,
        )
        if not paragrafo_valor_saldo:
            resultado['reason'] = (
                'No apareció el valor de dinero de la cuenta '
                'en la pantalla principal'
            )

            raise SystemError(resultado['reason'])

        resultado['status'] = 'done'
        resultado['reason'] = 'Función procesada'
    except Exception as error:
        resultado['status'] = 'undone'
        resultado['reason'] = str(error)
    return resultado


def hacer_login(valor_opcion: str, credenciales: dict[str, str]):
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
                if not credenciales.get('agencia'):
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

        button_acesar_en_login_selector = (
            '//button[contains(@class, "idl-more-access-submit-button")]'
        )
        button_acesar_en_login = clicar_elemento(
            seletor=button_acesar_en_login_selector,
            tipo_elemento=XPATH,
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


def resolver_login(valor_opcion: str, credenciales: dict[str, str]):
    resultado = {
        'status': '',
        'reason': '',
        'data': None
    }

    try:
        acceder_pagina_login()
        elegir_opcion_seleccion(valor_opcion)

        resultado_hacerLogin = hacer_login(valor_opcion, credenciales)
        if resultado_hacerLogin['status'] == 'undone':
            raise RuntimeError(resultado_hacerLogin['reason'])

        resultado['status'] = 'done'
        resultado['reason'] = 'Función procesada'
    except Exception as error:
        resultado['status'] = 'undone'
        resultado['reason'] = str(error)

    return resultado


def resolver_token(tiempo_limite = 180):
    resultado = {
        'status': '',
        'reason': '',
        'data': None
    }

    try:
        div_pantalla_iToken_app_selector = 'div[class="itoken-info"]'
        pantalla_iToken_app = aguardar_elemento(
            identificador=div_pantalla_iToken_app_selector,
            tipo_elemento=CSS_SELECTOR,
        )

        if not pantalla_iToken_app:
            resultado['reason'] = (
                'No apareció la opción de validar '
                'el iToken de Itaú'
            )

            raise SystemError(resultado['reason'])

        validacion_token = False
        contaje = 0
        valor_iToken = ''
        while (validacion_token == False and contaje < tiempo_limite):
            valor_iToken = input('Digite tu iToken en el sítio Itaú: ')

            if (
                (not valor_iToken == '') and
                (len(valor_iToken) == 6)
            ):
                validacion_token = True

            contaje = contaje + 1
            sleep(1)

        lista_valor_iToken = list(valor_iToken)
        for indice_iToken in range(1, 7):
            input_password_iToken = (
                '(//input[@type="password"]'
                f'[@maxlength="1"])[{indice_iToken}]'
            )

            escrever_em_elemento(
                seletor=input_password_iToken,
                texto=lista_valor_iToken.pop(0),
                tipo_elemento=XPATH,
            )

        link_continuar_iToken_selector = '//a[@id="app-codigoOk"]'

        validacion_link_continuar_iToken = coletar_atributo(
            seletor=link_continuar_iToken_selector,
            atributo='disabled',
            tipo_elemento=XPATH,
        )
        if validacion_link_continuar_iToken:
            resultado['reason'] = (
                'No se pude identificar el '
                f'butón continuar activo después del iToken completado.'
            )

            raise SystemError(resultado['reason'])

        link_continuar_iToken = clicar_elemento(
            seletor=link_continuar_iToken_selector,
            tipo_elemento=XPATH,
        )
        if (not link_continuar_iToken):
            resultado['reason'] = (
                'Erorr al hacer clik en link_continuar_iToken'
            )

            raise SystemError(resultado['reason'])

        resultado['status'] = 'done'
        resultado['reason'] = 'función procesada'
    except Exception as error:
        resultado['status'] = 'undone'
        resultado['reason'] = str(error)

    return resultado


def resolver_contraseña(contraseña):
    resultado = {
        'status': '',
        'reason': '',
        'data': None
    }

    try:
        input_pantalla_contraseña_teclado_selector = (
            'input[aria-label="senha de acesso"]'
        )
        pantalla_contraseña_teclado = aguardar_elemento(
            identificador=input_pantalla_contraseña_teclado_selector,
            tipo_elemento=CSS_SELECTOR,
        )

        if not pantalla_contraseña_teclado:
            resultado['reason'] = (
                "No apareció la opción de validar la contraseña de Itaú"
            )

            raise SystemError(resultado['reason'])

        for numero in range(0, len(contraseña)):
            link_teclas_teclado_virtual_selector = (
                '//div[@class="teclas clearfix"]/'
                f'a[contains(text(), "{contraseña[numero]}")]'
            )

            clicar_elemento(
                seletor=link_teclas_teclado_virtual_selector,
                tipo_elemento=XPATH,
            )

            sleep(1)

        validacion_pantalla_contraseña_teclado = coletar_atributo(
            seletor=input_pantalla_contraseña_teclado_selector,
            atributo='value',
            tipo_elemento=CSS_SELECTOR,
        )
        if (
            (
                validacion_pantalla_contraseña_teclado.upper() ==
                'SENHA DE ACESSO'
            )
            or (not len(
                validacion_pantalla_contraseña_teclado
            ) == len(contraseña))
        ):
            resultado['reason'] = 'Ocurrió un error al digitar la contraseña.'

            raise SystemError(resultado['reason'])

        acesar_en_teclado_virtual_boton_selector = 'a[aria-label="acessar"]'
        acesar_en_teclado_virtual_boton = clicar_elemento(
            seletor=acesar_en_teclado_virtual_boton_selector,
            tipo_elemento=CSS_SELECTOR,
        )
        if not acesar_en_teclado_virtual_boton:
            resultado['reason'] = (
                'Ocurrió un error al hacer clic en '
                'acesar_en_teclado_virtual_boton'
            )

            raise SystemError(resultado['reason'])

        resultado['status'] = 'done'
        resultado['reason'] = 'Función procesado'
    except Exception as error:
        resultado['status'] = 'undone'
        resultado['reason'] = str(error)

    return resultado


def validar_campo_valor_extrato_existe(tiempo_limite: int = 5):
    resultado = {
        'status': '',
        'reason': '',
        'data': None
    }

    try:
        paragrafo_valor_saldo_selector = 'p[id="saldo"]'
        paragrafo_valor_saldo = aguardar_elemento(
            identificador=paragrafo_valor_saldo_selector,
            tipo_elemento=CSS_SELECTOR,
            tempo=tiempo_limite,
        )

        resultado['data'] = False
        if paragrafo_valor_saldo:
            resultado['data'] = True

        resultado['status'] = 'done'
        resultado['reason'] = 'Función procesada'
    except Exception as error:
        resultado['status'] = 'undone'
        resultado['reason'] = str(error)

    return resultado


def colectar_extrato():
    resultado = {
        'status': '',
        'reason': '',
        'data': None
    }

    try:
        div_valor_saldo_selector = 'div[id="cor-valor-saldo-box"]'
        div_valor_saldo = aguardar_elemento(
            identificador=div_valor_saldo_selector,
            tipo_elemento=CSS_SELECTOR,
        )
        if not div_valor_saldo:
            resultado['reason'] = (
                "No apareció el valor de dinero de la " +
                "cuenta en la pantalla Saldo e Extrato"
            )

            raise SystemError(resultado['reason'])

        resultado_div_valor_saldo = extrair_texto(
            seletor=div_valor_saldo_selector,
            tipo_elemento=CSS_SELECTOR,
        )

        resultado['data'] = (
            resultado_div_valor_saldo.replace('R$', '').strip()
        )
        resultado['status'] = 'done'
        resultado['reason'] = 'Função procesada'
    except Exception as error:
        resultado['status'] = 'undone'
        resultado['reason'] = str(error)

    return resultado
