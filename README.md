# 快速入门
- 🚀 在[Server酱](https://sc3.ft07.com/)这个网站里注册一个账号，然后去官网下载他们的APP
- 🖊 下载这份代码。
- 🤗 在代码的`config.yaml`文件里写上你得到的API URL（[在这里查看](https://sc3.ft07.com/sendkey)）
- 💻 使用方式用两种，一种是命令行，一种是自己写代码里


## 配置 URL（命令行）

安装包后你可以使用命令行工具 `msg2phone-cli` 来配置或发送消息。

配置 URL（示例 PowerShell）：

```
msg2phone-cli config --url "https://example.com/send/abcd"
```

发送信息（示例 PowerShell）：

```shell
msg2phone-cli send -t "训练完成" -m "任务已结束" --tags tag1 tag2 --log-dir ./logs
```

如果尚未安装包，可以用模块方式运行相同命令：

```shell
python -m msg2phone.cli config --url "https://example.com/send/abcd"
python -m msg2phone.cli send -t "Title" -m "Message body"
```

命令会把 `url` 写入包内的 `msg2phone/config.yaml`（如果不存在会创建或覆盖原有 `url`）。
