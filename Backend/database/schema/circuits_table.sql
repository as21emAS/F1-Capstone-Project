-- First, create the circuits table
CREATE TABLE circuits (
    circuit_id VARCHAR(100) PRIMARY KEY,
    circuit_name VARCHAR(255) NOT NULL,
    location VARCHAR(255),
    country VARCHAR(100),
    latitude DECIMAL(10, 6),
    longitude DECIMAL(10, 6),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Second, populate it with data from races table
INSERT INTO circuits (circuit_id, circuit_name, country)
SELECT DISTINCT circuit_id, circuit_name, country
FROM races
ON CONFLICT (circuit_id) DO NOTHING;

-- Third, add the foreign key
ALTER TABLE races ADD FOREIGN KEY (circuit_id) REFERENCES circuits(circuit_id);

-- Exit
\q