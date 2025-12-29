# Ollama 安裝與操作完全指南

Ollama 是一個強大的工具，讓您能夠輕鬆在個人電腦（包括 Windows, macOS, Linux）以及 Raspberry Pi 上下載並執行大型語言模型（LLM）。本文件將引導您完成安裝、基本操作與模型介紹。

---

## 1. Ollama 安裝

請根據您的作業系統選擇對應的安裝方式。

### 1.1 macOS

macOS 使用者有兩種安裝方式：

- **官方網站下載**：
  1. 前往 [Ollama 官方網站](https://ollama.com/)。
  2. 點擊「Download for macOS」按鈕下載安裝檔。
  3. 下載完成後，打開 `.zip` 檔案並將 Ollama 應用程式拖曳至「應用程式」資料夾即可。

- **透過 Homebrew 安裝 (推薦給開發者)**：
  ```bash
  brew install ollama
  ```

### 1.2 Windows

- **官方網站下載**：
  1. 前往 [Ollama 官方網站](https://ollama.com/)。
  2. 點擊「Download for Windows (Preview)」按鈕下載安裝檔。
  3. 執行下載的 `.exe` 安裝程式，並依照指示完成安裝。

安裝完成後，Ollama 將在背景執行。

### 1.3 Linux & Raspberry Pi

對於大多數 Linux 發行版以及 Raspberry Pi (ARM64)，官方推薦使用一行指令稿進行安裝。

1. 打開您的終端機。
2. 執行以下指令：
   ```bash
   curl -fsSL https://ollama.com/install.sh | sh
   ```
3. 此指令稿會自動偵測您的系統、下載對應的二進位檔案，並將 Ollama 設定為系統服務。

安裝完成後，Ollama 服務會自動啟動。您可以使用 `systemctl status ollama` 來檢查其運行狀態。

---

## 2. Ollama 常用指令

安裝完成後，您可以透過終端機使用 `ollama` 指令來管理模型與互動。

### 2.1 執行並下載模型

`run` 是最常用的指令，它會自動下載模型（如果尚未下載）並直接進入互動模式。

```bash
# 執行 Meta 的 Llama 3 8B 模型
ollama run llama3

# 執行 Google 的 Gemma 2B 模型
ollama run gemma:2b
```
> 提示：在模型名稱後面加上 `:tag` 可以指定不同版本或大小，例如 `gemma:2b`（20億參數）或 `gemma:7b`（70億參數）。

### 2.2 僅下載模型

如果您想預先下載模型以備後用，可以使用 `pull` 指令。

```bash
ollama pull mistral
```

### 2.3 列出已下載的模型

使用 `list` 指令可以查看您電腦上已經安裝了哪些模型。

```bash
ollama list
```
輸出會顯示模型名稱、ID、大小以及下載時間。

### 2.4 移除模型

若要刪除不再需要的模型以釋放硬碟空間，可以使用 `rm` 指令。

```bash
ollama rm gemma:2b
```

### 2.5 查看幫助

如果您忘記了指令，可以隨時查詢幫助。

```bash
ollama --help
```

---

## 3. 熱門模型介紹

Ollama 支援數百種來自不同開發者的開源模型。以下是一些熱門且實用的模型，您可以根據需求選擇使用。

| 模型名稱 | 開發者 | 特點與應用場景 | 建議指令 |
|---|---|---|---|
| `llama3` | Meta | 目前最先進的開源模型之一，通用能力強，適合聊天、寫作、摘要等各種任務。 | `ollama run llama3` |
| `mistral` | Mistral AI | 輕量、高效且能力強勁，是兼顧速度與品質的絕佳選擇。 | `ollama run mistral` |
| `gemma` | Google | 由 Google DeepMind 開發，提供多種尺寸，在小型設備上表現優異。 | `ollama run gemma` |
| `llava` | LLAVA | **多模態模型**，能夠理解圖片內容並進行對話。您可以提供一張圖片讓它描述或提問。 | `ollama run llava` |
| `codegemma` | Google | 專為程式碼任務優化，適合寫程式、除錯、解釋程式碼。 | `ollama run codegemma` |
| `phi3` | Microsoft | 微軟推出的輕量級模型，效能優異，尤其適合在資源有限的設備上運行。 | `ollama run phi3` |

您可以從 [Ollama 模型庫](https://ollama.com/library) 探索更多有趣的模型。

---

## 4. 進階操作：建立自訂模型

Ollama 也允許您透過 `Modelfile` 來自訂模型的行為，例如設定系統提示詞、調整參數等。

1.  **建立一個名為 `Modelfile` 的檔案**：

    ```dockerfile
    # 基於 llama3 模型
    FROM llama3

    # 設定系統提示詞 (System Prompt)
    # 讓模型扮演一個樂於助人的程式碼專家
    SYSTEM """
    You are a master programmer. Your goal is to provide clear, correct, and efficient code solutions. Always provide explanations for your code.
    """

    # 設定模型參數
    PARAMETER temperature 0.8
    ```

2.  **使用 `create` 指令建立您的自訂模型**：

    ```bash
    # -f 指定 Modelfile 路徑
    # my-coder 是您為新模型取的名字
    ollama create my-coder -f ./Modelfile
    ```

3.  **執行您的自訂模型**：

    ```bash
    ollama run my-coder
    ```

現在，您執行的就是一個經過客製化、專門用於程式設計的 Llama 3 模型了！