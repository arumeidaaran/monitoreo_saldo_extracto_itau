# DOCUMENTACIÓN PARA SUBIR LA APLICACIÓN DE E-MAIL PYTHON

## PASO A PASO

Este es una documentación que explica como implementar el flujo OAuth2 en envio de e-mail usando Microsoft Graph.

### EL DISEÑO

```text
Authorization Code Flow + Refresh Token
```

Eso te permite:

* login una sola vez,
* guardar `refresh_token`,
* renovar `access_token` automáticamente,
* nunca copiar token manualmente.

---

### ARQUITECTURA REAL

El flujo se queda así:

```text
Usuario => 
Login Microsoft => 
Authorization Code => 
Access Token + Refresh Token => 
Guardar Refresh Token => 
Cuando access_token expira: => 
usar refresh_token => 
obtener nuevo access_token automáticamente
```

---

### CREAR LA APP EN AZURE/ENTRA

En:
[Microsoft Entra Admin Center](https://entra.microsoft.com/):

Autentica el sítio con tus credenciales de adminimistrador de la app.

Después ve a:

```text
=> Registros de aplicaciones
=> Nuevo registro
```

---

#### CONFIGURACIÓN DE LA APP

Nombre:

```text
Python Mail Service # Quitar este
Servicio de correo de Python
```

Tipos:

```text
Accounts in any organizational directory and personal Microsoft accounts
```

Redirect URI:

La plataforma:
```text
Web
```

Con el valor:
```text
http://localhost:8080/callback
```

---

Todavía en "Registros de aplicaciones", ve a tu app creada. En "Información general" necesitas guardar:

* Id. de aplicación (cliente)
* Id. de directorio (inquilino)

---

### CREAR CLIENT SECRET

Dentro de la aplicación ve a:

```text
=> Certificados y secretos
=> Nuevo secreto de cliente
```

Rellene los campos:
```text
Descripción:
    Escriba una descripción para este secreto de cliente.

Expira:
    Elige un tiempo en el que este secreto expirará.
```

Haz clic en Guardar.

Guarda el valor.

Es extremadamente importante que guarde estas informaciones creadas, principalmente el "valor". Esto no va aparecer otra vez. 
No comparta esto con nadie. 

---

### PERMISOS DE LA APP

Todavía dentro de la app, ve en:

```text
=> Permisos de API
=> Agregar un permiso
```

Elije "Permisos delegados".

Agrega de "Microsoft Graph":

```text
Mail.Send
offline_access
User.Read
```

Después haz clic en:

```text
Conceder consentimiento de administrador para Diretório Padrão
```

Y lo confirma.

---

## GRAVAR EN LOS ENTORNOS DEL SISTEMA

Ahora guardas en los entornos del sistema:

```text
SERVICIO_DE_CORREO_DE_PYTHON_CLIENT_ID = 'VALOR OBTENIDO DE MICROSOFT ENTRA'
SERVICIO_DE_CORREO_DE_PYTHON_CLIENT_SECRET = 'VALOR OBTENIDO DE MICROSOFT ENTRA'
```

## PROBAR LA APLICACIÓN

Ejecutar la aplicación y entra en tu cuenta Microsoft desde la ventana de navegador que va abrir.
Si he entrado y aparecer la información 202 en la consola, sí funcionó. Y sí no, valida cada paso de nuevo.

Al fin y al cabo, la aplicación hace:

1. Obtene acceso con la ayuda del usuario
2. Obtene Authorization Code
3. Obtene access token traz Authorization Code 
4. Renovar token automáticamente con refresh token cuando es necesario


### Importantísimo

Nunca guardes fijos en archivos ni compartes con otros 'client_secret', 'authorization_code', 'access_token' y 'refresh_token'. Usa variables de entorno porque eso equivale a acceso persistente a la cuenta.

