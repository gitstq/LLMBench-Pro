"""
Report Generator Module
Generates benchmark reports in various formats
"""

import json
import csv
import io
from typing import Dict, Any, List, Optional
from datetime import datetime
from pathlib import Path


class ReportGenerator:
    """
    Benchmark Report Generator
    
    Generates reports in JSON, CSV, Markdown, and HTML formats
    """
    
    def generate(
        self,
        results: Dict[str, Any],
        format: str = "json",
        output_path: Optional[str] = None,
    ) -> str:
        """
        Generate report in specified format
        
        Args:
            results: Benchmark results dictionary
            format: Output format (json, csv, markdown, html)
            output_path: Optional path to save report
            
        Returns:
            Report content or path
        """
        if format == "json":
            content = self._generate_json(results)
        elif format == "csv":
            content = self._generate_csv(results)
        elif format == "markdown":
            content = self._generate_markdown(results)
        elif format == "html":
            content = self._generate_html(results)
        else:
            raise ValueError(f"Unsupported format: {format}")
        
        if output_path:
            Path(output_path).write_text(content, encoding="utf-8")
            return output_path
        
        return content
    
    def compare(
        self,
        results_list: List[Dict[str, Any]],
        format: str = "table",
    ) -> str:
        """
        Generate comparison report for multiple models
        
        Args:
            results_list: List of benchmark results
            format: Output format (table, json, csv)
            
        Returns:
            Comparison report
        """
        if format == "json":
            return self._compare_json(results_list)
        elif format == "csv":
            return self._compare_csv(results_list)
        else:
            return self._compare_table(results_list)
    
    def _generate_json(self, results: Dict[str, Any]) -> str:
        """Generate JSON report"""
        return json.dumps(results, indent=2, ensure_ascii=False)
    
    def _generate_csv(self, results: Dict[str, Any]) -> str:
        """Generate CSV report"""
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Header
        writer.writerow([
            "Model Name", "Prompt", "Tokens Generated",
            "Time to First Token (ms)", "Total Time (ms)", 
            "Tokens/Second", "Prompt Tokens"
        ])
        
        # Data rows
        for run in results.get("results", []):
            writer.writerow([
                results.get("model_name", ""),
                run.get("prompt", "")[:50],
                run.get("tokens_generated", 0),
                round(run.get("time_to_first_token_ms", 0), 2),
                round(run.get("total_time_ms", 0), 2),
                round(run.get("tokens_per_second", 0), 2),
                run.get("prompt_tokens", 0),
            ])
        
        # Summary
        summary = results.get("summary", {})
        if summary:
            writer.writerow([])
            writer.writerow(["Summary Statistics"])
            writer.writerow(["Metric", "Mean", "Median", "Std", "Min", "Max"])
            
            for metric in ["time_to_first_token_ms", "tokens_per_second", "total_time_ms"]:
                stats = summary.get(metric, {})
                writer.writerow([
                    metric,
                    round(stats.get("mean", 0), 2),
                    round(stats.get("median", 0), 2),
                    round(stats.get("std", 0), 2),
                    round(stats.get("min", 0), 2),
                    round(stats.get("max", 0), 2),
                ])
        
        return output.getvalue()
    
    def _generate_markdown(self, results: Dict[str, Any]) -> str:
        """Generate Markdown report"""
        lines = []
        
        # Title
        lines.append("# 🚀 LLMBench-Pro Benchmark Report")
        lines.append("")
        
        # Model info
        lines.append("## 📊 Model Information")
        lines.append("")
        lines.append(f"- **Model**: {results.get('model_name', 'Unknown')}")
        lines.append(f"- **Path**: {results.get('model_path', 'N/A')}")
        lines.append(f"- **Timestamp**: {results.get('timestamp', 'N/A')}")
        lines.append("")
        
        # Configuration
        config = results.get("config", {})
        lines.append("## ⚙️ Benchmark Configuration")
        lines.append("")
        lines.append(f"- **Warmup Runs**: {config.get('warmup_runs', 'N/A')}")
        lines.append(f"- **Test Runs**: {config.get('test_runs', 'N/A')}")
        lines.append(f"- **Max Tokens**: {config.get('max_tokens', 'N/A')}")
        lines.append(f"- **Number of Prompts**: {config.get('num_prompts', 'N/A')}")
        lines.append("")
        
        # Summary
        summary = results.get("summary", {})
        if summary:
            lines.append("## 📈 Performance Summary")
            lines.append("")
            lines.append("| Metric | Mean | Median | Std | Min | Max |")
            lines.append("|--------|------|--------|-----|-----|-----|")
            
            for metric, label in [
                ("time_to_first_token_ms", "Time to First Token (ms)"),
                ("tokens_per_second", "Tokens/Second"),
                ("total_time_ms", "Total Time (ms)"),
            ]:
                stats = summary.get(metric, {})
                lines.append(f"| {label} | {stats.get('mean', 0):.2f} | "
                           f"{stats.get('median', 0):.2f} | "
                           f"{stats.get('std', 0):.2f} | "
                           f"{stats.get('min', 0):.2f} | "
                           f"{stats.get('max', 0):.2f} |")
            lines.append("")
        
        # Detailed results
        lines.append("## 📝 Detailed Results")
        lines.append("")
        lines.append("| # | Tokens | TTFT (ms) | Total (ms) | TPS |")
        lines.append("|---|--------|-----------|------------|-----|")
        
        for i, run in enumerate(results.get("results", [])[:20], 1):  # Limit to 20
            lines.append(
                f"| {i} | {run.get('tokens_generated', 0)} | "
                f"{run.get('time_to_first_token_ms', 0):.1f} | "
                f"{run.get('total_time_ms', 0):.1f} | "
                f"{run.get('tokens_per_second', 0):.1f} |"
            )
        
        lines.append("")
        lines.append("---")
        lines.append("*Generated by LLMBench-Pro*")
        
        return "\n".join(lines)
    
    def _generate_html(self, results: Dict[str, Any]) -> str:
        """Generate HTML report"""
        summary = results.get("summary", {})
        
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LLMBench-Pro Report</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; 
               max-width: 1000px; margin: 0 auto; padding: 20px; background: #f5f5f5; }}
        .container {{ background: white; border-radius: 10px; padding: 30px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        h1 {{ color: #333; border-bottom: 3px solid #4CAF50; padding-bottom: 10px; }}
        h2 {{ color: #555; margin-top: 30px; }}
        .stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; }}
        .stat-card {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                      color: white; padding: 20px; border-radius: 10px; text-align: center; }}
        .stat-value {{ font-size: 2em; font-weight: bold; }}
        .stat-label {{ font-size: 0.9em; opacity: 0.9; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
        th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
        th {{ background: #4CAF50; color: white; }}
        tr:hover {{ background: #f5f5f5; }}
        .info {{ background: #e3f2fd; padding: 15px; border-radius: 5px; margin: 10px 0; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 LLMBench-Pro Benchmark Report</h1>
        
        <div class="info">
            <strong>Model:</strong> {results.get('model_name', 'Unknown')}<br>
            <strong>Timestamp:</strong> {results.get('timestamp', 'N/A')}
        </div>
        
        <h2>📈 Performance Summary</h2>
        <div class="stats">
            <div class="stat-card">
                <div class="stat-value">{summary.get('tokens_per_second', {}).get('mean', 0):.1f}</div>
                <div class="stat-label">Tokens/Second (avg)</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{summary.get('time_to_first_token_ms', {}).get('mean', 0):.0f}ms</div>
                <div class="stat-label">Time to First Token</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{summary.get('total_tokens', 0)}</div>
                <div class="stat-label">Total Tokens Generated</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{summary.get('total_runs', 0)}</div>
                <div class="stat-label">Benchmark Runs</div>
            </div>
        </div>
        
        <h2>📊 Detailed Statistics</h2>
        <table>
            <tr>
                <th>Metric</th>
                <th>Mean</th>
                <th>Median</th>
                <th>Std</th>
                <th>Min</th>
                <th>Max</th>
            </tr>
            <tr>
                <td>Tokens/Second</td>
                <td>{summary.get('tokens_per_second', {}).get('mean', 0):.2f}</td>
                <td>{summary.get('tokens_per_second', {}).get('median', 0):.2f}</td>
                <td>{summary.get('tokens_per_second', {}).get('std', 0):.2f}</td>
                <td>{summary.get('tokens_per_second', {}).get('min', 0):.2f}</td>
                <td>{summary.get('tokens_per_second', {}).get('max', 0):.2f}</td>
            </tr>
            <tr>
                <td>Time to First Token (ms)</td>
                <td>{summary.get('time_to_first_token_ms', {}).get('mean', 0):.2f}</td>
                <td>{summary.get('time_to_first_token_ms', {}).get('median', 0):.2f}</td>
                <td>{summary.get('time_to_first_token_ms', {}).get('std', 0):.2f}</td>
                <td>{summary.get('time_to_first_token_ms', {}).get('min', 0):.2f}</td>
                <td>{summary.get('time_to_first_token_ms', {}).get('max', 0):.2f}</td>
            </tr>
            <tr>
                <td>Total Time (ms)</td>
                <td>{summary.get('total_time_ms', {}).get('mean', 0):.2f}</td>
                <td>{summary.get('total_time_ms', {}).get('median', 0):.2f}</td>
                <td>{summary.get('total_time_ms', {}).get('std', 0):.2f}</td>
                <td>{summary.get('total_time_ms', {}).get('min', 0):.2f}</td>
                <td>{summary.get('total_time_ms', {}).get('max', 0):.2f}</td>
            </tr>
        </table>
        
        <p style="text-align: center; color: #666; margin-top: 40px;">
            Generated by <strong>LLMBench-Pro</strong> on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        </p>
    </div>
</body>
</html>"""
        
        return html
    
    def _compare_json(self, results_list: List[Dict[str, Any]]) -> str:
        """Generate JSON comparison"""
        comparison = {
            "comparison": [],
            "timestamp": datetime.now().isoformat(),
        }
        
        for results in results_list:
            summary = results.get("summary", {})
            comparison["comparison"].append({
                "model": results.get("model_name", "Unknown"),
                "tokens_per_second": summary.get("tokens_per_second", {}).get("mean", 0),
                "time_to_first_token_ms": summary.get("time_to_first_token_ms", {}).get("mean", 0),
                "total_time_ms": summary.get("total_time_ms", {}).get("mean", 0),
            })
        
        return json.dumps(comparison, indent=2, ensure_ascii=False)
    
    def _compare_csv(self, results_list: List[Dict[str, Any]]) -> str:
        """Generate CSV comparison"""
        output = io.StringIO()
        writer = csv.writer(output)
        
        writer.writerow(["Model", "Tokens/Second", "TTFT (ms)", "Total Time (ms)"])
        
        for results in results_list:
            summary = results.get("summary", {})
            writer.writerow([
                results.get("model_name", "Unknown"),
                round(summary.get("tokens_per_second", {}).get("mean", 0), 2),
                round(summary.get("time_to_first_token_ms", {}).get("mean", 0), 2),
                round(summary.get("total_time_ms", {}).get("mean", 0), 2),
            ])
        
        return output.getvalue()
    
    def _compare_table(self, results_list: List[Dict[str, Any]]) -> str:
        """Generate table comparison"""
        lines = []
        lines.append("\n" + "="*80)
        lines.append("📊 Model Comparison Report")
        lines.append("="*80)
        lines.append("")
        lines.append(f"{'Model':<30} {'Tokens/s':>12} {'TTFT (ms)':>12} {'Total (ms)':>12}")
        lines.append("-"*80)
        
        for results in results_list:
            summary = results.get("summary", {})
            name = results.get("model_name", "Unknown")[:28]
            tps = summary.get("tokens_per_second", {}).get("mean", 0)
            ttft = summary.get("time_to_first_token_ms", {}).get("mean", 0)
            total = summary.get("total_time_ms", {}).get("mean", 0)
            
            lines.append(f"{name:<30} {tps:>12.2f} {ttft:>12.2f} {total:>12.2f}")
        
        lines.append("-"*80)
        lines.append("")
        
        return "\n".join(lines)
