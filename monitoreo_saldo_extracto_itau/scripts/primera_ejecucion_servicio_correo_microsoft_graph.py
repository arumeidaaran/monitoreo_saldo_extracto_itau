# first_execution_graph_mail_service
'''# Antes de ejecutar este script, ejecute los siguientes comandos en PowerShell:

## Para grabar las variables de entorno:  

```PowerShell
$variable = 'SERVICIO_DE_CORREO_DE_PYTHON_CLIENT_ID'
# complete el valor con tu dato de la app, $null para eliminarlo
$valor = $null

[System.Environment]::SetEnvironmentVariable($variable, $valor, [System.EnvironmentVariableTarget]::User)
[System.Environment]::SetEnvironmentVariable($variable, $valor, [System.EnvironmentVariableTarget]::Process)

$variable = 'SERVICIO_DE_CORREO_DE_PYTHON_CLIENT_SECRET'
# complete el valor con tu dato de la app, $null para eliminarlo
$valor = $null

[System.Environment]::SetEnvironmentVariable($variable, $valor, [System.EnvironmentVariableTarget]::User)
[System.Environment]::SetEnvironmentVariable($variable, $valor, [System.EnvironmentVariableTarget]::Process)
```

## Para probarlos:  

```PowerShell
$env:SERVICIO_DE_CORREO_DE_PYTHON_CLIENT_ID
$env:SERVICIO_DE_CORREO_DE_PYTHON_CLIENT_SECRET
```

'''

from pathlib import Path
from sys import path

path.append(str(Path('.').parent.absolute()))

from monitoreo_saldo_extracto_itau.src.utils.graph_mail_service import (
    adjuntar_archivo_email,
    definir_contenido_email,
    definir_destinatarios_email,
    obtener_variable_entorno_por_powershell,
    send_mail,
)

resultado_client_id = obtener_variable_entorno_por_powershell(
    nombre = 'SERVICIO_DE_CORREO_DE_PYTHON_CLIENT_ID',
)

if resultado_client_id['status'] == 'undone':
    raise RuntimeError(resultado_client_id['reason'])

if not resultado_client_id['data']:
    raise RuntimeError(
        'client_id vacío, revise las variables de entorno.'
    )

CLIENT_ID = resultado_client_id['data']

resultado_client_secret = obtener_variable_entorno_por_powershell(
    nombre = 'SERVICIO_DE_CORREO_DE_PYTHON_CLIENT_SECRET'
)

if resultado_client_secret['status'] == 'undone':
    raise RuntimeError(resultado_client_secret['reason'])

if not resultado_client_secret['data']:
    raise RuntimeError(
        'client_secret vacío, revise las variables de entorno.'
    )

CLIENT_SECRET = resultado_client_secret['data']

lista_correos = (
    'arumeidaaran@outlook.com',
    't1801lln@hotmail.com',
)

destinatarios = definir_destinatarios_email(lista_correos)
if destinatarios['status'] == 'undone':
    raise RuntimeError(destinatarios['reason'])

contenido_email_html = '''
    <h1>Hola</h1>

    <p>
    Correo automatico usando
    Microsoft Graph API.
    </p>
'''

body_email = definir_contenido_email('HTML', contenido_email_html,)
if body_email['status'] == 'undone':
    raise RuntimeError(body_email['reason'])


camino_archivo_email = (
    r'.\monitoreo_saldo_extracto_itau\scripts\archivo-de-prueba.txt'
)
camino_archivo_email_str = str(Path(camino_archivo_email).absolute())
archivo_email = adjuntar_archivo_email(camino_archivo_email_str)
if archivo_email['status'] == 'undone':
    raise RuntimeError(archivo_email['reason'])

attachments = [archivo_email['data'],]

resultado_send_mail = send_mail(
    destinatarios=destinatarios['data'],
    subject_email='Correo automático',
    body_email=body_email['data'],
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    attachments=attachments,
)
if resultado_send_mail['status'] == 'undone':
    raise RuntimeError(resultado_send_mail['reason'])

print('\n', resultado_send_mail['data']['status'])
print(resultado_send_mail['data']['body'], '\n')
