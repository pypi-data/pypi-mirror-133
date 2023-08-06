import uuid
from functools import wraps
import inspect
from configparser import ConfigParser
import time

from enum import Enum


class GattinoEvent(Enum):
    EVENT_START = "EVENT_START"
    EVENT_TICK = "EVENT_TICK"
    EVENT_EXIT = "EVENT_EXIT"


class Gattino:
    # 应用id
    appid = None
    # 配置文件
    conf_file = None
    # 配置文件节点
    conf_key = "gattino"
    # 应用id文件
    pid_file = "app.pid"
    # 命令行参数
    argv = None
    # 配置文件
    conf = {}
    # 扩展文件包
    ext = []
    # 配置工具
    cfg = None
    # 事件列表
    events = {}

    is_running = True

    def __init__(self, appid=None, conf=None, argv=None):
        self.appid = appid if appid else str(uuid.uuid1())
        self.conf_file = conf if conf else "app.conf"
        self.argv = argv if argv else None
        for item in GattinoEvent:
            self.events[item.value] = []

    """
    从配置文件读取配置信息
    """

    def load_conf(self):
        self.cfg = ConfigParser()
        self.cfg.read(self.conf_file)
        self.conf = dict(self.cfg.items(self.conf_key))
    """
    从配置函数读取配置信息
    """

    def load_conf_read_args(self, func, args):
        return dict(zip(inspect.signature(func).parameters.keys(), args))

    def init(self, func):
        @wraps(func)
        def wrapped_function(*args, **kwargs):
            # 初始化appid
            with open(self.pid_file, 'w') as f:
                f.write(self.appid)
            # 从配置文件加载
            self.load_conf()
            print(f"配置文件:[{self.conf_file}]加载[{len(self.conf.items())}]项配置信息")
            # 加载扩展配置
            for item in self.ext:
                item_conf = item.load_conf()
                print(
                    f"扩展配置文件:[{item.conf_key}]|[{self.conf_file}]加载[{len(item_conf)}]项配置信息")
                self.conf.update(item_conf)
            # 从参数中读取配置
            args_conf = self.load_conf_read_args(func, args)
            print(f"配置函数:[{func.__name__}]加载[{len(args_conf.items())}]项配置信息")
            self.conf.update(args_conf)
            # 执行配置函数
            return func(*args, **kwargs)
        return wrapped_function

    """
    启动装饰器
    """

    def run(self, func):
        @wraps(func)
        def wrapped_function(*args, **kwargs):
            self.is_running = True
            print(f"应用[{self.appid}]启动")
            [item(None)
             for item in self.events[GattinoEvent.EVENT_START.value]]
            while self.is_running:
                ts = time.time()
                [item(ts)
                 for item in self.events[GattinoEvent.EVENT_TICK.value]]
                func(*args, **kwargs)
            [item(None) for item in self.events[GattinoEvent.EVENT_EXIT.value]]
            print(f"应用[{self.appid}]退出")
            return
        return wrapped_function
