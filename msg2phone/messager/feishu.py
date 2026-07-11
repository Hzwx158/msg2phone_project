from .base import Messager
from pathlib import Path
import json
import requests


class FeishuMessager(Messager):
    FEISHU_TOKEN_URL = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal/"
    FEISHU_SEND_URL = "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id"


    def __init__(
        self,
        app_id: str,
        app_secret: str,
        user_open_id:str,
        msg_type: str = "text",
    ):
        self.app_id = app_id
        self.app_secret = app_secret
        self.user_open_id = user_open_id
        self.msg_type = msg_type

    def _get_tenant_access_token(self) -> str:
        response = requests.post(
            url=self.FEISHU_TOKEN_URL, 
            json={
                "app_id": self.app_id,
                "app_secret": self.app_secret,
            },
            headers={'Content-Type': 'application/json; charset=utf-8'}
        )
        data = response.json()
        if response.status_code != 200 or data.get("code", 0) != 0:
            raise RuntimeError(
                f"Failed to fetch Feishu access token: {response.status_code}\n{response.text}"
            )
        return data["tenant_access_token"]

    def info(self, title, msg, tags=None, log_dir: Path | None = None):
        print("Sending Feishu info...")

        title_text = self.ensure_str(title)
        message_text = self.ensure_str(msg)
        if tags:
            tag_str = " ".join(tags)
            content_text = f"{title_text}\n[{tag_str}]\n\n{message_text}"
        else:
            content_text = f"{title_text}\n\n{message_text}"

        if log_dir is not None and not log_dir.exists():
            log_dir.mkdir(parents=True, exist_ok=True)

        response = requests.post(
            self.FEISHU_SEND_URL,
            headers={"Authorization": f"Bearer {self._get_tenant_access_token()}"},
            json={
                "receive_id": self.user_open_id,
                "content": json.dumps({"text": content_text}),
                "msg_type": self.msg_type,
            },
        )

        reply = response.json()
        if response.status_code != 200 or reply.get("code", 0) != 0:
            raise RuntimeError(
                f"Failed to send Feishu message: {response.status_code} {response.text}"
            )

        if log_dir is not None:
            message_id = reply.get("data", {}).get("message_id", "feishu_message")
            with open(log_dir / f"{message_id}.json", "w") as log_file:
                log_file.write(response.text)


