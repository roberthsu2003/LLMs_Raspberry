# 履歷表單填寫助手 (lesson5_1.py)

Open-WebUI 的 Pipe 功能，透過 Gemini AI 對話收集使用者資料，自動填入 `.docx` 模板並產生下載連結。

---

## 運作流程

```
使用者輸入資料
     ↓
Gemini 對話收集欄位
     ↓
Gemini 輸出 JSON (action: generate_form)
     ↓
docxtpl 填入 template_form_fixed.docx
     ↓
Base64 編碼 → event_emitter 發送 HTML 下載按鈕
     ↓
使用者點擊下載 .docx
```

---

## 環境需求

| 項目 | 說明 |
|------|------|
| 套件 | `docxtpl`, `google-genai>=1.0.0` |
| 環境變數 | `GEMINI_API_KEY`（容器內設定） |
| 模板檔案 | `/app/backend/data/uploads/template_form_fixed.docx` |
| Python | 3.10+（需支援 `async def`） |

---

## 檔案說明

### `template_form_fixed.docx`
原始的 `template_form.docx` 經過修復的版本。

**為什麼需要修復？**
原始檔案內含空白佔位符 `{{ }}`，Jinja2 解析時會拋出：
```
Expected an expression, got 'end of print statement'
```
修復方式：用 Python `zipfile` 解開 docx，以 regex 移除所有 `{{ }}` 空白標籤後重新打包。

**上傳到容器的指令：**
```bash
docker cp lesson5/template_form_fixed.docx <容器名稱>:/app/backend/data/uploads/
```

---

## 程式碼重點說明

### 1. Valves（設定值）
```python
class Valves(BaseModel):
    GEMINI_API_KEY: str = Field(default="", description="Gemini API Key")
    GEMINI_MODEL: str = Field(default="gemini-2.5-flash", description="Gemini 模型名稱")
```
- Open-WebUI 介面上可手動填入，也可從容器環境變數自動讀取
- 優先順序：**Valves 手動設定 > 容器環境變數**

### 2. API Key 讀取
```python
def _api_key(self):
    return self.valves.GEMINI_API_KEY or os.environ.get("GEMINI_API_KEY", "")
```
- `__init__` 只在載入時執行一次，那時環境變數可能還未注入
- 因此改在每次 `pipe()` 執行時才讀取，確保能取到值

### 3. Gemini 對話歷史轉換
```python
history = []
for msg in messages[:-1]:
    role = "user" if msg["role"] == "user" else "model"
    history.append(
        types.Content(role=role, parts=[types.Part(text=msg["content"])])
    )
```
- Open-WebUI 的訊息格式（`assistant`）需轉換成 Gemini 的格式（`model`）
- 最後一則訊息單獨加入，不放進 history

### 4. 關閉 Auto Function Calling
```python
automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True)
```
- `gemini-2.5-flash` 預設啟用 AFC，會自動多次呼叫 API
- 對話場景不需要此功能，關閉可避免不必要的延遲和費用

### 5. JSON Action 偵測
```python
match = re.search(r"```json\s*(\{.*?\})\s*```", text, re.DOTALL)
```
- Gemini 收集完資料後，會在回應中輸出一個 JSON 區塊
- Pipe 偵測到 `action: generate_form` 就觸發產生文件

### 6. Base64 下載（不寫入磁碟）
```python
buf = io.BytesIO()
doc.save(buf)
buf.seek(0)
b64 = base64.b64encode(buf.read()).decode("utf-8")
```
- 使用記憶體緩衝區，不需要寫入伺服器磁碟
- 使用者無法直接存取容器路徑，所以用 Base64 data URI 讓瀏覽器直接下載

### 7. async pipe + event_emitter
```python
async def pipe(self, body, __user__=None, __event_emitter__=None):
    ...
    await __event_emitter__({
        "type": "message",
        "data": {"content": full_msg}
    })
```
- Open-WebUI 的 `pipe()` 支援 async
- `__event_emitter__` 發送 `type: "message"` 可讓 Open-WebUI 渲染 HTML 內容
- 若直接 `return` HTML 字串，Open-WebUI 會當成純文字顯示，按鈕無法點擊

---

## 注意事項

### ⚠️ 模型選擇
| 模型 | 適用場景 | 備註 |
|------|----------|------|
| `gemini-2.5-flash` | 對話、表單填寫 ✅ | 速度快、費用低 |
| `gemini-2.5-pro` | 複雜推理任務 | 有 thinking 機制，對話會很慢 |

> `gemini-2.0-flash` 已於 2025 年停用，不可使用。

### ⚠️ SDK 版本
- 使用 `google-genai`（新版），**不是** `google-generativeai`（已棄用）
- `google-generativeai` 的 GitHub repo 已於 2025/12/16 封存
- `requirements` 指定 `google-genai>=1.0.0` 確保容器安裝新版

### ⚠️ HTML 渲染
- `pipe()` 直接 `return` 的字串，Open-WebUI **不會渲染 HTML**
- 必須透過 `await __event_emitter__({"type": "message", ...})` 才能渲染 HTML 按鈕

### ⚠️ 模板佔位符
- `docxtpl` 使用 Jinja2 語法，模板內不能有 `{{ }}` 空白標籤
- 若出現 `Expected an expression, got 'end of print statement'` 錯誤，代表模板有空白佔位符需要修復

---

## 表單欄位一覽

| 類別 | 欄位 |
|------|------|
| 基本資料 | `name`, `id_number`, `phone`, `email`, `gender`, `marital_status` |
| 學歷（最多4筆） | `school_1~4`, `graduation_year_1~4` |
| 技能 | `programming_languages`, `other_languages`, `skills` |
| 工作經歷（最多3筆） | `company_1~3`, `position_1~3`, `years_1~3`, `duties_1~3` |
| 能力評估 | `溝通能力/團隊協作/問題解決/領導能力/學習能力` 各有 `_excellent/_good/_fair` |
| 同意聲明 | `confirm_accuracy`, `consent_recruitment`, `consent_notification`, `consent_privacy` |
| 簽名 | `signer_name`, `signature_date`, `signature`, `signature_notes` |
| 其他 | `special_needs`, `remarks` |
