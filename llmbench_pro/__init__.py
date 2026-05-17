"""
LLMBench-Pro - Lightweight Local LLM Benchmark & Intelligent Recommendation Engine
轻量级本地LLM基准测试与智能推荐引擎

Author: SOLO-Agent
License: MIT
Version: 1.0.0
"""

__version__ = "1.0.0"
__author__ = "SOLO-Agent"
__description__ = "Lightweight Local LLM Benchmark & Intelligent Recommendation Engine"

from .core import LLMBenchPro
from .hardware import HardwareDetector
from .benchmark import BenchmarkRunner
from .recommender import ModelRecommender
from .report import ReportGenerator

__all__ = [
    "LLMBenchPro",
    "HardwareDetector", 
    "BenchmarkRunner",
    "ModelRecommender",
    "ReportGenerator",
]
