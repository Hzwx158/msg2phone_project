# 📱 msg2phone_project

`msg2phone` 是一个极简、可扩展的通知推送工具。它可以帮助你在代码运行结束、抛出异常或在命令行中，将通知（如“训练完成”、“任务报错”）快速推送到你的手机（如 **Server酱**、**飞书** 等）。

## ✨ 特性

* 🛠 **多通道支持**：原生支持 Server酱、飞书，且极其容易自定义扩展。
* 💻 **命令行友好**：一句话发送通知，轻松集成到 Shell 脚本。
* 🐍 **优雅的代码集成**：提供 **上下文管理器（`with`）** 和 **装饰器（`@`）**，任务跑完/报错自动通知。
* ⚙️ **无缝配置**：基于 YAML 的轻量级配置管理，一次配置，全局生效。

---

## 🖊 快速入门

### 1. 安装

首先，克隆/下载代码到本地，并在项目根目录下执行安装：

```bash
cd msg2phone_project
pip install .

```

---

### 2. 配置 Config

`msg2phone` 采用全局配置机制。你可以将以下配置任选一种（或多种）写入你的 `config.yaml` 文件中。

写好 YAML 文件后，运行以下命令将其导入系统（一次导入，全局生效）：

```bash
msg2phone-cli config --file "你的yaml文件路径"

```

#### 2.1 选项 A：Server酱配置（推送至微信）

1. 🚀 在 [Server酱官网](https://sc3.ft07.com/) 注册账号，并下载其官方 APP。
2. 🤗 登录后，查看并复制你的 **API URL (SendKey)**（[在此查看](https://sc3.ft07.com/sendkey)）。
3. 新建一个 `config.yaml`（名字任意），写入以下内容：
```yaml
# 这里的名字可以自定义，后续代码或命令行中会用到
my-serverchan-config:
  - ServerCyannMessager
  - url: "填入你复制的 API URL (例如 https://sctapi.ft07.com/xxxx.send)"

```



#### 2.2 选项 B：飞书配置（推送至群聊/个人）

1. 前往 [飞书开放平台](https://open.feishu.cn/) 创建一个企业内部自建应用。
2. 获取该应用的 `app_id` 和 `app_secret`。
3. 获取接收人（或群聊）的 `user_open_id`。
4. 新建一个 `config.yaml`（名字任意），写入以下内容：
```yaml
my-feishu-config:
  - FeishuMessager
  - app_id: "你的 app_id"
    app_secret: "你的 app_secret"
    user_open_id: "你的 user_open_id"

```



---

## 🚀 命令行发送信息

配置完成后，你可以在任何地方通过命令行直接发送消息：

```bash
msg2phone-cli send -t "训练完成" -m "任务已结束" \
  --tags tag1 tag2 \ 
  --log-dir ./logs \ 
  -n yaml文件里的某个配置名（my-feishu-config等，默认叫default）

```

后面的参数不是必填

> 💡 **小贴士**：如果你在开发阶段不想全局安装包，也可以使用 Python 模块方式直接运行：
> ```bash
> python -m msg2phone.cli send -t "Title" -m "Message body"
> 
> ```
> 
> 

---

## 🐍 Python 代码用法

### 3.1 上下文管理器（with）：执行结束后自动发消息

非常适合包裹一整段训练或高耗时任务。支持在运行过程中动态修改消息内容。

```python
from msg2phone import InfoExitHandler

# name 传入你在 yaml 里配置的名称
with InfoExitHandler(
    title='Model Training Status', 
    success_msg='Training finished successfully!', 
    tags=['AI', 'Train'], 
    name='my-feishu-config'  # 对应 YAML 中的配置名
) as handler:
    # 1. 模拟你的核心业务
    # do_something()
    
    # 2. 支持在运行期间动态修改发送内容
    handler.msg = "Epoch 10/100 completed..." 
    
    # 3. 甚至可以传入一个函数（自动动态求值）
    a = 100
    handler.msg = lambda: f"Task completed dynamically! Final score: a={a}"

print("Msg has been sent automatically after the `with` block finished!")

```

### 3.2 函数装饰器（@）：函数调用后自动发消息

直接装饰你的入口函数，函数执行完后自动推送。

```python
from msg2phone import InfoExitHandler

@InfoExitHandler(
    title='Backup Job', 
    success_msg='Database backup complete!', 
    name='my-serverchan-config'
)
def run_backup():
    # 你的业务代码
    print("Backing up database...")

# 函数运行结束后就会自动发送通知
run_backup() 

```

### 3.3 纯消息接口（Messager）：随时随地单发消息

不依赖任何生命周期，只是单纯想在代码某处塞一个消息推送。

```python
from msg2phone import Messager

# 直接读取配置初始化
m = Messager.from_config("my-feishu-config")
m.info(title='Alert', msg='Low memory warning!', tags=['system'])

```

---

## 🛠 进阶扩展

`msg2phone` 拥有极佳的扩展性，你可以轻松定制属于你自己的推送通道。

### 4.1 扩展一个新的 Messager (推送通道)

所有的自定义 Messager 都必须继承自 `Messager` 基类，并重写 `info` 方法：

```python
from msg2phone.messager import Messager

class MyMessager(Messager):

    def __init__(self, user_name): 
        # 可自定义任意入参，无需强制调用 super().__init__()
        self.user_name = user_name
    
    def info(self, title, msg, tags, log_dir): 
        # 在这里实现你自定义通道的发送逻辑（例如调用别的 API、发邮件等）
        print(f"Sending message to {self.user_name}: [{title}] {msg}")

```

**如何使用它？**
只需在你的 `config.yaml` 配置文件中写上对应的类名和参数：

```yaml
my-custom-protocol:
  - MyMessager  # 你的 Messager 类名
  - user_name: "GitHub_User" # 对应你 __init__ 里的参数

```

最后，运行更新配置命令即可全局生效：

```bash
msg2phone-cli config --file "你刚才的yaml文件"
msg2phone-cli send -t "Test" -m "Test mine" -n my-custom-protocol
```

### 4.2 扩展 ExitHandler

*(暂略，敬请期待)*