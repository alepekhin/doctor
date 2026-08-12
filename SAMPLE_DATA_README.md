# Doctor - Medical Data File Loading Examples

This directory contains sample medical records you can load into the database using the `add_external_records.py` script.

## Sample Files

- **example_001.json** - Single patient record (John Doe - Diabetes Type 2)
- **example_002.json** - Single patient record (Jane Smith - Hypertension)
- **example_003.json** - Single patient record (Bob Wilson - Asthma)
- **example_batch.json** - Batch of 2 patient records
- **example_001_jsonl.jsonl** - JSON Lines format file

## Loading Examples

### Load a single patient:

```bash
python add_external_records.py example_001.json
```

### Load a batch of records:

```bash
python add_external_records.py example_batch.json
```

### Load JSON Lines format:

```bash
python add_external_records.py example_001_jsonl.jsonl
```

### Dry run (preview without inserting):

```bash
python add_external_records.py example_001.json --dry-run
```

### Check first records:

```bash
python add_external_records.py --check example_001.json
```

## Record Structure

Each record should contain:

```json
{
  "patient_id": "P001",
  "data": {
    "name": "John Doe",
    "age": 35,
    "diagnosis": "Diabetes Type 2",  // optional
    "vitals": {
      "blood_pressure": {"systolic": 120, "diastolic": 80},
      "pulse": 72
    },
    "labs": {  // optional
      "ALT": 45,
      "Glucose_Fasting": 118,
      "HbA1c": 7.5
    },
    "history": {  // optional
      "allergies": ["Penicillin"],
      "medications": ["Metformin"],
      "conditions": ["Diabetes Type 2"]
    }
  },
  "vitals_measurement_date": "2026-08-12T10:00:00Z",  // optional
  "measurement_source": "device"  // optional
}
```

## Custom Record

Create your own record following the same structure:

```bash
cp example_001.json my_patient.json
# Edit my_patient.json with custom data
python add_external_records.py my_patient.json
```

## Batch Upload

For bulk uploads, use `example_batch.json` format with a `records` array:

```bash
python add_external_records.py example_batch.json
```

## Supported Formats

- **JSON** - Single object or array of objects
- **JSONL** - JSON Lines (one JSON object per line)
- **CSV** - Tab-separated with patient_id, data, schema_info columns

## Data Examples

### Example 001: Diabetes Patient
```json
{
  "patient_id": "P001",
  "data": {
    "name": "John Doe",
    "age": 35,
    "diagnosis": "Diabetes Type 2",
    "vitals": {
      "blood_pressure": {"systolic": 120, "diastolic": 80},
      "pulse": 72
    },
    "labs": {
      "ALT": 45,
      "AST": 38,
      "WBC": 12.5,
      "Glucose_Fasting": 118,
      "HbA1c": 7.5
    },
    "history": {
      "allergies": ["Penicillin"],
      "medications": ["Metformin"],
      "conditions": ["Diabetes Type 2"],
      "family_history": ["Diabetes", "Hypertension"]
    }
  }
}
```

### Example Batch: Multiple Patients
```bash
python add_external_records.py example_batch.json
```

### Example 001 JSONL (Stream format)
See `example_001_jsonl.jsonl` for streaming format.
