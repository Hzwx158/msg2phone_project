from pprint import pprint
from pathlib import Path
import yaml
import typer
from msg2phone.messager import Messager
from msg2phone.config import update_config, relink_config_file, get_config_file

app = typer.Typer(help="Remote Message to Phone Helper")


@app.command(help="Configure package default URL")
def config(
    file: Path|None = typer.Option(
        None, 
        "--file", "-f",
        help="Update from file (e.g. ~/msg2phone-config.yml"),
    relink_to: Path|None = typer.Option(
        None, 
        "--relink-to", "--relink_to", "-r",
        help="Relink the config file to this file"),
    show:bool = typer.Option(
        False, 
        "--show",  
        help="Show now config"),
    clear:bool = typer.Option(
        False,
        "--clear",
        help="Clear all config"
    )
):
    """Handler for `config` subcommand: set the url."""
    if show:
        with open(get_config_file(), "r") as f:
            cfg = yaml.safe_load(f)
        pprint(cfg)
        return
     
    if clear:
        with open(get_config_file(), "w") as f:
            f.write("\n")
        print("Clear all config")
        return
    
    if relink_to is not None:
        assert relink_to.exists(), f"{relink_to} not exist"
        relink_config_file(relink_to)
        return
    
    if file is None:
        name = input("input new config name: ")
        messager_name = input("input messager name: ")
        kwargs = {}
        i=0
        while True:
            k = input(f"input KEY of args[{i}] ('*' to quit): ")
            if k == '*':
                break
            v = input(f"input VAL of args[{i}]: ")
            kwargs[k] = v
        new_cfg = {name:[messager_name, kwargs]}
        
    else:
        with open(file, 'r') as f:
            new_cfg = yaml.safe_load(f)
    update_config(new_cfg)
    

@app.command(help="Send a message via configured URL (calls info)")
def send(
    name:str = typer.Option("default", "--name", "-n", help="Messager name"),
    title:str = typer.Option(..., "--title", "-t", help="Title of the message"),
    message:str = typer.Option(..., "--message", "-m", help="Message body (markdown supported)"),
    log_dir:Path|None = typer.Option(None, help="Directory to save response logs (optional)"),
    tags:list[str] = typer.Option([], help="Tags for the message, space separated"),
):
    """Handler for `send` subcommand: call msg2phone.info.info()."""
    messager = Messager.from_config(name)
    messager.info(
        title=title, 
        msg=message, 
        log_dir=log_dir, 
        tags=tags,
    )

if __name__ == '__main__':
    app()