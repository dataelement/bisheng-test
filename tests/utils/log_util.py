import logging
import logging.handlers
import os
import time


# 日志输出工具封装
class LogUtil(object):
    def __init__(self):
        self.logger = logging.getLogger("")
        self.logger.handlers.clear()
        # 创建日志文件目录
        # output_path = os.environ.get('OUTPUT_PATH', '/app/output')
        output_path = os.environ.get('OUTPUT_PATH', '/Users/sara/Desktop/DataElem/dev/bisheng-test/output')

        logs_dir = "%s/logs" % output_path
        if os.path.exists(logs_dir) and os.path.isdir(logs_dir):
            pass
        else:
            os.mkdir(logs_dir)
        # 修改log保存位置
        timestamp = time.strftime("%Y%m%d", time.localtime())
        logfilename = '%sBiShengApiTest.txt' % timestamp
        logfilepath = os.path.join(logs_dir, logfilename)
        rotatingFileHandler = logging.handlers.RotatingFileHandler(
            filename=logfilepath,
            maxBytes=1024 * 1024 * 50,
            backupCount=5)

        # 设置输出格式
        formatter = logging.Formatter(
            '[%(asctime)s] [%(levelname)s] %(message)s', '%Y-%m-%d %H:%M:%S')
        rotatingFileHandler.setFormatter(formatter)
        # 控制台句柄
        console = logging.StreamHandler()
        console.setLevel(logging.NOTSET)
        console.setFormatter(formatter)
        # 添加内容到日志句柄中
        self.logger.addHandler(rotatingFileHandler)
        self.logger.addHandler(console)
        self.logger.setLevel(logging.INFO)

    def info(self, message):
        self.logger.info(message)

    def debug(self, message):
        self.logger.debug(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

