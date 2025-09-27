FROM mysql:8.0

# Variables por defecto
ENV MYSQL_ROOT_PASSWORD=root
ENV MYSQL_DATABASE=primac
ENV MYSQL_USER=admin
ENV MYSQL_PASSWORD=admin
ENV INIT_DB=true

# Instalar Python para Faker
RUN apt-get update && apt-get install -y python3 python3-pip && rm -rf /var/lib/apt/lists/*
COPY requirements.txt /requirements.txt
RUN pip3 install -r /requirements.txt

# Copiar scripts y schema
COPY ./scripts/generate_data.py /generate_data.py
COPY ./init/schema.sql /docker-entrypoint-initdb.d/0_schema.sql

# Generar data.sql con Faker durante el build
RUN python3 /generate_data.py && mv data.sql /docker-entrypoint-initdb.d/1_data.sql

COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
