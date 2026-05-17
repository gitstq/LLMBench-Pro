"""
LLMBench-Pro Core Module
Main entry point for the benchmark engine
"""

import argparse
import sys
import json
from typing import Optional, List, Dict, Any
from pathlib import Path

from .hardware import HardwareDetector
from .benchmark import BenchmarkRunner
from .recommender import ModelRecommender
from .report import ReportGenerator
from .tui import TUIDashboard


class LLMBenchPro:
    """
    LLMBench-Pro Main Class
    
    轻量级本地LLM基准测试与智能推荐引擎
    Lightweight Local LLM Benchmark & Intelligent Recommendation Engine
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize LLMBench-Pro
        
        Args:
            config_path: Optional path to configuration file
        """
        self.config = self._load_config(config_path) if config_path else {}
        self.hardware_detector = HardwareDetector()
        self.benchmark_runner = BenchmarkRunner(self.config)
        self.model_recommender = ModelRecommender()
        self.report_generator = ReportGenerator()
        
    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Load configuration from JSON file"""
        path = Path(config_path)
        if path.exists():
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def detect_hardware(self) -> Dict[str, Any]:
        """
        Detect system hardware configuration
        
        Returns:
            Dictionary containing hardware information
        """
        return self.hardware_detector.detect()
    
    def run_benchmark(
        self,
        model_path: Optional[str] = None,
        model_name: Optional[str] = None,
        test_prompts: Optional[List[str]] = None,
        warmup_runs: int = 3,
        test_runs: int = 10,
        max_tokens: int = 256,
    ) -> Dict[str, Any]:
        """
        Run benchmark on specified model
        
        Args:
            model_path: Path to model weights
            model_name: Name of the model for reporting
            test_prompts: Custom test prompts
            warmup_runs: Number of warmup runs
            test_runs: Number of test runs
            max_tokens: Maximum tokens to generate
            
        Returns:
            Benchmark results dictionary
        """
        hardware_info = self.detect_hardware()
        
        return self.benchmark_runner.run(
            model_path=model_path,
            model_name=model_name,
            test_prompts=test_prompts,
            warmup_runs=warmup_runs,
            test_runs=test_runs,
            max_tokens=max_tokens,
            hardware_info=hardware_info,
        )
    
    def recommend_models(
        self,
        hardware_info: Optional[Dict[str, Any]] = None,
        use_case: str = "general",
        prefer_speed: bool = False,
        prefer_quality: bool = False,
    ) -> List[Dict[str, Any]]:
        """
        Get model recommendations based on hardware
        
        Args:
            hardware_info: Hardware information (auto-detected if None)
            use_case: Use case (general, coding, chat, reasoning)
            prefer_speed: Prioritize speed over quality
            prefer_quality: Prioritize quality over speed
            
        Returns:
            List of recommended models
        """
        if hardware_info is None:
            hardware_info = self.detect_hardware()
            
        return self.model_recommender.recommend(
            hardware_info=hardware_info,
            use_case=use_case,
            prefer_speed=prefer_speed,
            prefer_quality=prefer_quality,
        )
    
    def generate_report(
        self,
        benchmark_results: Dict[str, Any],
        output_format: str = "json",
        output_path: Optional[str] = None,
    ) -> str:
        """
        Generate benchmark report
        
        Args:
            benchmark_results: Benchmark results dictionary
            output_format: Output format (json, csv, markdown, html)
            output_path: Path to save report
            
        Returns:
            Report content or path
        """
        return self.report_generator.generate(
            results=benchmark_results,
            format=output_format,
            output_path=output_path,
        )
    
    def compare_models(
        self,
        model_results: List[Dict[str, Any]],
        output_format: str = "table",
    ) -> str:
        """
        Compare multiple model benchmark results
        
        Args:
            model_results: List of benchmark results for different models
            output_format: Output format (table, json, csv)
            
        Returns:
            Comparison report
        """
        return self.report_generator.compare(
            results_list=model_results,
            format=output_format,
        )
    
    def launch_tui(self):
        """Launch Terminal User Interface dashboard"""
        dashboard = TUIDashboard(self)
        dashboard.run()


def main():
    """Command line entry point"""
    parser = argparse.ArgumentParser(
        prog="llmbench-pro",
        description="🚀 LLMBench-Pro - Lightweight Local LLM Benchmark & Intelligent Recommendation Engine",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  llmbench-pro detect              # Detect hardware configuration
  llmbench-pro recommend           # Get model recommendations
  llmbench-pro benchmark -m ./model --runs 10  # Run benchmark
  llmbench-pro tui                 # Launch TUI dashboard
        """,
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Detect command
    detect_parser = subparsers.add_parser(
        "detect", help="Detect system hardware configuration"
    )
    detect_parser.add_argument(
        "-j", "--json", action="store_true", help="Output as JSON"
    )
    
    # Recommend command
    recommend_parser = subparsers.add_parser(
        "recommend", help="Get model recommendations based on hardware"
    )
    recommend_parser.add_argument(
        "-u", "--use-case", default="general",
        choices=["general", "coding", "chat", "reasoning"],
        help="Use case for model recommendation"
    )
    recommend_parser.add_argument(
        "--speed", action="store_true", help="Prioritize inference speed"
    )
    recommend_parser.add_argument(
        "--quality", action="store_true", help="Prioritize output quality"
    )
    recommend_parser.add_argument(
        "-j", "--json", action="store_true", help="Output as JSON"
    )
    
    # Benchmark command
    bench_parser = subparsers.add_parser(
        "benchmark", help="Run benchmark on a model"
    )
    bench_parser.add_argument(
        "-m", "--model", required=True, help="Path to model or model name"
    )
    bench_parser.add_argument(
        "-n", "--name", help="Model name for reporting"
    )
    bench_parser.add_argument(
        "--warmup", type=int, default=3, help="Number of warmup runs"
    )
    bench_parser.add_argument(
        "--runs", type=int, default=10, help="Number of test runs"
    )
    bench_parser.add_argument(
        "--max-tokens", type=int, default=256, help="Maximum tokens to generate"
    )
    bench_parser.add_argument(
        "-o", "--output", help="Output file path for report"
    )
    bench_parser.add_argument(
        "-f", "--format", default="json", 
        choices=["json", "csv", "markdown"],
        help="Output format"
    )
    
    # Compare command
    compare_parser = subparsers.add_parser(
        "compare", help="Compare multiple benchmark results"
    )
    compare_parser.add_argument(
        "-r", "--results", nargs="+", required=True,
        help="Paths to benchmark result JSON files"
    )
    compare_parser.add_argument(
        "-f", "--format", default="table",
        choices=["table", "json", "csv"],
        help="Output format"
    )
    
    # TUI command
    subparsers.add_parser("tui", help="Launch TUI dashboard")
    
    # Version
    parser.add_argument("-v", "--version", action="version", version="%(prog)s 1.0.0")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(0)
    
    bench = LLMBenchPro()
    
    if args.command == "detect":
        hardware = bench.detect_hardware()
        if args.json:
            print(json.dumps(hardware, indent=2, ensure_ascii=False))
        else:
            print_hardware_info(hardware)
            
    elif args.command == "recommend":
        recommendations = bench.recommend_models(
            use_case=args.use_case,
            prefer_speed=args.speed,
            prefer_quality=args.quality,
        )
        if args.json:
            print(json.dumps(recommendations, indent=2, ensure_ascii=False))
        else:
            print_recommendations(recommendations)
            
    elif args.command == "benchmark":
        results = bench.run_benchmark(
            model_path=args.model,
            model_name=args.name,
            warmup_runs=args.warmup,
            test_runs=args.runs,
            max_tokens=args.max_tokens,
        )
        report = bench.generate_report(
            results,
            output_format=args.format,
            output_path=args.output,
        )
        if args.output:
            print(f"✅ Report saved to: {args.output}")
        else:
            print(report)
            
    elif args.command == "compare":
        results_list = []
        for path in args.results:
            with open(path, 'r', encoding='utf-8') as f:
                results_list.append(json.load(f))
        comparison = bench.compare_models(results_list, args.format)
        print(comparison)
        
    elif args.command == "tui":
        bench.launch_tui()


def print_hardware_info(hardware: Dict[str, Any]):
    """Print hardware information in formatted output"""
    print("\n" + "="*60)
    print("🖥️  Hardware Detection Report")
    print("="*60)
    
    # CPU
    cpu = hardware.get("cpu", {})
    print(f"\n📌 CPU")
    print(f"   Model: {cpu.get('model', 'Unknown')}")
    print(f"   Cores: {cpu.get('cores', 'Unknown')} physical, {cpu.get('threads', 'Unknown')} threads")
    print(f"   Frequency: {cpu.get('frequency', 'Unknown')} MHz")
    
    # Memory
    mem = hardware.get("memory", {})
    print(f"\n📌 Memory")
    print(f"   Total: {mem.get('total_gb', 'Unknown')} GB")
    print(f"   Available: {mem.get('available_gb', 'Unknown')} GB")
    
    # GPU
    gpus = hardware.get("gpu", [])
    if gpus:
        print(f"\n📌 GPU ({len(gpus)} detected)")
        for i, gpu in enumerate(gpus):
            print(f"   [{i}] {gpu.get('name', 'Unknown')}")
            print(f"       VRAM: {gpu.get('vram_gb', 'Unknown')} GB")
            print(f"       Driver: {gpu.get('driver', 'Unknown')}")
    else:
        print(f"\n📌 GPU: No CUDA-capable GPU detected")
    
    # Storage
    storage = hardware.get("storage", {})
    print(f"\n📌 Storage")
    print(f"   Total: {storage.get('total_gb', 'Unknown')} GB")
    print(f"   Free: {storage.get('free_gb', 'Unknown')} GB")
    
    # Recommendations
    rec = hardware.get("recommendations", {})
    print(f"\n💡 Recommendations")
    print(f"   Max Model Size: ~{rec.get('max_model_size_gb', 'Unknown')} GB")
    print(f"   Suggested Quantization: {rec.get('suggested_quantization', 'Unknown')}")
    
    print("\n" + "="*60)


def print_recommendations(recommendations: List[Dict[str, Any]]):
    """Print model recommendations in formatted output"""
    print("\n" + "="*60)
    print("🎯 Model Recommendations")
    print("="*60)
    
    for i, rec in enumerate(recommendations, 1):
        print(f"\n{i}. {rec.get('name', 'Unknown')}")
        print(f"   Size: {rec.get('size_gb', 'Unknown')} GB")
        print(f"   Quantization: {rec.get('quantization', 'Unknown')}")
        print(f"   Estimated Speed: {rec.get('estimated_speed', 'Unknown')}")
        print(f"   Use Case: {rec.get('use_case', 'Unknown')}")
        print(f"   Score: {rec.get('score', 'Unknown')}/100")
        if rec.get('notes'):
            print(f"   Notes: {rec.get('notes')}")
    
    print("\n" + "="*60)


if __name__ == "__main__":
    main()
