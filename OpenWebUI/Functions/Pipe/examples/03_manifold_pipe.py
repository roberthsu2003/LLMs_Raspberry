from typing import Union, Generator, Iterator

class Pipe:
    def __init__(self):
        self.type = "pipe"
        self.id = "manifold_pipe"
        self.name = "多模型組合包 (Manifold)"

    def pipes(self) -> list[dict]:
        """
        這是在 Manifold 模式下最重要的部分。
        回傳一個清單，包含你想在選單中顯示的模型 ID 與名稱。
        """
        return [
            {"id": "math_agent", "name": "數學專家 Agent"},
            {"id": "translator_agent", "name": "翻譯專家 Agent"},
        ]

    def pipe(self, body: dict) -> Union[str, Generator, Iterator]:
        # 判斷使用者目前選的是哪一個模型 ID
        model_id = body.get("model", "")
        user_message = body["messages"][-1]["content"]

        if model_id == "math_agent":
            return f"[數學模式] 正在計算：{user_message} ... 結果為 42"
        
        elif model_id == "translator_agent":
            return f"[翻譯模式] 翻譯結果：{user_message} (English version)"
        
        else:
            return "未知的模型 ID"
