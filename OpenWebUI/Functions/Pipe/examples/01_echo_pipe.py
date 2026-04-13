from typing import Union, Generator, Iterator

class Pipe:
    def __init__(self):
        self.type = "pipe"
        self.id = "echo_pipe"
        self.name = "回聲模型 (Echo Pipe)"

    def pipe(self, body: dict) -> Union[str, Generator, Iterator]:
        # 從 body 中取得最後一則使用者訊息
        user_message = body["messages"][-1]["content"]

        # 直接回傳加工後的文字
        return f"【回聲回應】：{user_message}"
