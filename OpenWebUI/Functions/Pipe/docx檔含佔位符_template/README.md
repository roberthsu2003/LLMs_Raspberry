# Docx 檔含佔位符 Template：檔案存取與掛載指南

在 Open WebUI 開發 Function 或 Pipe 時，我們經常需要讀取預設的範本檔案（例如 `template.docx`）。本篇指南將為您整理如何在 Open WebUI 環境中正確地讀取與掛載檔案。

---

### 📥 佔位符檔案下載

- [docx檔含佔位符_template.docx](docx檔含佔位符_template.docx)
- [docx檔含佔位符_template_jinja2.docx](docx檔含佔位符_template_jinja2.docx)

---

### 一、 🔍 在 Open WebUI 內能否讀到檔案？

#### 情況 A：讀取實體檔案位置
**✅ 可以讀取** - 您可以直接存取容器內的 `/app/backend/data/uploads` 等實體路徑來讀取檔案。

```python
"""
title: 讀取實體檔案範例
author: YourName
version: 1.0
description: 讀取實體檔案範例
requirements: docxtpl
"""

import os
from docxtpl import DocxTemplate

class Pipe:
    def pipe(self, body: dict, __user__=None) -> str:
        # ✅ 可以讀取這個路徑
        uploads_dir = "/app/backend/data/uploads"
        
        # 列出所有檔案
        if os.path.exists(uploads_dir):
            files = os.listdir(uploads_dir)
            print(f"找到的檔案: {files}")
            
            # 讀取特定檔案
            for file in files:
                file_path = os.path.join(uploads_dir, file)
                if file.endswith('.docx'):
                    doc = DocxTemplate(file_path)
                    print(f"✅ 成功讀取: {file}")
        
        return "完成"
```

<details>
<summary>💡 程式碼詳細說明</summary>

- **`uploads_dir`**：指定容器內部的實體上傳資料夾路徑。
- **`os.listdir` 與 `os.path.join`**：用來列出目錄下的所有檔案，並將路徑組合起來。
- **`DocxTemplate`**：從 `docxtpl` 載入，可以直接讀取指定路徑的 `.docx` 範本準備進行後續替換。

</details>

#### 情況 B：使用 `__files__` 參數存取
**✅ 可以讀取** - 如果使用者是在對話對話框中臨時上傳檔案，可以透過 `__files__` 參數進行存取：

```python
"""
title: 讀取上傳檔案範例
author: YourName
version: 1.0
description: 讀取使用者上傳檔案範例
"""

class Pipe:
    def pipe(self, body: dict, __user__=None, __files__: list = []) -> str:
        # 存取上傳的檔案
        if __files__:
            for file_obj in __files__:
                file_id = file_obj['id']
                file_name = file_obj.get('filename', '')
                print(f"檔案 ID: {file_id}, 名稱: {file_name}")
                
                # 檔案內容可以從此取得
                content = file_obj['file']['data']['content']
        return "完成"
```

<details>
<summary>💡 程式碼詳細說明</summary>

- **`__files__: list`**：這是 Open WebUI 的特殊參數，當使用者在聊天室上傳檔案時，系統會把檔案資訊透過這個參數帶入 Pipe 中。
- **`file_obj['file']['data']['content']`**：透過字典的鍵值結構，可以讀取到被系統解析出的檔案內文或屬性資料。

</details>

---

### 二、 ⚠️ 實際需要注意的限制

在使用本地範本時，您必須注意 Docker 容器化帶來的隔離限制：

> [!WARNING]
> **本地範本使用限制**
> - **Docker 容器隔離**：若您將 Pipe 運行在外部獨立的 `Pipelines` 容器中，它將無法存取主 `open-webui` 容器的 `/app/backend/data/uploads` 路徑。解決方案是必須在 `docker-compose.yml` 中將相同的本地目錄同時掛載給兩個服務。
> - **強烈建議**：對於存取本地範本的需求，建議直接使用 Open WebUI 內建的 Function 或 Pipe，而不是部署獨立的 Pipeline 外部伺服器。

---

### 三、 🏆 最佳實踐：3 種專案讀取方案

#### 方案 1：在 Open WebUI 本身執行（推薦，最簡單）
直接在 Open WebUI UI 中建立 Function -> Pipe，沒有額外的容器隔離問題，能直接存取路徑。

```python
"""
title: 內建環境產生 Docx 範例
author: YourName
version: 1.0
description: 內建環境產生 Docx 範例
requirements: docxtpl
"""

from docxtpl import DocxTemplate
import os

class Pipe:
    def __init__(self):
        self.type = "pipe"
        self.id = "doc_generator"
    
    def pipe(self, body: dict, __user__=None) -> str:
        try:
            template_path = "/app/backend/data/uploads/template.docx"
            if not os.path.exists(template_path):
                return f"❌ 找不到範本: {template_path}"
            
            # 填入資料並產生新檔案
            doc = DocxTemplate(template_path)
            context = {"company_name": "台灣科技", "employee_name": "王小明"}
            doc.render(context)
            
            output_path = "/app/backend/data/uploads/output_document.docx"
            doc.save(output_path)
            return f"✅ 已產生: {output_path}"
        except Exception as e:
            return f"❌ 錯誤: {str(e)}"
```

<details>
<summary>💡 程式碼詳細說明</summary>

- **`context` 字典**：準備要塞入 Word 範本的資料，鍵名必須與 `.docx` 裡的佔位符（如 `{{ company_name }}`）完全一致。
- **`doc.render(context)`**：將備妥的資料替換進原本的 Word 範本佔位符中。
- **`doc.save(output_path)`**：將合成完畢的新文件存檔到容器內的 `/app/backend/data/uploads/` 目錄。

</details>


#### 方案 2：建立專用的範本目錄（最穩定，易於版本控制）
不依賴會與使用者上傳混雜的 uploads 目錄，改用自訂的掛載位置（如 `/app/templates`）。

```python
"""
title: 指定範本目錄範例
author: YourName
version: 1.0
description: 指定範本目錄範例
requirements: docxtpl
"""

import os
from docxtpl import DocxTemplate

class Pipe:
    def __init__(self):
        self.template_dir = "/app/templates" # 在 Docker 中掛載此目錄
    
    def pipe(self, body: dict, __user__=None) -> str:
        template_path = os.path.join(self.template_dir, "template.docx")
        if os.path.exists(template_path):
            doc = DocxTemplate(template_path)
            return "✅ 成功"
        return f"❌ 找不到範本在: {template_path}"
```

<details>
<summary>💡 程式碼詳細說明</summary>

- **`__init__` 初始化**：在 Pipe 類別建立時，就將 `self.template_dir` 指定為自訂的掛載目錄 `/app/templates`。
- **`os.path.exists` 安全檢查**：確保檔案確實存在後再呼叫 `DocxTemplate`，避免因路徑錯誤引發無預期的程式崩潰。

</details>


#### 方案 3：透過 API 獲取（適用於外接的 Pipelines 伺服器）
如果您的架構受限只能使用獨立 Pipelines 伺服器，就必須使用 API 獲取檔案。

```python
"""
title: 透過內部 API 獲取檔案範例
author: YourName
version: 1.0
description: 透過內部 API 獲取檔案範例
requirements: requests
"""

import requests

class Pipeline:
    def __init__(self):
        self.type = "filter"
    
    async def inlet(self, body: dict, __user__=None) -> dict:
        # 用 open-webui 伺服器內部 API 獲取檔案內容
        api_url = "http://open-webui:8080/api/v1/files/{file_id}/content"
        try:
            response = requests.get(api_url, headers={"Authorization": f"Bearer {api_key}"})
            if response.status_code == 200:
                content = response.content
        except Exception as e:
            print(f"Error: {e}")
        return body
```

<details>
<summary>💡 程式碼詳細說明</summary>

- **`async def inlet`**：這是在 Pipeline 架構中用來攔截與前置處理請求的進入點（Filter/Inlet）。
- **呼叫內部 API**：使用獨立 API Key 發送 `requests.get` 請求到主伺服器（open-webui 容器），從 `response.content` 取回實體的檔案串流。

</details>

---

### 四、 🛠️ 如何測試可存取的目錄？

如果不確定腳本可以讀到什麼，可以先在 Pipe 裡寫一個除錯探測器：

```python
"""
title: 路徑測試探測器
author: YourName
version: 1.0
description: 用來測試與除錯可讀取路徑的探測器
"""

import os

class Pipe:
    def pipe(self, body: dict, __user__=None) -> str:
        paths_to_test = [
            "/app/backend/data/uploads",
            "/app/backend/data",
            "/app/templates",
            "/app",
        ]
        result = "📍 路徑測試結果：\n"
        for path in paths_to_test:
            exists = os.path.exists(path)
            result += f"{'✅' if exists else '❌'} {path}\n"
            if exists and os.path.isdir(path):
                try:
                    files = os.listdir(path)[0:3]
                    result += f"   檔案: {files}\n" 
                except Exception as e:
                    result += f"   ⚠️ 無法讀目錄: {e}\n"
        return result
```

<details>
<summary>💡 程式碼詳細說明</summary>

- **路徑陣列 `paths_to_test`**：預先把想檢查的所有伺服器目錄路徑寫成串列。
- **`os.path.isdir` 與 `os.listdir`**：檢查路徑存不存在；若該路徑是資料夾，試著印出前三筆檔案，來驗證目錄權限是否足夠。
- **`try...except` 區塊**：避免因為 Linux 讀取權限不足導致錯誤而中斷迴圈。

</details>

---

### 五、 📦 如何手動將 Template 放入容器的正確位置？

如果您需要把 `template.docx` 固定放到伺服器讓 Pipe 調用，以下介紹三種方法：

#### 1️⃣ 如果您使用 Docker Compose（推薦永久方案）
在您的 `docker-compose.yml` 中新增 **volumes** 掛載本機資料夾：

```yaml
version: '3.8'

services:
  open-webui:
    image: ghcr.io/open-webui/open-webui:main
    ports:
      - "3000:8080"
    volumes:
      - open-webui-data:/app/backend/data
      # ✅ 將主機上的 local-templates 資料夾，掛載到容器內的 /app/templates
      - ./local-templates:/app/templates  
    environment:
      - WEBUI_SECRET_KEY=your_secret_key

volumes:
  open-webui-data:
```

<details>
<summary>💡 程式碼詳細說明</summary>

- **`volumes`**：在 Docker 中用來讓容器存取宿主機（您的運行主機）資料夾的實體對應機制。
- **`./local-templates:/app/templates`**：冒號前面是您本機的相對路徑，冒號後面是容器裡面的對應路徑，設定完後容器就能讀取您放入的檔案。

</details>

**操作步驟：**
1. 建立本機資料夾 `mkdir -p local-templates`
2. 將 `template.docx` 放入此目錄。
3. 重啟容器：`docker-compose down` 然後 `docker-compose up -d`
4. 您的 Pipe 即可去讀取 `/app/templates/template.docx`！

#### 2️⃣ 臨時複製檔案進入容器（不適合永久部署）
如果您只想快速測試，可以直接把電腦上的檔案複製進運行中的容器。

**Windows 用戶：**
```bash
docker cp C:\Users\您的使用者\Documents\template.docx open-webui:/app/backend/data/uploads/
```

**Mac / Linux 用戶：**
```bash
docker cp ~/Documents/template.docx open-webui:/app/backend/data/uploads/
```

<details>
<summary>💡 程式碼詳細說明</summary>

- **`docker cp`**：Docker 的強制複製指令。冒號 `:` 分隔後，會將本機端的檔案強制推送進指定的 `[容器名稱]:[容器內部路徑]` 中。

</details>

**驗證是否成功：**
```bash
docker exec open-webui ls -la /app/backend/data/uploads/
```

<details>
<summary>💡 程式碼詳細說明</summary>

- **`docker exec`**：對正在運行中的 `open-webui` 容器發送 Linux 指令。
- **`ls -la`**：列出目標目錄底下的所有詳細檔案資訊，確認 `template.docx` 是否有成功覆寫過去。

</details>

#### 3️⃣ 不使用 Docker 而是純 Python (PiOS Local) 執行
如果您是直接在 Pi 環境下用 Python 虛擬環境啟動 Open WebUI，需要先尋找配置檔案的存放處（通常在家目錄）：

```bash
# MacOS/Linux 尋找預設目錄
cp ~/Documents/template.docx ~/.local/lib/python3.11/site-packages/open_webui/backend/data/uploads/
```

<details>
<summary>💡 程式碼詳細說明</summary>

- **`~/.local/lib/...`**：使用 `pip` 或原生系統安裝 Open WebUI 時常見的依賴庫安裝路徑，可透過手動複製（`cp`）強行將檔案遷移過去。

</details>

> [!CAUTION]
> **不推薦的方法**
> 請勿在 Open WebUI 工作區介面的 Admin Panel 直接上傳範本檔案。因為伺服器會將檔案名稱進行雜湊 (Hash) 改名，且重啟後可能難以追蹤路徑，非常不適合當作系統固定讀取的程式範本。

---

### 六、 🚀 實戰進階範例：履歷表單助手

為了讓大家徹底了解「範本讀取」加上「AI 邏輯」的威力，本目錄提供了一個完整的整合型實戰範例：**履歷表單助手** (`resume_assistant_pipe.py`)。

> [!IMPORTANT]
> **重要前置作業**
> 此實戰範例的底層邏輯依賴 Google Gemini API 驅動。使用前請務必至 [Google AI Studio](https://aistudio.google.com/) 申請免付費的 **GEMINI_API_KEY**，安裝 Pipe 後，您必須直接在 Open WebUI 介面的「設定 (Valves)」區塊中填入該金鑰才能順利運行！

此範例的強大亮點在於：
1. **💡 對話式收集填表**：利用 `google-genai` 套件串接 Gemini API，以聊天的方式逐步向使用者索取履歷表需要的每一個欄位資訊。
2. **🤖 自動填充 Word 範本**：當 AI 判斷資料齊全後，會自動輸出 JSON 格式供程式攔截，並呼叫 `docxtpl` 結合預設的 `template_form.docx` 產生出全新的檔案。
3. **📥 前端動態下載按鈕 (Base64)**：不將產生的檔案寫死在伺服器硬碟，而是透過記憶體暫存 (Buffer) 轉為 Base64 URI 下載連結，搭配 `__event_emitter__` 直接顯示在聊天畫面的按鈕上，使用者一鍵即可下載實體 Word 檔！

#### 📂 範例檔案導覽

**如果您使用商用 Gemini API：**
- **[程式碼本體：resume_assistant_pipe.py](./resume_assistant_pipe.py)**：適合想要極速開發、強悍解讀能力的開發者。
- **[深度解析：注意事項.md](./注意事項.md)**：👉 **強烈建議閱讀！** 裡面解析了歷史對話格式轉換、關閉 function calling 與前端 `__event_emitter__` 渲染按鈕的機制。

**如果您擁有自己的地端 Ollama 環境（100% 隱私落地）：**
- **[Ollama 版程式：resume_assistant_ollama_pipe.py](./resume_assistant_ollama_pipe.py)**：拔除外部依賴，透過 `requests` 純地端連線打入 Ollama API。
- **[Ollama 開發眉角：注意事項_ollama.md](./注意事項_ollama.md)**：解決了純地端常見的「Docker 容器網路互不通（host.docker.internal）」與「地端模型一直講廢話破壞 JSON 格式」的實務痛點。

#### 🧪 快速測試
當您設定好這個 Pipe 之後，可以一口氣貼上以下**這段測試對話**給 AI，享受全自動化生成的快感：

```text
我叫王小明，身分證 A123456789，電話 0912-345-678，Email: wang@example.com，男性，未婚。學歷：台灣大學資訊工程系，2020年畢業。程式語言會 Python、JavaScript。曾在台積電擔任軟體工程師2年，負責系統開發與維護。溝通能力優秀，團隊協作良好，問題解決優秀，領導能力普通，學習能力優秀。同意所有聲明，簽名人王小明，日期2026-04-14。
```

<details>
<summary>💡 程式碼詳細說明</summary>

- 此段為純文字測試樣本，複製貼上於對話框欄位可直接驗證模型是否能自訂解析這段內容並填寫至 Word 中。

</details>