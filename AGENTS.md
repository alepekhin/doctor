# Doctor - AI Medical Data Agent Guide

## Overview

This document guides AI agents working on the medical data analysis project. The goal is to create a simple, autonomous command-line application for storing and analyzing medical data using PostgreSQL and Ollama.

## Core Requirements

- **Simplicity**: Keep implementation minimal and straightforward
- **Autonomy**: Work independently on Ubuntu 26.04 with full user access
- **CLI-first**: Command-line interface, no external web dependencies
- **Offline**: No internet access required (uses local Ollama)
- **Migration-ready**: Handle database schema migrations within the app
- **Flexible schema**: Support arbitrary JSONB medical data structures

## Technology Stack

- Python 3.8+
- PostgreSQL 15+
- Ollama with `carstenuhlig/omnicoder-2-9b:latest` model

## Agent Responsibilities

### 1. Database Agent

**Tasks:**
- Initialize `medical_data` table with JSONB storage
- Implement migration commands for schema updates
- Create sample seeding utilities

**Database Schema:**
```sql
medical_data (
    id INTEGER PRIMARY KEY,
    created_at TIMESTAMPTZ,
    updated_at TIMESTAMPTZ,
    patient_id VARCHAR(50) NOT NULL,
    data JSONB,
    schema_info JSON
)
```

### 2. Analysis Agent

**Tasks:**
- Extract vitals data (blood pressure, pulse) from JSONB records
- Generate AI prompts for medical data analysis
- Parse and format model responses

**Workflow:**
1. Query database for relevant records
2. Format data into prompts for Ollama
3. Call `chat()` API with model
4. Parse and present AI analysis

### 3. CLI Agent

**Tasks:**
- Implement simple command-line entry points
- Handle PostgreSQL connection strings
- Parse command-line arguments
- Graceful error handling

### 4. Code Quality Agent

**Tasks:**
- Maintain simple, readable code
- Add type hints where beneficial
- Write inline docstrings
- Follow existing code style in codebase

## Constraints & Guidelines

1. **No external services**: Use only local PostgreSQL and Ollama
2. **Minimal dependencies**: Keep requirements lean
3. **Single responsibility**: Each script handles one task
4. **No external internet**: All AI calls via local Ollama
5. **PostgreSQL credentials**: Store in config, not hardcoded (consider `.env`)

## Entry Point Scripts

- `analyze_data.py` - Full schema analysis
- `analyze_vitals.py` - Vitals extraction & health assessment
- `seed_data.py` - Populate sample records
- `db-migrate` - Console script for migrations

## Testing Strategy

- Unit tests for data extraction functions
- Integration tests for Ollama API calls
- Database schema tests
- CLI argument parsing tests

## Sample Commands

```
Initialize database:
  python src/commands/migrate/schema.py "postgresql://user:pass@localhost/db?seed=true"

Analyze all records:
  python analyze_data.py

Extract vitals:
  python analyze_vitals.py

Seed test data:
  python seed_data.py
```

## Current State

- ✅ Database schema defined
- ✅ Sample data seeding working
- ✅ Ollama analysis pipeline functional
- ✅ Vitals extraction implemented
- ⏳ Production error handling needed
- ⏳ Configuration management desired

## Next Steps for Agents

1. Add environment variable support for DB credentials
2. Implement connection pooling for long-running analysis
3. Add unit tests for all functions
4. Create comprehensive CLI with argument parsing
5. Add logging for audit trail
6. Implement schema validation against known patterns