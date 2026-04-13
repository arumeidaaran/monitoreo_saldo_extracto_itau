# Nome: ItauAutomacao
from py_rpautom.python_utils import cls

from os import getenv

from utils.pom import entrar_sitio_itau, resolver_login

def executar_fluxo():
    resultado = {
        'status': '',
        'reason': '',
        'data': None
    }

    try:
        opcion_login = 'AGENCY-ACCOUNT'
        credenciales = {
            'agencia': getenv('MONITOREO_SALDO_EXTRACTO_ITAU_AGENCIA_ITAU'),
            'cuenta': getenv('MONITOREO_SALDO_EXTRACTO_ITAU_CUENTA_ITAU'),
        }
        contraseñaTeclado = getenv(
            'MONITOREO_SALDO_EXTRACTO_ITAU_CONTRASENA_ITAU'
        )

        entrar_sitio_itau(False)

        resultado_resolver_login = resolver_login(
            valor_opcion=opcion_login,
            credenciales=credenciales,
        )
        if resultado_resolver_login['status'] == 'undone':
            raise RuntimeError(resultado_resolver_login['reason'])

        resultado['status'] = 'done'
        resultado['reason'] = 'Función procesada'
        resultado['data'] = {
            'credenciales': credenciales,
            'contraseñaTeclado': contraseñaTeclado,
        }
    except Exception as error:
        resultado['status'] = 'undone'
        resultado['reason'] = str(error)

    return resultado


def main():
    resultado = executar_fluxo()
    cls()
    print(resultado)


if __name__ == '__main__':
    main()
