# Doctor - Medical Data Analysis & Schema Inspection

A Python project for analyzing medical data stored in PostgreSQL using JSONB, with AI-powered schema analysis and health insights using the carstenuhlig/omnicoder-2-9b model via Ollama.

## Features

- **Flexible JSONB Storage**: Store arbitrary medical records in a single `medical_data` table
- **AI-Powered Analysis**: Use LLMs to analyze data patterns, extract insights, and generate recommendations
- **Vitals Extraction**: Extract blood pressure and pulse data for health assessments
- **Schema Recommendations**: Get actionable recommendations for schema optimization and compliance

## Installation

```bash
pip install -e ".[dev]"  # Install with development dependencies
```

## Prerequisites

- Python >= 3.8
- PostgreSQL database
- Ollama running locally with the `carstenuhlig/omnicoder-2-9b:latest` model

## Configuration

Update these values in the script files:

```python
DB_URL = "postgresql://postgres:mysecretpassword@localhost/postgres"
MODEL = "carstenuhlig/omnicoder-2-9b:latest"
```

## Usage

### 1. Initialize Database Schema & Seed Sample Data

```bash
python src/commands/migrate/schema.py "postgresql://user:pass@localhost/dbname" --seed
```

Or use the console script:
```bash
db-migrate "postgresql://user:pass@localhost/dbname" --seed
```

### 2. Analyze Medical Data Schema

```bash
python analyze_data.py
```

This will:
- Fetch all medical records from PostgreSQL
- Send them to the AI model for analysis
- Output schema patterns, recommendations, and potential issues

### 3. Extract and Analyze Vitals Data

```bash
python analyze_vitals.py
```

This will:
- Extract blood pressure and pulse data from patients
- Provide AI analysis on health assessments and recommendations

### 4. Seed Database with Sample Data

```bash
python seed_data.py
```

## Database Schema

The `medical_data` table structure:

```sql
CREATE TABLE medical_data (
    id SERIAL PRIMARY KEY,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    patient_id VARCHAR(50) NOT NULL,
    data JSONB,           -- Flexible medical data storage
    schema_info JSON      -- Schema metadata (version, type)
);
```

### Data Structure Example

```json
{
  "name": "John Doe",
  "age": 35,
  "diagnosis": "Diabetes Type 2",
  "vitals": {
    "blood_pressure": "120/80",
    "pulse": 72
  },
  "history": {
    "allergies": ["Penicillin"],
    "medications": ["Metformin"],
    "conditions": ["Diabetes Type 2"]
  }
}
```

## Project Structure

```
/
├── analyze_data.py              # Full schema analysis with AI
├── analyze_vitals.py            # Vitals extraction and health analysis
├── seed_data.py                 # Populate database with sample records
├── analysis_result.py           # Static analysis output reference
├── setup.py                     # Build configuration
├── pyproject.toml               # Project metadata
├── src/
│   └── commands/
│       └── migrate/             # Database migration scripts
│           └── schema.py        # Schema initialization
└── tests/                       # Test suite
```

## Analysis Report

The AI analysis provides:

1. **Schema Analysis**: Identifies consistent fields and data structures
2. **Data Patterns**: Recognizes nested hierarchies (vitals, history)
3. **Recommendations**:
   - Type safety improvements
   - Compliance features (HIPAA/GDPR)
   - Performance optimizations
   - Schema evolution strategies
4. **Potential Issues**: Data quality, security, and regulatory concerns

## License

MIT License

## Development Dependencies

```bash
terminal -e bash -c 'pip install -e "./[dev]"'
```

Installs: pytest, pytest-cov, black, ruff, mypy

## Contributing

Contributions are welcome. Please feel free to submit a Pull Request.

## Support

For issues or questions, please open an issue in the repository.
