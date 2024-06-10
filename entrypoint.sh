#!/bin/bash
# Detén la ejecución en caso de errores
set -e

# Ejecuta las migraciones
alembic upgrade head

# Ejecutar el comando CMD desde Dockerfile
exec "$@"
