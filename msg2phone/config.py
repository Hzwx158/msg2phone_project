from pathlib import Path
from typing import Any
import yaml

CONFIG_PATH = Path(__file__).parent / "config.yaml"

def get_config_file(default_real_file:Path|None = None):
    if not CONFIG_PATH.exists():
        if not CONFIG_PATH.parent.exists():
            CONFIG_PATH.parent.mkdir(parents=True)
        if default_real_file is not None:
            CONFIG_PATH.symlink_to(default_real_file)
        else:
            CONFIG_PATH.touch()
    return CONFIG_PATH

def relink_config_file(real_file:Path):
    CONFIG_PATH.unlink(True)
    CONFIG_PATH.symlink_to(real_file)

def update_config(new_cfg:dict[str, Any], **kwargs):
    new_cfg.update(kwargs)
    with open(get_config_file(), 'r') as f:
        cfg = yaml.safe_load(f)
    cfg.update(new_cfg)
    with open(get_config_file(), 'w') as f:
        yaml.safe_dump(cfg, f)
