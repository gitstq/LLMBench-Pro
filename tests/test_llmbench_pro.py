#!/usr/bin/env python3
"""
LLMBench-Pro Test Suite
"""

import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from llmbench_pro.hardware import HardwareDetector
from llmbench_pro.benchmark import BenchmarkRunner, SimulatedModel
from llmbench_pro.recommender import ModelRecommender
from llmbench_pro.report import ReportGenerator


class TestHardwareDetector(unittest.TestCase):
    """Test HardwareDetector class"""
    
    def setUp(self):
        self.detector = HardwareDetector()
    
    def test_detect_returns_dict(self):
        """Test that detect returns a dictionary"""
        result = self.detector.detect()
        self.assertIsInstance(result, dict)
    
    def test_detect_has_required_keys(self):
        """Test that detect returns required keys"""
        result = self.detector.detect()
        required_keys = ["system", "cpu", "memory", "gpu", "storage", "recommendations"]
        for key in required_keys:
            self.assertIn(key, result)
    
    def test_cpu_detection(self):
        """Test CPU detection"""
        cpu = self.detector._detect_cpu()
        self.assertIn("model", cpu)
        self.assertIn("cores", cpu)
        self.assertIn("threads", cpu)
    
    def test_memory_detection(self):
        """Test memory detection"""
        memory = self.detector._detect_memory()
        self.assertIn("total_gb", memory)
        self.assertIn("available_gb", memory)
        self.assertGreater(memory["total_gb"], 0)


class TestBenchmarkRunner(unittest.TestCase):
    """Test BenchmarkRunner class"""
    
    def setUp(self):
        self.runner = BenchmarkRunner()
    
    def test_default_prompts_exist(self):
        """Test that default prompts are defined"""
        self.assertGreater(len(BenchmarkRunner.DEFAULT_PROMPTS), 0)
    
    def test_simulated_model(self):
        """Test simulated model"""
        model = SimulatedModel("test-model")
        result = model.generate("Hello, world!", max_tokens=100)
        
        self.assertIn("tokens_generated", result)
        self.assertIn("time_to_first_token_ms", result)
        self.assertIn("total_time_ms", result)
        self.assertIn("tokens_per_second", result)
    
    def test_run_benchmark(self):
        """Test running benchmark with simulated model"""
        results = self.runner.run(
            model_path="simulated",
            model_name="test-model",
            warmup_runs=1,
            test_runs=2,
            max_tokens=64,
        )
        
        self.assertIn("model_name", results)
        self.assertIn("results", results)
        self.assertIn("summary", results)
        self.assertEqual(len(results["results"]), 10)  # 5 prompts * 2 runs


class TestModelRecommender(unittest.TestCase):
    """Test ModelRecommender class"""
    
    def setUp(self):
        self.recommender = ModelRecommender()
    
    def test_model_database_not_empty(self):
        """Test that model database is not empty"""
        self.assertGreater(len(self.recommender.models), 0)
    
    def test_recommend_returns_list(self):
        """Test that recommend returns a list"""
        hardware = {
            "gpu": [{"name": "RTX 3080", "vram_gb": 10, "type": "cuda"}],
            "memory": {"total_gb": 32},
            "recommendations": {"max_model_size_gb": 8}
        }
        recommendations = self.recommender.recommend(hardware)
        self.assertIsInstance(recommendations, list)
    
    def test_recommend_respects_top_n(self):
        """Test that recommend respects top_n parameter"""
        hardware = {
            "gpu": [{"name": "RTX 3080", "vram_gb": 10, "type": "cuda"}],
            "memory": {"total_gb": 32},
            "recommendations": {"max_model_size_gb": 8}
        }
        recommendations = self.recommender.recommend(hardware, top_n=3)
        self.assertLessEqual(len(recommendations), 3)
    
    def test_get_model_info(self):
        """Test getting model info"""
        model_names = self.recommender.list_all_models()
        self.assertGreater(len(model_names), 0)
        
        # Get info for first model
        info = self.recommender.get_model_info(model_names[0])
        self.assertIsNotNone(info)
        self.assertIn("name", info)


class TestReportGenerator(unittest.TestCase):
    """Test ReportGenerator class"""
    
    def setUp(self):
        self.generator = ReportGenerator()
        self.sample_results = {
            "model_name": "test-model",
            "model_path": "/path/to/model",
            "timestamp": "2024-01-01T00:00:00",
            "config": {
                "warmup_runs": 3,
                "test_runs": 10,
                "max_tokens": 256,
                "num_prompts": 5,
            },
            "results": [
                {
                    "prompt": "Test prompt",
                    "tokens_generated": 100,
                    "time_to_first_token_ms": 50.0,
                    "total_time_ms": 1000.0,
                    "tokens_per_second": 100.0,
                    "prompt_tokens": 10,
                }
            ],
            "summary": {
                "tokens_per_second": {"mean": 100.0, "median": 100.0, "std": 5.0, "min": 95.0, "max": 105.0},
                "time_to_first_token_ms": {"mean": 50.0, "median": 50.0, "std": 2.0, "min": 48.0, "max": 52.0},
                "total_time_ms": {"mean": 1000.0, "median": 1000.0, "std": 50.0, "min": 950.0, "max": 1050.0},
                "total_runs": 10,
                "total_tokens": 1000,
            },
        }
    
    def test_generate_json(self):
        """Test JSON report generation"""
        report = self.generator.generate(self.sample_results, format="json")
        self.assertIsInstance(report, str)
        self.assertIn("test-model", report)
    
    def test_generate_csv(self):
        """Test CSV report generation"""
        report = self.generator.generate(self.sample_results, format="csv")
        self.assertIsInstance(report, str)
        self.assertIn("Model Name", report)
    
    def test_generate_markdown(self):
        """Test Markdown report generation"""
        report = self.generator.generate(self.sample_results, format="markdown")
        self.assertIsInstance(report, str)
        self.assertIn("#", report)
        self.assertIn("test-model", report)
    
    def test_generate_html(self):
        """Test HTML report generation"""
        report = self.generator.generate(self.sample_results, format="html")
        self.assertIsInstance(report, str)
        self.assertIn("<!DOCTYPE html>", report)
        self.assertIn("test-model", report)
    
    def test_compare_table(self):
        """Test comparison table generation"""
        comparison = self.generator.compare([self.sample_results], format="table")
        self.assertIsInstance(comparison, str)
        self.assertIn("test-model", comparison)


if __name__ == "__main__":
    unittest.main(verbosity=2)
