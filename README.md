# 🖊 快速入门
首先，下载这份代码: `pip install .`

## 1 配置config

以下配置任选N种写入配置yaml文件即可，写好yaml文件、运行过最开始的 `pip install .` 之后，命令行里运行这个命令：

```bash
msg2phone-cli config --file "你刚才创建的yaml文件路径"
```

下面是yaml文件内容的各种选择：


### 1.1 Server酱配置

先获取Server酱的配置：

- 🚀 在[Server酱](https://sc3.ft07.com/)这个网站里注册一个账号，然后去官网下载他们的APP
- 🤗 查看并复制API URL（[在这里查看](https://sc3.ft07.com/sendkey)

然后随便新建一个yaml文件，写入如下内容：
```yaml
your-config-proxy-name:
  - servercyann
  - url: "填入上面复制好的API URL"
```

### 1.2 飞书配置

先创建飞书开放平台应用，并在“企业内部开发”或“自建应用”中获取以下参数：

- `app_id`
- `app_secret`
- `user_open_id`：接收者用户的 `open_id`

然后随便新建一个 yaml 文件，写入如下内容：

```yaml
your-feishu-config-name:
  - FeishuMessager
  - app_id: "你的 app_id"
    app_secret: "你的 app_secret"
    user_open_id: "你的 user_open_id"
```

## 2 发送信息

```bash
msg2phone-cli send -t "训练完成" -m "任务已结束" --tags tag1 tag2 --log-dir ./logs
```

如果尚未安装包，可以用模块方式运行相同命令：

```bash
python -m msg2phone.cli send -t "Title" -m "Message body"
```

## 3 代码用法
主要是通过`InfoExitHandler`类，提供了上下文管理器和函数装饰器两种方式。

上下文管理器：
```python
from msg2phone import InfoExitHandler
with InfoExitHandler(title='test', msg='test msg', tags=['test']) as handler:
  #do something
  handler.msg = "abcabc" # 可以动态更改发送内容
  a = input()
  handler.msg = lambda : f"也可以设置成一个返回字符串的函数，会自动调用: a={a}"
print("Msg has been sent after `with` block ended")
```

函数装饰器：
```python
from msg2phone import InfoExitHandler
@InfoExitHandler(...) #同上
def func():
  ...

func() #函数运行结束后就会发送信息
```

## 4 扩展

### 4.1 Messager扩展
Messager类是用于发送消息的类，所有子类必须重写其`info`方法：
```python
from msg2phone.messager import Messager
class ServerCyannMessager(Messager):
    __cfg_path = Path(__file__).parents[1] / "config.yaml"

    def __init__(self, url:str):
        self.url_template = url + "?title={title}&desp={desp}&tags={tags}"
    
    def info(self, title, msg, tags, log_dir):
        print("Sending info...")
        need_log = log_dir is not None
        if need_log and not log_dir.exists():
            log_dir.mkdir(parents=True, exist_ok=True)
        response = requests.get(self.url_template.format(
            title=title(),
            desp=msg(),
            tags='|'.join(tags)
        ))
        reply = json.loads(response.text)
        if need_log:
            pushid = reply["data"]["pushid"]
            with open(log_dir / f"{pushid}.txt", 'w') as log_file:
                log_file.write(response.text)
```
### 4.2 ExitHandler扩展

略