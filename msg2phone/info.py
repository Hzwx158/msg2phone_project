from typing import Callable, Optional
import requests
import json
from pathlib import Path
import torch
from .exit_handler import ExitHandler
import yaml

def _get_url_template(url:str=None):
    if url is None:
        cfg_path = Path(__file__).parent/"config.yaml"
        if not cfg_path.exists():
            return None
        with open(cfg_path, 'r') as f:
            cfg = yaml.safe_load(f)
        if ("url" not in cfg) or (cfg["url"] is None):
            return None
        url = cfg["url"]
    return url + "?title={title}&desp={desp}&tags={tags}"

def info(title:str, msg:str, log_dir:Optional[Path], tags:list[str], url:str=None):
    """
    通知
    Args:
        title(str): 标题
        msg(str): 消息，满足markdown格式，我替你进行了把一行空格换成两个的操作
        log_dir(Path): 日志记录，可以为None
        tags(list[str]): 标签 
        url(str): Server酱给的链接, 默认为config.yaml里的
    """
    url_template = _get_url_template(url)
    if url_template is None:
        return
    print("Sending info...")
    need_log = log_dir is not None
    if need_log and not log_dir.exists():
        log_dir.mkdir(parents=True, exist_ok=True)
    response = requests.get(url_template.format(
        title=title, desp=msg,
        tags='|'.join(tags)
    ))
    reply = json.loads(response.text)
    if need_log:
        pushid = reply["data"]["pushid"]
        with open(log_dir / f"{pushid}.txt", 'w') as log_file:
            log_file.write(response.text)
    # return reply["code"]

class InfoExitHandler(ExitHandler):
    def __init__(self, title:str, success_msg:str|Callable[[], str], log_dir:Path|None, tags:list[str]):
        """
        注册python程序退出函数用的类，你可以自己继承ExitHandler写自己的事件
        Args:
            title(str): 标题
            success_msg(str): 成功运行的消息
            log_dir(str): 日志记录，可以为None
            tags(list[str]): 消息的tag
        """
        super().__init__()
        self.title = title
        self.success_msg = success_msg
        self.log_dir = log_dir
        self.tags = tags

    def on_success_exit(self):
        if torch.distributed.is_initialized() and torch.distributed.get_rank() != 0:
            return
        if isinstance(self.success_msg, str):
            success_msg = self.success_msg.replace('\n', '\n\n')
        else:
            success_msg = self.success_msg().replace('\n', '\n\n')
        info(self.title, success_msg, self.log_dir, self.tags)
    
    def on_fail_exit(self, *exc_args):
        if torch.distributed.is_initialized() and torch.distributed.get_rank() != 0:
            return
        msg = self.format_error(*exc_args)
        info(self.title, f"```shell\n{msg}\n```", self.log_dir, self.tags)
    