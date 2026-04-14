# 最常用 Skill 清單（辦公室應用場景）

在 OpenWebUI 的社群生態系中，有許多開發者與使用者分享了實用的「公開 Skill」（通常在官方 Hub 中被歸類為 Prompts、Tools 或 Pipelines）。這些公開資源非常適合直接應用於日常辦公室場景中。

以下為您整理常見的辦公室應用情境，以及對應的公開 Skill 類型，並附上如何取得與使用的完整教學。

---

## 🏢 常見的辦公室公開 Skill 應用情境

雖然每一款社群 Skill 的名稱可能隨時間變動，但您可以透過關鍵字在社群中找到這些「辦公室神器」：

### 1️⃣ 會議記錄重點摘要 (Meeting Summarizer)
*   **用途**：當您上傳逐字稿或貼上長篇的會議文字後，AI 會自動將其轉換為「會議摘要」、「Action Items（待辦事項）」與「決策結果」。
*   **搜尋關鍵字**：`Meeting`, `Summary`, `Minutes`, `Action Items`
*   **實際效果**：省去手動整理逐字稿的時間，確保團隊跟進事項不漏掉。

### 2️⃣ 商務外語翻譯與潤飾 (Business Email Translator)
*   **用途**：輸入口語化的中文，AI 立刻幫你轉化為語氣專業、符合外商習慣的商務英文（或日文等其他語言）Email。
*   **搜尋關鍵字**：`Business Email`, `Translator`, `Formal Rewrite`, `Polite`
*   **實際效果**：不再需要倚靠 Google 翻譯，也不會寫出帶有濃厚「中式英文 (Chinglish)」的信件。

### 3️⃣ 財務數據/發票資訊擷取 (Data Extractor)
*   **用途**：搭配 RAG（文件上傳功能），限定 AI 只能從您上傳的 PDF 報表或發票中擷取「總金額」、「統編」、「日期」等特定欄位，並輸出成 CSV 格式。
*   **搜尋關鍵字**：`JSON Extractor`, `Data Extraction`, `Invoice`, `CSV Formatter`
*   **實際效果**：方便財務人員快速處理大量單據，並匯入 Excel。

### 4️⃣ 行銷文案與 SEO 產生器 (Marketing Copywriter)
*   **用途**：輸入簡單的產品特點，自動產生適合發布於 Facebook、LinkedIn 或官方部落格的貼文，並自帶相關 Hashtag 與 SEO 架構。
*   **搜尋關鍵字**：`SEO`, `LinkedIn Post`, `Copywriter`, `Marketing`
*   **實際效果**：行銷人員能夠快速產出多種版本的社群貼文 A/B Test 素材。

---

## 🛠️ 如何取得並使用公開的 Skill？

OpenWebUI 擁有一個活躍的官方社群分享中心（Hub），您可以輕鬆地將別人寫好的 Skill（或 Prompts/Tools）匯入到您 Raspberry Pi 上的本地端系統。

### 方法 1：從官方 Hub「一鍵匯入」(推薦)

最快的方式是直接串接 OpenWebUI 的官方 Hub：

1. **前往社群 Hub**：開啟瀏覽器，前往 [OpenWebUI 官方分享中心](https://openwebui.com/)。
2. **尋找所需資源**：在首頁尋找您需要的 **Prompts**（提示詞指令）或 **Tools**（輔助工具）。
3. **點擊 Import (匯入)**：找到喜歡的辦公室 Skill 後，點擊頁面上的 `Get` 或 `Import to WebUI` 按鈕。
4. **確認本地端網址**：系統會詢問您的 OpenWebUI 本地端網址。若您架設在樹莓派上，請輸入您的樹莓派 IP 與 Port（例如 `http://192.168.x.x:8080`）。
5. **完成安裝**：瀏覽器會將您導向您的本地端系統，點擊「確定」後，該 Skill 就會出現在您的 **Workspace (工作區)** 裡面了！

### 方法 2：手動複製貼上 (適合自定義修改)

如果您在 GitHub、論壇或網路社團看到好用的 Prompt/Skill 結構，可以用手動方式加入：

1. **複製內容**：將網路上公開的 Prompt 或 Markdown 指令複製起來。
2. **進入工作區**：打開您的本地端 OpenWebUI，點擊左側邊欄進入 **Workspace (工作區) → Prompts 或 Skills**。
3. **新增 Skill**：點擊 **+ New**（新增）。
4. **填寫指令**：將複製的內容貼入 `Content` 欄位，並為它取一個好記的名稱（例如：`@商務英文翻譯機`）。
5. **儲存並呼叫**：按下儲存。未來在聊天室對話時，只需輸入 `@商務英文翻譯機` 或 `#商務英文翻譯機`（依您的系統版本預設符號而定），就能立刻呼叫這個 Skill 來幫忙辦公！

---

> 💡 **小撇步**：對於辦公室場景，非常推薦您將這些 Skills 與 **Ollama 中推論能力較強的模型（如 Llama-3-8B 或 Gemma）** 搭配使用，以獲得最佳的摘要與翻譯邏輯！
