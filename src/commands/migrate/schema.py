"""Database migration tool for PostgreSQL medical records."""

from sqlalchemy import (create_engine, Column, Integer, String, Boolean, DateTime, JSON,
                         Text, Sequence, ForeignKey, Table, inspect, event)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from sqlalchemy.sql import select
from datetime import datetime

Base = declarative_base()


def create_table_schema(engine):
    """Create the medical_data table for storing arbitrary medical records."""
    metadata = inspect(Base.metadata)
    if 'medical_data' not in metadata.tables:
        Base.metadata.create_all(engine)
        print("Table 'medical_data' created successfully.")
    else:
        print("Table 'medical_data' already exists.")


class MedicalData(Base):
    """Table for storing arbitrary medical data."""
    __tablename__ = 'medical_data'
    
    id = Column(Integer, Sequence('medical_data_id'), primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(String(50), comment="User or system that created the record")
    updated_by = Column(String(50), comment="User or system that last updated")
    
    # Flexible JSONB field for storing arbitrary medical data
    patient_id = Column(String(50), nullable=False, index=True)
    data = Column(JSONB, comment="Arbitrary medical data as JSON")
    schema_info = Column(JSON, comment="Schema information for the data")
    vitals_measurement_date = Column(DateTime, comment="Date/vitals were measured (optional)")
    measurement_source = Column(String(20), comment="Source of measurement (device/manual)")
    
    @property
    def schema(self):
        """Get schema information from metadata."""
        return self.metadata if self.metadata else {}


def init_schema(connection_uri):
    """Initialize the database schema."""
    engine = create_engine(connection_uri)
    
    with engine.begin() as conn:
        # Drop existing tables
        Base.metadata.drop_all(bind=engine)
        # Create new tables
        Base.metadata.create_all(bind=engine)
    
    print("Database schema initialized successfully.")
    return engine


def create_sample_data(engine, samples):
    """Create sample medical data records."""
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()
    
    try:
        from datetime import timedelta
        base_time = datetime.utcnow() - timedelta(hours=6)
        for sample in samples:
            data = MedicalData(
                patient_id=sample['patient_id'],
                data=sample['data'],
                schema_info=sample.get('schema_info', {}),
                vitals_measurement_date=base_time,
                measurement_source='device'
            )
            session.add(data)
    finally:
        session.close()


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python schema.py <connection_uri> [--seed]")
        print("  connection_uri: e.g., postgresql://user:pass@localhost:5432/dbname")
        print("  --seed: Optional flag to populate with sample data")
        sys.exit(1)
    
    connection_uri = sys.argv[1]
    seed = '--seed' in sys.argv
    
    engine = init_schema(connection_uri)
    create_table_schema(engine)
    
    if seed:
        samples = [
            {
                "patient_id": "P001",
                "data": {
                    "name": "John Doe",
                    "age": 35,
                    "diagnosis": "Diabetes Type 2",
                    "vitals": {"blood_pressure": "120/80", "pulse": 72},
                    "labs": {
                        "ALT": 45,
                        "AST": 38,
                        "WBC": 12.5
                    },
                    "history": {
                        "allergies": ["Penicillin"],
                        "medications": ["Metformin"],
                        "conditions": ["Diabetes Type 2"]
                    }
                },
                "metadata": {"version": "1.0", "schema_type": "general_patient"}
            },
            {
                "patient_id": "P002",
                "data": {
                    "name": "Jane Smith",
                    "age": 28,
                    "diagnosis": "Hypertension",
                    "vitals": {"blood_pressure": "145/92", "pulse": 68},
                    "labs": {
                        "ALT": 32,
                        "AST": 28,
                        "WBC": 8.2
                    },
                    "history": {
                        "allergies": [],
                        "medications": ["Lisinopril"],
                        "conditions": ["Hypertension"]
                    }
                },
                "metadata": {"version": "1.0", "schema_type": "general_patient"}
            },
        ]
        create_sample_data(engine, samples)
        print(f"Created {len(samples)} sample records.")