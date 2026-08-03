from typing import Callable
import requests
import json
from pathlib import Path
from msg2phone.exit_handler import ExitHandler
from msg2phone.messager import Messager, MessageString
import yaml

def is_main_process(cached=True) -> bool:
    """Check if the current process is the main process.
    Args:
        cached (bool): Whether to cache the result. Default is True.
    Returns:
        bool: True if the current process is the main process, False otherwise.
    """
    try:
        from torch import distributed as tdst
        if cached and hasattr(is_main_process, ":is_main_process"):
            return getattr(is_main_process, ":is_main_process")
        
        res = not tdst.is_initialized() or tdst.get_rank() == 0
        if cached:
            setattr(is_main_process, ":is_main_process", res)
        return res
    except ImportError:
        return True

class InfoExitHandler(ExitHandler):
    def __init__(
        self, 
        title:MessageString, 
        success_msg:MessageString, 
        log_dir:Path|None = None, 
        tags:list[str] = None,
        name:str = "default",
    ):
        """
        注册python程序退出函数用的类，你可以自己继承ExitHandler写自己的事件
        Args:
            title(str): 标题
            success_msg(str): 成功运行的消息
            log_dir(str): 日志记录，可以为None
            tags(list[str]): 消息的tag
            name(str): 配置名称
        """
        super().__init__()
        self.title = title
        self.success_msg = success_msg
        self.log_dir = log_dir
        self.tags = tags or []
        self.messager = Messager.from_config(name)

    def on_success_exit(self):
        if not is_main_process():
            return
        
        self.messager.info(
            title=self.title, 
            msg=self.success_msg, 
            log_dir=self.log_dir, 
            tags=self.tags,
        )
    
    def on_fail_exit(self, *exc_args):
        if not is_main_process():
            return
        msg = self.format_error(*exc_args)
        self.messager.info(
            title=self.title, 
            msg=f"```shell\n{msg}\n```", 
            log_dir=self.log_dir, 
            tags=self.tags,
        )
    