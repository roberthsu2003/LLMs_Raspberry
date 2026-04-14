# 履歷表單填寫助手 - 本機 Ollama 版 (resume_assistant_ollama_pipe.py)

這是基於原版（Gemini）履歷表單填寫助手的「完全地端化分支」。它使用本機執行的 Ollama 服務（推薦 `gemma` 等進階模型）來完成同樣的對話收集與表單填入工作。此方案**無須任何外部網路或金鑰**，能確保隱私 100% 落地。

---

## 運作流程與原版的差異

相較於呼叫 Google 官方的 `google-genai` SDK，這個 Pipe 改為使用 Python 內建的 `requests` 模組，對 Ollama 的端點發起 OpenAI 相容的 `POST /v1/chat/completions` API 請求。流程如下：

```
使用者輸入資料
     ↓
Pipe 發送 POST 至 http://host.docker.internal:11434
     ↓
Ollama (例如 gemma4:31b-cloud) 推論並對話收集欄位
     ↓
Ollama 輸出 JSON (action: generate_form)
     ↓
docxtpl 填入 template_form.docx
     ↓
Base64 編碼，使用 event_emitter 發送 HTML 下載按鈕！
```

---

## 實務注意事項

### ⚠️ Docker 容器網路穿透問題
如果您的 Open WebUI 運行在 Docker 內，而 Ollama 運行在宿主機 (Host Machine) 上，您必須注意「如何讓容器打到外面的 Ollama」。
* **Windows / macOS**：可在此 Pipe 的 Valves 直接填入 `http://host.docker.internal:11434/v1/chat/completions`。
* **Linux 主機**：預設沒有 `host.docker.internal`，請填入您宿主機的內網 IP（例如 `http://192.168.x.x:11434/v1/chat/completions`）或設定 docker network 的 Gateway IP。
* **Ollama 設定**：若 Ollama 還是拒絕連線，請修改伺服器的環境變數 `OLLAMA_HOST=0.0.0.0` 並重新啟動 Ollama 服務。

### ⚠️ 地端模型的 "喋喋不休綜合症" 
在使用商用的模型（如 Gemini）時，只要在 Prompt 中要求「輸出 JSON」，它通常就能完美閉嘴只給 JSON；然而地端模型（尤其是被 fine-tune 成對話助手取向的模型），常常會在輸出 JSON 的前面補一句：
> *"好的！這是您完整的履歷資料，JSON 如下："*

為了解決這個問題，在 Ollama 版的程式碼中做了以下優化：
1. **加強 System Prompt 指令**：明確補上了一句警告：*「【非常重要】：當你最後準備輸出 JSON 時，請『直接』輸出 JSON 區塊，不要在前綴加上多餘的提醒對話！」*
2. **降低 Temperature**：在 API 發送 `payload` 時，強制將 `temperature` 設為低於 `0.2`，這能限縮模型的創造力並盡可能加強它服從固定格式（JSON）的傾向。
3. **無損字串清理 (Regex)**：就算模型還是多嘴說了話，程式中的 Regex `re.search(r"```json\s*(\{.*?\})\s*```")` 依然能強悍地尋找其中的大括號區塊來攔截資料。

### 🔧 如何改變模型？
您不需要修改這支程式碼。安裝好這個 Pipe 後，在 Open WebUI 左側的「Valves (設定)」中，您可以隨時更新 `OLLAMA_MODEL` 欄位為您本機安裝的其他模型名稱（例如 `llama3:8b` 或是 `gemma4:31b-cloud`），儲存即可即時生效。
