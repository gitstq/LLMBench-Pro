"""
Terminal User Interface Module
Interactive TUI Dashboard for LLMBench-Pro
"""

import sys
from typing import Dict, Any, Optional

# Simple TUI without external dependencies
class TUIDashboard:
    """
    Terminal User Interface Dashboard
    
    Provides an interactive terminal interface for LLMBench-Pro
    """
    
    def __init__(self, bench):
        """
        Initialize TUI Dashboard
        
        Args:
            bench: LLMBenchPro instance
        """
        self.bench = bench
        self.running = True
        
    def run(self):
        """Run the TUI dashboard"""
        self._clear_screen()
        self._show_header()
        
        while self.running:
            self._show_menu()
            choice = self._get_input("\n请选择操作 / Select option: ")
            self._handle_choice(choice)
    
    def _clear_screen(self):
        """Clear terminal screen"""
        print("\033[2J\033[H", end="")
    
    def _show_header(self):
        """Show application header"""
        print("""
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║   🚀 LLMBench-Pro v1.0.0                                        ║
║   轻量级本地LLM基准测试与智能推荐引擎                              ║
║   Lightweight Local LLM Benchmark & Intelligent Recommendation   ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
""")
    
    def _show_menu(self):
        """Show main menu"""
        print("""
┌──────────────────────────────────────────────────────────────────┐
│  主菜单 / Main Menu                                              │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  [1] 🔍 硬件检测 / Hardware Detection                            │
│  [2] 🎯 模型推荐 / Model Recommendations                         │
│  [3] 📊 运行基准测试 / Run Benchmark                             │
│  [4] 📈 查看结果 / View Results                                  │
│  [5] ⚙️  设置 / Settings                                         │
│  [0] 🚪 退出 / Exit                                              │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
""")
    
    def _get_input(self, prompt: str) -> str:
        """Get user input"""
        try:
            return input(prompt).strip()
        except (EOFError, KeyboardInterrupt):
            return "0"
    
    def _handle_choice(self, choice: str):
        """Handle menu choice"""
        if choice == "1":
            self._hardware_detection()
        elif choice == "2":
            self._model_recommendations()
        elif choice == "3":
            self._run_benchmark()
        elif choice == "4":
            self._view_results()
        elif choice == "5":
            self._settings()
        elif choice == "0":
            self._exit()
        else:
            print("\n❌ 无效选择 / Invalid choice")
            self._pause()
    
    def _pause(self):
        """Pause for user input"""
        self._get_input("\n按回车继续 / Press Enter to continue...")
    
    def _hardware_detection(self):
        """Show hardware detection results"""
        self._clear_screen()
        self._show_header()
        
        print("\n🔍 正在检测硬件 / Detecting hardware...\n")
        
        hardware = self.bench.detect_hardware()
        
        # System
        sys_info = hardware.get("system", {})
        print("┌─────────────────────────────────────────────────────────────┐")
        print("│  📌 系统信息 / System Information                           │")
        print("├─────────────────────────────────────────────────────────────┤")
        print(f"│  OS: {sys_info.get('os', 'Unknown'):<20} Arch: {sys_info.get('arch', 'Unknown'):<15} │")
        print("└─────────────────────────────────────────────────────────────┘")
        
        # CPU
        cpu = hardware.get("cpu", {})
        print("\n┌─────────────────────────────────────────────────────────────┐")
        print("│  💻 CPU 信息                                                │")
        print("├─────────────────────────────────────────────────────────────┤")
        print(f"│  Model: {cpu.get('model', 'Unknown')[:45]:<45} │")
        print(f"│  Cores: {cpu.get('cores', 0)} Physical, {cpu.get('threads', 0)} Threads{' '*20} │")
        print(f"│  Frequency: {cpu.get('frequency', 0)} MHz{' '*35} │")
        print("└─────────────────────────────────────────────────────────────┘")
        
        # Memory
        mem = hardware.get("memory", {})
        print("\n┌─────────────────────────────────────────────────────────────┐")
        print("│  🧠 内存信息 / Memory Information                           │")
        print("├─────────────────────────────────────────────────────────────┤")
        print(f"│  Total: {mem.get('total_gb', 0)} GB{' '*45} │")
        print(f"│  Available: {mem.get('available_gb', 0)} GB{' '*40} │")
        print(f"│  Used: {mem.get('used_percent', 0)}%{' '*48} │")
        print("└─────────────────────────────────────────────────────────────┘")
        
        # GPU
        gpus = hardware.get("gpu", [])
        print("\n┌─────────────────────────────────────────────────────────────┐")
        print("│  🎮 GPU 信息                                                │")
        print("├─────────────────────────────────────────────────────────────┤")
        if gpus:
            for i, gpu in enumerate(gpus):
                print(f"│  [{i}] {gpu.get('name', 'Unknown')[:40]:<40} │")
                print(f"│      VRAM: {gpu.get('vram_gb', 'Unknown')} GB{' '*35} │")
                print(f"│      Type: {gpu.get('type', 'Unknown')}{' '*35} │")
        else:
            print("│  No GPU detected / 未检测到GPU                              │")
        print("└─────────────────────────────────────────────────────────────┘")
        
        # Recommendations
        rec = hardware.get("recommendations", {})
        print("\n┌─────────────────────────────────────────────────────────────┐")
        print("│  💡 推荐配置 / Recommendations                               │")
        print("├─────────────────────────────────────────────────────────────┤")
        print(f"│  Max Model Size: ~{rec.get('max_model_size_gb', 0)} GB{' '*30} │")
        print(f"│  Suggested Quantization: {rec.get('suggested_quantization', 'N/A'):<20} │")
        print(f"│  Framework: {rec.get('suggested_framework', 'auto')}{' '*38} │")
        if rec.get("warnings"):
            for warning in rec.get("warnings", []):
                print(f"│  ⚠️  {warning[:50]:<50} │")
        print("└─────────────────────────────────────────────────────────────┘")
        
        self._pause()
    
    def _model_recommendations(self):
        """Show model recommendations"""
        self._clear_screen()
        self._show_header()
        
        print("\n🎯 模型推荐设置 / Model Recommendation Settings\n")
        
        use_case = self._get_input("用例类型 / Use case (general/coding/chat/reasoning) [general]: ") or "general"
        prefer_speed = self._get_input("优先速度 / Prefer speed? (y/N): ").lower() == "y"
        prefer_quality = self._get_input("优先质量 / Prefer quality? (y/N): ").lower() == "y"
        
        print("\n🔍 正在分析硬件并生成推荐 / Analyzing hardware and generating recommendations...\n")
        
        recommendations = self.bench.recommend_models(
            use_case=use_case,
            prefer_speed=prefer_speed,
            prefer_quality=prefer_quality,
        )
        
        print("┌─────────────────────────────────────────────────────────────┐")
        print("│  🏆 推荐模型 / Recommended Models                            │")
        print("├─────────────────────────────────────────────────────────────┤")
        
        for i, rec in enumerate(recommendations, 1):
            print(f"│                                                             │")
            print(f"│  {i}. {rec.get('name', 'Unknown')[:45]:<45} │")
            print(f"│     Size: {rec.get('size_gb', 0)} GB  |  Quant: {rec.get('quantization', 'N/A'):<10} │")
            print(f"│     Speed: {rec.get('estimated_speed', 'N/A'):<12} |  Score: {rec.get('score', 0)}/100 │")
            if rec.get("notes"):
                print(f"│     📝 {rec.get('notes', '')[:45]:<45} │")
        
        print("└─────────────────────────────────────────────────────────────┘")
        
        self._pause()
    
    def _run_benchmark(self):
        """Run benchmark"""
        self._clear_screen()
        self._show_header()
        
        print("\n📊 基准测试配置 / Benchmark Configuration\n")
        
        model_path = self._get_input("模型路径 / Model path (留空使用模拟模式): ")
        model_name = self._get_input("模型名称 / Model name: ") or "test-model"
        
        try:
            warmup = int(self._get_input("预热次数 / Warmup runs [3]: ") or "3")
            test_runs = int(self._get_input("测试次数 / Test runs [10]: ") or "10")
            max_tokens = int(self._get_input("最大Token数 / Max tokens [256]: ") or "256")
        except ValueError:
            warmup, test_runs, max_tokens = 3, 10, 256
        
        print(f"\n🚀 正在运行基准测试 / Running benchmark...\n")
        
        def progress_callback(current, total):
            bar_length = 40
            filled = int(bar_length * current / total)
            bar = "█" * filled + "░" * (bar_length - filled)
            print(f"\r  [{bar}] {current}/{total}", end="", flush=True)
        
        results = self.bench.run_benchmark(
            model_path=model_path or None,
            model_name=model_name,
            warmup_runs=warmup,
            test_runs=test_runs,
            max_tokens=max_tokens,
            progress_callback=progress_callback,
        )
        
        print("\n\n✅ 基准测试完成 / Benchmark completed!\n")
        
        # Show summary
        summary = results.get("summary", {})
        print("┌─────────────────────────────────────────────────────────────┐")
        print("│  📈 测试结果摘要 / Results Summary                           │")
        print("├─────────────────────────────────────────────────────────────┤")
        print(f"│  Tokens/Second: {summary.get('tokens_per_second', {}).get('mean', 0):.2f} (±{summary.get('tokens_per_second', {}).get('std', 0):.2f}){' '*15} │")
        print(f"│  Time to First Token: {summary.get('time_to_first_token_ms', {}).get('mean', 0):.2f} ms{' '*22} │")
        print(f"│  Total Runs: {summary.get('total_runs', 0)}{' '*40} │")
        print(f"│  Total Tokens: {summary.get('total_tokens', 0)}{' '*38} │")
        print("└─────────────────────────────────────────────────────────────┘")
        
        # Save results
        save = self._get_input("\n保存结果? / Save results? (y/N): ").lower() == "y"
        if save:
            filename = f"benchmark_{model_name}_{results.get('timestamp', 'unknown').replace(':', '-')}.json"
            self.bench.generate_report(results, "json", filename)
            print(f"✅ 结果已保存 / Results saved: {filename}")
        
        self._pause()
    
    def _view_results(self):
        """View saved results"""
        self._clear_screen()
        self._show_header()
        
        print("\n📈 查看结果 / View Results\n")
        print("  此功能需要先运行基准测试并保存结果")
        print("  Run benchmark first and save results to use this feature\n")
        
        self._pause()
    
    def _settings(self):
        """Settings menu"""
        self._clear_screen()
        self._show_header()
        
        print("\n⚙️  设置 / Settings\n")
        print("  配置文件位置: ~/.llmbench-pro/config.json")
        print("  Config file location: ~/.llmbench-pro/config.json\n")
        
        self._pause()
    
    def _exit(self):
        """Exit application"""
        self._clear_screen()
        print("\n👋 感谢使用 LLMBench-Pro! / Thanks for using LLMBench-Pro!\n")
        self.running = False
