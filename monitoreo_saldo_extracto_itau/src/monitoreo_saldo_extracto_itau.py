# Nome: ItauAutomacao
from py_rpautom.python_utils import cls

from os import getenv

from utils.pom import (
    acceder_elemento_menu_saldo_e_extrato,
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

        entrar_sitio_itau(False)

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
                resultado_acceder_elemento_menu_saldo_e_extrato = (
                    acceder_elemento_menu_saldo_e_extrato()
                )
                if (
                    resultado_acceder_elemento_menu_saldo_e_extrato[
                        'status'
                    ] == 'undone'
                ):
                    raise RuntimeError(
                        resultado_acceder_elemento_menu_saldo_e_extrato[
                            'reason'
                        ]
                    )

                esperar_loading(salir = True, tiempoLimite = 30)

                resultado_colectar_extrato = colectar_extrato()
                if resultado_colectar_extrato['status'] == 'undone':
                    raise RuntimeError(
                        resultado_colectar_extrato['reason']
                    )

                if not (
                    valor_extrato ==
                    resultado_colectar_extrato['data']
                ):
                    valor_extrato = resultado_colectar_extrato['data']

                    print('Enviar e-mail')
            except KeyboardInterrupt:
                print("Interrumpido por el usuario")
                break
            except Exception as error:
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
