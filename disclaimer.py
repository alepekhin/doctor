"""Medical disclaimer formatter module."""


def get_disclaimer() -> str:
    """Get the medical disclaimer text."""
    return "\n⚠️ Medical Disclaimer: This analysis is AI-generated. Consult a qualified medical professional for medical advice."


def format_result(analysis: str) -> str:
    """Format analysis result with disclaimer."""
    return f"Medical Analysis Result:\n{analysis}{get_disclaimer()}"


def is_disclaimer_present(text: str) -> bool:
    """Check if disclaimer is present in text."""
    return "Medical Disclaimer" in text
