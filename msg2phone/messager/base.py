from abc import ABC, abstractmethod

from typing import Callable, Literal, TypeVar
from pathlib import Path
import yaml
from msg2phone.config import get_config_file
from importlib import import_module


MessageString = str | Callable[[], str]

class Messager(ABC):

    __subclasses:set[type] = set()

    def __init_subclass__(cls):
        Messager.__subclasses.add(cls)

    @staticmethod
    def ensure_str(m:MessageString)->str:
        return m if isinstance(m, str) else m()
    
    @abstractmethod
    def info(
        self, 
        title:MessageString, 
        msg:MessageString,
        tags:list[str] = None, 
        log_dir:Path|None = None, 
    ) -> None:
        pass

    @staticmethod
    def from_config(name:str) -> "Messager":
        with open(get_config_file(), "r") as f:
            cfg = yaml.safe_load(f)
        messager_name, kwargs = cfg[name]
        for t in Messager.__subclasses:
            # print(t.__name__)
            if messager_name == t.__name__:
                return t(**kwargs)


