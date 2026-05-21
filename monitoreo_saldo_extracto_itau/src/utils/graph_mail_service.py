# graph_mail_service
from http.server import BaseHTTPRequestHandler


_TOKEN_SCOPE = (
    'openid '
    'offline_access '
    'https://graph.microsoft.com/Mail.Send '
    'https://graph.microsoft.com/User.Read'
)

_REDIRECT_URI = (
    'http://localhost:8080/callback'
)

# Para Outlook/Hotmail personal debe ser consumers
# Para O365 debe ser TENANT_ID del aplicativo
_TENANT_ID = 'consumers'

class OAuthCallbackHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        from urllib.parse import parse_qs, urlparse

        parsed_url = urlparse(self.path)
        query_params = parse_qs(parsed_url.query)

        self.server.authorization_code = (
            query_params.get('code', [None])[0]
        )

        # HTML de confirmación seguro, sin información sensible
        html_salida = '''
            <html>
                <body style="
                    background:#111;
                    color:#fff;
                    font-family:Segoe UI;
                    padding:40px;
                ">
                    <h1>Autenticación completada</h1>
                    <p>Puedes cerrar esta ventana.</p>
                </body>
            </html>
        '''

        self.send_response(200)
        self.send_header(
            'Content-Type',
            'text/html; charset=utf-8'
        )
        self.end_headers()

        self.wfile.write(
            html_salida.encode('utf-8')
        )

    def log_message(self, format, *args):
        pass


def guardar_variable_entorno(
    nombre: str,
    valor: str,
):
    resultado = {
        'status': '',
        'reason': '',
        'data': None
    }

    try:
        from subprocess import run

        comando = (
            '[System.Environment]'
            '::SetEnvironmentVariable('
            f'"{nombre}",'
            f'"{valor}",'
            '[System.EnvironmentVariableTarget]::User'
            ')'
        )

        run(
            [
                'powershell',
                '-Command',
                comando
            ]
        )

        resultado['status'] = 'done'
        resultado['reason'] = 'Función procesada'
    except Exception as error:
        resultado['status'] = 'undone'
        resultado['reason'] = str(error)

    return resultado


def obtener_variable_entorno_por_powershell(nombre: str,):
    resultado = {
        'status': '',
        'reason': '',
        'data': None
    }

    try:
        from subprocess import PIPE, run

        comando_get = (
            '[System.Environment]'
            '::GetEnvironmentVariable('
            f'"{nombre}",'
            '[System.EnvironmentVariableTarget]::User'
            ')'
        )

        valor = run(
            [
                'powershell',
                '-Command',
                comando_get,
            ],
            stdout=PIPE,
        )

        valor_str = valor.stdout.decode('utf8').strip()

        resultado['data'] = valor_str
        resultado['status'] = 'done'
        resultado['reason'] = 'Función procesada'
    except Exception as error:
        resultado['status'] = 'undone'
        resultado['reason'] = str(error)

    return resultado


def guardar_tokens(data: dict):
    resultado = {
        'status': '',
        'reason': '',
        'data': None
    }

    try:
        from time import time

        access_token = data['access_token']
        refresh_token = data['refresh_token']

        expires_at = (
            int(time()) +
            int(data['expires_in'])
        )

        guardar_variable_entorno(
            'SERVICIO_DE_CORREO_DE_PYTHON_ACCESS_TOKEN',
            access_token
        )
        guardar_variable_entorno(
            'SERVICIO_DE_CORREO_DE_PYTHON_REFRESH_TOKEN',
            refresh_token
        )
        guardar_variable_entorno(
            'SERVICIO_DE_CORREO_DE_PYTHON_EXPIRES_AT',
            str(expires_at)
        )

        resultado['status'] = 'done'
        resultado['reason'] = 'Función procesada'
    except Exception as error:
        resultado['status'] = 'undone'
        resultado['reason'] = str(error)

    return resultado


def obtener_access_token():
    resultado = {
        'status': '',
        'reason': '',
        'data': None
    }

    try:
        variable_entorno = (
            obtener_variable_entorno_por_powershell(
                'SERVICIO_DE_CORREO_DE_PYTHON_ACCESS_TOKEN'
            )
        )

        if variable_entorno['status'] == 'undone':
            raise RuntimeError(variable_entorno['reason'])

        resultado['data'] = variable_entorno['data']
        resultado['status'] = 'done'
        resultado['reason'] = 'Función procesada'
    except Exception as error:
        resultado['status'] = 'undone'
        resultado['reason'] = str(error)

    return resultado


def obtener_refresh_token():
    resultado = {
        'status': '',
        'reason': '',
        'data': None
    }

    try:
        variable_entorno = obtener_variable_entorno_por_powershell(
            'SERVICIO_DE_CORREO_DE_PYTHON_REFRESH_TOKEN'
        )

        if variable_entorno['status'] == 'undone':
            raise RuntimeError(variable_entorno['reason'])

        resultado['data'] = variable_entorno['data']
        resultado['status'] = 'done'
        resultado['reason'] = 'Función procesada'
    except Exception as error:
        resultado['status'] = 'undone'
        resultado['reason'] = str(error)

    return resultado


def obtener_expires_at():
    resultado = {
        'status': '',
        'reason': '',
        'data': None
    }

    try:
        variable_entorno = obtener_variable_entorno_por_powershell(
            'SERVICIO_DE_CORREO_DE_PYTHON_EXPIRES_AT'
        )

        if variable_entorno['status'] == 'undone':
            raise RuntimeError(variable_entorno['reason'])

        resultado['data'] = int(variable_entorno['data'])
        resultado['status'] = 'done'
        resultado['reason'] = 'Función procesada'
    except Exception as error:
        resultado['status'] = 'undone'
        resultado['reason'] = str(error)

    return resultado


def obtener_authorization_code(
    client_id: str = None,
):
    resultado = {
        'status': '',
        'reason': '',
        'data': None
    }

    try:
        from http.server import HTTPServer
        from urllib.parse import urlencode
        from webbrowser import open as open_browser

        # Construir URL de autenticación
        params = {
            'client_id': client_id,
            'response_type': 'code',
            'redirect_uri': _REDIRECT_URI,
            'response_mode': 'query',
            'scope': _TOKEN_SCOPE,
        }
        query = urlencode(params)
        auth_url = (
            'https://login.microsoftonline.com/'
            f'{_TENANT_ID}/oauth2/v2.0/authorize?{query}'
        )

        # Iniciar servidor local seguro
        server = HTTPServer(
            ('localhost', 8080),
            OAuthCallbackHandler
        )

        server.authorization_code = None

        # Abrir navegador sin exponer código en consola
        open_browser(auth_url)

        # Esperar a que el usuario complete el login
        server.handle_request()

        authorization_code = server.authorization_code

        if not authorization_code:
            raise RuntimeError(
                'Hubo falla al obtener el authorization code, '
                'revisa los datos en los entornos del sistema.'
            )

        # Retornar el código de autorización guardado en memoria
        resultado['data'] = authorization_code
        resultado['status'] = 'done'
        resultado['reason'] = 'Autenticación completada sin exponer información'
    except Exception as error:
        resultado['status'] = 'undone'
        resultado['reason'] = str(error)

    return resultado


def request_token(payload: dict, tenant_id: str):
    resultado = {
        'status': '',
        'reason': '',
        'data': None
    }

    try:
        from http.client import HTTPSConnection
        from json import loads
        from urllib.parse import urlencode

        conn = HTTPSConnection('login.microsoftonline.com')

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }

        conn.request(
            'POST',
            f'/{tenant_id}/oauth2/v2.0/token',
            urlencode(payload),
            headers
        )

        response = conn.getresponse()

        dato_response = loads(response.read().decode())

        resultado['data'] = dato_response
        resultado['status'] = 'done'
        resultado['reason'] = 'Función procesada'
    except Exception as error:
        resultado['status'] = 'undone'
        resultado['reason'] = str(error)

    return resultado


def login_interactivo(
    client_id: str = None,
    client_secret: str = None,
):
    resultado = {
        'status': '',
        'reason': '',
        'data': None
    }

    try:
        from json import dumps

        authorization_code = obtener_authorization_code(client_id=client_id)
        if authorization_code['status'] == 'undone':
            raise RuntimeError(authorization_code['reason'])

        payload = {
            'client_id': client_id,
            'scope': _TOKEN_SCOPE,
            'code': authorization_code['data'],
            'redirect_uri': _REDIRECT_URI,
            'grant_type': 'authorization_code',
            'client_secret': client_secret,
        }

        dato_token = request_token(payload=payload, tenant_id=_TENANT_ID)
        if dato_token['status'] == 'undone':
            raise RuntimeError(dato_token['reason'])

        if 'access_token' not in dato_token['data']:
            raise RuntimeError(dumps(dato_token['data'], indent=4))

        guardar_tokens(dato_token['data'])

        resultado['data'] = dato_token['data']['access_token']
        resultado['status'] = 'done'
        resultado['reason'] = 'Función procesada'
    except Exception as error:
        resultado['status'] = 'undone'
        resultado['reason'] = str(error)

    return resultado


def renovar_access_token(
    client_id: str = None,
    client_secret: str = None,
):
    resultado = {
        'status': '',
        'reason': '',
        'data': None
    }

    try:
        refresh_token = obtener_refresh_token()

        if refresh_token['status'] == 'undone':
            raise RuntimeError(refresh_token['reason'])

        payload = {
            'client_id': client_id,
            'client_secret': client_secret,
            'refresh_token': refresh_token['data'],
            'grant_type': 'refresh_token',
            'scope': _TOKEN_SCOPE,
        }

        dato_token = request_token(payload=payload, tenant_id=_TENANT_ID)
        if dato_token['status'] == 'undone':
            raise RuntimeError(dato_token['reason'])

        if 'access_token' not in dato_token['data']:
            resultado['reason'] = (
                'Refresh token expirado. Nuevo login requerido.'
            )

            raise RuntimeError(resultado['reason'])

        guardar_tokens(dato_token['data'])

        resultado['data'] = dato_token['data']['access_token']
        resultado['status'] = 'done'
        resultado['reason'] = 'Función procesada'
    except Exception as error:
        resultado['status'] = 'undone'
        resultado['reason'] = str(error)

    return resultado


def token_expirado():
    resultado = {
        'status': '',
        'reason': '',
        'data': None
    }

    try:
        from time import time

        expires_at = obtener_expires_at()
        if expires_at['status'] == 'undone':
            raise RuntimeError(expires_at['reason'])

        validacion_token = True
        if expires_at['data']:
            validacion_token = time() > (expires_at['data'] - 300)

        resultado['data'] = validacion_token
        resultado['status'] = 'done'
        resultado['reason'] = 'Función procesada'
    except Exception as error:
        resultado['status'] = 'undone'
        resultado['reason'] = str(error)

    return resultado


def get_valid_access_token(
    client_id: str = None,
    client_secret: str = None,
):
    resultado = {
        'status': '',
        'reason': '',
        'data': None
    }

    try:
        token_valido = ''

        access_token = obtener_access_token()
        if access_token['status'] == 'undone':
            raise RuntimeError(access_token['reason'])

        if not access_token['data']:
            resultado['reason'] = (
                'No hay token. Login requerido.'
            )

            raise RuntimeError(resultado['reason'])

        token_valido = access_token['data']

        resultado_token_expirado = token_expirado()
        if resultado_token_expirado['status'] == 'undone':
            raise RuntimeError(resultado_token_expirado['reason'])

        if resultado_token_expirado['data']:
            resultado_renovar_access_token = renovar_access_token(
                client_id = client_id,
                client_secret = client_secret,
            )
            if resultado_renovar_access_token['status'] == 'undone':
                raise RuntimeError(resultado_renovar_access_token['reason'])

            token_valido = resultado_renovar_access_token['data']

        resultado['data'] = token_valido
        resultado['status'] = 'done'
        resultado['reason'] = 'Función procesada'
    except Exception as error:
        resultado['status'] = 'undone'
        resultado['reason'] = str(error)

    return resultado


def codificar_archivo_base64(camino_archivo: str,):
    resultado = {
        'status': '',
        'reason': '',
        'data': None
    }

    try:
        from base64 import b64encode

        with open(camino_archivo, 'rb',) as archivo:
            contenido_archivo = b64encode(archivo.read()).decode('utf-8')

        resultado['data'] = contenido_archivo
        resultado['status'] = 'done'
        resultado['reason'] = 'Función procesada'
    except Exception as error:
        resultado['status'] = 'undone'
        resultado['reason'] = str(error)

    return resultado


def adjuntar_archivo_email(camino_archivo: str,):
    resultado = {
        'status': '',
        'reason': '',
        'data': None
    }

    try:
        nombre_archivo = camino_archivo.rpartition('\\')[-1]

        archivo_base64 = codificar_archivo_base64(camino_archivo)
        if archivo_base64['status'] == 'undone':
            raise RuntimeError(archivo_base64['reason'])

        dato_archivo_email = {
            '@odata.type': '#microsoft.graph.fileAttachment',
            'name': nombre_archivo,
            'contentBytes': archivo_base64['data'],
        }

        resultado['data'] = dato_archivo_email
        resultado['status'] = 'done'
        resultado['reason'] = 'Función procesada'
    except Exception as error:
        resultado['status'] = 'undone'
        resultado['reason'] = str(error)

    return resultado


def definir_destinatarios_email(lista_correos: tuple[str],):
    resultado = {
        'status': '',
        'reason': '',
        'data': None
    }

    try:
        dato_destinatarios_email = [
            {
                'emailAddress': {
                    'address': correo
                }
            }
            for correo in lista_correos
        ]

        resultado['data'] = dato_destinatarios_email
        resultado['status'] = 'done'
        resultado['reason'] = 'Función procesada'
    except Exception as error:
        resultado['status'] = 'undone'
        resultado['reason'] = str(error)

    return resultado


def definir_contenido_email(tipo_contenido: str, contenido: str,):
    resultado = {
        'status': '',
        'reason': '',
        'data': None
    }

    try:
        if tipo_contenido.upper() not in ['TEXT', 'HTML']:
            raise ValueError('Tipo no permitido.')

        dato_contenido_email = {
            'contentType': tipo_contenido.upper(),
            'content': contenido
        }

        resultado['data'] = dato_contenido_email
        resultado['status'] = 'done'
        resultado['reason'] = 'Función procesada'
    except Exception as error:
        resultado['status'] = 'undone'
        resultado['reason'] = str(error)

    return resultado


def send_mail(
    destinatarios: list,
    subject_email: str,
    body_email: dict,
    client_id: str,
    client_secret: str,
    attachments: list | None = None,
):
    resultado = {
        'status': '',
        'reason': '',
        'data': None
    }

    try:
        from http.client import HTTPSConnection
        from json import dumps


        access_token_valido = get_valid_access_token(
            client_id = client_id,
            client_secret = client_secret,
        )
        if access_token_valido['status'] == 'undone':
            if not (
                'LOGIN REQUERIDO' in
                str(access_token_valido['reason']).upper()
            ):
                raise RuntimeError(access_token_valido['reason'])

            resultado_login_interactivo = login_interactivo(
                client_id = client_id,
                client_secret = client_secret,
            )
            if resultado_login_interactivo['status'] == 'undone':
                raise RuntimeError(resultado_login_interactivo['reason'])

            access_token_valido = resultado_login_interactivo

        message = {
            'subject': subject_email,
            'body': body_email,
            'toRecipients': destinatarios,
        }

        if attachments:
            message['attachments'] = attachments

        payload = dumps(
            {'message': message}
        )

        headers = {
            'Authorization': f'Bearer {access_token_valido['data']}',
            'Content-Type': 'application/json',
        }

        conn = HTTPSConnection('graph.microsoft.com')

        conn.request(
            'POST',
            '/v1.0/me/sendMail',
            payload,
            headers
        )

        response = conn.getresponse()

        dato_response = {
            'status': response.status,
            'body': response.read().decode('utf8').strip()
        }

        resultado['data'] = dato_response
        resultado['status'] = 'done'
        resultado['reason'] = 'Función procesada'
    except Exception as error:
        resultado['status'] = 'undone'
        resultado['reason'] = str(error)

    return resultado
