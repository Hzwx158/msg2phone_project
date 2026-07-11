from .base import Messager
from pathlib import Path
import yaml, json
import requests


class ServerCyannMessager(Messager):

    def __init__(self, url:str):
        self.url_template = url + "?title={title}&desp={desp}&tags={tags}"
    
    def info(self, title, msg, tags, log_dir):
        print("Sending info...")
        need_log = log_dir is not None
        if need_log and not log_dir.exists():
            log_dir.mkdir(parents=True, exist_ok=True)
        response = requests.get(self.url_template.format(
            title=self.ensure_str(title),
            desp=self.ensure_str(msg),
            tags='|'.join(tags)
        ))
        reply = json.loads(response.text)
        if need_log:
            pushid = reply["data"]["pushid"]
            with open(log_dir / f"{pushid}.txt", 'w') as log_file:
                log_file.write(response.text)

