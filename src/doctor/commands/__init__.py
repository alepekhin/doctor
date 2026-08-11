"""Command module for main CLI entry point."""

from click import command


@command()
def main():
    """Main entry point."""
    print("Doctor - Main CLI")
