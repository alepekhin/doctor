"""Entry point for db-migrate command."""
import sys
from urllib.parse import parse_qs, urlparse


def get_connection_uri(arg=sys.argv[1]):
    """Parse connection URI from command line argument."""
    if not arg:
        print("Usage: db-migrate <connection_uri>")
        print("  connection_uri: postgresql://user:pass@localhost:5432/dbname")
        print("  Example: postgresql://user:password@localhost/med_db")
        sys.exit(1)
    
    return arg


def main():
    """Entry point for database migration."""
    from .schema import init_schema, create_sample_data, MedicalData
    
    print("Database Migration Tool for PostgreSQL")
    print("="*40)
    
    try:
        engine = init_schema(get_connection_uri())
        print("\nSchema initialized successfully.")
    
        print("\n" + "="*40 + "\n")
        print("Optional: Add --seed to populate sample data.")
        
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
