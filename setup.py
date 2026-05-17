#!/usr/bin/env python3
"""
LLMBench-Pro Setup Script
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="llmbench-pro",
    version="1.0.0",
    author="SOLO-Agent",
    author_email="solo-agent@example.com",
    description="🚀 LLMBench-Pro - Lightweight Local LLM Benchmark & Intelligent Recommendation Engine",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gitstq/LLMBench-Pro",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Testing",
        "Topic :: System :: Benchmark",
    ],
    python_requires=">=3.8",
    install_requires=[
        # No external dependencies - uses only Python standard library
    ],
    extras_require={
        "llama-cpp": ["llama-cpp-python>=0.2.0"],
        "transformers": ["transformers>=4.30.0", "torch>=2.0.0"],
        "ctransformers": ["ctransformers>=0.2.0"],
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "isort>=5.0.0",
            "mypy>=1.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "llmbench-pro=llmbench_pro.core:main",
        ],
    },
    keywords="llm benchmark local-llm model-recommendation performance-testing",
    project_urls={
        "Bug Tracker": "https://github.com/gitstq/LLMBench-Pro/issues",
        "Documentation": "https://github.com/gitstq/LLMBench-Pro#readme",
        "Source Code": "https://github.com/gitstq/LLMBench-Pro",
    },
)
