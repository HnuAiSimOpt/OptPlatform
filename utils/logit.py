# 日志级别对应数字
# 10:"DEBUG"
# 20:"INFO"
# 30:"WARNING"
# 40:"ERROR"
# 50:"CRITICAL"

# 通过项目索引 proj_idx 区分不同项目的日志器


import time
import logging

from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWidgets import QApplication 

class StreamHandler(QObject, logging.StreamHandler):
    """流数据处理器
    
    通过信号将日志信息输出在主界面的日志窗口
    """
    new_record = pyqtSignal(object)

    def __init__(self):
        super().__init__()

    def emit(self, record):
        # record: LogRecord类数据
        self.new_record.emit(record)

class TextBrowserLogger(QObject):
    """日志记录器"""
    def __init__(self, parent, file_name="log.log", logger_name=None, file_mode="w") -> None:
        """
        Args:
            parent (QWidget): MxDesign
            file_name (str, optional): 日志文件的输出位置. Defaults to "log.log".
            logger_name (str, optional): 日志器的名称. Defaults to None.
        """
        super().__init__()

        self._OptPlatform = parent
        self._text_browser = parent.textBrowser_log
        self.file_name = file_name  # 日志路径
        self.format = '%(asctime)s %(name)s-%(levelname)s : %(message)s'  # 日志规范格式
        self.datefmt = '%Y-%m-%d %X'
        self.file_mode = file_mode  # 覆盖模式 w  追加模式 a
        self.html = "<table>" \
                        "<tr>" \
                            "<td><img height=\"16\" src=\"{}\">" \
                            "<td style=\"vertical-align: middle;\"> &nbsp; {} &nbsp; </td>" \
                            "<td style=\"vertical-align: middle; color:{}\"> {} </td>" \
                        "</tr>" \
                    "</table>"  # 信息流格式: 图片--时间--颜色--消息
        
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(logging.DEBUG)
        self.logger.propagate = False  # 不向root logger汇报

        file_handler = logging.FileHandler(self.file_name, encoding='utf-8', mode=self.file_mode)  # 文件数据处理器
        file_handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter(self.format, self.datefmt)
        file_handler.setFormatter(formatter)

        stream_handler = StreamHandler()
        stream_handler.setLevel(logging.DEBUG)

        self.logger.addHandler(stream_handler)
        self.logger.addHandler(file_handler)

        stream_handler.new_record.connect(self.stream)

    def stream(self, record):
        """流数据输出显示

        由于存在多个项目, 包含项目信息的字符不在标准模板中, 且流数据日志会存在集中显示而文件数据日志需要分开写入的情况, 
        因此不好设置流数据的输出模板格式. 在这个函数中重新定义了流数据日志格式

        Args:
            record_msg (str): StreamHandler抽取的级别和消息
        """
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        level_name = record.levelname
        msg = record.msg  # 抽出输入字符串信息 
        
        msg = level_name + ": &nbsp; " + msg

        if level_name == "WARNING":
            html = self.html.format(":/pic/icons/警告.png", t, "orange", msg)
            self._text_browser.append(html)

        elif level_name == "ERROR":
            html = self.html.format(":/pic/icons/错误圈.png", t, "red", msg)
            self._text_browser.append(html)

        else:
            html = self.html.format(":/pic/icons/信息.png", t, "black", msg)
            self._text_browser.append(html)

        QApplication.processEvents()

         


