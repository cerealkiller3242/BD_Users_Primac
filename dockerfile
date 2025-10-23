FROM mysql:8.0-debian

# Variables por defecto
ENV MYSQL_ROOT_PASSWORD=root
ENV MYSQL_DATABASE=primac
ENV MYSQL_USER=admin
ENV MYSQL_PASSWORD=admin
ENV INIT_DB=true

# Instalar Python para Faker
RUN echo "deb [trusted=yes] http://repo.mysql.com/apt/debian/ bullseye mysql-8.0" > /etc/apt/sources.list.d/mysql.list && \
    apt-get update --allow-unauthenticated && \
    apt-get install -y --allow-unauthenticated python3 python3-pip && \
    rm -rf /var/lib/apt/lists/*
COPY requirements.txt /requirements.txt
RUN pip3 install --break-system-packages -r /requirements.txt

# Copiar scripts y schema
COPY ./scripts/generate_data.py /generate_data.py
COPY ./init/schema.sql /docker-entrypoint-initdb.d/0_schema.sql
COPY ./init/9_mark_complete.sql /docker-entrypoint-initdb.d/9_mark_complete.sql

# NO generar data.sql durante el build - se hará en runtime

COPY ./entrypoint.sh /custom-entrypoint.sh
RUN chmod +x /custom-entrypoint.sh && sed -i 's/\r$//' /custom-entrypoint.sh

ENTRYPOINT ["/custom-entrypoint.sh"]
