# Nome: monitoreo_saldo_extracto_itau
from py_rpautom.python_utils import cls
from os import getenv
import re

from utils.graph_mail_service import (
    definir_contenido_email,
    definir_destinatarios_email,
    obtener_variable_entorno_por_powershell,
    send_mail,
)
from utils.pom import (
    acceder_elemento_menu_saldo_e_extrato,
    aprobar_cookies,
    colectar_campo_valor_extrato,
    colectar_extrato,
    entrar_sitio_itau,
    esperar_loading,
    resolver_contraseña,
    resolver_login,
    resolver_token,
    validar_campo_valor_extrato_existe,
    habilitar_campo_valor_extrato,
)


def ejecutar_flujo():
    resultado = {
        'status': '',
        'reason': '',
        'data': None
    }

    try:
        valor_extrato = '0,00'

        opcion_login = 'AGENCY-ACCOUNT'
        credenciales = {
            'agencia': getenv('MONITOREO_SALDO_EXTRACTO_ITAU_AGENCIA_ITAU'),
            'cuenta': getenv('MONITOREO_SALDO_EXTRACTO_ITAU_CUENTA_ITAU'),
        }
        contraseñaTeclado = getenv(
            'MONITOREO_SALDO_EXTRACTO_ITAU_CONTRASENA_ITAU'
        )

        if not credenciales['agencia']:
            resultado['reason'] = (
                'Agencia no definida correctamente en '
                'los entornos del sistema'
            )

            raise SystemError(resultado['reason'])

        if not credenciales['cuenta']:
            resultado['reason'] = (
                'Cuenta no definida correctamente en '
                'los entornos del sistema'
            )

            raise SystemError(resultado['reason'])

        if not contraseñaTeclado:
            resultado['reason'] = (
                'Contraseña del teclado virtual no definida correctamente '
                'en los entornos del sistema'
            )

            raise SystemError(resultado['reason'])

        
        resultado_client_id = obtener_variable_entorno_por_powershell(
            nombre = 'SERVICIO_DE_CORREO_DE_PYTHON_CLIENT_ID',
        )

        if resultado_client_id['status'] == 'undone':
            raise RuntimeError(resultado_client_id['reason'])

        if not resultado_client_id['data']:
            raise RuntimeError(
                'client_id vacío, revise las variables de entorno.'
            )

        client_id = resultado_client_id['data']

        resultado_client_secret = obtener_variable_entorno_por_powershell(
            nombre = 'SERVICIO_DE_CORREO_DE_PYTHON_CLIENT_SECRET'
        )

        if resultado_client_secret['status'] == 'undone':
            raise RuntimeError(resultado_client_secret['reason'])

        if not resultado_client_secret['data']:
            raise RuntimeError(
                'client_secret vacío, revise las variables de entorno.'
            )

        client_secret = resultado_client_secret['data']

        lista_correos = (
            'arumeidaaran@outlook.com',
            't1801lln@hotmail.com',
        )

        destinatarios = definir_destinatarios_email(lista_correos)
        if destinatarios['status'] == 'undone':
            raise RuntimeError(destinatarios['reason'])

        contenido_email_html_original = '''
            <h1>Hubo modificación en tu cuenta</h1>

            <p>
            texto_contenido_email
            </p>
        '''

        titulo_email = 'Correo automático'

        entrar_sitio_itau(pantalla_intera=True)

        resultado_aprobar_cookies = aprobar_cookies()
        if resultado_aprobar_cookies['status'] == 'undone':
            raise RuntimeError(resultado_aprobar_cookies['reason'])

        resultado_resolver_login = resolver_login(
            valor_opcion=opcion_login,
            credenciales=credenciales,
        )
        if resultado_resolver_login['status'] == 'undone':
            raise RuntimeError(resultado_resolver_login['reason'])

        resultado_resolver_token = resolver_token()
        if resultado_resolver_token['status'] == 'undone':
            raise RuntimeError(resultado_resolver_token['reason'])

        resultado_resolver_contraseña = resolver_contraseña(contraseñaTeclado)
        if resultado_resolver_contraseña['status'] == 'undone':
            raise RuntimeError(resultado_resolver_contraseña['reason'])

        validacao_campo_valor_extrato_existe = (
            validar_campo_valor_extrato_existe()
        )
        if validacao_campo_valor_extrato_existe['status'] == 'undone':
            raise RuntimeError(
                validacao_campo_valor_extrato_existe['reason']
            )

        if validacao_campo_valor_extrato_existe['data'] is False:
            resultado_habilitar_campo_valor_extrato = (
                habilitar_campo_valor_extrato()
            )
            if resultado_habilitar_campo_valor_extrato['status'] == 'undone':
                raise RuntimeError(
                    resultado_habilitar_campo_valor_extrato['reason']
                )

        resultado_colectar_campo_valor_extrato = (
            colectar_campo_valor_extrato()
        )
        if resultado_colectar_campo_valor_extrato['status'] == 'undone':
            raise RuntimeError(
                resultado_colectar_campo_valor_extrato['reason']
            )

        valor_extrato = resultado_colectar_campo_valor_extrato['data']

        while True:
            try:
                validacion_menu_saldo_e_extrato = False
                contaje = 0
                contaje_total = 10
                while (
                    (validacion_menu_saldo_e_extrato is False)
                    and (contaje < contaje_total)
                ):
                    resultado_acceder_elemento_menu_saldo_e_extrato = (
                        acceder_elemento_menu_saldo_e_extrato()
                    )
                    if resultado_acceder_elemento_menu_saldo_e_extrato[
                        'data'
                    ]:
                        validacion_menu_saldo_e_extrato = True

                    contaje = contaje + 1

                if not validacion_menu_saldo_e_extrato:
                    resultado['reason'] = (
                        'No apareció el elemento de menu Saldo e Extrato'
                    )

                    raise SystemError(resultado['reason'])

                if resultado_acceder_elemento_menu_saldo_e_extrato[
                    'status'
                ] == 'undone':
                    raise RuntimeError(
                        resultado_acceder_elemento_menu_saldo_e_extrato[
                            'reason'
                        ]
                    )

                esperar_loading(salir = True, tiempoLimite = 30)

                resultado_colectar_extrato = colectar_extrato()
                if resultado_colectar_extrato['status'] == 'undone':
                    resultado_esperar_loading = esperar_loading(
                        salir = True,
                        tiempoLimite = 30,
                    )
                    if resultado_esperar_loading['status'] == 'undone':
                        raise RuntimeError(
                            resultado_colectar_extrato['reason']
                        )

                    resultado_colectar_extrato = colectar_extrato()
                    if resultado_colectar_extrato['status'] == 'undone':
                        raise RuntimeError(
                            resultado_colectar_extrato['reason']
                        )

                if not (
                    valor_extrato ==
                    resultado_colectar_extrato['data']
                ):
                    texto_contenido_email = f'''
                    <b>Saldo anterior:</b>
                        {valor_extrato}
                    <br/>
                    <b>Saldo nuevo:</b>
                        {resultado_colectar_extrato['data']}
                    '''

                    valor_extrato = resultado_colectar_extrato['data']

                    contenido_email_html = (
                        contenido_email_html_original.replace(
                            'texto_contenido_email',
                            texto_contenido_email,
                        )
                    )
                    contenido_limpio = re.sub(
                        r'\s+', ' ',
                        contenido_email_html
                    ).strip()

                    body_email = definir_contenido_email(
                        'HTML',
                        contenido_limpio,
                    )
                    if body_email['status'] == 'undone':
                        raise RuntimeError(body_email['reason'])

                    resultado_send_mail = send_mail(
                        destinatarios=destinatarios['data'],
                        subject_email=titulo_email,
                        body_email=body_email['data'],
                        client_id=client_id,
                        client_secret=client_secret,
                        attachments=None,
                    )
                    if resultado_send_mail['status'] == 'undone':
                        raise RuntimeError(resultado_send_mail['reason'])
            except KeyboardInterrupt:
                print("Interrumpido por el usuario")
                break
            except Exception as error:
                print(error)
                breakpoint()
                raise error

        resultado['status'] = 'done'
        resultado['reason'] = 'Función procesada'
    except Exception as error:
        resultado['status'] = 'undone'
        resultado['reason'] = str(error)

    return resultado


def main():
    resultado = ejecutar_flujo()
    cls()
    print(resultado)


if __name__ == '__main__':
    main()
