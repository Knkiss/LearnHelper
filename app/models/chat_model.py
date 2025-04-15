from openai import OpenAI

class ChatModel:
    def __init__(self, model_type, key, model_name=None):
        self.model_type = model_type
        self.key = key
        self.model_name = model_name
        self.client = None
        self.select_model()

    def select_model(self):
        if self.model_type == "chatgpt":
            self.client = OpenAI(api_key=self.key)
        elif self.model_type == "qwen":
            self.client = OpenAI(
                api_key=self.key,
                base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
            )
        else:
            raise NotImplementedError(f"模型类型未支持: {self.model_type}")

    def get_answer(self, question: str, prompt=None):
        if prompt is None:
            prompt = "回答以下我的问题，以严谨简洁的回答给出答案和理由，随后明确答案是什么，不做与问题无关的扩展说明，不要使用latex或代码格式。"

        try:
            if self.model_name in ["qwen-vl-max"]:
                # 多模态图像输入（base64）
                img_base64 = question
                completion = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=[
                        {"role": "system", "content": [{"type": "text", "text": "You are a helpful assistant."}]},
                        {"role": "user", "content": [
                            {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img_base64}"}},
                            {"type": "text", "text": prompt}
                        ]}
                    ]
                )
            else:
                # 文本输入
                completion = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=[
                        {"role": "system", "content": prompt},
                        {"role": "user", "content": question}
                    ]
                )

            # ✅ 通用解析返回
            if completion.choices and completion.choices[0].message:
                return completion.choices[0].message.content
            else:
                return "[系统错误] 模型无有效返回内容"

        except Exception as e:
            return f"[模型调用异常] {str(e)}"