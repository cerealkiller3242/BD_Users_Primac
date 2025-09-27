INSERT INTO users (username, email, password, role, phone, created_at, updated_at, street, city, state)
VALUES 
('cereal', 'cereal@test.com', '123456', 'USER', 999888777, NOW(), NOW(), 'Av. Siempre Viva 123', 'Lima', 'LIMA');

INSERT INTO clients (user_id, first_name, last_name, document_type, document_number, birth_date, created_at, updated_at)
VALUES
(1, 'Juan', 'Perez', 'DNI', '12345678', '2000-01-01', NOW(), NOW());

INSERT INTO users (username, email, password, role, phone, created_at, updated_at, street, city, state)
VALUES 
('andres', 'andres@test.com', 'abcdef', 'AGENT', 987654321, NOW(), NOW(), 'Calle Falsa 456', 'Cusco', 'CUSCO');

INSERT INTO agents (code, first_name, last_name, is_active, user_id)
VALUES 
('AGT001', 'Andres', 'Gomez', true, 2);
