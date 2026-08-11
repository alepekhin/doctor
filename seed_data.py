"""Seed the medical_data table with sample records."""

from datetime import datetime, timedelta
from sqlalchemy import create_engine, insert
from src.commands.migrate.schema import MedicalData

engine = create_engine("postgresql://postgres:mysecretpassword@localhost/postgres")

base_time = datetime.utcnow() - timedelta(hours=6)
samples = [
    {
        "patient_id": "P001",
        "data": {
            "name": "John Doe",
            "age": 35,
            "diagnosis": "Diabetes Type 2",
            "vitals": {"blood_pressure": {"systolic": 120, "diastolic": 80}, "pulse": 72},
            "history": {
                "allergies": ["Penicillin"],
                "medications": ["Metformin"],
                "conditions": ["Diabetes Type 2"]
            }
        },
        "schema_info": {"version": "1.0", "schema_type": "general_patient"},
        "vitals_measurement_date": base_time,
        "measurement_source": "device"
    },
    {
        "patient_id": "P002",
        "data": {
            "name": "Jane Smith",
            "age": 28,
            "diagnosis": "Hypertension",
            "vitals": {"blood_pressure": {"systolic": 145, "diastolic": 92}, "pulse": 68},
            "history": {
                "allergies": [],
                "medications": ["Lisinopril"],
                "conditions": ["Hypertension"]
            }
        },
        "schema_info": {"version": "1.0", "schema_type": "general_patient"},
        "vitals_measurement_date": base_time + timedelta(hours=3),
        "measurement_source": "device"
    },
    {
        "patient_id": "P001",
        "data": {
            "name": "John Doe",
            "age": 35,
            "diagnosis": "Diabetes Type 2",
            "vitals": {"blood_pressure": {"systolic": 135, "diastolic": 88}, "pulse": 75},
            "history": {
                "allergies": ["Penicillin"],
                "medications": ["Metformin"],
                "conditions": ["Diabetes Type 2"]
            }
        },
        "schema_info": {"version": "1.0", "schema_type": "general_patient"},
        "vitals_measurement_date": base_time + timedelta(hours=5),
        "measurement_source": "manual"
    },
    {
        "patient_id": "P003",
        "data": {
            "name": "Bob Wilson",
            "age": 52,
            "diagnosis": "Asthma",
            "vitals": {"blood_pressure": {"systolic": 118, "diastolic": 76}, "pulse": 84},
            "history": {
                "allergies": [],
                "medications": ["Inhaled Corticosteroids"],
                "conditions": ["Asthma", "Obesity"]
            }
        },
        "schema_info": {"version": "1.0", "schema_type": "general_patient"},
        "vitals_measurement_date": base_time + timedelta(hours=12),
        "measurement_source": "device"
    },
    {
        "patient_id": "P003",
        "data": {
            "name": "Bob Wilson",
            "age": 52,
            "diagnosis": "Asthma",
            "vitals": {"blood_pressure": {"systolic": 122, "diastolic": 79}, "pulse": 88},
            "history": {
                "allergies": [],
                "medications": ["Inhaled Corticosteroids"],
                "conditions": ["Asthma", "Obesity"]
            }
        },
        "schema_info": {"version": "1.0", "schema_type": "general_patient"},
        "vitals_measurement_date": base_time + timedelta(hours=24),
        "measurement_source": "device"
    },
]

with engine.connect() as conn:
    for sample in samples:
        conn.execute(insert(MedicalData), sample)
    conn.commit()

print(f"Created {len(samples)} sample records.")
