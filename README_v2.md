# wxauto-restful-api v2.0

## 🎯 核心改进

### ✅ 已解决的问题
1. **服务启动时自动初始化 WeChat 实例**
2. **提供获取实例的 API 接口**
3. **未激活时服务正常启动，核心功能返回友好提示**
4. **修复 AttributeError 错误**

---

## 🚀 快速开始

### 1. 启动服务
```bash
python run.py
```

**启动时会自动尝试初始化微信实例**

### 2. 检查状态
```bash
curl http://127.0.0.1:8000/api/v1/wechat/status
```

### 3. 手动初始化（如果需要）
```bash
curl -X POST http://127.0.0.1:8000/api/v1/wechat/initialize
```

### 4. 使用核心功能
```bash
curl -X POST http://127.0.0.1:8000/api/v1/wechat/send \
  -H "Content-Type: application/json" \
  -d '{"msg": "Hello", "who": "文件传输助手"}'
```

---

## 📡 新增 API 接口

### 1. 获取/初始化微信实例
```
POST /api/v1/wechat/initialize
```

**响应示例：**
```json
{
  "success": true,
  "message": "成功初始化 1 个微信客户端实例",
  "data": {
    "status": "initialized",
    "clients_count": 1,
    "clients": [{"nickname": "星浩", "logged_in": true}]
  }
}
```

### 2. 查看实例状态
```
GET /api/v1/wechat/status
```

**响应示例：**
```json
{
  "success": true,
  "message": "微信实例运行中，当前有 1 个客户端",
  "data": {
    "status": "running",
    "clients_count": 1,
    "clients": ["星浩"]
  }
}
```

---

## 📖 详细文档

- **启动逻辑说明：** [STARTUP_LOGIC.md](STARTUP_LOGIC.md)
- **改进总结：** [IMPROVEMENTS_SUMMARY.md](IMPROVEMENTS_SUMMARY.md)
- **错误修复：** [FIX_SUMMARY.md](FIX_SUMMARY.md)
- **API 文档：** http://127.0.0.1:8000/docs

---

## 🎨 启动流程

```
启动服务
   ↓
自动初始化（startup_event）
   ↓
   ├─ 成功 → 实例就绪 → 可以使用核心功能
   │
   └─ 失败 → 服务仍启动 → 返回友好提示
               ↓
         可调用 /initialize 接口重试
```

---

## ⚠️ 错误处理

### 实例未就绪时
所有核心功能接口会返回：
```json
{
  "success": false,
  "message": "微信实例未就绪。请先调用 /api/v1/wechat/initialize 接口...",
  "data": {
    "error": "NOT_ACTIVATED",
    "solution": "请先激活 wxautox4"
  }
}
```

**注意：** 此类错误不会被记录到日志（预期行为）

---

## 🛠️ 测试

运行测试脚本：
```bash
python test_startup.py
```

**测试内容：**
- ✅ 状态查询
- ✅ 自动初始化
- ✅ 实例获取
- ✅ 错误处理

---

## 📝 版本历史

### v2.0.0 (2026-03-09)
- ✅ 启动时自动初始化
- ✅ 提供手动初始化接口
- ✅ 提供状态查询接口
- ✅ 优化错误提示
- ✅ 修复 AttributeError 错误
- ✅ 完善文档

### v1.0.0
- 基础功能
- 延迟初始化
- 错误处理不够友好

---

## 💡 使用建议

### 开发环境
1. 确保微信已登录
2. 启动服务（会自动初始化）
3. 直接使用核心功能

### 生产环境
1. 启动服务
2. 调用 `/status` 检查状态
3. 如未就绪，调用 `/initialize` 初始化
4. 定期健康检查

---

## 📞 技术支持

- **API 文档：** http://127.0.0.1:8000/docs
- **错误日志：** `logs/errors/`
- **详细文档：** 查看 STARTUP_LOGIC.md

---

**维护者：** wxauto-restful-api Team
**版本：** v2.0.0
**更新日期：** 2026-03-09
