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
  <strong>轻量级本地LLM基准测试与智能推荐引擎</strong><br>
  <sub>Lightweight Local LLM Benchmark & Intelligent Recommendation Engine</sub>
</p>

---

## 🎉 项目介绍

**LLMBench-Pro** 是一款专为本地大语言模型（LLM）设计的轻量级基准测试与智能推荐引擎。它能够自动检测您的硬件配置，运行全面的性能测试，并基于您的系统规格推荐最适合的模型。

### 🎯 解决的痛点

- ❓ **不知道我的电脑能跑哪些模型？** → 自动检测硬件，智能推荐
- ❓ **模型加载后速度如何？** → 全面基准测试，量化性能指标
- ❓ **如何选择最佳量化方案？** → 基于显存/内存自动推荐
- ❓ **多个模型如何对比？** → 一键对比，生成可视化报告

### ✨ 自研差异化亮点

| 特性 | LLMBench-Pro | 其他工具 |
|------|--------------|----------|
| 零依赖安装 | ✅ 仅需Python标准库 | ❌ 需要安装大量依赖 |
| 硬件自动检测 | ✅ CPU/GPU/内存全面分析 | ⚠️ 部分支持 |
| 智能模型推荐 | ✅ 基于硬件的个性化推荐 | ❌ 无 |
| 多维度测试 | ✅ TTFT/TPS/吞吐量 | ⚠️ 单一指标 |
| 可视化报告 | ✅ JSON/CSV/Markdown/HTML | ⚠️ 格式有限 |
| TUI交互界面 | ✅ 终端图形化操作 | ❌ 仅命令行 |

---

## ✨ 核心特性

### 🔍 硬件智能检测
- **CPU分析**：型号、核心数、线程数、频率
- **GPU检测**：NVIDIA/AMD/Apple Silicon全支持
- **内存统计**：总量、可用量、使用率
- **存储评估**：磁盘空间检测

### 📊 多维度基准测试
- **首Token延迟（TTFT）**：衡量响应速度
- **每秒Token数（TPS）**：衡量生成速度
- **吞吐量分析**：综合性能评估
- **稳定性测试**：多次运行统计分析

### 🎯 智能模型推荐
- **硬件适配**：基于显存/内存推荐最佳模型
- **场景匹配**：支持通用/编程/对话/推理场景
- **量化建议**：自动推荐最佳量化方案
- **评分排序**：综合质量与速度评分

### 📈 可视化报告
- **JSON格式**：结构化数据，便于程序处理
- **CSV格式**：表格数据，Excel兼容
- **Markdown格式**：文档友好，GitHub展示
- **HTML格式**：美观报告，支持分享

### 🖥️ TUI交互界面
- **终端图形化**：无需GUI，终端即可操作
- **中英双语**：界面支持中英文切换
- **实时进度**：测试进度可视化显示

---

## 🚀 快速开始

### 📋 环境要求

- Python 3.8 或更高版本
- 无需任何外部依赖！

### 📦 安装

```bash
# 方式一：从源码安装
git clone https://github.com/gitstq/LLMBench-Pro.git
cd LLMBench-Pro
pip install -e .

# 方式二：直接运行
git clone https://github.com/gitstq/LLMBench-Pro.git
cd LLMBench-Pro
python -m llmbench_pro
```

### 🎮 基本使用

```bash
# 检测硬件配置
llmbench-pro detect

# 获取模型推荐
llmbench-pro recommend

# 运行基准测试（模拟模式）
llmbench-pro benchmark -m simulated -n test-model

# 启动TUI界面
llmbench-pro tui
```

---

## 📖 详细使用指南

### 🔍 硬件检测

```bash
# 基本检测
llmbench-pro detect

# JSON格式输出
llmbench-pro detect --json
```

**输出示例：**
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

### 🎯 模型推荐

```bash
# 基本推荐
llmbench-pro recommend

# 指定使用场景
llmbench-pro recommend --use-case coding

# 优先速度
llmbench-pro recommend --speed

# 优先质量
llmbench-pro recommend --quality

# JSON格式输出
llmbench-pro recommend --json
```

**使用场景选项：**
- `general`：通用场景（默认）
- `coding`：代码生成
- `chat`：对话聊天
- `reasoning`：逻辑推理

### 📊 基准测试

```bash
# 基本测试
llmbench-pro benchmark -m /path/to/model.gguf

# 指定模型名称
llmbench-pro benchmark -m ./model.gguf -n "Llama-3-8B"

# 自定义测试参数
llmbench-pro benchmark -m ./model.gguf --warmup 5 --runs 20 --max-tokens 512

# 保存报告
llmbench-pro benchmark -m ./model.gguf -o report.json -f json
```

**参数说明：**
| 参数 | 说明 | 默认值 |
|------|------|--------|
| `-m, --model` | 模型路径或名称 | 必填 |
| `-n, --name` | 模型名称（用于报告） | 自动检测 |
| `--warmup` | 预热次数 | 3 |
| `--runs` | 每个提示词测试次数 | 10 |
| `--max-tokens` | 最大生成Token数 | 256 |
| `-o, --output` | 报告输出路径 | 无 |
| `-f, --format` | 报告格式 | json |

### 📈 结果对比

```bash
# 对比多个测试结果
llmbench-pro compare -r result1.json result2.json result3.json

# 指定输出格式
llmbench-pro compare -r *.json -f csv
```

### 🖥️ TUI界面

```bash
# 启动交互界面
llmbench-pro tui
```

TUI界面提供：
1. 🔍 硬件检测
2. 🎯 模型推荐
3. 📊 运行基准测试
4. 📈 查看结果
5. ⚙️ 设置

---

## 💡 设计思路与迭代规划

### 🏗️ 技术架构

```
LLMBench-Pro
├── core.py          # 核心入口，CLI命令处理
├── hardware.py      # 硬件检测模块
├── benchmark.py     # 基准测试引擎
├── recommender.py   # 模型推荐引擎
├── report.py        # 报告生成器
└── tui.py           # 终端交互界面
```

### 🎨 设计理念

1. **零依赖优先**：仅使用Python标准库，降低安装门槛
2. **模块化设计**：各模块独立，易于扩展和维护
3. **跨平台兼容**：支持Windows/macOS/Linux
4. **用户友好**：中英双语支持，TUI交互界面

### 📅 迭代规划

**v1.1.0（计划中）**
- [ ] 支持更多推理后端（vLLM、TensorRT-LLM）
- [ ] 添加模型下载功能
- [ ] 支持远程API测试

**v1.2.0（计划中）**
- [ ] Web UI界面
- [ ] 历史记录管理
- [ ] 性能趋势分析

**v2.0.0（远期）**
- [ ] 分布式测试支持
- [ ] 云端报告同步
- [ ] 社区模型库集成

---

## 📦 打包与部署指南

### 开发环境

```bash
# 克隆仓库
git clone https://github.com/gitstq/LLMBench-Pro.git
cd LLMBench-Pro

# 安装开发依赖
pip install -e ".[dev]"

# 运行测试
pytest tests/ -v

# 代码格式化
black llmbench_pro/
isort llmbench_pro/
```

### 构建发布

```bash
# 构建包
python -m build

# 上传到PyPI
twine upload dist/*
```

---

## 🤝 贡献指南

我们欢迎所有形式的贡献！

### 如何贡献

1. **Fork** 本仓库
2. **创建分支**：`git checkout -b feature/your-feature`
3. **提交更改**：`git commit -m 'feat: 添加新功能'`
4. **推送分支**：`git push origin feature/your-feature`
5. **创建PR**：提交Pull Request

### 提交规范

使用Angular提交规范：
- `feat:` 新功能
- `fix:` 修复问题
- `docs:` 文档更新
- `refactor:` 代码重构
- `test:` 测试相关
- `chore:` 构建/工具相关

---

## 📄 开源协议

本项目采用 **MIT License** 开源协议。

详见 [LICENSE](LICENSE) 文件。

---

<p align="center">
  Made with ❤️ by <a href="https://github.com/gitstq">SOLO-Agent</a>
</p>

<p align="center">
  如果这个项目对您有帮助，请给一个 ⭐️ Star！
</p>
