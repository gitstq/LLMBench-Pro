<p align="center">
  <img src="https://img.shields.io/badge/version-1.0.0-blue.svg" alt="Version">
  <img src="https://img.shields.io/badge/python-3.8+-green.svg" alt="Python">
  <img src="https://img.shields.io/badge/license-MIT-orange.svg" alt="License">
  <img src="https://img.shields.io/badge/dependencies-0-brightgreen.svg" alt="Dependencies">
</p>

<p align="center">
  <a href="README.md">简体中文</a> | 
  <a href="README_EN.md">English</a> | 
  <a href="README_TW.md">繁體中文</a>
</p>

<h1 align="center">🚀 LLMBench-Pro</h1>

<p align="center">
  <strong>Lightweight Local LLM Benchmark & Intelligent Recommendation Engine</strong>
</p>

---

## 🎉 Introduction

**LLMBench-Pro** is a lightweight benchmark and intelligent recommendation engine designed specifically for local Large Language Models (LLMs). It automatically detects your hardware configuration, runs comprehensive performance tests, and recommends the most suitable models based on your system specifications.

### 🎯 Problems We Solve

- ❓ **Which models can my computer run?** → Automatic hardware detection & smart recommendations
- ❓ **How fast will the model be after loading?** → Comprehensive benchmark testing with quantified metrics
- ❓ **Which quantization should I choose?** → Automatic recommendations based on VRAM/RAM
- ❓ **How to compare multiple models?** → One-click comparison with visual reports

### ✨ Key Differentiators

| Feature | LLMBench-Pro | Other Tools |
|---------|--------------|-------------|
| Zero Dependencies | ✅ Python standard library only | ❌ Requires many dependencies |
| Hardware Detection | ✅ CPU/GPU/Memory analysis | ⚠️ Partial support |
| Smart Recommendations | ✅ Hardware-based personalized suggestions | ❌ None |
| Multi-dimensional Testing | ✅ TTFT/TPS/Throughput | ⚠️ Single metric |
| Visual Reports | ✅ JSON/CSV/Markdown/HTML | ⚠️ Limited formats |
| TUI Interface | ✅ Terminal graphical interface | ❌ CLI only |

---

## ✨ Core Features

### 🔍 Smart Hardware Detection
- **CPU Analysis**: Model, cores, threads, frequency
- **GPU Detection**: Full support for NVIDIA/AMD/Apple Silicon
- **Memory Statistics**: Total, available, usage percentage
- **Storage Assessment**: Disk space detection

### 📊 Multi-dimensional Benchmarking
- **Time to First Token (TTFT)**: Measures response speed
- **Tokens Per Second (TPS)**: Measures generation speed
- **Throughput Analysis**: Comprehensive performance evaluation
- **Stability Testing**: Multi-run statistical analysis

### 🎯 Intelligent Model Recommendations
- **Hardware Matching**: Best model recommendations based on VRAM/RAM
- **Scenario Matching**: Supports general/coding/chat/reasoning scenarios
- **Quantization Suggestions**: Automatic best quantization recommendations
- **Score Ranking**: Combined quality and speed scoring

### 📈 Visual Reports
- **JSON Format**: Structured data for programmatic processing
- **CSV Format**: Tabular data, Excel compatible
- **Markdown Format**: Documentation friendly, GitHub display
- **HTML Format**: Beautiful reports, shareable

### 🖥️ TUI Interactive Interface
- **Terminal Graphics**: No GUI needed, operate from terminal
- **Bilingual Support**: Chinese/English interface
- **Real-time Progress**: Visual test progress display

---

## 🚀 Quick Start

### 📋 Requirements

- Python 3.8 or higher
- No external dependencies required!

### 📦 Installation

```bash
# Method 1: Install from source
git clone https://github.com/gitstq/LLMBench-Pro.git
cd LLMBench-Pro
pip install -e .

# Method 2: Run directly
git clone https://github.com/gitstq/LLMBench-Pro.git
cd LLMBench-Pro
python -m llmbench_pro
```

### 🎮 Basic Usage

```bash
# Detect hardware configuration
llmbench-pro detect

# Get model recommendations
llmbench-pro recommend

# Run benchmark (simulation mode)
llmbench-pro benchmark -m simulated -n test-model

# Launch TUI interface
llmbench-pro tui
```

---

## 📖 Detailed Usage Guide

### 🔍 Hardware Detection

```bash
# Basic detection
llmbench-pro detect

# JSON format output
llmbench-pro detect --json
```

**Sample Output:**
```
============================================================
🖥️  Hardware Detection Report
============================================================

📌 CPU
   Model: AMD Ryzen 9 5950X 16-Core Processor
   Cores: 16 physical, 32 threads
   Frequency: 3400 MHz

📌 Memory
   Total: 64.0 GB
   Available: 48.5 GB

📌 GPU (1 detected)
   [0] NVIDIA GeForce RTX 4090
       VRAM: 24.0 GB
       Driver: 535.104.05

💡 Recommendations
   Max Model Size: ~19 GB
   Suggested Quantization: Q8_0 or FP16
============================================================
```

### 🎯 Model Recommendations

```bash
# Basic recommendations
llmbench-pro recommend

# Specify use case
llmbench-pro recommend --use-case coding

# Prioritize speed
llmbench-pro recommend --speed

# Prioritize quality
llmbench-pro recommend --quality

# JSON format output
llmbench-pro recommend --json
```

**Use Case Options:**
- `general`: General purpose (default)
- `coding`: Code generation
- `chat`: Conversational chat
- `reasoning`: Logical reasoning

### 📊 Benchmark Testing

```bash
# Basic test
llmbench-pro benchmark -m /path/to/model.gguf

# Specify model name
llmbench-pro benchmark -m ./model.gguf -n "Llama-3-8B"

# Custom test parameters
llmbench-pro benchmark -m ./model.gguf --warmup 5 --runs 20 --max-tokens 512

# Save report
llmbench-pro benchmark -m ./model.gguf -o report.json -f json
```

**Parameter Reference:**
| Parameter | Description | Default |
|-----------|-------------|---------|
| `-m, --model` | Model path or name | Required |
| `-n, --name` | Model name (for report) | Auto-detect |
| `--warmup` | Number of warmup runs | 3 |
| `--runs` | Test runs per prompt | 10 |
| `--max-tokens` | Maximum tokens to generate | 256 |
| `-o, --output` | Report output path | None |
| `-f, --format` | Report format | json |

### 📈 Results Comparison

```bash
# Compare multiple test results
llmbench-pro compare -r result1.json result2.json result3.json

# Specify output format
llmbench-pro compare -r *.json -f csv
```

### 🖥️ TUI Interface

```bash
# Launch interactive interface
llmbench-pro tui
```

TUI Interface Features:
1. 🔍 Hardware Detection
2. 🎯 Model Recommendations
3. 📊 Run Benchmark
4. 📈 View Results
5. ⚙️ Settings

---

## 💡 Design Philosophy & Roadmap

### 🏗️ Technical Architecture

```
LLMBench-Pro
├── core.py          # Core entry point, CLI command handling
├── hardware.py      # Hardware detection module
├── benchmark.py     # Benchmark engine
├── recommender.py   # Model recommendation engine
├── report.py        # Report generator
└── tui.py           # Terminal interactive interface
```

### 🎨 Design Principles

1. **Zero Dependencies First**: Only use Python standard library to lower installation barriers
2. **Modular Design**: Independent modules, easy to extend and maintain
3. **Cross-platform Compatibility**: Support Windows/macOS/Linux
4. **User Friendly**: Bilingual support, TUI interactive interface

### 📅 Roadmap

**v1.1.0 (Planned)**
- [ ] Support more inference backends (vLLM, TensorRT-LLM)
- [ ] Add model download functionality
- [ ] Support remote API testing

**v1.2.0 (Planned)**
- [ ] Web UI interface
- [ ] History management
- [ ] Performance trend analysis

**v2.0.0 (Future)**
- [ ] Distributed testing support
- [ ] Cloud report synchronization
- [ ] Community model library integration

---

## 📦 Packaging & Deployment

### Development Environment

```bash
# Clone repository
git clone https://github.com/gitstq/LLMBench-Pro.git
cd LLMBench-Pro

# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/ -v

# Code formatting
black llmbench_pro/
isort llmbench_pro/
```

### Build & Release

```bash
# Build package
python -m build

# Upload to PyPI
twine upload dist/*
```

---

## 🤝 Contributing

We welcome all forms of contributions!

### How to Contribute

1. **Fork** this repository
2. **Create branch**: `git checkout -b feature/your-feature`
3. **Commit changes**: `git commit -m 'feat: add new feature'`
4. **Push branch**: `git push origin feature/your-feature`
5. **Create PR**: Submit Pull Request

### Commit Convention

Use Angular commit convention:
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation update
- `refactor:` Code refactoring
- `test:` Test related
- `chore:` Build/tool related

---

## 📄 License

This project is licensed under the **MIT License**.

See [LICENSE](LICENSE) file for details.

---

<p align="center">
  Made with ❤️ by <a href="https://github.com/gitstq">SOLO-Agent</a>
</p>

<p align="center">
  If this project helps you, please give it a ⭐️ Star!
</p>
