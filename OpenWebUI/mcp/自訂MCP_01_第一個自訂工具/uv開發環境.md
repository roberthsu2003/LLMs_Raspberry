# uv 開發環境

本文件說明如何使用 **uv** 為本範例建立獨立的 Python 虛擬環境，進行本機開發與測試。

---

## 什麼是 uv？

**uv** 是由 Astral 開發的快速 Python 套件管理工具（以 Rust 撰寫），可取代 pip 與 venv，安裝與建立環境速度顯著較快。

---

## 安裝 uv

### macOS / Linux

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Windows (PowerShell)

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 驗證安裝

```bash
uv --version
```

---

## 建立開發環境

### 1. 進入範例目錄

```bash
cd 自訂MCP_01_第一個自訂工具/範例檔/mcpo-custom
```

### 2. 建立虛擬環境

```bash
uv venv
```

會在當前目錄建立 `.venv/` 資料夾。

### 3. 安裝依賴

```bash
uv pip install -r requirements.txt
```

或使用 `uv sync`（若專案有 `pyproject.toml`）：

```bash
uv sync
```

### 4. 啟動虛擬環境

**macOS / Linux：**

```bash
source .venv/bin/activate
```

**Windows (PowerShell)：**

```powershell
.venv\Scripts\activate
```

**Windows (CMD)：**

```cmd
.venv\Scripts\activate.bat
```

### 5. 驗證

```bash
python server.py
```

或執行測試腳本：

```bash
python test_tools.py
```

---

## 常用指令

| 指令 | 說明 |
|------|------|
| `uv venv` | 建立虛擬環境 |
| `uv pip install -r requirements.txt` | 依 requirements.txt 安裝套件 |
| `uv pip install <套件>` | 安裝單一套件 |
| `uv pip list` | 列出已安裝套件 |
| `deactivate` | 離開虛擬環境 |

---

## 目錄結構（含 .venv）

```
mcpo-custom/
├── .venv/           # uv 建立的虛擬環境（建議加入 .gitignore）
├── Dockerfile
├── requirements.txt
├── server.py
└── test_tools.py
```

> **建議：** 將 `.venv/` 加入 `.gitignore`，避免將虛擬環境提交至版控。

---

## 與 Docker 的關係

- **uv 虛擬環境**：用於**本機開發**，在宿主機上直接執行 `python server.py` 或 `python test_tools.py`
- **Docker**：用於**部署與整合**，容器內使用 `pip install`，不依賴本機的 `.venv`

兩者互不衝突，可依需求選擇本機開發或 Docker 部署。
