import argparse
import sys
from pathlib import Path
from typing import List
import yaml

CONFIG_PATH = Path(__file__).parent / "config.yaml"


def load_config():
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            cfg = yaml.safe_load(f)
            return cfg or {}
    return {}


def save_config(cfg: dict):
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        yaml.safe_dump(cfg, f, default_flow_style=False, allow_unicode=True)


def cmd_config(args: argparse.Namespace) -> int:
    """Handler for `config` subcommand: set the url."""
    try:
        cfg = load_config()
        cfg["url"] = args.url
        save_config(cfg)
        print(f"Saved url to {CONFIG_PATH}")
        return 0
    except Exception as e:
        print("Error writing config:", e, file=sys.stderr)
        return 2


def cmd_send(args: argparse.Namespace) -> int:
    """Handler for `send` subcommand: call msg2phone.info.info()."""
    try:
        # Import lazily so CLI works even if requests isn't available for config-only flows
        from .info import info as send_info
        log_dir = Path(args.log_dir) if args.log_dir else None
        tags: List[str] = args.tags or []
        # Ensure message formatting consistent with info() expectation
        send_info(args.title, args.message, log_dir, tags)
        return 0
    except Exception as e:
        print("Error sending info:", e, file=sys.stderr)
        return 3


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="msg2phone-cli", description="msg2phone command line tool")
    sub = parser.add_subparsers(title="commands", dest="command")

    # config subcommand
    p_cfg = sub.add_parser("config", help="Configure package default URL")
    p_cfg.add_argument("--url", required=True, help="The base url to push messages (e.g. https://.../send/...)")
    p_cfg.set_defaults(func=cmd_config)

    # send subcommand
    p_send = sub.add_parser("send", help="Send a message via configured URL (calls info)")
    p_send.add_argument("-t", "--title", required=True, help="Title of the message")
    p_send.add_argument("-m", "--message", required=True, help="Message body (markdown supported)")
    p_send.add_argument("--log-dir", default=None, help="Directory to save response logs (optional)")
    p_send.add_argument("--tags", nargs="*", help="Tags for the message, space separated")
    p_send.set_defaults(func=cmd_send)

    return parser


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if not hasattr(args, "func"):
        parser.print_help()
        return 1
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
