from faker import Faker
import random
from datetime import datetime
fake = Faker("es_PE")

N = 20000

roles = ["ADMIN", "USER", "AGENT"]
states = [
    "AMAZONAS","ANCASH","APURIMAC","AREQUIPA","AYACUCHO","CAJAMARCA","CALLAO","CUSCO",
    "HUANCAVELICA","HUANUCO","ICA","JUNIN","LA_LIBERTAD","LAMBAYEQUE","LIMA","LORETO",
    "MADRE_DE_DIOS","MOQUEGUA","PASCO","PIURA","PUNO","SAN_MARTIN","TACNA","TUMBES","UCAYALI"
]

with open("data.sql", "w", encoding="utf-8") as f:
    # Users
    for i in range(1, N+1):
        username = fake.user_name()
        email = fake.unique.email()
        password = fake.password(length=10)
        role = random.choice(roles)
        phone = fake.unique.random_int(min=900000000, max=999999999)
        created = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        street = fake.street_address()
        city = fake.city()
        state = random.choice(states)

        f.write(f"INSERT INTO users (id, username, email, password, role, phone, created_at, updated_at, street, city, state) VALUES ({i}, '{username}', '{email}', '{password}', '{role}', {phone}, '{created}', '{updated}', '{street}', '{city}', '{state}');\n")

    # Clients (1-20000 basados en los mismos users)
    for i in range(1, N+1):
        first_name = fake.first_name()
        last_name = fake.last_name()
        document_type = "DNI"
        document_number = fake.unique.random_int(min=10000000, max=99999999)
        birth_date = fake.date_of_birth(minimum_age=18, maximum_age=80).strftime("%Y-%m-%d")
        created = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        f.write(f"INSERT INTO clients (user_id, first_name, last_name, document_type, document_number, birth_date, created_at, updated_at) VALUES ({i}, '{first_name}', '{last_name}', '{document_type}', '{document_number}', '{birth_date}', '{created}', '{updated}');\n")

    # Agents (otra tanda 1-20000, cada uno linkeado a un user)
    for i in range(1, N+1):
        code = f"AGT{i:05d}"
        first_name = fake.first_name()
        last_name = fake.last_name()
        is_active = random.choice(["true","false"])
        user_id = i

        f.write(f"INSERT INTO agents (code, first_name, last_name, is_active, user_id) VALUES ('{code}', '{first_name}', '{last_name}', {is_active}, {user_id});\n")
