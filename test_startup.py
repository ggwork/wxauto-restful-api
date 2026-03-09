#!/usr/bin/env python3
"""
测试微信实例初始化流程
"""
import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
sys.path.insert(0, str(Path(__file__).parent.parent))


def test_initialization():
    """测试初始化流程"""
    print("="*70)
    print("Testing WeChat Initialization Flow")
    print("="*70)
    print()

    from app.services.init import initialize_wechat_on_startup, get_initialization_status

    # 1. 查看初始状态
    print("1. Initial Status:")
    status = get_initialization_status()
    print(f"   initialized: {status['initialized']}")
    print(f"   attempted: {status['attempted']}")
    print(f"   clients_count: {status['clients_count']}")
    print()

    # 2. 执行初始化
    print("2. Executing Initialization...")
    result = initialize_wechat_on_startup()
    print()

    # 3. 查看初始化后状态
    print("3. Status After Initialization:")
    status = get_initialization_status()
    print(f"   initialized: {status['initialized']}")
    print(f"   attempted: {status['attempted']}")
    print(f"   clients_count: {status['clients_count']}")
    print(f"   clients: {status['clients']}")
    print()

    # 4. 测试获取微信实例
    print("4. Testing Get WeChat Instance...")
    try:
        from app.services.wechat_service import get_wechat
        wx = get_wechat('')
        print(f"   [OK] Successfully got WeChat instance: {wx.nickname}")
    except Exception as e:
        print(f"   [FAIL] Failed to get instance: {e}")
    print()

    # 5. 测试错误处理
    print("5. Testing Error Handling...")
    from app.services.wechat_service import WeChatNotInitializedError
    from app.utils.error_handler import handle_service_error

    @handle_service_error()
    def test_function():
        raise WeChatNotInitializedError('Test exception')

    result = test_function()
    print(f"   success: {result.success}")
    print(f"   message: {result.message[:50]}...")
    print(f"   data: {result.data}")
    print()

    print("="*70)
    print("Test Completed!")
    print("="*70)


if __name__ == "__main__":
    test_initialization()
