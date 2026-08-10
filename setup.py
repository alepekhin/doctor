from setuptools import setup, find_packages

with open("README.md") as f:
    long_description = f.read()

setup(
    name="doctor",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Doctor project",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/...",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    python_requires=">=3.8",
    install_requires=[],
    extras_require={
        "dev": ["pytest", "black", "ruff", "mypy"],
    },
    entry_points={
        "console_scripts": [
            "documentor=src.commands:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
