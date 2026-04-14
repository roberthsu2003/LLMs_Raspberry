"""
title: 履歷表單填寫助手 (Ollama 版)
author: YourName
version: 1.0
description: 使用地端 Ollama 收集使用者輸入，填入 template_form.docx 並以 Base64 下載連結回傳
requirements: docxtpl, requests
"""

import os
import io
import json
import re
import base64
import requests
from docxtpl import DocxTemplate
from pydantic import BaseModel, Field


TEMPLATE_PATH = "/app/backend/data/uploads/template_form.docx"

FIELDS = [
    "name", "id_number", "phone", "email", "gender", "marital_status",
    "school_1", "graduation_year_1",
    "school_2", "graduation_year_2",
    "school_3", "graduation_year_3",
    "school_4", "graduation_year_4",
    "programming_languages", "other_languages", "skills",
    "company_1", "position_1", "years_1", "duties_1",
    "company_2", "position_2", "years_2", "duties_2",
    "company_3", "position_3", "years_3", "duties_3",
    "溝通能力_excellent", "溝通能力_good", "溝通能力_fair",
    "團隊協作_excellent", "團隊協作_good", "團隊協作_fair",
    "問題解決_excellent", "問題解決_good", "問題解決_fair",
    "領導能力_excellent", "領導能力_good", "領導能力_fair",
    "學習能力_excellent", "學習能力_good", "學習能力_fair",
    "special_needs", "remarks",
    "confirm_accuracy", "consent_recruitment", "consent_notification", "consent_privacy",
    "signer_name", "signature_date", "signature", "signature_notes",
]

SYSTEM_PROMPT = """你是一個履歷表單填寫助手。
你的任務是透過對話收集使用者的個人資料，然後將資料填入履歷表單。

表單欄位說明：
- name: 姓名
- id_number: 身分證字號
- phone: 電話
- email: 電子郵件
- gender: 性別
- marital_status: 婚姻狀況
- school_1~4: 學校名稱（最多4所）
- graduation_year_1~4: 畢業年份
- programming_languages: 程式語言技能
- other_languages: 其他語言能力
- skills: 其他技能
- company_1~3: 公司名稱（最多3間）
- position_1~3: 職位
- years_1~3: 任職年資
- duties_1~3: 工作職責
- 溝通能力/團隊協作/問題解決/領導能力/學習能力 各有 _excellent/_good/_fair（填 ✓ 或空白）
- special_needs: 特殊需求
- remarks: 備註
- confirm_accuracy/consent_recruitment/consent_notification/consent_privacy: 同意聲明（填 ✓ 或空白）
- signer_name: 簽名人姓名
- signature_date: 簽名日期
- signature: 簽名
- signature_notes: 簽名備註

請用繁體中文與使用者對話，逐步收集資料。
當你認為已收集足夠資料可以產生表單時，請輸出一個 JSON 區塊，格式如下：
```json
{"action": "generate_form", "data": { ...所有欄位的值... }}
```
未填寫的欄位請填入空字串 ""。
【非常重要】：當你最後準備輸出 JSON 時，請「直接」輸出 JSON 區塊，不要在前綴加上多餘的提醒對話！
"""


class Pipe:
    class Valves(BaseModel):
        OLLAMA_API_URL: str = Field(default="http://127.0.0.1:11434/v1/chat/completions", description="Ollama API 端點 (相容 OpenAI 格式)")
        OLLAMA_MODEL: str = Field(default="gpt-oss:20b-cloud", description="您本機的 Ollama 模型名稱")

    def __init__(self):
        self.valves = self.Valves()

    def _api_url(self):
        return self.valves.OLLAMA_API_URL or os.environ.get("OLLAMA_API_URL", "http://127.0.0.1:11434/v1/chat/completions")

    def _model_name(self):
        return self.valves.OLLAMA_MODEL or os.environ.get("OLLAMA_MODEL", "gemma4:31b-cloud")

    def _generate_docx_base64(self, data):
        context = {field: data.get(field, "") for field in FIELDS}
        doc = DocxTemplate(TEMPLATE_PATH)
        doc.render(context)
        buf = io.BytesIO()
        doc.save(buf)
        buf.seek(0)
        b64 = base64.b64encode(buf.read()).decode("utf-8")
        filename = "履歷表_{}.docx".format(data.get("name", "output"))
        return b64, filename

    def _download_link(self, b64, filename):
        mime = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        data_uri = "data:{};base64,{}".format(mime, b64)
        return "[📥 點擊此處立即下載 {}]({})".format(filename, data_uri)

    def _extract_action(self, text):
        match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(1))
            except Exception:
                pass
        
        # 嘗試尋找無 markdown tag、直接裸露的 JSON
        match = re.search(r"(\{.*\})", text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(1))
            except Exception:
                pass

        return None

    async def pipe(self, body, __user__=None, __event_emitter__=None):
        api_url = self._api_url()
        if not api_url:
            return "❌ 請設定 OLLAMA_API_URL"

        messages = body.get("messages", [])
        if not messages:
            return "❌ 沒有收到訊息"

        try:
            # 建立發送給 Ollama 的訊息格式
            payload_messages = [{"role": "system", "content": SYSTEM_PROMPT}]
            for msg in messages:
                payload_messages.append({"role": msg["role"], "content": msg["content"]})

            payload = {
                "model": self._model_name(),
                "messages": payload_messages,
                "stream": False,
                # 許多在地端模型為了確保不亂說話，可以調低 temperature
                "temperature": 0.2 
            }

            headers = {
                "Content-Type": "application/json"
            }

            if __event_emitter__:
                await __event_emitter__({
                    "type": "status",
                    "data": {"description": "🧠 正在呼叫 Ollama 進行地端推論 (大型模型可能需時數十秒至數分鐘，請耐心等候...)", "done": False}
                })

            response = requests.post(api_url, json=payload, headers=headers, timeout=300)
            response.raise_for_status()

            if __event_emitter__:
                await __event_emitter__({
                    "type": "status",
                    "data": {"description": "✅ Ollama 推論完成，正在產生回應！", "done": True}
                })

            # 解析 OpenAI 相容格式的回應
            result = response.json()
            reply_text = result["choices"][0]["message"]["content"]

            # 檢查是否產生表單
            action = self._extract_action(reply_text)
            if action and action.get("action") == "generate_form":
                form_data = action.get("data", {})
                
                clean = re.sub(r"```(?:json)?.*?```", "", reply_text, flags=re.DOTALL).strip()
                if clean == reply_text or clean.startswith("{"):
                    clean = re.sub(r"\{.*\}", "", reply_text, flags=re.DOTALL).strip()

                try:
                    b64, filename = self._generate_docx_base64(form_data)
                    markdown_link = self._download_link(b64, filename)
                    success_msg = f"\n\n---\n✅ **表單已產生**：\n\n{markdown_link}\n"
                    
                    if __event_emitter__:
                        # 透過事件發射器直接推送 Markdown 連結
                        await __event_emitter__({
                            "type": "message",
                            "data": {"content": success_msg}
                        })
                        return clean
                    else:
                        return clean + success_msg + "\n\n[系統未開啟 event_emitter，無法渲染載點]"
                        
                except Exception as docx_err:
                    err_msg = (
                        f"\n\n---\n❌ **產生 Word 檔案失敗**\n\n"
                        f"**錯誤原因**：讀取或渲染範本檔 `{TEMPLATE_PATH}` 時失敗。\n\n"
                        f"**詳細訊息**：`{str(docx_err)}`\n\n"
                        f"> 💡 **開發提示**：系統可能遇到了 `TemplateSyntaxError: Expected an expression` 錯誤，這通常代表被掛載的 `.docx` 範本中包含了「空白的」或「語法錯誤的」 Jinja2 標籤（例如不小心打出了 `{{{{ }}}}` 但中間沒內容）。請用 Word 開啟您的上傳檔案，仔細檢查是否有殘留的大括號標記！"
                    )
                    if __event_emitter__:
                        await __event_emitter__({
                            "type": "message",
                            "data": {"content": err_msg}
                        })
                        return clean
                    else:
                        return clean + err_msg

            return reply_text

        except requests.exceptions.ConnectionError:
            return f"❌ 無法連線至 Ollama 主機：{api_url}。請確認 Ollama 正在運行且開啟 OLLAMA_HOST=0.0.0.0。"
        except Exception as e:
            import traceback
            tb = traceback.format_exc()
            return "❌ 發生錯誤：{}\n\n```python\n{}\n```".format(str(e), tb)
