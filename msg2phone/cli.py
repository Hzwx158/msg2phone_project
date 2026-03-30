import argparse
import sys
from pathlib import Path
import yaml
import typer

app = typer.Typer(help="Remote Message to Phone Helper")

CONFIG_PATH = Path(__file__).parent / "config.yaml"

def load_config() -> dict:
    if not CONFIG_PATH.exists():
        return {}
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
        return cfg or {}


def save_config(cfg: dict) -> None:
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        yaml.safe_dump(cfg, f, default_flow_style=False, allow_unicode=True)


@app.command(help="Configure package default URL")
def config(
    url: str = typer.Option(..., help="The base url to push messages (e.g. https://.../send/...)")
):
    """Handler for `config` subcommand: set the url."""
    try:
        cfg = load_config()
        cfg["url"] = url
        save_config(cfg)
        print(f"Saved url to {CONFIG_PATH}")
        
    except Exception as e:
        print("Error writing config:", e, file=sys.stderr)
        raise typer.Exit(code=2)

@app.command(help="Send a message via configured URL (calls info)")
def send(
    title:str = typer.Option(..., "--title", "-t", help="Title of the message"),
    message:str = typer.Option(..., "--message", "-m", help="Message body (markdown supported)"),
    log_dir:Path|None = typer.Option(None, help="Directory to save response logs (optional)"),
    tags:list[str] = typer.Option([], help="Tags for the message, space separated"),
):
    """Handler for `send` subcommand: call msg2phone.info.info()."""
    try:
        # Import lazily so CLI works even if requests isn't available for config-only flows
        from .info import info as send_info
        # Ensure message formatting consistent with info() expectation
        send_info(title, message, log_dir, tags)
    except Exception as e:
        print("Error sending info:", e, file=sys.stderr)
        raise typer.Exit(3)


if __name__ == "__main__":
    raise SystemExit(app())
