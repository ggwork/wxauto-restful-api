# wxauto-restful-api 启动逻辑说明

## 📋 目录
- [启动流程](#启动流程)
- [API 接口](#api-接口)
- [错误处理](#错误处理)
- [使用示例](#使用示例)

---

## 🚀 启动流程

### 1. 服务启动（`run.py`）
```bash
python run.py
```

### 2. 自动初始化（`app/main.py`）
服务启动时会触发 `startup_event`，自动调用微信实例初始化：

```python
@app.on_event("startup")
async def startup_event():
    from app.services.init import initialize_wechat_on_startup
    initialize_wechat_on_startup()
```

### 3. 初始化逻辑（`app/services/init.py`）

#### 初始化尝试流程：

```
┌─────────────────────────────────────┐
│   服务启动，触发 startup_event       │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│   检查 wxautox4 是否已激活          │
└──────────────┬──────────────────────┘
               │
        ┌──────┴──────┐
        │             │
    已激活        未激活
        │             │
        ▼             ▼
┌───────────────┐  ┌─────────────────┐
│ 获取微信实例  │  │ 返回失败，提示  │
│ 缓存到全局    │  │ 需要先激活      │
└───────┬───────┘  └─────────────────┘
        │
        ▼
┌─────────────────────────────────────┐
│   服务启动完成（无论成功或失败）     │
└─────────────────────────────────────┘
```

#### 可能的启动结果：

**✅ 成功场景：**
```
============================================================
🚀 启动时初始化微信实例
============================================================
🔍 正在检测微信客户端...
✅ 成功初始化 1 个微信客户端实例
   - 星浩
============================================================
```

**⚠️ 失败场景 1 - 未激活：**
```
============================================================
🚀 启动时初始化微信实例
============================================================
🔍 正在检测微信客户端...
❌ wxautox4 未激活
💡 激活方法：
   wxautox4 -a your-activation-code
   或在网页中调用 /api/v1/wechat/initialize 接口
============================================================
```

**⚠️ 失败场景 2 - 微信未登录：**
```
============================================================
🚀 启动时初始化微信实例
============================================================
🔍 正在检测微信客户端...
⚠️  未检测到微信客户端
💡 请确保微信已登录，然后调用获取实例接口
============================================================
```

---

## 🔌 API 接口

### 1. 获取/初始化微信实例

**接口：** `POST /api/v1/wechat/initialize`

**说明：**
- 检测微信是否已激活
- 获取微信实例并全局缓存
- 供后续核心功能使用

**请求：** 无需参数

**响应示例：**

成功：
```json
{
  "success": true,
  "message": "成功初始化 1 个微信客户端实例",
  "data": {
    "status": "initialized",
    "clients_count": 1,
    "clients": [
      {
        "nickname": "星浩",
        "logged_in": true
      }
    ]
  }
}
```

已就绪（重复调用）：
```json
{
  "success": true,
  "message": "微信实例已就绪，当前有 1 个客户端",
  "data": {
    "status": "ready",
    "clients_count": 1,
    "clients": ["星浩"]
  }
}
```

失败：
```json
{
  "success": false,
  "message": "未检测到微信客户端，请确保微信已登录",
  "data": {
    "status": "failed",
    "error": "INITIALIZATION_FAILED",
    "solution": "请确保微信已登录，或先激活 wxautox4"
  }
}
```

### 2. 查看实例状态

**接口：** `GET /api/v1/wechat/status`

**说明：** 查看微信实例当前的初始化状态

**请求：** 无需参数

**响应示例：**

运行中：
```json
{
  "success": true,
  "message": "微信实例运行中，当前有 1 个客户端",
  "data": {
    "status": "running",
    "clients_count": 1,
    "clients": ["星浩"],
    "initialized": true,
    "attempted": true
  }
}
```

未就绪：
```json
{
  "success": false,
  "message": "微信实例未就绪",
  "data": {
    "status": "not_ready",
    "clients_count": 0,
    "clients": [],
    "initialized": true,
    "attempted": true,
    "solution": "请调用 /api/v1/wechat/initialize 接口初始化"
  }
}
```

---

## ⚠️ 错误处理

### 核心功能调用时的错误处理

当微信实例未就绪时，所有核心功能接口会返回统一的友好提示：

**响应格式：**
```json
{
  "success": false,
  "message": "微信实例未就绪。请先调用 /api/v1/wechat/initialize 接口获取实例。确保微信已登录，如提示未激活请运行: wxautox4 -a your-activation-code",
  "data": {
    "error": "NOT_ACTIVATED",
    "solution": "请先激活 wxautox4"
  }
}
```

**注意：** 此类错误不会被记录到错误日志，因为这是预期的业务逻辑，而非系统错误。

---

## 💡 使用示例

### 场景 1：正常启动流程

```bash
# 1. 启动服务
python run.py

# 输出：
# ============================================================
# 🚀 启动时初始化微信实例
# ============================================================
# 🔍 正在检测微信客户端...
# ✅ 成功初始化 1 个微信客户端实例
#    - 星浩
# ============================================================

# 2. 服务已就绪，可以直接使用核心功能
# 例如：调用发送消息接口
POST /api/v1/wechat/send
{
  "msg": "测试消息",
  "who": "文件传输助手"
}
```

### 场景 2：启动时未激活

```bash
# 1. 启动服务
python run.py

# 输出：
# ============================================================
# 🚀 启动时初始化微信实例
# ============================================================
# ❌ wxautox4 未激活
# 💡 激活方法：
#    wxautox4 -a your-activation-code
# ============================================================

# 2. 服务仍会启动，但核心功能不可用
# 访问 http://127.0.0.1:8000/docs 查看 API 文档

# 3. 先激活 wxautox4
wxautox4 -a your-activation-code

# 4. 调用获取实例接口
POST /api/v1/wechat/initialize

# 5. 现在可以使用核心功能了
```

### 场景 3：启动时微信未登录

```bash
# 1. 启动服务
python run.py

# 输出：
# ============================================================
# 🚀 启动时初始化微信实例
# ============================================================
# ⚠️  未检测到微信客户端
# 💡 请确保微信已登录，然后调用获取实例接口
# ============================================================

# 2. 服务已启动，但实例未就绪

# 3. 登录微信

# 4. 手动调用获取实例接口
POST /api/v1/wechat/initialize

# 5. 现在可以使用核心功能了
```

### 场景 4：使用 API 客户端

```javascript
// 1. 检查状态
GET /api/v1/wechat/status

// 2. 如果未就绪，初始化实例
POST /api/v1/wechat/initialize

// 3. 使用核心功能
POST /api/v1/wechat/send
{
  "msg": "Hello",
  "who": "文件传输助手"
}
```

---

## 📊 架构设计

### 全局状态管理（`app/services/init.py`）

```python
# 全局缓存字典
WxClient = {}  # {nickname: WeChat实例}

# 初始化状态标志
_wechat_initialized = False      # 是否已完成初始化流程
_initialization_attempted = False  # 是否已尝试过初始化
```

### 错误处理机制（`app/services/wechat_service.py`）

```python
class WeChatNotInitializedError(Exception):
    """微信实例未初始化异常"""
    pass

def get_wechat(wxname: str) -> WeChat:
    """获取微信实例，失败时抛出 WeChatNotInitializedError"""
    # ... 初始化逻辑
```

错误处理器（`app/utils/error_handler.py`）会捕获此异常并返回友好提示，不会记录为错误日志。

---

## 🎯 最佳实践

### 开发环境
1. 先激活 wxautox4
2. 登录微信
3. 启动服务（会自动初始化）
4. 直接使用核心功能

### 生产环境
1. 启动服务
2. 调用 `/api/v1/wechat/status` 检查状态
3. 如果未就绪，调用 `/api/v1/wechat/initialize`
4. 使用核心功能
5. 定期调用 `/api/v1/wechat/status` 进行健康检查

### 监控建议
```python
# 定期健康检查
import requests

def health_check():
    response = requests.get("http://127.0.0.1:8000/api/v1/wechat/status")
    data = response.json()

    if not data['success']:
        # 尝试重新初始化
        requests.post("http://127.0.0.1:8000/api/v1/wechat/initialize")

    return data
```

---

## 🔧 故障排查

### 问题 1：服务启动失败
**检查：** Python 环境、依赖包安装
```bash
pip install -r requirements.txt
```

### 问题 2：初始化失败 - 未激活
**解决：** 激活 wxautox4
```bash
wxautox4 -a your-activation-code
```

### 问题 3：初始化失败 - 未检测到微信
**解决：** 确保微信已登录

### 问题 4：核心功能返回错误
**检查：** 调用 `/api/v1/wechat/status` 查看状态
```bash
curl -X GET http://127.0.0.1:8000/api/v1/wechat/status
```

如果未就绪，调用初始化接口：
```bash
curl -X POST http://127.0.0.1:8000/api/v1/wechat/initialize
```

---

## 📝 版本历史

### v2.0.0 (当前版本)
- ✅ 启动时自动初始化微信实例
- ✅ 提供手动获取实例的 API 接口
- ✅ 提供状态查询接口
- ✅ 优化错误提示，区分预期错误和系统错误
- ✅ 未激活时服务仍能正常启动

### v1.0.0
- ❌ 启动时未自动初始化
- ❌ 缺少获取实例接口
- ❌ 错误提示不够友好

---

## 📞 技术支持

如有问题，请查看：
1. API 文档：`http://127.0.0.1:8000/docs`
2. 错误日志：`logs/errors/`
3. 本文档
