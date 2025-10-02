#!/bin/bash
set -e

# Verificar si el archivo de datos ya existe o si hay datos en la BD
DATA_FILE="/docker-entrypoint-initdb.d/1_data.sql"
MARKER_FILE="/var/lib/mysql/.data_generated"

if [ "$INIT_DB" = "true" ]; then
    # Solo generar datos si no existe el archivo marcador
    if [ ! -f "$MARKER_FILE" ]; then
        echo ">> Primera ejecución detectada. Generando datos con Faker..."
        
        # Generar el archivo de datos
        python3 /generate_data.py
        mv data.sql "$DATA_FILE"
        
        # Agregar comando para crear el archivo marcador al final de la inicialización
        echo "SYSTEM touch $MARKER_FILE;" >> "$DATA_FILE"
        
        echo ">> Datos generados correctamente."
    else
        echo ">> Los datos ya fueron generados previamente. Saltando generación..."
        # Remover el archivo de datos para evitar reinserción
        rm -f "$DATA_FILE"
    fi
else
    echo ">> INIT_DB=false. Saltando inicialización de datos..."
    rm -f "$DATA_FILE"
fi

# Ejecutar el entrypoint original de MySQL
exec /entrypoint.sh mysqld
