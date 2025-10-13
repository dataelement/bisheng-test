import os

from dotenv import load_dotenv

from .cookie_manager import CookieManager

# 加载环境变量（从 .env 文件或系统环境）
load_dotenv()

# 初始化 CookieManager 并自动登录
_cookie_manager = CookieManager()
if not _cookie_manager.cookies:
    _cookie_manager.get_cookies()  # 自动从环境变量读取凭据

# 暴露接口
get_cookies = _cookie_manager.get_cookies
session = _cookie_manager.session
base_url = _cookie_manager.base_url