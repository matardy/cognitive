#!/bin/bash
# Script para crear una red Docker si no existe

# Para ejecutar
# chmod +x docker-network.sh
# sudo ./docker-network.sh
NETWORK_NAME="shared_network"
if ! docker network ls | grep -qw $NETWORK_NAME; then
  docker network create --driver bridge $NETWORK_NAME
fi
