import time
import queue
import threading

from app import logger
from app.models.ocr_model import OCRModel
from app.models.chat_model import ChatModel
from app.utils.status_store import user_status, update_user_status

# OCR 任务并发控制
active_task_count = 0
task_lock = threading.Lock()

# OCR 模型池（最多 4 并发）
OCR_POOL_SIZE = 4
ocr_model_pool = queue.Queue(maxsize=OCR_POOL_SIZE)
for _ in range(OCR_POOL_SIZE):
    ocr_model_pool.put(OCRModel())


def process_image_no_ocr(user_id, img_base64, chat_model: ChatModel):
    global active_task_count
    with task_lock:
        active_task_count += 1
    logger.info(f"[图问答] 用户 {user_id} 提交任务（并发数：{active_task_count}）")

    start_time = time.time()
    try:
        update_user_status(user_id, "🤖 正在调用多模态大模型")

        answer = chat_model.get_answer(img_base64)
        logger.info(f"[图问答] Qwen 多模态回答完成，用户 {user_id}")

        user_status[user_id]["ocr"] = "无需OCR"
        user_status[user_id]["answer"] = answer
        update_user_status(user_id, "✅ 回答完成（数字键5）")

    except Exception as e:
        logger.exception(f"[图问答] 用户 {user_id} 异常")
        update_user_status(user_id, "❌ 处理失败", error=str(e))

    finally:
        with task_lock:
            active_task_count -= 1
        duration = round(time.time() - start_time, 2)
        logger.info(f"✅ 图问答任务完成：用户 {user_id}（耗时 {duration}s），并发数：{active_task_count}")


def process_image_ocr(user_id, img_np, chat_model: ChatModel):
    global active_task_count
    with task_lock:
        active_task_count += 1
    logger.info(f"[OCR问答] 用户 {user_id} 提交任务（并发数：{active_task_count}）")

    start_time = time.time()
    ocr_model = None

    try:
        ocr_model = ocr_model_pool.get(timeout=10)
        logger.info(f"[OCR问答] OCR 模型借出，用户 {user_id}，池剩余：{ocr_model_pool.qsize()}")

        update_user_status(user_id, "🔍 正在进行 OCR 识别")

        question = ocr_model.get_question_np(img_np)
        logger.info(f"[OCR问答] OCR 完成，用户 {user_id}，问题：{question}")

        update_user_status(user_id, "🤖 正在调用大模型")

        answer = chat_model.get_answer(question)
        logger.info(f"[OCR问答] Qwen 回答完成，用户 {user_id}")

        user_status[user_id]["ocr"] = question
        user_status[user_id]["answer"] = answer
        update_user_status(user_id, "✅ 回答完成（数字键3）")

    except Exception as e:
        logger.exception(f"[OCR问答] 用户 {user_id} 异常")
        update_user_status(user_id, "❌ 处理失败", error=str(e))

    finally:
        if ocr_model:
            ocr_model_pool.put(ocr_model)
            logger.info(f"[OCR问答] OCR 模型归还，用户 {user_id}，池剩余：{ocr_model_pool.qsize()}")

        with task_lock:
            active_task_count -= 1
        duration = round(time.time() - start_time, 2)
        logger.info(f"✅ OCR问答任务完成：用户 {user_id}（耗时 {duration}s），并发数：{active_task_count}")
