# Brain AI

Agente de Inteligencia artificial para manejar flujos de conversaciones utilizando diferentes herramientas a su disposición

Este proyecto implementa una API con FastAPI y SQLAlchemy, utilizando Alembic para gestionar las migraciones de la base de datos. La API permite crear usuarios, conversaciones y mensajes, y recuperar información sobre estas entidades.

## Instalación

1. Clona el repositorio:
    ```sh
    git clone https://github.com/intelnexoec/VoiceFlow-AI.git
    ```

2. Crea un entorno virtual e instala las dependencias:
    ```sh
    python -m venv env
    source env/bin/activate  # En Windows usa `env\Scripts\activate`
    pip install -r requirements.txt
    ```

3. Configura las variables de entorno en un archivo `.env`, puedes verificar cuales son en `example.env`:
    ```ini
    OPENAI_API_KEY=
    OPENAI_MODEL=
    LANGCHAIN_TRACING_V2=
    LANGCHAIN_API_KEY=
    ```
5. Iniciar los contenedores de docker
    ```sh
    docker compose up --build
    ```
6. Inicializa la base de datos y aplica las migraciones:
    ```sh
    alembic upgrade head
    ```


## Estructura del Proyecto

- `app/models`: Modelos de SQLAlchemy para las tablas de la base de datos.
- `app/schemas`: Esquemas Pydantic para la validación y serialización de datos.
- `app/repository`: Repositorios para acceder a los datos de la base de datos.
- `app/services`: Lógica de negocio y servicios para manejar las operaciones.
- `app/routes`: Rutas de FastAPI que definen los endpoints de la API.
- `alembic`: Configuración y migraciones de Alembic.
- `agents`: Configración y lógica de agentes con inteligencia articial
- `cache`: Maneja el cache de historial de mensajes

## Endpoints de la API
Puedes revisar una documentación más detallada en `localhost:8001/docs`
### Usuarios

- **Crear Usuario**
    - **Endpoint:** `/user/`
    - **Método:** `POST`
    - **Descripción:** Crea un nuevo usuario.
    - **Body:**
        ```json
        {
            "user_id": "string"
        }
        ```

### Conversaciones

- **Crear Conversación**
    - **Endpoint:** `/conversation/`
    - **Método:** `POST`
    - **Descripción:** Crea una nueva conversación para un usuario.
    - **Body:**
        ```json
        {
            "user_id": "string"
        }
        ```

- **Obtener Conversación por ID**
    - **Endpoint:** `/conversation/{conversation_id}`
    - **Método:** `GET`
    - **Descripción:** Recupera una conversación por su ID.
    - **Response:**
        ```json
        {
            "id": "integer",
            "user_id": "string",
            "messages": [
                {
                    "id": "integer",
                    "conversation_id": "integer",
                    "role": "string",
                    "content": "string"
                }
            ]
        }
        ```

### Mensajes

- **Enviar Mensaje**
    - **Endpoint:** `/message/`
    - **Método:** `POST`
    - **Descripción:** Envía un nuevo mensaje en una conversación.
    - **Body:**
        ```json
        {
            "message": "string"
        }
        ```
    - **Query Parameters:**
        - `session_id`: ID de la sesión
        - `conversation_id`: ID de la conversación

    - **Response:**
        ```json
        {
            "input": "string",
            "chat_history": [
                {
                    "content": "string"
                },
                {
                    "content": "string"
                }
            ],
            "output": "string"
        }
        ```

## Gestión de Migraciones con Alembic

### Crear una Nueva Migración

Para crear una nueva migración que refleje los cambios en los modelos:

```sh
alembic revision --autogenerate -m "Descripción de los cambios"
```