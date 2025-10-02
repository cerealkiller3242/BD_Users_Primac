from faker import Faker
import random
from datetime import datetime

fake = Faker("es_MX")

N = 20000           # Total de usuarios
CLIENTS_N = 15000   # Clientes (15k)
AGENTS_N = 5000     # Agentes (5k)
BENEFICIARIES_N = 20000  # Beneficiarios (20k)
BATCH_SIZE = 1000

roles = ["ADMIN", "USER", "AGENT"]
states = [
    "AMAZONAS","ANCASH","APURIMAC","AREQUIPA","AYACUCHO","CAJAMARCA","CALLAO","CUSCO",
    "HUANCAVELICA","HUANUCO","ICA","JUNIN","LA_LIBERTAD","LAMBAYEQUE","LIMA","LORETO",
    "MADRE_DE_DIOS","MOQUEGUA","PASCO","PIURA","PUNO","SAN_MARTIN","TACNA","TUMBES","UCAYALI"
]

relationships = ["HIJO", "HIJA", "CONYUGE", "PADRE", "MADRE", "HERMANO", "HERMANA", "ABUELO", "ABUELA"]

def escape(val: str) -> str:
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
    for start in range(1, CLIENTS_N+1, BATCH_SIZE):
        end = min(start + BATCH_SIZE - 1, CLIENTS_N)
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
    for start in range(CLIENTS_N+1, N+1, BATCH_SIZE):
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

    # ===================== BENEFICIARIES =====================
    # Distribuir beneficiarios entre clientes (0-4 por cliente)
    beneficiaries_per_client = []
    remaining_beneficiaries = BENEFICIARIES_N
    
    for client_id in range(1, CLIENTS_N + 1):
        if remaining_beneficiaries <= 0:
            beneficiaries_per_client.append(0)
            continue
            
        # Cada cliente puede tener entre 0 y 4 beneficiarios
        max_possible = min(4, remaining_beneficiaries)
        num_beneficiaries = random.randint(0, max_possible)
        
        # Si estamos cerca del final, asegurar que distribuyamos todos los beneficiarios
        if client_id > CLIENTS_N - 1000 and remaining_beneficiaries > 0:
            num_beneficiaries = min(4, remaining_beneficiaries)
        
        beneficiaries_per_client.append(num_beneficiaries)
        remaining_beneficiaries -= num_beneficiaries
    
    # Si quedan beneficiarios, distribuirlos aleatoriamente
    while remaining_beneficiaries > 0:
        client_id = random.randint(0, CLIENTS_N - 1)
        if beneficiaries_per_client[client_id] < 4:
            beneficiaries_per_client[client_id] += 1
            remaining_beneficiaries -= 1
    
    # Generar beneficiarios
    beneficiary_id = 1
    for client_idx, num_beneficiaries in enumerate(beneficiaries_per_client):
        if num_beneficiaries == 0:
            continue
            
        client_id = client_idx + 1
        values = []
        
        for _ in range(num_beneficiaries):
            first_name = escape(fake.first_name())
            last_name = escape(fake.last_name())
            document_type = "DNI"
            document_number = fake.unique.random_int(min=10000000, max=99999999)
            birth_date = fake.date_of_birth(minimum_age=0, maximum_age=90).strftime("%Y-%m-%d")
            relationship = random.choice(relationships)
            created = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            values.append(
                f"({beneficiary_id}, {client_id}, '{first_name}', '{last_name}', '{document_type}', '{document_number}', '{birth_date}', '{relationship}', '{created}', '{updated}')"
            )
            beneficiary_id += 1
        
        if values:
            f.write("INSERT INTO beneficiaries (id, client_id, first_name, last_name, document_type, document_number, birth_date, relationship, created_at, updated_at) VALUES\n")
            f.write(",\n".join(values))
            f.write(";\n\n")
