import keyboard

from code.uploader import ScreenshotUploader
from code.utils import init_or_load_config


if __name__ == '__main__':
    user_id, server_url = init_or_load_config()
    uploader = ScreenshotUploader(server_url=f"http://{server_url}/qa/upload", user_id=user_id)
    keyboard.wait()
