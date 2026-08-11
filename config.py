"""Centralized configuration for Doctor application."""

import sys
from pathlib import Path

try:
    import toml, json
    HAS_TOML = True
except ImportError:
    HAS_TOML = False

try:
    import dotenv
    HAS_DOTENV = True
except ImportError:
    HAS_DOTENV = False

# Base directories
PROJECT_ROOT = Path(__file__).parent.parent.parent
CONFIG_PATH = PROJECT_ROOT / ".env"
PYPROJECT_PATH = PROJECT_ROOT / "pyproject.toml"


def load_config() -> dict:
    """Load configuration from environment or default values."""
    config = {
        "db_url": "postgresql://postgres:mysecretpassword@localhost/postgres",
        "model": "carstenuhlig/omnicoder-2-9b:latest",
    }
    
    # Load from .env file if available
    if HAS_DOTENV and CONFIG_PATH.exists():
        try:
            dotenv.load_dotenv(CONFIG_PATH)
            config["db_url"] = dotenv.get_key(str(CONFIG_PATH), "DB_URL", default=config["db_url"])
            config["model"] = dotenv.get_key(str(CONFIG_PATH), "MODEL", default=config["model"])
        except Exception:
            pass
    
    # Fall back to environment variables
    if "DB_URL" in sys.environ:
        config["db_url"] = sys.environ["DB_URL"]
    if "MODEL" in sys.environ:
        config["model"] = sys.environ["MODEL"]
    
    return config


def get_connection_uri() -> str:
    """Get database connection URI from config."""
    import urllib.parse
    return str(load_config()["db_url"])


def get_model() -> str:
    """Get AI model name from config."""
    return load_config()["model"]


# Default sample data for seeding
SAMPLES = [
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
    },
]


__all__ = ["load_config", "get_connection_uri", "get_model", "SAMPLES"]