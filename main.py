"""Main CLI entry point for Doctor - Medical Data Analysis."""
import argparse
import sys
import os

# Add current directory to path
sys.path.insert(0, os.getcwd())

from api_client import OllamaApiClient
from models import ModelManager
from analyzers import AnalysisEngine


def main():
    parser = argparse.ArgumentParser(
        description="Doctor - Medical Data Analysis CLI"
    )
    parser.add_argument(
        "file",
        help="JSON or image file to analyze"
    )
    
    args = parser.parse_args()
    
    try:
        print(f"Analyzing: {args.file}")
        print()
        
        # Load model manager
        model_manager = ModelManager()
        model_manager.load_config()
        model_manager.check_env_override()
        
        # Print available models info
        available = model_manager.get_available_models()
        if not available:
            print("Note: Ollama models not detected. Proceeding with default...")
            print("Make sure these models are installed:")
            print(f"  - carstenuhlig/omnicoder-2-9b:latest")
            print(f"  - gemma4:latest")
            print()
        else:
            print(f"Available Ollama models: {available}")
            print()
        
        # Ensure models are loaded
        print("Loading required models...")
        print()
        
        client = OllamaApiClient()
        
        # Get appropriate model for file type
        model = model_manager.get_model_for_input(args.file)
        
        # Load model before analysis
        print(f"Loading model: {model}")
        if not model_manager.ensure_model_loaded(model):
            print("Warning: Model loading failed, proceeding with limited functionality")
        
        print()
        
        # Analyze file
        engine = AnalysisEngine(model_manager)
        result = engine.analyze_file(args.file)
        
        # Output result
        print(result)
        
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Analysis failed: {type(e).__name__}: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
