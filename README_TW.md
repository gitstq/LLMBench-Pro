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
  <strong>輕量級本地LLM基準測試與智能推薦引擎</strong><br>
  <sub>Lightweight Local LLM Benchmark & Intelligent Recommendation Engine</sub>
</p>

---

## 🎉 專案介紹

**LLMBench-Pro** 是一款專為本地大型語言模型（LLM）設計的輕量級基準測試與智能推薦引擎。它能夠自動檢測您的硬體配置，運行全面的效能測試，並基於您的系統規格推薦最適合的模型。

### 🎯 解決的痛點

- ❓ **不知道我的電腦能跑哪些模型？** → 自動檢測硬體，智能推薦
- ❓ **模型載入後速度如何？** → 全面基準測試，量化效能指標
- ❓ **如何選擇最佳量化方案？** → 基於顯存/記憶體自動推薦
- ❓ **多個模型如何對比？** → 一鍵對比，生成視覺化報告

### ✨ 自研差異化亮點

| 特性 | LLMBench-Pro | 其他工具 |
|------|--------------|----------|
| 零依賴安裝 | ✅ 僅需Python標準庫 | ❌ 需要安裝大量依賴 |
| 硬體自動檢測 | ✅ CPU/GPU/記憶體全面分析 | ⚠️ 部分支援 |
| 智能模型推薦 | ✅ 基於硬體的個性化推薦 | ❌ 無 |
| 多維度測試 | ✅ TTFT/TPS/吞吐量 | ⚠️ 單一指標 |
| 視覺化報告 | ✅ JSON/CSV/Markdown/HTML | ⚠️ 格式有限 |
| TUI互動介面 | ✅ 終端圖形化操作 | ❌ 僅命令列 |

---

## ✨ 核心特性

### 🔍 硬體智能檢測
- **CPU分析**：型號、核心數、執行緒數、頻率
- **GPU檢測**：NVIDIA/AMD/Apple Silicon全支援
- **記憶體統計**：總量、可用量、使用率
- **儲存評估**：磁碟空間檢測

### 📊 多維度基準測試
- **首Token延遲（TTFT）**：衡量響應速度
- **每秒Token數（TPS）**：衡量生成速度
- **吞吐量分析**：綜合效能評估
- **穩定性測試**：多次運行統計分析

### 🎯 智能模型推薦
- **硬體適配**：基於顯存/記憶體推薦最佳模型
- **場景匹配**：支援通用/程式設計/對話/推理場景
- **量化建議**：自動推薦最佳量化方案
- **評分排序**：綜合品質與速度評分

### 📈 視覺化報告
- **JSON格式**：結構化資料，便於程式處理
- **CSV格式**：表格資料，Excel相容
- **Markdown格式**：文檔友好，GitHub展示
- **HTML格式**：美觀報告，支援分享

### 🖥️ TUI互動介面
- **終端圖形化**：無需GUI，終端即可操作
- **中英雙語**：介面支援中英文切換
- **即時進度**：測試進度視覺化顯示

---

## 🚀 快速開始

### 📋 環境要求

- Python 3.8 或更高版本
- 無需任何外部依賴！

### 📦 安裝

```bash
# 方式一：從原始碼安裝
git clone https://github.com/gitstq/LLMBench-Pro.git
cd LLMBench-Pro
pip install -e .

# 方式二：直接運行
git clone https://github.com/gitstq/LLMBench-Pro.git
cd LLMBench-Pro
python -m llmbench_pro
```

### 🎮 基本使用

```bash
# 檢測硬體配置
llmbench-pro detect

# 獲取模型推薦
llmbench-pro recommend

# 運行基準測試（模擬模式）
llmbench-pro benchmark -m simulated -n test-model

# 啟動TUI介面
llmbench-pro tui
```

---

## 📖 詳細使用指南

### 🔍 硬體檢測

```bash
# 基本檢測
llmbench-pro detect

# JSON格式輸出
llmbench-pro detect --json
```

**輸出範例：**
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

### 🎯 模型推薦

```bash
# 基本推薦
llmbench-pro recommend

# 指定使用場景
llmbench-pro recommend --use-case coding

# 優先速度
llmbench-pro recommend --speed

# 優先品質
llmbench-pro recommend --quality

# JSON格式輸出
llmbench-pro recommend --json
```

**使用場景選項：**
- `general`：通用場景（預設）
- `coding`：程式碼生成
- `chat`：對話聊天
- `reasoning`：邏輯推理

### 📊 基準測試

```bash
# 基本測試
llmbench-pro benchmark -m /path/to/model.gguf

# 指定模型名稱
llmbench-pro benchmark -m ./model.gguf -n "Llama-3-8B"

# 自訂測試參數
llmbench-pro benchmark -m ./model.gguf --warmup 5 --runs 20 --max-tokens 512

# 儲存報告
llmbench-pro benchmark -m ./model.gguf -o report.json -f json
```

**參數說明：**
| 參數 | 說明 | 預設值 |
|------|------|--------|
| `-m, --model` | 模型路徑或名稱 | 必填 |
| `-n, --name` | 模型名稱（用於報告） | 自動檢測 |
| `--warmup` | 預熱次數 | 3 |
| `--runs` | 每個提示詞測試次數 | 10 |
| `--max-tokens` | 最大生成Token數 | 256 |
| `-o, --output` | 報告輸出路徑 | 無 |
| `-f, --format` | 報告格式 | json |

### 📈 結果對比

```bash
# 對比多個測試結果
llmbench-pro compare -r result1.json result2.json result3.json

# 指定輸出格式
llmbench-pro compare -r *.json -f csv
```

### 🖥️ TUI介面

```bash
# 啟動互動介面
llmbench-pro tui
```

TUI介面提供：
1. 🔍 硬體檢測
2. 🎯 模型推薦
3. 📊 運行基準測試
4. 📈 查看結果
5. ⚙️ 設定

---

## 💡 設計思路與迭代規劃

### 🏗️ 技術架構

```
LLMBench-Pro
├── core.py          # 核心入口，CLI命令處理
├── hardware.py      # 硬體檢測模組
├── benchmark.py     # 基準測試引擎
├── recommender.py   # 模型推薦引擎
├── report.py        # 報告生成器
└── tui.py           # 終端互動介面
```

### 🎨 設計理念

1. **零依賴優先**：僅使用Python標準庫，降低安裝門檻
2. **模組化設計**：各模組獨立，易於擴展和維護
3. **跨平台相容**：支援Windows/macOS/Linux
4. **使用者友善**：中英雙語支援，TUI互動介面

### 📅 迭代規劃

**v1.1.0（計劃中）**
- [ ] 支援更多推理後端（vLLM、TensorRT-LLM）
- [ ] 添加模型下載功能
- [ ] 支援遠端API測試

**v1.2.0（計劃中）**
- [ ] Web UI介面
- [ ] 歷史記錄管理
- [ ] 效能趨勢分析

**v2.0.0（遠期）**
- [ ] 分散式測試支援
- [ ] 雲端報告同步
- [ ] 社群模型庫整合

---

## 📦 打包與部署指南

### 開發環境

```bash
# 複製儲存庫
git clone https://github.com/gitstq/LLMBench-Pro.git
cd LLMBench-Pro

# 安裝開發依賴
pip install -e ".[dev]"

# 運行測試
pytest tests/ -v

# 程式碼格式化
black llmbench_pro/
isort llmbench_pro/
```

### 建置發布

```bash
# 建置套件
python -m build

# 上傳到PyPI
twine upload dist/*
```

---

## 🤝 貢獻指南

我們歡迎所有形式的貢獻！

### 如何貢獻

1. **Fork** 本儲存庫
2. **建立分支**：`git checkout -b feature/your-feature`
3. **提交變更**：`git commit -m 'feat: 添加新功能'`
4. **推送分支**：`git push origin feature/your-feature`
5. **建立PR**：提交Pull Request

### 提交規範

使用Angular提交規範：
- `feat:` 新功能
- `fix:` 修復問題
- `docs:` 文檔更新
- `refactor:` 程式碼重構
- `test:` 測試相關
- `chore:` 建置/工具相關

---

## 📄 開源協議

本專案採用 **MIT License** 開源協議。

詳見 [LICENSE](LICENSE) 文件。

---

<p align="center">
  Made with ❤️ by <a href="https://github.com/gitstq">SOLO-Agent</a>
</p>

<p align="center">
  如果這個專案對您有幫助，請給一個 ⭐️ Star！
</p>
