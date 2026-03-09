# API 响应格式规范

本文档定义了 wxauto-restful-api 项目中所有接口的统一响应格式。

## 📋 目录

- [标准响应结构](#标准响应结构)
- [响应类型](#响应类型)
- [使用示例](#使用示例)
- [错误码规范](#错误码规范)
- [最佳实践](#最佳实践)

---

## 标准响应结构

所有 API 接口都遵循统一的响应格式：

```json
{
  "success": boolean,
  "message": string,
  "data": any
}
```

### 字段说明

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `success` | boolean | ✅ | 操作是否成功 |
| `message` | string | ✅ | 提示信息，成功或失败的描述 |
| `data` | any | ❌ | 返回数据，可以是对象、数组或 null |

---

## 响应类型

### 1. 成功响应

#### 基础成功响应
```json
{
  "success": true,
  "message": "操作成功",
  "data": null
}
```

#### 带数据成功响应
```json
{
  "success": true,
  "message": "获取成功",
  "data": {
    "key": "value"
  }
}
```

---

### 2. 列表数据响应

用于返回列表类型的接口，如获取会话列表、好友列表等。

#### 标准格式
```json
{
  "success": true,
  "message": "",
  "data": {
    "total": 100,
    "items": [
      {
        "id": "唯一标识",
        "name": "名称",
        "type": "类型",
        "...": "其他字段"
      }
    ]
  }
}
```

#### 字段说明
- `total`: 总数量
- `items`: 数据列表，每个元素包含 `id`、`name`、`type` 等基本字段

#### 示例接口
- `POST /api/v1/wechat/getallsubwindow` - 获取所有子窗口
- `GET /api/v1/wechat/getsession` - 获取会话列表
- `POST /api/v1/wechat/getrecentgroups` - 获取群聊列表
- `POST /api/v1/wechat/getfriends` - 获取好友列表
- `GET /api/v1/files/` - 获取文件列表

---

### 3. 单个对象响应

用于返回单个对象或实体的接口。

#### 标准格式
```json
{
  "success": true,
  "message": "获取成功",
  "data": {
    "item": {
      "id": "唯一标识",
      "...": "其他字段"
    }
  }
}
```

#### 字段说明
- `item`: 对象数据，包含实体的所有字段

#### 示例接口
- `GET /api/v1/files/{file_id}` - 获取文件信息
- `POST /api/v1/wechat/getsubwindow` - 获取子窗口
- `POST /api/v1/wechat/chatwith` - 切换聊天窗口
- `POST /api/v1/wechat/getmyinfo` - 获取我的信息
- `POST /api/v1/wechat/isonline` - 检查在线状态
- `POST /api/v1/wechat/moments` - 进入朋友圈

---

### 4. 消息数据响应

用于返回聊天消息的接口。

#### 标准格式
```json
{
  "success": true,
  "message": "",
  "data": {
    "chat_info": {
      "who": "联系人名称",
      "type": "friend/group",
      "...": "其他聊天信息"
    },
    "messages": [
      {
        "type": "消息类型",
        "content": "消息内容",
        "time": "时间戳",
        "...": "其他消息字段"
      }
    ]
  }
}
```

#### 字段说明
- `chat_info`: 聊天窗口信息
- `messages`: 消息列表

#### 示例接口
- `POST /api/v1/wechat/getallmessage` - 获取所有消息
- `POST /api/v1/wechat/gethistorymessage` - 获取历史消息
- `POST /api/v1/wechat/getnextnewmessage` - 获取新消息
- `POST /api/v1/chat/getallmessage` - 获取子窗口所有消息
- `POST /api/v1/chat/getnewmessage` - 获取子窗口新消息

---

### 5. 操作结果响应

用于执行增删改操作的接口。

#### 标准格式
```json
{
  "success": true,
  "message": "操作成功",
  "data": {
    "affected": 1,
    "result": {
      "额外结果信息": "可选"
    }
  }
}
```

#### 字段说明
- `affected`: 影响的行数或对象数
- `result`: 额外的结果信息（可选）

#### 示例接口
- `DELETE /api/v1/files/{file_id}` - 删除文件
- `POST /api/v1/wechat/send` - 发送消息
- `POST /api/v1/wechat/sendfile` - 发送文件

---

### 6. 错误响应

用于返回操作失败的错误信息。

#### 基础错误响应
```json
{
  "success": false,
  "message": "操作失败的描述",
  "data": null
}
```

#### 带错误详情的响应
```json
{
  "success": false,
  "message": "wxautox4未激活，无法使用微信功能",
  "data": {
    "error_code": "NOT_ACTIVATED",
    "solution": "请先运行: wxautox4 -a your-activation-code"
  }
}
```

#### 字段说明
- `error_code`: 错误代码（可选）
- `solution`: 解决方案（可选）

---

## 使用示例

### 前端 JavaScript 示例

```javascript
// 统一的 API 调用函数
async function callApi(url, options = {}) {
  const response = await fetch(url, options);
  const result = await response.json();

  // 检查操作是否成功
  if (!result.success) {
    // 处理错误
    console.error(result.message);
    if (result.data && result.data.error_code) {
      console.error('错误码:', result.data.error_code);
      console.error('解决方案:', result.data.solution);
    }
    throw new Error(result.message);
  }

  return result.data;
}

// 列表数据示例
async function getSessions() {
  const data = await callApi('/api/v1/wechat/getsession', {
    method: 'POST'
  });

  console.log(`总计 ${data.total} 个会话`);
  data.items.forEach(item => {
    console.log(`${item.name} (${item.type})`);
  });
}

// 单个对象示例
async function getMyInfo() {
  const data = await callApi('/api/v1/wechat/getmyinfo', {
    method: 'POST'
  });

  console.log('我的信息:', data.item);
}

// 消息数据示例
async function getAllMessages(who) {
  const data = await callApi('/api/v1/wechat/getallmessage', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ who })
  });

  console.log(`与 ${data.chat_info.who} 的聊天`);
  console.log(`共 ${data.messages.length} 条消息`);
}
```

### Python 后端示例

```python
from app.utils.response_builder import (
    success, error, list_response,
    single_object, message_data, operation_result
)

# 成功响应
return success(message="操作成功", data={"key": "value"})

# 错误响应
return error(
    message="操作失败",
    error_code="OPERATION_FAILED",
    solution="请检查参数后重试"
)

# 列表数据
return list_response(items=[...], total=100)

# 单个对象
return single_object(obj={...}, message="获取成功")

# 消息数据
return message_data(messages=[...], chat_info={...})

# 操作结果
return operation_result(affected=1, message="删除成功")
```

---

## 错误码规范

### 通用错误码

| 错误码 | 说明 | 解决方案 |
|--------|------|----------|
| `NOT_ACTIVATED` | wxautox4 未激活 | 运行 `wxautox4 -a your-activation-code` |
| `NOT_INITIALIZED` | 微信实例未初始化 | 调用 `/api/v1/wechat/initialize` 接口 |
| `FILE_NOT_FOUND` | 文件不存在 | 检查文件 ID 是否正确 |
| `CHAT_NOT_FOUND` | 聊天窗口不存在 | 检查联系人名称是否正确 |
| `SUBWINDOW_NOT_FOUND` | 子窗口不存在 | 检查子窗口名称是否正确 |
| `SWITCH_FAILED` | 切换窗口失败 | 重试或检查微信状态 |
| `MOMENTS_FAILED` | 进入朋友圈失败 | 检查网络连接和微信状态 |

---

## 最佳实践

### 1. 响应构建

**✅ 推荐：使用响应构建工具**
```python
from app.utils.response_builder import list_response

return list_response(items=items, total=total)
```

**❌ 不推荐：手动构建响应**
```python
return APIResponse(
    success=True,
    message="",
    data={"total": total, "items": items}
)
```

### 2. 错误处理

**✅ 推荐：使用标准错误响应**
```python
from app.utils.response_builder import error

return error(
    message="操作失败",
    error_code="OPERATION_FAILED"
)
```

**❌ 不推荐：只返回错误消息**
```python
return APIResponse(success=False, message="操作失败")
```

### 3. 前端解析

**✅ 推荐：统一的解析逻辑**
```javascript
const { success, message, data } = response;
if (!success) {
  throw new Error(message);
}
// 使用 data
```

**❌ 不推荐：针对每个接口写不同逻辑**
```javascript
if (endpoint === '/xxx') {
  // 特殊处理
} else if (endpoint === '/yyy') {
  // 特殊处理
}
```

---

## 版本历史

- **v1.0** (2026-03-09) - 初始版本，统一所有接口响应格式

---

*文档更新时间: 2026-03-09*
