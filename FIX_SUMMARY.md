# Fix Summary: WeChat Service AttributeError

## Problem
The application was throwing an `AttributeError: 'NoneType' object has no attribute 'GetSession'` error when calling WeChat API endpoints. This occurred because:

1. The `get_wechat()` function returned `None` when WeChat failed to initialize
2. The `get_session()` method (and other methods) didn't check for `None` before calling methods on the `wx` object
3. This caused `AttributeError` which was logged as an error, even though it's an expected condition (WeChat not activated)

## Solution
Implemented an exception-based approach to handle WeChat initialization failures:

### 1. Created Custom Exception (`app/services/wechat_service.py`)
```python
class WeChatNotInitializedError(Exception):
    """微信实例未初始化异常"""
    pass
```

### 2. Modified `get_wechat()` Function
Changed from returning `None` on failure to raising `WeChatNotInitializedError`:
- Provides clear error messages
- Forces proper error handling
- Includes helpful hints for users

### 3. Updated Error Handler (`app/utils/error_handler.py`)
Modified both `async_wrapper` and `sync_wrapper` to:
- Catch `WeChatNotInitializedError` specially
- Return user-friendly error response without logging as an error
- Include helpful information about activation

### 4. Updated `get_wechat_subwin()` Function
Added proper exception handling for the new exception type.

## Benefits

1. **Better Error Messages**: Users get clear, actionable error messages
2. **Cleaner Logs**: Expected errors (like WeChat not activated) are not logged as errors
3. **Consistent Handling**: All WeChat operations now handle initialization failures uniformly
4. **Type Safety**: Functions that expect a `WeChat` instance no longer need to check for `None`

## Files Modified

1. `app/services/wechat_service.py`
   - Added `WeChatNotInitializedError` exception class
   - Modified `get_wechat()` to raise exception instead of returning `None`
   - Updated `get_wechat_subwin()` to catch the new exception
   - Added explicit None checks in `get_session()` and `get_session_sync()` methods

2. `app/utils/error_handler.py`
   - Modified `async_wrapper()` to handle `WeChatNotInitializedError`
   - Modified `sync_wrapper()` to handle `WeChatNotInitializedError`

## Testing

Verified that:
1. The code imports without errors
2. The error handler correctly catches and processes `WeChatNotInitializedError`
3. Error responses are properly formatted with helpful information

## Example Error Response

When WeChat is not activated, users now receive:
```json
{
  "success": false,
  "message": "wxautox4未激活，无法使用微信功能。请先运行: wxautox4 -a your-activation-code",
  "data": {
    "error": "NOT_ACTIVATED",
    "solution": "请先激活 wxautox4"
  }
}
```

This is not logged as an error, keeping the error logs clean for actual issues.
