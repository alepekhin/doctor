"""Check sample data."""
from sqlalchemy import create_engine, text

DB_URL = "postgresql://postgres:mysecretpassword@localhost/postgres"
engine = create_engine(DB_URL)

with engine.connect() as conn:
    result = conn.execute(text("""
        SELECT patient_id, id, vitals_measurement_date 
        FROM medical_data 
        ORDER BY patient_id, vitals_measurement_date
    """))
    print("\nSample Records:\n")
    for row in result:
        print(f"Patient {row.patient_id}: ID {row.id}, Date {row.vitals_measurement_date}")
