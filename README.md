# Doctor - Medical Data Analysis CLI

A simple, autonomous command-line tool for analyzing medical data using Ollama LLM.

## Features

- Analyze JSON lab test data with medical insights
- Process medical imaging (tables) and convert to analytical conclusions
- Works offline on Ubuntu 26.04+ with local Ollama
- Minimal dependencies, Python 3.8+

## Requirements

- Python 3.8+
- [Ollama](https://ollama.ai) server running locally
- Models: `carstenuhlig/omnicoder-2-9b:latest`, `gemma4:latest`

## Installation

```bash
# Install Python dependencies
pip install -r requirements.txt

# (Optional) Pull required Ollama models
ollama pull carstenuhlig/omnicoder-2-9b:latest
ollama pull gemma4:latest
```

## Usage

### Analyze JSON file

```bash
python main.py blood.json

# Output:
Medical Analysis Result:
[Analysis conclusion]

⚠️ Medical Disclaimer: This analysis is AI-generated. Consult a qualified medical professional for medical advice.
```

### Analyze image file

```bash
python main.py blood.jpg

# Output:
Medical Analysis Result:
[Extraction and analysis from image]

⚠️ Medical Disclaimer: This analysis is AI-generated. Consult a qualified medical professional for medical advice.
```

## Testing

```bash
# Run unit tests (no Ollama required)
python3 -m pytest tests/test_all.py -v

# Run live integration tests against a running Ollama server
python3 -m pytest tests/test_live.py -v

# Run the full suite (unit + live)
python3 -m pytest tests/ -v
```

Live tests are skipped automatically if Ollama is unreachable.

## Project Structure

```
doctor/
├── main.py                    # CLI entry point
├── api_client.py              # Ollama API client
├── models.py                  # Model routing & detection
├── analyzers.py               # Data analysis logic
├── disclaimer.py              # Medical disclaimer
├── tests/                     # Comprehensive test suite
│   └── test_all.py
├── config/models.json         # Model configuration
├── requirements.txt           # Dependencies
├── AGENTS.md                  # Project guide
├── LICENSE                    # MIT License
└── README.md                  # This file
```

## Technical Details

### Data Flow

- **JSON input**: Direct analysis with `carstenuhlig/omnicoder-2-9b:latest`
- **Image input**: Convert to JSON with `gemma4:latest` → Analyze → Output

### Output Format

- Streaming analysis to stdout
- JSON input → Medical conclusion → Disclaimer
- Image input → Table extraction → Medical conclusion → Disclaimer

### Error Handling

- Graceful handling of missing models
- Automatic model loading with progress
- Connection retries with exponential backoff
- Clear error messages for file not found, invalid JSON, etc.

## License

MIT License - See [LICENSE](LICENSE) file.
