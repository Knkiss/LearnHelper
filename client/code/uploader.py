import cv2
import keyboard
import numpy as np
import pyautogui
import requests
import os

from code.logger import logger
from code.utils import get_tmp_dir


class ScreenshotUploader:
    def __init__(self, server_url, user_id):
        self.server_url = server_url
        self.user_id = user_id

        self.first_x, self.first_y = None, None
        self.second_x, self.second_y = None, None
        self._bind_keys()

        self.save_path = os.path.join(get_tmp_dir(), 'screenshot.jpg')

    def _bind_keys(self):
        logger.info("正在绑定热键，请使用以下按键：")
        keyboard.add_hotkey('1', self._record_top_left)
        keyboard.add_hotkey('2', self._record_bottom_right)
        keyboard.add_hotkey('3', self._mode_text)
        keyboard.add_hotkey('4', self._mode_only_show)
        keyboard.add_hotkey('5', self._mode_image)
        logger.info("绑定完成！\n按 1 设置左上角\n按 2 设置右下角\n按 3 上传文本回答\n按 4 上传仅展示\n按 5 上传图像回答")

    def _record_top_left(self):
        self.first_x, self.first_y = pyautogui.position()
        logger.info(f"已记录左上角位置：({self.first_x}, {self.first_y})")

    def _record_bottom_right(self):
        self.second_x, self.second_y = pyautogui.position()
        logger.info(f"已记录右下角位置：({self.second_x}, {self.second_y})")

    def _region_valid(self):
        if None in [self.first_x, self.first_y, self.second_x, self.second_y]:
            logger.warning("请先设置完整的截图区域（按 1 和 2）")
            return False
        if self.first_x >= self.second_x or self.first_y >= self.second_y:
            logger.warning("截图区域无效，请确保左上角小于右下角")
            return False
        return True

    def _capture_screenshot(self):
        try:
            img = pyautogui.screenshot(region=(
                self.first_x,
                self.first_y,
                self.second_x - self.first_x,
                self.second_y - self.first_y
            ))
            img = cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)
            cv2.imwrite(self.save_path, img)
            return True
        except Exception as e:
            logger.error(f"截图失败：{str(e)}")
            return False

    def _mode_text(self):
        logger.info("开始截图并上传（进行识别）...")

        if not self._region_valid():
            return

        if not self._capture_screenshot():
            return

        try:
            with open(self.save_path, 'rb') as img_file:
                files = {'file': img_file}
                data = {'mode': 'text', 'user_id': self.user_id}
                response = requests.post(self.server_url, files=files, data=data)

            if response.status_code == 200:
                logger.info("上传成功！服务端返回：" + str(response.json()))
            else:
                logger.warning(f"上传失败：状态码 {response.status_code}，响应：{response.text}")
        except Exception as e:
            logger.error(f"上传过程中出错：{str(e)}")

    def _mode_only_show(self):
        logger.info("开始截图并上传（仅用于展示）...")

        if not self._region_valid():
            return

        if not self._capture_screenshot():
            return

        try:
            with open(self.save_path, 'rb') as img_file:
                files = {'file': img_file}
                data = {'mode': 'show', 'user_id': self.user_id}
                response = requests.post(self.server_url, files=files, data=data)

            if response.status_code == 200:
                logger.info("仅展示截图上传成功！服务端返回：" + str(response.json()))
            else:
                logger.warning(f"上传失败：状态码 {response.status_code}，响应：{response.text}")
        except Exception as e:
            logger.error(f"上传过程中出错：{str(e)}")


    def _mode_image(self):
        logger.info("开始截图并上传（进行图像识别）...")

        if not self._region_valid():
            return

        if not self._capture_screenshot():
            return

        try:
            with open(self.save_path, 'rb') as img_file:
                files = {'file': img_file}
                data = {'mode': 'image', 'user_id': self.user_id}
                response = requests.post(self.server_url, files=files, data=data)

            if response.status_code == 200:
                logger.info("上传成功！服务端返回：" + str(response.json()))
            else:
                logger.warning(f"上传失败：状态码 {response.status_code}，响应：{response.text}")
        except Exception as e:
            logger.error(f"上传过程中出错：{str(e)}")
