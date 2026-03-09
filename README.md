# wxautox4 API

这是一个基于FastAPI开发的HTTP API服务，用于适配wxautox4的自动化操作。该服务提供了微信自动化操作的RESTful API接口，支持消息发送、群管理、好友管理等全部功能。

## 功能特性

- 微信消息发送与接收
- 群聊管理
- 好友管理
- 统一的认证机制
- 标准化的API响应格式
- 灵活的配置管理
- **全面支持wxautox4的所有功能**
- **完整的功能覆盖** - 会话管理、消息监听、朋友圈、好友管理等

## 技术栈

- **wxautox4** - 微信自动化基础库
- **FastAPI** - 现代化的Python Web框架
- **Pydantic** - 数据验证和设置管理
- **SQLite** - 数据存储（可配置其他数据库）

## 项目结构

```
wxauto-restful-api/
├── app/                    # 主应用目录
│   ├── api/               # API路由
│   │   └── v1/           # API版本1
│   ├── models/           # 数据模型
│   ├── services/         # 业务逻辑
│   ├── utils/            # 工具函数
│   │   └── wx_package_manager.py   # wxautox4包管理器
│   └── main.py           # 应用入口
├── config.yaml            # 主配置文件
├── run.py                 # 启动脚本
├── requirements.txt       # 项目依赖
└── schemas.json          # API模式定义（可选）
```

### 安装依赖

```bash
# 安装wxautox4
pip install wxautox4

# 或使用requirements.txt
pip install -r requirements.txt
```

> [!NOTE]
> 本项目专门为wxautox4设计，需要wxautox4 Plus版本

> [!IMPORTANT]
> **激活要求**：wxautox4需要激活后才能使用。请先使用以下方式激活：
> ```bash
> # 检查激活状态
> wxautox4 -k
>
> # 激活
> wxautox4 -a your-activation-code
> ```

## 配置管理

### 配置文件
项目使用 `config.yaml` 作为主配置文件，所有服务器设置都通过此文件管理：

```yaml
server:
  host: "0.0.0.0"  # 服务器监听地址
  port: 8000       # 服务器监听端口
  reload: true     # 是否启用热重载

auth:
  token: "your-secret-token-here"  # API认证密钥

database:
  type: "sqlite"  # 数据库类型
  sqlite:
    path: "./data/wxautox.db"  # SQLite数据库路径
```

### 手动模式
```bash
# 启动服务（使用配置文件中的设置）
python run.py

# 或使用uvicorn直接启动
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## API文档

启动服务后，可以通过以下地址访问API文档：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

**注意**：实际端口号请查看 `config.yaml` 中的 `server.port` 设置

## API接口

### 微信功能接口

#### 会话管理
- `POST /v1/wechat/getsession` - 获取会话列表
- `POST /v1/wechat/getsubwindow` - 获取指定子窗口
- `POST /v1/wechat/getallsubwindow` - 获取所有子窗口

#### 消息功能
- `POST /v1/wechat/send` - 发送消息
- `POST /v1/wechat/sendfile` - 发送文件
- `POST /v1/wechat/sendurlcard` - 发送URL卡片
- `POST /v1/wechat/getallmessage` - 获取当前窗口消息
- `POST /v1/wechat/gethistorymessage` - 获取历史消息

#### 监听功能
- `POST /v1/wechat/addlistenchat` - 添加监听
- `POST /v1/wechat/removelistenchat` - 移除监听
- `POST /v1/wechat/getnextnewmessage` - 获取新消息

#### 好友管理
- `POST /v1/wechat/getnewfriends` - 获取好友申请
- `POST /v1/wechat/newfriend/accept` - 接受好友申请
- `POST /v1/wechat/addnewfriend` - 添加新好友
- `POST /v1/wechat/getfriends` - 获取好友列表

#### 群聊管理
- `POST /v1/wechat/getrecentgroups` - 获取群聊列表

#### 页面控制
- `POST /v1/wechat/chatwith` - 切换聊天窗口
- `POST /v1/wechat/switch/chat` - 切换到聊天页面
- `POST /v1/wechat/switch/contact` - 切换到联系人页面

#### 朋友圈功能
- `POST /v1/wechat/moments` - 进入朋友圈
- `POST /v1/wechat/publishmoment` - 发送朋友圈

#### 账号信息
- `POST /v1/wechat/getmyinfo` - 获取我的信息
- `POST /v1/wechat/isonline` - 检查在线状态

### 系统接口
- `GET /v1/info/package` - 获取包信息

## 认证

所有API请求都需要在Header中包含有效的认证token：
```
Authorization: Bearer <your-token>
```

## 响应格式

所有API响应都遵循统一的格式：
```json
{
    "success": true,
    "message": "操作成功",
    "data": {}
}
```

## 配置说明

### 主要配置文件
- `config.yaml` - 主配置文件（包含所有服务器设置）
- `pyproject.toml` - 项目依赖配置

### 重要配置项
- `server.port` - 服务端口（默认8000）
- `server.host` - 服务器监听地址（默认0.0.0.0）
- `server.reload` - 热重载开关（默认true）
- `auth.token` - API访问令牌
- `database.type` - 数据库类型（默认sqlite）

## 开发说明

- 使用FastAPI框架开发
- 采用模块化设计
- 包含完整的类型注解
- 统一的错误处理机制
- 详细的API文档
- 灵活的配置管理

## 注意事项

- 请确保wxautox4已正确安装并激活
- 建议在开发环境中使用，生产环境请注意安全配置
- 注意保护API访问token
- 定期检查日志文件
- 服务部署需要管理员权限
- **重要**：wxautox4需要激活后才能使用
- **方法名**：wxautox4使用大写驼峰命名（如 `SendMsg`）

## 许可证

MIT License
