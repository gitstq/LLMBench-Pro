"""
Model Recommender Module
Recommends optimal models based on hardware configuration
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass


@dataclass
class ModelInfo:
    """Model information"""
    name: str
    size_gb: float
    parameters: str
    quantization: str
    use_cases: List[str]
    min_vram_gb: float
    min_ram_gb: float
    estimated_speed: str
    quality_score: int
    speed_score: int
    notes: str = ""


# Model database with realistic specifications
MODEL_DATABASE = [
    # 7B Models
    ModelInfo(
        name="Llama-3.2-3B-Instruct",
        size_gb=2.0,
        parameters="3B",
        quantization="Q4_K_M",
        use_cases=["general", "chat", "coding"],
        min_vram_gb=4,
        min_ram_gb=8,
        estimated_speed="Fast",
        quality_score=75,
        speed_score=90,
        notes="Great for quick tasks, excellent speed",
    ),
    ModelInfo(
        name="Llama-3.2-3B-Instruct-Q8",
        size_gb=3.5,
        parameters="3B",
        quantization="Q8_0",
        use_cases=["general", "chat", "coding"],
        min_vram_gb=6,
        min_ram_gb=12,
        estimated_speed="Fast",
        quality_score=82,
        speed_score=85,
        notes="Higher quality version of 3B model",
    ),
    ModelInfo(
        name="Mistral-7B-Instruct-v0.3",
        size_gb=4.1,
        parameters="7B",
        quantization="Q4_K_M",
        use_cases=["general", "chat", "coding", "reasoning"],
        min_vram_gb=6,
        min_ram_gb=12,
        estimated_speed="Medium",
        quality_score=85,
        speed_score=75,
        notes="Excellent all-around model, great balance",
    ),
    ModelInfo(
        name="Llama-3.1-8B-Instruct",
        size_gb=4.7,
        parameters="8B",
        quantization="Q4_K_M",
        use_cases=["general", "chat", "coding"],
        min_vram_gb=8,
        min_ram_gb=16,
        estimated_speed="Medium",
        quality_score=88,
        speed_score=70,
        notes="Latest Llama model, excellent quality",
    ),
    ModelInfo(
        name="Qwen2.5-7B-Instruct",
        size_gb=4.3,
        parameters="7B",
        quantization="Q4_K_M",
        use_cases=["general", "chat", "coding"],
        min_vram_gb=6,
        min_ram_gb=12,
        estimated_speed="Medium",
        quality_score=86,
        speed_score=75,
        notes="Strong multilingual support",
    ),
    # 14B Models
    ModelInfo(
        name="Qwen2.5-14B-Instruct",
        size_gb=8.5,
        parameters="14B",
        quantization="Q4_K_M",
        use_cases=["general", "chat", "coding", "reasoning"],
        min_vram_gb=12,
        min_ram_gb=24,
        estimated_speed="Medium-Slow",
        quality_score=90,
        speed_score=60,
        notes="Excellent reasoning and coding abilities",
    ),
    ModelInfo(
        name="Gemma-2-9B-Instruct",
        size_gb=5.5,
        parameters="9B",
        quantization="Q4_K_M",
        use_cases=["general", "chat", "coding"],
        min_vram_gb=10,
        min_ram_gb=18,
        estimated_speed="Medium",
        quality_score=87,
        speed_score=68,
        notes="Google's efficient model",
    ),
    # Large Models
    ModelInfo(
        name="Llama-3.1-70B-Instruct",
        size_gb=40,
        parameters="70B",
        quantization="Q4_K_M",
        use_cases=["general", "chat", "coding", "reasoning"],
        min_vram_gb=48,
        min_ram_gb=64,
        estimated_speed="Slow",
        quality_score=95,
        speed_score=25,
        notes="Top-tier quality, requires significant hardware",
    ),
    ModelInfo(
        name="Qwen2.5-32B-Instruct",
        size_gb=19,
        parameters="32B",
        quantization="Q4_K_M",
        use_cases=["general", "chat", "coding", "reasoning"],
        min_vram_gb=24,
        min_ram_gb=40,
        estimated_speed="Slow",
        quality_score=92,
        speed_score=40,
        notes="Excellent for complex tasks",
    ),
    # Specialized Models
    ModelInfo(
        name="CodeLlama-34B-Instruct",
        size_gb=20,
        parameters="34B",
        quantization="Q4_K_M",
        use_cases=["coding"],
        min_vram_gb=24,
        min_ram_gb=40,
        estimated_speed="Slow",
        quality_score=93,
        speed_score=38,
        notes="Best for code generation",
    ),
    ModelInfo(
        name="DeepSeek-Coder-33B-Instruct",
        size_gb=19,
        parameters="33B",
        quantization="Q4_K_M",
        use_cases=["coding"],
        min_vram_gb=24,
        min_ram_gb=40,
        estimated_speed="Slow",
        quality_score=94,
        speed_score=40,
        notes="Excellent coding model",
    ),
    # Small/Fast Models
    ModelInfo(
        name="Phi-3.5-mini-instruct",
        size_gb=2.3,
        parameters="3.8B",
        quantization="Q4_K_M",
        use_cases=["general", "chat"],
        min_vram_gb=4,
        min_ram_gb=8,
        estimated_speed="Very Fast",
        quality_score=78,
        speed_score=95,
        notes="Microsoft's efficient small model",
    ),
    ModelInfo(
        name="Gemma-2-2B-Instruct",
        size_gb=1.4,
        parameters="2B",
        quantization="Q4_K_M",
        use_cases=["general", "chat"],
        min_vram_gb=3,
        min_ram_gb=6,
        estimated_speed="Very Fast",
        quality_score=72,
        speed_score=98,
        notes="Lightweight and fast",
    ),
]


class ModelRecommender:
    """
    Model Recommendation Engine
    
    Recommends optimal models based on hardware configuration
    """
    
    def __init__(self):
        self.models = MODEL_DATABASE
        
    def recommend(
        self,
        hardware_info: Dict[str, Any],
        use_case: str = "general",
        prefer_speed: bool = False,
        prefer_quality: bool = False,
        top_n: int = 5,
    ) -> List[Dict[str, Any]]:
        """
        Recommend models based on hardware and preferences
        
        Args:
            hardware_info: Hardware information dictionary
            use_case: Primary use case (general, coding, chat, reasoning)
            prefer_speed: Prioritize inference speed
            prefer_quality: Prioritize output quality
            top_n: Number of recommendations to return
            
        Returns:
            List of recommended models with scores
        """
        # Extract hardware constraints
        recommendations_data = hardware_info.get("recommendations", {})
        gpus = hardware_info.get("gpu", [])
        memory = hardware_info.get("memory", {})
        
        # Determine available memory
        if gpus:
            max_memory = sum(
                gpu.get("vram_gb", 0) 
                for gpu in gpus 
                if isinstance(gpu.get("vram_gb"), (int, float))
            )
            use_gpu = True
        else:
            max_memory = memory.get("total_gb", 0) * 0.6  # Use 60% of RAM
            use_gpu = False
        
        # Filter and score models
        scored_models = []
        
        for model in self.models:
            # Check if model fits in memory
            min_memory = model.min_vram_gb if use_gpu else model.min_ram_gb
            
            if model.size_gb > max_memory * 1.1:  # 10% buffer
                continue
                
            # Check use case match
            use_case_match = use_case in model.use_cases or use_case == "general"
            
            # Calculate score
            score = self._calculate_score(
                model=model,
                max_memory=max_memory,
                use_case_match=use_case_match,
                prefer_speed=prefer_speed,
                prefer_quality=prefer_quality,
                use_gpu=use_gpu,
            )
            
            scored_models.append({
                "name": model.name,
                "size_gb": model.size_gb,
                "parameters": model.parameters,
                "quantization": model.quantization,
                "use_case": ", ".join(model.use_cases),
                "estimated_speed": model.estimated_speed,
                "score": score,
                "quality_score": model.quality_score,
                "speed_score": model.speed_score,
                "notes": model.notes,
                "fits_memory": model.size_gb <= max_memory,
            })
        
        # Sort by score
        scored_models.sort(key=lambda x: x["score"], reverse=True)
        
        return scored_models[:top_n]
    
    def _calculate_score(
        self,
        model: ModelInfo,
        max_memory: float,
        use_case_match: bool,
        prefer_speed: bool,
        prefer_quality: bool,
        use_gpu: bool,
    ) -> int:
        """Calculate recommendation score"""
        score = 0
        
        # Base quality and speed scores
        quality_weight = 0.5
        speed_weight = 0.3
        fit_weight = 0.2
        
        if prefer_quality:
            quality_weight = 0.7
            speed_weight = 0.1
            fit_weight = 0.2
        elif prefer_speed:
            quality_weight = 0.3
            speed_weight = 0.6
            fit_weight = 0.1
        
        # Quality score
        score += int(model.quality_score * quality_weight)
        
        # Speed score (higher is better)
        score += int(model.speed_score * speed_weight)
        
        # Memory fit score (how well it fits available memory)
        memory_ratio = model.size_gb / max_memory if max_memory > 0 else 1
        if memory_ratio < 0.5:
            fit_score = 100
        elif memory_ratio < 0.7:
            fit_score = 90
        elif memory_ratio < 0.85:
            fit_score = 80
        else:
            fit_score = 70
        score += int(fit_score * fit_weight)
        
        # Use case bonus
        if use_case_match:
            score += 10
        
        # GPU bonus
        if use_gpu and model.min_vram_gb <= max_memory:
            score += 5
        
        return min(score, 100)
    
    def get_model_info(self, model_name: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about a specific model"""
        for model in self.models:
            if model.name == model_name:
                return {
                    "name": model.name,
                    "size_gb": model.size_gb,
                    "parameters": model.parameters,
                    "quantization": model.quantization,
                    "use_cases": model.use_cases,
                    "min_vram_gb": model.min_vram_gb,
                    "min_ram_gb": model.min_ram_gb,
                    "estimated_speed": model.estimated_speed,
                    "quality_score": model.quality_score,
                    "speed_score": model.speed_score,
                    "notes": model.notes,
                }
        return None
    
    def list_all_models(self) -> List[str]:
        """List all available models"""
        return [model.name for model in self.models]
