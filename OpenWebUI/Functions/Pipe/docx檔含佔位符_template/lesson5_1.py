"""
title: 履歷表單填寫助手
author: YourName
version: 1.0
description: 使用 Gemini API 收集使用者輸入，填入 template_form.docx 並以 Base64 下載連結回傳
requirements: docxtpl, google-genai>=1.0.0
"""

import os
import io
import json
import re
import base64
from docxtpl import DocxTemplate
from google import genai
from google.genai import types
from pydantic import BaseModel, Field


TEMPLATE_PATH = "/app/backend/data/uploads/template_form_fixed.docx"

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
"""


class Pipe:
    class Valves(BaseModel):
        GEMINI_API_KEY: str = Field(default="", description="Gemini API Key")
        GEMINI_MODEL: str = Field(default="gemini-2.5-flash", description="Gemini 模型名稱")

    def __init__(self):
        self.valves = self.Valves()

    def _api_key(self):
        return self.valves.GEMINI_API_KEY or os.environ.get("GEMINI_API_KEY", "")

    def _model_name(self):
        return self.valves.GEMINI_MODEL or os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")

    def _save_and_get_url(self, data):
        """儲存檔案並回傳下載路徑"""
        context = {field: data.get(field, "") for field in FIELDS}
        doc = DocxTemplate(TEMPLATE_PATH)
        doc.render(context)
        filename = "履歷表_{}.docx".format(data.get("name", "output"))
        output_path = "/app/backend/data/uploads/{}".format(filename)
        doc.save(output_path)
        return filename, output_path

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

    def _download_html(self, b64, filename):
        mime = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        # HTML base64 下載連結
        return (
            '<a href="data:{};base64,{}" download="{}">'
            "📄 點此下載 {}</a>"
        ).format(mime, b64, filename, filename)

    def _extract_action(self, text):
        match = re.search(r"```json\s*(\{.*?\})\s*```", text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(1))
            except Exception:
                pass
        return None

    async def pipe(self, body, __user__=None, __event_emitter__=None):
        api_key = self._api_key()
        if not api_key:
            return "❌ 請設定 GEMINI_API_KEY"

        messages = body.get("messages", [])
        if not messages:
            return "❌ 沒有收到訊息"

        try:
            client = genai.Client(api_key=api_key)

            history = []
            for msg in messages[:-1]:
                role = "user" if msg["role"] == "user" else "model"
                history.append(
                    types.Content(role=role, parts=[types.Part(text=msg["content"])])
                )

            history.append(
                types.Content(role="user", parts=[types.Part(text=messages[-1]["content"])])
            )

            response = client.models.generate_content(
                model=self._model_name(),
                contents=history,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                    automatic_function_calling=types.AutomaticFunctionCallingConfig(
                        disable=True
                    ),
                ),
            )

            reply_text = response.text

            # 檢查是否產生表單
            action = self._extract_action(reply_text)
            if action and action.get("action") == "generate_form":
                form_data = action.get("data", {})
                b64, filename = self._generate_docx_base64(form_data)
                clean = re.sub(r"```json.*?```", "", reply_text, flags=re.DOTALL).strip()

                mime = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                data_uri = "data:{};base64,{}".format(mime, b64)
                download_link = "\n\n---\n✅ **表單已產生**：\n\n[📥 點擊此處立即下載 {}]({})".format(filename, data_uri)

                return clean + download_link

            return reply_text

        except Exception as e:
            return "❌ 發生錯誤：{}".format(str(e))
