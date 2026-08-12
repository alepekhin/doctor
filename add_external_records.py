"""Load medical data records from external JSON/CSV files into the database."""

import json
import csv
from datetime import datetime, timedelta
from sqlalchemy import create_engine, insert
from config import get_connection_uri
from src.commands.migrate.schema import MedicalData


def load_from_json_file(filepath):
    """Load records from a JSON file."""
    with open(filepath, 'r') as f:
        if filepath.endswith('.jsonl'):  # JSON Lines format
            records = []
            for line in f:
                line = line.strip()
                if line:
                    records.append(json.loads(line))
            return records
        else:
            # Array of records or single record
            data = json.load(f)
            if isinstance(data, list):
                return data
            return [data]


def load_from_csv_file(filepath):
    """Load records from a CSV file."""
    records = []
    required_fields = ['patient_id', 'data', 'schema_info']
    
    with open(filepath, 'r', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Convert data field to JSON if it's a JSON string
            data = row['data']
            if isinstance(data, str) and data.startswith('{'):
                try:
                    data = json.loads(data)
                except json.JSONDecodeError:
                    pass  # Keep as string if parsing fails
            
            record = {
                'patient_id': row['patient_id'],
                'data': data,
                'schema_info': row['schema_info'] if row['schema_info'] else '{}',
                'vitals_measurement_date': datetime.utcnow() - timedelta(hours=2) if row.get('vitals_measurement_date') else None,
                'measurement_source': row.get('measurement_source') or 'device'
            }
            records.append(record)
    
    return records


def load_records_from_file(filepath):
    """Auto-detect file format and load records."""
    if not filepath:
        print("Error: No file path provided.")
        return []
    
    if not filepath.endswith(('.json', '.jsonl', '.csv')):
        print(f"Warning: Unsupported file format '{filepath}'. Trying to parse as JSON.")
    
    try:
        return load_from_json_file(filepath)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        try:
            return load_from_csv_file(filepath)
        except Exception as csv_error:
            print(f"Error loading from file: {e}")
            print(f"CSV error: {csv_error}")
            return []


def insert_records(engine, records):
    """Insert records into the medical_data table."""
    inserted = 0
    errors = []
    
    for record in records:
        try:
            # Add missing fields with defaults
            sample = {
                'patient_id': record.get('patient_id', ''),
                'data': record.get('data', {}),
                'schema_info': record.get('schema_info', {}),
                'vitals_measurement_date': record.get('vitals_measurement_date') or datetime.utcnow(),
                'measurement_source': record.get('measurement_source') or 'device'
            }
            
            conn = engine.connect()
            conn.execute(insert(MedicalData), sample)
            conn.commit()
            inserted += 1
        except Exception as e:
            errors.append(f"Failed to insert {record.get('patient_id', 'unknown')}: {e}")
            conn.rollback()
    
    return inserted, errors


def main():
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python add_external_records.py <json|csv_file> [--dry-run]")
        print("")
        print("Examples:")
        print("  python add_external_records.py patients.json")
        print("  python add_external_records.py vital-signs.jsonl")
        print("  python add_external_records.py visits.csv --dry-run")
        return
    
    filepath = sys.argv[1]
    dry_run = '--dry-run' in sys.argv
    
    print("Loading records from:", filepath)
    records = load_records_from_file(filepath)
    
    if not records:
        print("No records found.")
        return
    
    print(f"Found {len(records)} record(s).")
    
    if dry_run:
        print("\nDry run - no records will be inserted.")
    else:
        engine = create_engine(get_connection_uri())
        inserted, errors = insert_records(engine, records)
        
        print(f"\nInserted {inserted} record(s).")
        
        if errors:
            print("\nErrors occurred during insertion:")
            for error in errors:
                print(f"  - {error}")


if __name__ == "__main__":
    main()
