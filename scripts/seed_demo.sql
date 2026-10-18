
-- Parking Lima - Demo seed
-- Solo datos ficticios para pruebas.
-- Ejecutar sobre parking_db después de Alembic.

BEGIN;

-- 1. Distritos
INSERT INTO districts (id, name) VALUES
    (1, 'Miraflores'),
    (2, 'San Isidro'),
    (3, 'Santiago de Surco'),
    (4, 'San Borja'),
    (5, 'La Molina')
ON CONFLICT (id) DO NOTHING;

-- 2. Estacionamientos ficticios
WITH demo_parkings(district_name, parking_name, address) AS (
    VALUES
        ('Miraflores', 'Parking Demo Miraflores', 'Dirección ficticia M-101'),
        ('San Isidro', 'Parking Demo San Isidro', 'Dirección ficticia SI-102'),
        ('Santiago de Surco', 'Parking Demo Surco', 'Dirección ficticia S-103'),
        ('San Borja', 'Parking Demo San Borja', 'Dirección ficticia SB-104'),
        ('La Molina', 'Parking Demo La Molina', 'Dirección ficticia LM-105')
)
INSERT INTO parkings (district_id, name, address)
SELECT d.id, dp.parking_name, dp.address
FROM demo_parkings dp
JOIN districts d ON d.name = dp.district_name
WHERE NOT EXISTS (
    SELECT 1
    FROM parkings p
    WHERE p.district_id = d.id
      AND p.name = dp.parking_name
      AND p.address = dp.address
);

-- 3. Tres espacios por estacionamiento de demostración
WITH demo_parkings(name, address) AS (
    VALUES
        ('Parking Demo Miraflores', 'Dirección ficticia M-101'),
        ('Parking Demo San Isidro', 'Dirección ficticia SI-102'),
        ('Parking Demo Surco', 'Dirección ficticia S-103'),
        ('Parking Demo San Borja', 'Dirección ficticia SB-104'),
        ('Parking Demo La Molina', 'Dirección ficticia LM-105')
)
INSERT INTO parking_spaces (parking_id, code, is_active)
SELECT p.id, codes.code, TRUE
FROM demo_parkings dp
JOIN parkings p
  ON p.name = dp.name AND p.address = dp.address
CROSS JOIN (VALUES ('A01'), ('A02'), ('A03')) AS codes(code)
ON CONFLICT (parking_id, code) DO NOTHING;

COMMIT;
