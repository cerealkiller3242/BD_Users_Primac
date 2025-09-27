from faker import Faker
import random
from datetime import datetime

fake = Faker("es_MX")

N = 20000
BATCH_SIZE = 1000  # cantidad de filas por bloque de inserción

roles = ["ADMIN", "USER", "AGENT"]
states = [
    "AMAZONAS","ANCASH","APURIMAC","AREQUIPA","AYACUCHO","CAJAMARCA","CALLAO","CUSCO",
    "HUANCAVELICA","HUANUCO","ICA","JUNIN","LA_LIBERTAD","LAMBAYEQUE","LIMA","LORETO",
    "MADRE_DE_DIOS","MOQUEGUA","PASCO","PIURA","PUNO","SAN_MARTIN","TACNA","TUMBES","UCAYALI"
]

def escape(val: str) -> str:
    """Escapar comillas simples para SQL."""
    return val.replace("'", "''")

with open("data.sql", "w", encoding="utf-8") as f:

    # ===================== USERS =====================
    for start in range(1, N+1, BATCH_SIZE):
        end = min(start + BATCH_SIZE - 1, N)
        values = []
        for i in range(start, end+1):
            username = escape(fake.user_name())
            email = escape(fake.unique.email())
            password = escape(fake.password(length=10))
            role = random.choice(roles)
            phone = fake.unique.random_int(min=900000000, max=999999999)
            created = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            street = escape(fake.street_address())
            city = escape(fake.city())
            state = random.choice(states)

            values.append(
                f"({i}, '{username}', '{email}', '{password}', '{role}', {phone}, '{created}', '{updated}', '{street}', '{city}', '{state}')"
            )
        f.write("INSERT INTO users (id, username, email, password, role, phone, created_at, updated_at, street, city, state) VALUES\n")
        f.write(",\n".join(values))
        f.write(";\n\n")

    # ===================== CLIENTS =====================
    for start in range(1, N+1, BATCH_SIZE):
        end = min(start + BATCH_SIZE - 1, N)
        values = []
        for i in range(start, end+1):
            first_name = escape(fake.first_name())
            last_name = escape(fake.last_name())
            document_type = "DNI"
            document_number = fake.unique.random_int(min=10000000, max=99999999)
            birth_date = fake.date_of_birth(minimum_age=18, maximum_age=80).strftime("%Y-%m-%d")
            created = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            values.append(
                f"({i}, '{first_name}', '{last_name}', '{document_type}', '{document_number}', '{birth_date}', '{created}', '{updated}')"
            )
        f.write("INSERT INTO clients (user_id, first_name, last_name, document_type, document_number, birth_date, created_at, updated_at) VALUES\n")
        f.write(",\n".join(values))
        f.write(";\n\n")

    # ===================== AGENTS =====================
    for start in range(1, N+1, BATCH_SIZE):
        end = min(start + BATCH_SIZE - 1, N)
        values = []
        for i in range(start, end+1):
            code = f"AGT{i:05d}"
            first_name = escape(fake.first_name())
            last_name = escape(fake.last_name())
            is_active = random.choice(["true", "false"])
            user_id = i

            values.append(
                f"('{code}', '{first_name}', '{last_name}', {is_active}, {user_id})"
            )
        f.write("INSERT INTO agents (code, first_name, last_name, is_active, user_id) VALUES\n")
        f.write(",\n".join(values))
        f.write(";\n\n")
