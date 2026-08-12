"""Add sample blood test records to the database."""

from datetime import datetime, timedelta
from sqlalchemy import create_engine, insert
from config import get_connection_uri
from src.commands.migrate.schema import MedicalData

engine = create_engine(get_connection_uri())

base_time = datetime.utcnow()

blood_tests = [
    {
        "patient_id": "P001",
        "data": {
            "name": "John Doe",
            "age": 35,
            "diagnosis": "Diabetes Type 2",
            "vitals": {"blood_pressure": {"systolic": 120, "diastolic": 80}, "pulse": 72},
            "labs": {
                "HbA1c": 7.5,  # Elevated (normal: <5.7%)
                "Glucose_Fasting": 118,  # Elevated (normal: <100 mg/dL)
                "Glucose_Homeostatic_Model_Assessment": 2.8,  # Elevated
                "ALT": 45,
                "AST": 38,
                "WBC": 12.5,
                "Creatinine": 1.1,  # Slightly elevated (normal: 0.6-1.2 mg/dL)
                "eGFR": 75  # Decreased kidney function (normal: >90)
            },
            "history": {
                "allergies": ["Penicillin"],
                "medications": ["Metformin"],
                "conditions": ["Diabetes Type 2"],
                "family_history": ["Diabetes", "Hypertension"],
                "surgical_history": []
            }
        },
        "schema_info": {"version": "2.0", "schema_type": "patient_with_blood_tests"},
        "vitals_measurement_date": base_time + timedelta(hours=1),
        "measurement_source": "device"
    },
    {
        "patient_id": "P002",
        "data": {
            "name": "Jane Smith",
            "age": 28,
            "diagnosis": "Hypertension",
            "vitals": {"blood_pressure": {"systolic": 145, "diastolic": 92}, "pulse": 68},
            "labs": {
                "HbA1c": 5.2,  # Normal
                "Glucose_Fasting": 85,  # Normal
                "Glucose_Homeostatic_Model_Assessment": 1.9,  # Normal
                "ALT": 32,
                "AST": 28,
                "WBC": 8.2,
                "Creatinine": 0.9,  # Normal
                "eGFR": 105  # Normal
            },
            "history": {
                "allergies": [],
                "medications": ["Lisinopril"],
                "conditions": ["Hypertension"],
                "family_history": ["Heart Disease", "Type 2 Diabetes"],
                "surgical_history": ["Appendectomy (2015)"]
            }
        },
        "schema_info": {"version": "2.0", "schema_type": "patient_with_blood_tests"},
        "vitals_measurement_date": base_time + timedelta(hours=2),
        "measurement_source": "device"
    },
    {
        "patient_id": "P003",
        "data": {
            "name": "Bob Wilson",
            "age": 52,
            "diagnosis": "Asthma",
            "vitals": {"blood_pressure": {"systolic": 118, "diastolic": 76}, "pulse": 84},
            "labs": {
                "HbA1c": 5.5,  # Normal
                "Glucose_Fasting": 92,  # Pre-diabetic range
                "Glucose_Homeostatic_Model_Assessment": 2.1,  # Borderline
                "ALT": 28,
                "AST": 30,
                "WBC": 9.1,
                "Creatinine": 1.0,  # Normal
                "eGFR": 98,
                "Iron_Ferritin": 120,  # Slightly elevated (normal: 30-400 ng/mL)
                "TSH": 2.8  # Normal (normal: 0.4-4.0 mIU/L)
            },
            "history": {
                "allergies": ["Pollen", "Dust"],
                "medications": ["Inhaled Corticosteroids", "LABA/LAMA Combo"],
                "conditions": ["Asthma", "Obesity", "Metabolic Syndrome"],
                "family_history": ["Asthma", "Type 2 Diabetes"],
                "surgical_history": ["Liposuction (2018)"]
            }
        },
        "schema_info": {"version": "2.0", "schema_type": "patient_with_blood_tests"},
        "vitals_measurement_date": base_time + timedelta(hours=3),
        "measurement_source": "device"
    },
    {
        "patient_id": "P004",
        "data": {
            "name": "Alice Johnson",
            "age": 41,
            "diagnosis": "None",
            "vitals": {"blood_pressure": {"systolic": 128, "diastolic": 84}, "pulse": 76},
            "labs": {
                "HbA1c": 5.8,  # Pre-diabetic
                "Glucose_Fasting": 102,  # Pre-diabetic (normal: <100)
                "Glucose_Homeostatic_Model_Assessment": 2.3,  # Borderline
                "ALT": 52,  # Elevated (normal: <40)
                "AST": 45,  # Elevated (normal: <35)
                "WBC": 7.8,
                "Creatinine": 0.85,
                "eGFR": 108,
                "Ferritin": 180,
                "TSH": 3.2
            },
            "history": {
                "allergies": ["Shellfish"],
                "medications": ["Multivitamin"],
                "conditions": [],
                "family_history": ["Type 2 Diabetes"],
                "surgical_history": []
            }
        },
        "schema_info": {"version": "2.0", "schema_type": "general_patient"},
        "vitals_measurement_date": base_time + timedelta(hours=4),
        "measurement_source": "manual"
    },
    {
        "patient_id": "P001",
        "data": {
            "name": "John Doe",
            "age": 35,
            "diagnosis": "Diabetes Type 2",
            "vitals": {"blood_pressure": {"systolic": 132, "diastolic": 86}, "pulse": 74},
            "labs": {
                "HbA1c": 7.2,  # Still elevated
                "Glucose_Fasting": 125,  # Diabetic range
                "Glucose_Homeostatic_Model_Assessment": 2.6,  # Elevated
                "ALT": 48,
                "AST": 40,
                "WBC": 13.1,
                "Creatinine": 1.05,
                "eGFR": 80
            },
            "history": {
                "allergies": ["Penicillin"],
                "medications": ["Metformin", "Glipizide"],
                "conditions": ["Diabetes Type 2", "Hypertension"],
                "family_history": ["Diabetes", "Hypertension"],
                "surgical_history": []
            }
        },
        "schema_info": {"version": "2.0", "schema_type": "patient_with_blood_tests"},
        "vitals_measurement_date": base_time + timedelta(hours=5),
        "measurement_source": "device"
    },
]

with engine.connect() as conn:
    for sample in blood_tests:
        conn.execute(insert(MedicalData), sample)
    conn.commit()

print(f"Created {len(blood_tests)} blood test records.")
