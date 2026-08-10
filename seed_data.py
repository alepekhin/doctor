"""Seed the medical_data table with sample records."""

from sqlalchemy import create_engine, insert
from src.commands.migrate.schema import MedicalData

engine = create_engine("postgresql://postgres:mysecretpassword@localhost/postgres")
samples = [
    {
        "patient_id": "P001",
        "data": {
            "name": "John Doe",
            "age": 35,
            "diagnosis": "Diabetes Type 2",
            "vitals": {"blood_pressure": "120/80", "pulse": 72},
            "history": {
                "allergies": ["Penicillin"],
                "medications": ["Metformin"],
                "conditions": ["Diabetes Type 2"]
            }
        },
        "schema_info": {"version": "1.0", "schema_type": "general_patient"}
    },
    {
        "patient_id": "P002",
        "data": {
            "name": "Jane Smith",
            "age": 28,
            "diagnosis": "Hypertension",
            "vitals": {"blood_pressure": "145/92", "pulse": 68},
            "history": {
                "allergies": [],
                "medications": ["Lisinopril"],
                "conditions": ["Hypertension"]
            }
        },
        "schema_info": {"version": "1.0", "schema_type": "general_patient"}
    },
]

with engine.connect() as conn:
    for sample in samples:
        conn.execute(insert(MedicalData), sample)
    conn.commit()

print(f"Created {len(samples)} sample records.")
