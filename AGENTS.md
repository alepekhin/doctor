# Doctor - AI Medical Data Agent Guide

## Overview

This document guides AI agents working on the medical data analysis project.    
The goal is to create a simple, autonomous command-line application for analyzing medical data with Ollama LLM.   

## Core Requirements

- **Simplicity**: Keep implementation minimal and straightforward
- **Autonomy**: Work independently on Ubuntu 26.04 with full user access
- **CLI-first**: Command-line interface, no external web dependencies
- **Offline**: No internet access required (uses local Ollama)

## Technology Stack

- Python 3.8+
- Ollama with `carstenuhlig/omnicoder-2-9b:latest` model

## Supposed Data Flow 

- Medical data is provided as JSON text file or image 
- if file is not *.json it considered as image file 
- image should be processed with Ollama model gamma4:latest converting image table to json 
- json file is processed with Ollama model cars1ten1uhlig/omnicoder-2-9b:latest to get conclusion 
- result should be output to stdout 

## Testing 

Use files blood.json and blood.jpg for testing 
