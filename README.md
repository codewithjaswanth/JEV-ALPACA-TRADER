# JEV-ALPACA-TRADER

[![Python 3.10+](https://img.shields.io/badge/python-3.10%20%7C%203.11-blue.svg)](https://www.python.org/)
[![Alpaca API](https://img.shields.io/badge/broker-Alpaca%20Markets-yellow.svg)](https://alpaca.markets/)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Deployment Status](https://img.shields.io/badge/deployment-verified%20workspace-success.svg)](#deployment--verification-status)

**JEV-ALPACA-TRADER** is an institutional-grade quantitative trading and algorithmic execution framework. Built upon the FinRL trading foundation and integrated with the Alpaca Paper/Live Trading API, it supports end-to-end automated pipelines: market data ingestion (FMP, Yahoo Finance, Finnhub, WRDS), machine learning feature engineering, predictive stock selection (LightGBM, XGBoost), risk-constrained portfolio optimization, and broker execution.

---

## 📑 Table of Contents
1. [Architecture Overview](#architecture-overview)
2. [Uploaded Files & Catalog](#uploaded-files--catalog)
3. [Missing Elements & Senior Dev Audit Notes](#missing-elements--senior-dev-audit-notes)
4. [Deployment & Verification Status](#deployment--verification-status)
5. [Quickstart & Setup Instructions](#quickstart--setup-instructions)
6. [Security & Risk Guidelines](#security--risk-guidelines)

---

## 🏛 Architecture Overview

The repository consists of two core directories:
- **`FinRL-Trading/`**: The complete production codebase containing trading engines, strategy definitions, configuration schemas, documentation, and the Streamlit web dashboard.
- **`verification_logs/`**: The deployment verification suite, containing automated audit scripts, encoding analyzers, executed test notebooks, amended dependency specs, and run logs proving build reproducibility.

```
JEV-ALPACA-TRADER/
├── .gitignore                      # Comprehensive Git exclusion rules
├── README.md                       # Repository catalog, architecture & audit notes
├── FinRL-Trading/                  # Core trading engine & application suite
│   ├── .dockerignore
│   ├── .env.example                # Canonical environment variable configuration template
│   ├── .gitattributes
│   ├── .gitignore
│   ├── Dockerfile                  # Container build specification
│   ├── docker-compose.yml          # Container orchestration (Trading service + Web UI)
│   ├── LICENSE                     # Apache 2.0 open-source license
│   ├── ML_STOCK_SELECTION.md       # Technical paper and documentation on ML selection models
│   ├── README.md                   # FinRL-Trading component documentation
│   ├── deploy.sh                   # Automated deployment shell script
│   ├── requirements.txt            # Base Python requirements
│   ├── setup.py                    # Package build & distribution setup
│   ├── data/                       # Static market and constituent datasets
│   ├── docs/                       # Architectural and technical documentation
│   ├── examples/                   # Jupyter notebook execution tutorials
│   ├── figs/                       # Strategy performance diagrams and workflow charts
│   └── src/                        # Modular source code
│       ├── main.py                 # System entrypoint (CLI & orchestration)
│       ├── backtest/               # Event-driven backtesting engine
│       ├── config/                 # Pydantic settings & environment validation
│       ├── data/                   # Ingestion, validation, caching & processing
│       ├── strategies/             # ML stock selection & rebalancing logic
│       ├── trading/                # Alpaca manager, execution engine, risk guardrails
│       └── utils/                  # Structured logging and error handling
└── verification_logs/              # Deployment audit trail & verification suite
    ├── FinRL_Full_selection_copy.ipynb
    ├── FinRL_Full_selection_executed.ipynb
    ├── requirements.amended.txt     # Verified production requirements (fixes PyPI typos)
    ├── step1_clean_install.log     # Raw pip install log capturing unamended failure
    ├── step1_amended_install.log   # Clean pip install log with verified requirements
    ├── step1_pip_freeze.log        # Environment dependency freeze
    ├── step2_smoke_check.log       # Import smoke-check validation output
    ├── step3_tutorial.log          # Tutorial execution trace
    ├── tutorial_execution.log      # Non-interactive notebook validation log
    ├── scripts/                    # Reproduction & audit automation scripts
    └── stage1c/                    # Cryptographic hashes and audit log outputs
```

---

## 📦 Uploaded Files & Catalog

### 1. Root Configuration
| File | Description |
| :--- | :--- |
| [`.gitignore`](file:///.gitignore) | Multi-tier exclusion rules for `.env`, virtualenvs, cache files, databases, and OS metadata. |
| [`README.md`](file:///README.md) | Central deployment documentation, file manifest, architecture overview, and audit report. |

### 2. `FinRL-Trading/` Core Codebase
| Subdirectory / File | Purpose |
| :--- | :--- |
| [`FinRL-Trading/src/main.py`](file:///FinRL-Trading/src/main.py) | Main application entrypoint supporting CLI commands for backtesting, live paper trading, and web UI. |
| [`FinRL-Trading/src/config/settings.py`](file:///FinRL-Trading/src/config/settings.py) | Strongly-typed Pydantic settings validator managing Alpaca keys, model parameters, database URLs, and risk thresholds. |
| [`FinRL-Trading/src/data/data_fetcher.py`](file:///FinRL-Trading/src/data/data_fetcher.py) | Market data fetcher querying Yahoo Finance, FMP, and Alpaca data APIs with rate-limit protection. |
| [`FinRL-Trading/src/data/data_processor.py`](file:///FinRL-Trading/src/data/data_processor.py) | Technical indicator computation, missing data imputation, and ML feature matrix generator. |
| [`FinRL-Trading/src/data/data_store.py`](file:///FinRL-Trading/src/data/data_store.py) | Local caching and persistent SQLite storage layer for historical prices and fundamentals. |
| [`FinRL-Trading/src/strategies/base_strategy.py`](file:///FinRL-Trading/src/strategies/base_strategy.py) | Abstract base class defining interface contracts for signal generation, rebalancing, and risk enforcement. |
| [`FinRL-Trading/src/strategies/ml_strategy.py`](file:///FinRL-Trading/src/strategies/ml_strategy.py) | Predictive ML stock selection strategy utilizing ensemble models (LightGBM/XGBoost). |
| [`FinRL-Trading/src/strategies/ml_bucket_selection.py`](file:///FinRL-Trading/src/strategies/ml_bucket_selection.py) | Quantile ranking, bucket classification, and portfolio weighting mechanisms. |
| [`FinRL-Trading/src/backtest/backtest_engine.py`](file:///FinRL-Trading/src/backtest/backtest_engine.py) | Historical simulator with realistic transaction costs, slippage, and performance metrics (Sharpe, Max DD, CAGR). |
| [`FinRL-Trading/src/trading/alpaca_manager.py`](file:///FinRL-Trading/src/trading/alpaca_manager.py) | Alpaca REST/WebSocket client wrapper for account checks, order submissions, and position tracking. |
| [`FinRL-Trading/src/trading/trade_executor.py`](file:///FinRL-Trading/src/trading/trade_executor.py) | Order generation, risk guardrails validation (order caps, sector exposure), and execution pipeline. |
| [`FinRL-Trading/src/trading/performance_analyzer.py`](file:///FinRL-Trading/src/trading/performance_analyzer.py) | Equity curve tracking, portfolio benchmark comparisons (vs. SPY/QQQ), and trade analytics. |
| [`FinRL-Trading/src/utils/logger.py`](file:///FinRL-Trading/src/utils/logger.py) | Rotating file and console logger with configurable formatting. |
| [`FinRL-Trading/data/finrl_trading.7z`](file:///FinRL-Trading/data/finrl_trading.7z) | Compressed baseline historical dataset archive. |
| [`FinRL-Trading/data/fundamental_data_full.csv`](file:///FinRL-Trading/data/fundamental_data_full.csv) | Historical fundamental metrics (P/E, ROE, Debt-to-Equity, Margins) for S&P 500 constituents. |
| [`FinRL-Trading/data/sp500_historical_constituents.csv`](file:///FinRL-Trading/data/sp500_historical_constituents.csv) | Historical point-in-time constituent list to eliminate survivorship bias during backtesting. |
| [`FinRL-Trading/examples/FinRL_Full_selection.ipynb`](file:///FinRL-Trading/examples/FinRL_Full_selection.ipynb) | End-to-end tutorial notebook demonstrating dataset loading, model training, backtesting, and Alpaca paper execution. |
| [`FinRL-Trading/.env.example`](file:///FinRL-Trading/.env.example) | Complete template for all configuration parameters, API keys, risk limits, and broker settings. |
| [`FinRL-Trading/Dockerfile`](file:///FinRL-Trading/Dockerfile) | Production Docker container specification based on Python 3.10 slim. |
| [`FinRL-Trading/docker-compose.yml`](file:///FinRL-Trading/docker-compose.yml) | Compose service configuration for running automated traders and Streamlit dashboards. |
| [`FinRL-Trading/deploy.sh`](file:///FinRL-Trading/deploy.sh) | Shell script for system dependencies, environment checks, and Docker orchestration. |

### 3. `verification_logs/` Audit Suite
| Script / Artifact | Description |
| :--- | :--- |
| [`verification_logs/requirements.amended.txt`](file:///verification_logs/requirements.amended.txt) | Corrected dependency list resolving PyPI package name typos for reproducible installation. |
| [`verification_logs/scripts/clean_rebuild.ps1`](file:///verification_logs/scripts/clean_rebuild.ps1) | PowerShell script executing an automated clean virtualenv rebuild and pip install. |
| [`verification_logs/scripts/install_amended.ps1`](file:///verification_logs/scripts/install_amended.ps1) | PowerShell installer testing the amended requirements file. |
| [`verification_logs/scripts/smoke_check.py`](file:///verification_logs/scripts/smoke_check.py) | Automated module import smoke test validating all core `src` submodules without runtime crashes. |
| [`verification_logs/scripts/decode_alpaca_comments.py`](file:///verification_logs/scripts/decode_alpaca_comments.py) | Forensic script detecting and decoding non-UTF-8 character encodings in source files. |
| [`verification_logs/scripts/item1_encoding_audit.py`](file:///verification_logs/scripts/item1_encoding_audit.py) | Automated encoding scanner across all repository Python source files. |
| [`verification_logs/scripts/item3_requirements_audit.py`](file:///verification_logs/scripts/item3_requirements_audit.py) | Requirement analyzer inspecting package pinning, obsolete backports, and unbound versions. |
| [`verification_logs/scripts/item4_notebook_audit.py`](file:///verification_logs/scripts/item4_notebook_audit.py) | AST analysis script examining notebook cells for external network calls and credentials. |
| [`verification_logs/stage1c/`](file:///verification_logs/stage1c/) | Cryptographic audit logs and execution traces proving verification integrity. |

---

## 🔍 Missing Elements & Senior Dev Audit Notes

As part of a professional deployment review, the following items, technical debts, and missing operational elements have been identified:

### 1. Missing Secrets & Credentials (`.env`)
- **Status:** By design, **`.env` is omitted from version control** to adhere to twelve-factor security standards and prevent leakage of private keys.
- **Missing Keys Required for Operation:**
  - `APCA_API_KEY` & `APCA_API_SECRET`: Required for Alpaca Paper / Live Trading.
  - `FMP_API_KEY`: Required for fetching high-fidelity fundamental financial statements from Financial Modeling Prep.
  - `OPENAI_API_KEY`: Required if utilizing LLM-based sentiment or summary modules.
  - `FINNHUB_API_KEY`: Required for Finnhub market news and sentiment streams.
  - `WRDS_USERNAME` / `WRDS_PASSWORD`: Optional academic data access.
- **Action Required:** Copy `FinRL-Trading/.env.example` to `FinRL-Trading/.env` and supply valid credentials.

### 2. Dependency Discrepancy in `requirements.txt`
- **Issue:** In [`FinRL-Trading/requirements.txt`](file:///FinRL-Trading/requirements.txt) line 44, the requirement is specified as:
  ```text
  finnhub>=2.4.19
  ```
  On PyPI, this package is published under the name **`finnhub-python`**, not `finnhub`. Attempting `pip install -r requirements.txt` directly fails with:
  ```
  ERROR: Could not find a version that satisfies the requirement finnhub>=2.4.19
  ```
- **Remedy:** Use the tested and verified file [`verification_logs/requirements.amended.txt`](file:///verification_logs/requirements.amended.txt) which specifies `finnhub-python>=2.4.19`.

### 3. Obsolete PyPI Backport & Unbounded Dependencies
- **Obsolete Backport:** `pathlib>=1.0.1` is included in `requirements.txt`. `pathlib` is part of the Python Standard Library since Python 3.4. Installing the PyPI backport is unnecessary and can cause conflicts in Python 3.10+.
- **Unbounded Upper Bounds:** Core data science libraries (`pandas>=2.0.0`, `numpy>=1.24.0`, `scipy>=1.11.0`, `lightgbm>=4.0.0`) lack upper version constraints (e.g., `<3.0.0`), creating potential forward breaking change risks when deploying on future Python/package versions.

### 4. Character Encoding Anomaly in `alpaca_manager.py`
- **Issue:** [`FinRL-Trading/src/trading/alpaca_manager.py`](file:///FinRL-Trading/src/trading/alpaca_manager.py) lines 440, 460, and 464 contain comments encoded in **GBK** rather than pure UTF-8:
  - Line 440: `# Filter与规范化: 仅保留可交易标的；负权重视为0；必要时归一化到<=1`
  - Line 460: `# 若权重和>1，按总和进行缩放归一化`
  - Line 464: `# 和<=1则保留，允许剩余现金`
- **Impact:** While Python 3 handles UTF-8 by default, tools or IDEs parsing files under strict UTF-8 readers may throw `UnicodeDecodeError` unless converted or opened with appropriate error handlers. A decoding script is preserved in `verification_logs/scripts/decode_alpaca_comments.py`.

### 5. Runtime Database & Historical Data Caching
- **Missing Database:** The local SQLite database `finrl_trading.db` is intentionally omitted from version control. The database will automatically initialize its schema via SQLAlchemy upon first run.
- **Dynamic Caches:** Directories `FinRL-Trading/data/cache/`, `FinRL-Trading/data/processed/`, and `FinRL-Trading/data/raw/` are excluded. Historical prices will be downloaded and cached dynamically upon strategy initialization.

### 6. Platform Consideration: Windows Application Control / WDAC
- During verification on Windows workstations with strict AppLocker or Windows Defender Application Control (WDAC) policies, compiled C-extensions in virtual environments (`pandas._libs`, `scipy`) may encounter:
  ```
  ImportError: DLL load failed while importing lib: An Application Control policy has blocked this file.
  ```
- **Recommendation:** Deploy within Linux, WSL2, or via the included [Dockerfile](file:///FinRL-Trading/Dockerfile).

### 7. Automated CI/CD Workflows
- **Missing CI/CD:** A `.github/workflows/` directory with automated linting (`flake8`, `black`), type checking (`mypy`), and unit tests (`pytest`) is not yet included in the upstream codebase. Adding a GitHub Actions workflow is recommended for production.

---

## 🚀 Quickstart & Setup Instructions

### Prerequisites
- Python 3.10 or 3.11 installed.
- Git.
- An Alpaca Markets Paper Trading account.

### 1. Clone the Repository
```bash
git clone https://github.com/codewithjaswanth/JEV-ALPACA-TRADER.git
cd JEV-ALPACA-TRADER/FinRL-Trading
```

### 2. Create and Activate Virtual Environment
```bash
# On Linux/macOS
python3 -m venv venv
source venv/bin/activate

# On Windows (PowerShell)
py -3.10 -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install Dependencies (Amended Spec)
```bash
pip install --upgrade pip setuptools wheel
pip install -r ../verification_logs/requirements.amended.txt
```

### 4. Configure Environment Variables
```bash
cp .env.example .env
```
Edit `.env` and set your Alpaca credentials:
```ini
APCA_API_KEY=your_actual_alpaca_key
APCA_API_SECRET=your_actual_alpaca_secret
APCA_BASE_URL=https://paper-api.alpaca.markets
APCA_USE_PAPER_TRADING=true
```

### 5. Verify Installation (Smoke Test)
Run the verified module test from the `FinRL-Trading` directory:
```bash
python ../verification_logs/scripts/smoke_check.py
```
Expected output:
```text
success: executed without error - src.config.settings
success: executed without error - src.data.data_fetcher
success: executed without error - src.data.data_processor
success: executed without error - src.data.data_store
success: executed without error - src.backtest.backtest_engine
success: executed without error - src.strategies.base_strategy
success: executed without error - src.strategies.ml_strategy
success: executed without error - src.trading.alpaca_manager
success: executed without error - src.trading.trade_executor
success: executed without error - src.trading.performance_analyzer
success: executed without error - src.main
```

### 6. Run Backtest or Launch Dashboard
```bash
# Run historical backtest
python src/main.py --mode backtest --config config/backtest_config.json

# Launch Streamlit web dashboard
streamlit run src/main.py -- --mode web
```

---

## 🛡 Security & Risk Management

1. **Paper Trading Default:** The default configuration enforces `APCA_USE_PAPER_TRADING=true`. Do NOT switch to live trading without extensive backtesting and paper trading evaluation.
2. **Order Constraints:** Built-in safeguards (`TRADING_MAX_ORDER_VALUE=100000.0`, `STRATEGY_MAX_WEIGHT_PER_STOCK=0.10`, `STRATEGY_MAX_SECTOR_WEIGHT=0.30`) prevent single-stock concentration risk and rogue order submission.
3. **Key Safety:** Never check in `.env` or hardcode API keys in notebooks or source scripts.

---

## 📄 License
This project is licensed under the Apache License, Version 2.0. See [`FinRL-Trading/LICENSE`](file:///FinRL-Trading/LICENSE) for details.
