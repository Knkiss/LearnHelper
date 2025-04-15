from paddlex import create_pipeline

class OCRModel:
    def __init__(self):
        self.model = create_pipeline(pipeline='OCR')

    def get_question_np(self, img_np):
        result = self.model.predict(img_np)
        ans = []
        for i in result:
            ans = i['rec_text']
        return str('\n'.join(ans))
