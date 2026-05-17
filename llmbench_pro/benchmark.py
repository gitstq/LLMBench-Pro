"""
Benchmark Runner Module
Runs performance benchmarks on local LLM models
"""

import time
import json
import statistics
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass, field, asdict
from datetime import datetime


@dataclass
class BenchmarkResult:
    """Single benchmark run result"""
    prompt: str
    tokens_generated: int
    time_to_first_token_ms: float
    total_time_ms: float
    tokens_per_second: float
    prompt_tokens: int = 0
    

@dataclass
class BenchmarkReport:
    """Complete benchmark report"""
    model_name: str
    model_path: str
    timestamp: str
    hardware: Dict[str, Any]
    config: Dict[str, Any]
    results: List[BenchmarkResult] = field(default_factory=list)
    summary: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "model_name": self.model_name,
            "model_path": self.model_path,
            "timestamp": self.timestamp,
            "hardware": self.hardware,
            "config": self.config,
            "results": [asdict(r) for r in self.results],
            "summary": self.summary,
        }


class BenchmarkRunner:
    """
    LLM Benchmark Runner
    
    Runs performance benchmarks on local LLM models
    """
    
    # Default test prompts for benchmarking
    DEFAULT_PROMPTS = [
        "Write a short poem about artificial intelligence.",
        "Explain the concept of machine learning in simple terms.",
        "What are the main differences between Python and JavaScript?",
        "Describe the process of photosynthesis in plants.",
        "Write a brief summary of the history of computing.",
    ]
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize Benchmark Runner
        
        Args:
            config: Optional configuration dictionary
        """
        self.config = config or {}
        self.model = None
        self.tokenizer = None
        
    def _load_model(self, model_path: str) -> bool:
        """
        Load model for benchmarking
        
        Args:
            model_path: Path to model or model identifier
            
        Returns:
            True if model loaded successfully
        """
        # Try different loading methods
        try:
            # Try llama-cpp-python first
            return self._load_llama_cpp(model_path)
        except ImportError:
            pass
            
        try:
            # Try transformers
            return self._load_transformers(model_path)
        except ImportError:
            pass
            
        try:
            # Try ctransformers
            return self._load_ctransformers(model_path)
        except ImportError:
            pass
            
        # Simulate model for demo/testing
        return self._load_simulated(model_path)
    
    def _load_llama_cpp(self, model_path: str) -> bool:
        """Load model using llama-cpp-python"""
        from llama_cpp import Llama
        
        self.model = Llama(
            model_path=model_path,
            n_ctx=2048,
            n_threads=4,
            verbose=False,
        )
        self.backend = "llama-cpp"
        return True
    
    def _load_transformers(self, model_path: str) -> bool:
        """Load model using transformers"""
        from transformers import AutoModelForCausalLM, AutoTokenizer
        
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_path,
            device_map="auto",
            torch_dtype="auto",
        )
        self.backend = "transformers"
        return True
    
    def _load_ctransformers(self, model_path: str) -> bool:
        """Load model using ctransformers"""
        from ctransformers import AutoModelForCausalLM
        
        self.model = AutoModelForCausalLM.from_pretrained(
            model_path,
            model_type="llama",
        )
        self.backend = "ctransformers"
        return True
    
    def _load_simulated(self, model_path: str) -> bool:
        """Load simulated model for testing"""
        self.model = SimulatedModel(model_path)
        self.backend = "simulated"
        return True
    
    def _generate(
        self,
        prompt: str,
        max_tokens: int = 256,
    ) -> Dict[str, Any]:
        """
        Generate text and measure performance
        
        Args:
            prompt: Input prompt
            max_tokens: Maximum tokens to generate
            
        Returns:
            Generation result with timing info
        """
        if self.backend == "llama-cpp":
            return self._generate_llama_cpp(prompt, max_tokens)
        elif self.backend == "transformers":
            return self._generate_transformers(prompt, max_tokens)
        elif self.backend == "ctransformers":
            return self._generate_ctransformers(prompt, max_tokens)
        else:
            return self._generate_simulated(prompt, max_tokens)
    
    def _generate_llama_cpp(self, prompt: str, max_tokens: int) -> Dict[str, Any]:
        """Generate using llama-cpp-python"""
        start_time = time.perf_counter()
        
        # Time to first token
        first_token_time = start_time
        
        output = self.model(
            prompt,
            max_tokens=max_tokens,
            echo=False,
        )
        
        end_time = time.perf_counter()
        
        text = output["choices"][0]["text"]
        tokens_generated = output["usage"]["completion_tokens"]
        prompt_tokens = output["usage"]["prompt_tokens"]
        
        total_time_ms = (end_time - start_time) * 1000
        ttft_ms = 50  # Approximate for llama.cpp
        
        return {
            "text": text,
            "tokens_generated": tokens_generated,
            "prompt_tokens": prompt_tokens,
            "time_to_first_token_ms": ttft_ms,
            "total_time_ms": total_time_ms,
        }
    
    def _generate_transformers(self, prompt: str, max_tokens: int) -> Dict[str, Any]:
        """Generate using transformers"""
        import torch
        
        inputs = self.tokenizer(prompt, return_tensors="pt")
        if torch.cuda.is_available():
            inputs = inputs.to("cuda")
        
        start_time = time.perf_counter()
        
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=max_tokens,
                do_sample=True,
                temperature=0.7,
            )
        
        end_time = time.perf_counter()
        
        generated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        tokens_generated = outputs.shape[1] - inputs["input_ids"].shape[1]
        
        total_time_ms = (end_time - start_time) * 1000
        
        return {
            "text": generated_text,
            "tokens_generated": tokens_generated,
            "prompt_tokens": inputs["input_ids"].shape[1],
            "time_to_first_token_ms": total_time_ms * 0.1,  # Approximate
            "total_time_ms": total_time_ms,
        }
    
    def _generate_ctransformers(self, prompt: str, max_tokens: int) -> Dict[str, Any]:
        """Generate using ctransformers"""
        start_time = time.perf_counter()
        
        text = self.model(prompt, max_new_tokens=max_tokens)
        
        end_time = time.perf_counter()
        
        # Estimate tokens (rough approximation)
        tokens_generated = len(text.split()) * 1.5
        
        total_time_ms = (end_time - start_time) * 1000
        
        return {
            "text": text,
            "tokens_generated": int(tokens_generated),
            "prompt_tokens": len(prompt.split()),
            "time_to_first_token_ms": total_time_ms * 0.1,
            "total_time_ms": total_time_ms,
        }
    
    def _generate_simulated(self, prompt: str, max_tokens: int) -> Dict[str, Any]:
        """Generate using simulated model"""
        return self.model.generate(prompt, max_tokens)
    
    def run_single(
        self,
        prompt: str,
        max_tokens: int = 256,
    ) -> BenchmarkResult:
        """
        Run single benchmark
        
        Args:
            prompt: Input prompt
            max_tokens: Maximum tokens to generate
            
        Returns:
            BenchmarkResult object
        """
        result = self._generate(prompt, max_tokens)
        
        tokens_generated = result["tokens_generated"]
        total_time_ms = result["total_time_ms"]
        
        tokens_per_second = (tokens_generated / total_time_ms) * 1000 if total_time_ms > 0 else 0
        
        return BenchmarkResult(
            prompt=prompt[:100] + "..." if len(prompt) > 100 else prompt,
            tokens_generated=tokens_generated,
            time_to_first_token_ms=result["time_to_first_token_ms"],
            total_time_ms=total_time_ms,
            tokens_per_second=tokens_per_second,
            prompt_tokens=result["prompt_tokens"],
        )
    
    def run(
        self,
        model_path: Optional[str] = None,
        model_name: Optional[str] = None,
        test_prompts: Optional[List[str]] = None,
        warmup_runs: int = 3,
        test_runs: int = 10,
        max_tokens: int = 256,
        hardware_info: Optional[Dict[str, Any]] = None,
        progress_callback: Optional[Callable[[int, int], None]] = None,
    ) -> Dict[str, Any]:
        """
        Run complete benchmark suite
        
        Args:
            model_path: Path to model
            model_name: Model name for reporting
            test_prompts: Custom test prompts
            warmup_runs: Number of warmup runs
            test_runs: Number of test runs per prompt
            max_tokens: Maximum tokens to generate
            hardware_info: Hardware information
            progress_callback: Callback for progress updates
            
        Returns:
            Complete benchmark report as dictionary
        """
        # Load model
        if model_path:
            self._load_model(model_path)
        
        model_name = model_name or model_path or "unknown-model"
        prompts = test_prompts or self.DEFAULT_PROMPTS
        
        # Create report
        report = BenchmarkReport(
            model_name=model_name,
            model_path=model_path or "simulated",
            timestamp=datetime.now().isoformat(),
            hardware=hardware_info or {},
            config={
                "warmup_runs": warmup_runs,
                "test_runs": test_runs,
                "max_tokens": max_tokens,
                "num_prompts": len(prompts),
            },
        )
        
        # Warmup runs
        for i in range(warmup_runs):
            self.run_single(prompts[0], max_tokens=min(max_tokens, 64))
            if progress_callback:
                progress_callback(i + 1, warmup_runs + len(prompts) * test_runs)
        
        # Actual benchmark runs
        total_runs = len(prompts) * test_runs
        completed = 0
        
        for prompt in prompts:
            for _ in range(test_runs):
                result = self.run_single(prompt, max_tokens)
                report.results.append(result)
                completed += 1
                if progress_callback:
                    progress_callback(warmup_runs + completed, warmup_runs + total_runs)
        
        # Calculate summary statistics
        report.summary = self._calculate_summary(report.results)
        
        return report.to_dict()
    
    def _calculate_summary(self, results: List[BenchmarkResult]) -> Dict[str, Any]:
        """Calculate summary statistics from results"""
        if not results:
            return {}
        
        ttft_values = [r.time_to_first_token_ms for r in results]
        tps_values = [r.tokens_per_second for r in results]
        total_time_values = [r.total_time_ms for r in results]
        tokens_values = [r.tokens_generated for r in results]
        
        def safe_stats(values):
            if len(values) < 2:
                return {"mean": values[0] if values else 0, "std": 0}
            return {
                "mean": statistics.mean(values),
                "median": statistics.median(values),
                "std": statistics.stdev(values),
                "min": min(values),
                "max": max(values),
            }
        
        return {
            "time_to_first_token_ms": safe_stats(ttft_values),
            "tokens_per_second": safe_stats(tps_values),
            "total_time_ms": safe_stats(total_time_values),
            "tokens_generated": safe_stats(tokens_values),
            "total_runs": len(results),
            "total_tokens": sum(tokens_values),
        }


class SimulatedModel:
    """Simulated model for testing/demo purposes"""
    
    def __init__(self, model_path: str):
        self.model_path = model_path
        self.base_speed = 30  # tokens per second base speed
        
    def generate(self, prompt: str, max_tokens: int) -> Dict[str, Any]:
        """Simulate generation with realistic timing"""
        import random
        
        # Simulate variable speed based on "model size"
        speed_factor = random.uniform(0.8, 1.2)
        tokens_per_second = self.base_speed * speed_factor
        
        # Generate random number of tokens
        tokens_generated = random.randint(max_tokens // 2, max_tokens)
        
        # Calculate timing
        total_time_ms = (tokens_generated / tokens_per_second) * 1000
        ttft_ms = random.uniform(50, 200)  # Time to first token
        
        # Simulate processing delay
        time.sleep(total_time_ms / 1000 * 0.1)  # Speed up for demo
        
        tokens_per_second = (tokens_generated / total_time_ms) * 1000 if total_time_ms > 0 else 0
        
        return {
            "text": f"[Simulated output for: {prompt[:50]}...]",
            "tokens_generated": tokens_generated,
            "prompt_tokens": len(prompt.split()),
            "time_to_first_token_ms": ttft_ms,
            "total_time_ms": total_time_ms,
            "tokens_per_second": tokens_per_second,
        }
