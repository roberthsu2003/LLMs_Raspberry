# 串接台北市 YouBike 2.0 即時查詢 (Ollama 生成式查詢 Pipe)

這篇文章將實作一個進階的 Pipe，它不再只是單純地把對話轉發給 Ollama，而是**賦予 AI 查詢外部即時開放資料庫的能力** (這也是檢索增強生成 RAG 的基礎概念)。

我們將介接台北市的 YouBike 2.0 即時 API：
`https://tcgbusfs.blob.core.windows.net/dotapp/youbike/v2/youbike_immediate.json`

---

### 💡 核心兩階段推論架構 (Two-Stage Inference)

由於全台北市 YouBike 站點超過 1000 個，如果把整個 JSON 直接丟給模型，不僅速度極慢，而且容易因為 Token (字數) 上限導致崩潰。因此我們採用兩階段策略：
1. **意圖提取**：先請 Ollama 模型從使用者的「自然對話」中，分析出他想找的「地點關鍵字」(例如：科技大樓、延吉街、信義區)。
2. **過濾與生成回答**：用爬蟲抓下最新 JSON 後，用程式邏輯篩選出符合關鍵字的少數站點資料，最後再把濃縮後的資料與使用者的問題，一起丟給 Ollama 整理並回答。

---

### 🔍 JSON 資料結構解析

這個 API 回傳的是一個 JSON 陣列，裡面包含了每個站點的資訊。以下是重要的欄位：
- `sna`: 站點名稱（例如 `"YouBike2.0_捷運科技大樓站"`）
- `sarea`: 所在行政區（例如 `"大安區"`）
- `ar`: 站點地址（例如 `"復興南路二段235號前"`）
- `Quantity`: 總車位數量
- `available_rent_bikes`: **目前可借車輛數**
- `available_return_bikes`: **目前可還空位數**
- `mday`: 資料更新時間

---

### 📄 程式碼實作

請在 Open WebUI 新增一個 Pipe，並貼上以下程式碼：

```python
"""
title: 台北市 YouBike 查詢幫手 Pipe
author: YourName
version: 1.0
requirements: requests, pydantic
"""

import requests
import json

from typing import Union, Generator, Iterator, Optional, Callable, Any
from pydantic import BaseModel, Field


class Pipe:
    class Valves(BaseModel):
        OLLAMA_API_URL: str = Field(
            default="http://127.0.0.1:11434/v1/chat/completions",
            description="本機 Ollama 伺服器 API 網址",
        )
        OLLAMA_MODEL: str = Field(
            default="gemma4:31b-cloud",  # 請填入您的本機模型名稱 (可至命令列輸入 ollama list 查詢)
            description="用於處理分析與回答的模型名稱",
        )
        YOUBIKE_URL: str = Field(
            default="https://tcgbusfs.blob.core.windows.net/dotapp/youbike/v2/youbike_immediate.json",
            description="YouBike 2.0 即時資訊開放資料網址",
        )

    def __init__(self):
        self.type = "pipe"
        self.id = "youbike_assistant"
        self.name = "YouBike 🤖 智慧查詢精靈"
        self.valves = self.Valves()
        # 使用 requests，不需手動處理 ssl context

    def call_ollama(self, messages: list, temperature: float = 0.7) -> str:
        """負責將訊息發送給本地 Ollama 使用的輔助函式"""
        payload = {
            "model": self.valves.OLLAMA_MODEL,
            "messages": messages,
            "stream": False,
            "temperature": temperature,
        }

        try:
            response = requests.post(
                self.valves.OLLAMA_API_URL,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=120,
            )
            response.raise_for_status()
            result = response.json()
            return result["choices"][0]["message"]["content"].strip()
        except Exception as e:
            return f"[系統例外錯誤: {str(e)}]"

    async def pipe(
        self,
        body: dict,
        __user__: Optional[dict] = None,
        __event_emitter__: Optional[Callable[..., Any]] = None,
    ) -> Union[str, Generator, Iterator]:

        # 定義小工具：用來在對話視窗上方顯示「處理中...」的小狀態列
        async def emit_status(msg: str, done: bool = False):
            if __event_emitter__:
                await __event_emitter__(
                    {"type": "status", "data": {"description": msg, "done": done}}
                )

        messages = body.get("messages", [])
        if not messages:
            return ""

        # 取得使用者傳送的最新文字
        user_message = messages[-1].get("content", "")

        try:
            # ========================
            # 任務一：AI 提取地點關鍵字
            # ========================
            await emit_status("🧠 正在思考你想找的地點...")
            sys_prompt = (
                "請從使用者的問題中提取出一個最重要的「地點關鍵字」（例如：大安區、科技大樓、台大、延吉街、101）。"
                "規則：只需輸出關鍵字本身，**絕對不要**有任何語氣詞、標點符號或其他額外的對話文字。"
                "如果使用者的話語中沒有提到任何地點，請回傳字串：「無」。"
            )

            keyword = self.call_ollama(
                [
                    {"role": "system", "content": sys_prompt},
                    {"role": "user", "content": user_message},
                ],
                temperature=0.1,
            )

            # 清理常見的冗餘詞彙
            keyword_clean = (
                keyword.replace("YouBike", "")
                .replace("2.0", "")
                .replace("_", "")
                .replace("附近", "")
                .strip()
            )

            if keyword_clean == "無" or not keyword_clean:
                await emit_status("❌ 無法辨識地點", done=True)
                return "請問您想查詢哪個地點或行政區的 YouBike 呢？（例如：請幫我查一下台大附近的 YouBike）"

            # ========================
            # 任務二：下載開放資料並過濾
            # ========================
            await emit_status(f"🌐 正在前往台北市資料庫查詢「{keyword_clean}」...")
            response = requests.get(
                self.valves.YOUBIKE_URL,
                headers={"User-Agent": "Mozilla/5.0"},
                timeout=30,
            )
            response.raise_for_status()
            data = response.json()

            await emit_status("⚙️ 正在比對符合條件的站點...")
            matched_stations = []

            # 走訪所有的 JSON 站點，把符合關鍵字的留下來
            for station in data:
                if (
                    keyword_clean in station.get("sna", "")
                    or keyword_clean in station.get("sarea", "")
                    or keyword_clean in station.get("ar", "")
                ):
                    matched_stations.append(station)

            # 防呆：如果找到太多站，只取前 10 站以避免超過模型處理上限
            matched_stations = matched_stations[:10]

            if not matched_stations:
                await emit_status("❌ 找不到相關站點", done=True)
                return f"抱歉，我從 YouBike 資料中找不到與「{keyword_clean}」相關的站點資訊。請試著縮短或更換搜尋的地標名稱！"

            # ========================
            # 任務三：組裝資料交給 AI 總結
            # ========================
            await emit_status("🤖 正在為您整理最終報告...")

            # 把 JSON 字典轉成白話文清單，這樣模型才看得懂
            station_info_text = "【YouBike 即時資料清單】\n"
            for s in matched_stations:
                station_name = s.get("sna", "").replace("YouBike2.0_", "")
                station_info_text += f"- 站名：{station_name}\n"
                station_info_text += f"  地址：{s.get('sarea','')}{s.get('ar','')}\n"
                station_info_text += (
                    f"  🚲 可借車輛數：{s.get('available_rent_bikes', 0)} 輛\n"
                )
                station_info_text += (
                    f"  🅿️ 可還空位數：{s.get('available_return_bikes', 0)} 位\n"
                )
                station_info_text += "---\n"

            # 給模型下達最終回答指令
            final_sys_prompt = (
                "你是熱心的台北市 YouBike 查詢小夥伴。請你根據以下提供的「YouBike 即時資料清單」，"
                "針對使用者的問題給予清楚、口語且帶有溫度的回答！\n"
                "重點提醒：\n"
                "1. 如果資料上顯示可借車輛為 0，請溫馨提醒使用者可能會借不到車。\n"
                "2. 如果有可還空位為 0，也請提醒使用者該站已經滿了無法還車。\n"
                "3. 排版請使用條列式讓畫面乾淨清爽。"
            )
            final_user_prompt = f"{station_info_text}\n\n[使用者的提問]：{user_message}"

            # 呼叫模型進行最終生成
            final_response = self.call_ollama(
                [
                    {"role": "system", "content": final_sys_prompt},
                    {"role": "user", "content": final_user_prompt},
                ],
                temperature=0.7,
            )

            await emit_status("✅ 查詢完成！", done=True)
            return final_response

        except Exception as e:
            await emit_status(f"❌ 發生錯誤", done=True)
            return f"執行過程中發生系統錯誤，請稍後再試。\n錯誤細節：`{str(e)}`"

```

---

<details>
<summary>💡 程式碼詳細說明（給 Python 初學者）</summary>

### 1. 使用 `urllib.request` 處理網路連線
過去常使用 `requests` 套件，但在部分環境下，我們可以直接使用 Python 內建的 `urllib` 函式庫，這樣可以確保程式即使在沒有額外安裝套件的環境中也能順利發送 `GET` (/youbike.json) 與 `POST` (/v1/chat/completions) 請求。

### 2. `__event_emitter__` 的非同步狀態列
透過 `await emit_status("...")`，我們能夠即時將當下的處理進度推送給前端介面。使用者會看到「處理中...」的跳動文字，不但能降低使用者的等待焦慮感，也非常具有未來科技感！

### 3. 多提示詞 (Prompt Chaining) 的概念
這裡示範了非常經典的「提示詞串聯」技巧：
- **第一個提示詞：** 扮演一個「萃取機」，我們要求模型嚴格且冷酷地只吐出「地名」這兩個字。
- **第二個提示詞：** 扮演一個「客服人員」，負責把我們用程式 (`for station in data`) 爬下來的硬梆梆資料，咀嚼後用溫馨的排版回饋給使用者。
</details>
