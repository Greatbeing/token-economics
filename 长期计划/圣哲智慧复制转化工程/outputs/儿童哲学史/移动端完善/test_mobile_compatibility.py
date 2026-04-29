#!/usr/bin/env python3
"""
移动端兼容性测试脚本
"""

print("移动端兼容性测试")
print("=================")
print(f"测试文件: {html_path}")
print("")
print("测试要点:")
print("1. 图片宽度: 380px")
print("2. 最小屏幕适配: iPhone SE (375px)")
print("3. CSS响应式控制:")
print("   - 容器宽度限制")
print("   - 图片双重保险")
print("   - 超小屏幕媒体查询")
print("4. 预期效果: 无水平滚动条")
print("")
print("请在实际设备上测试:")
print("1. iPhone SE (375px)")
print("2. iPhone 12 (390px)")
print("3. Pixel 5 (393px)")
print("4. iPhone 14 Pro (430px)")
print("")
print("验证标准:")
print("- 图片完整显示在视口内")
print("- 无需水平滚动")
print("- 图片质量可接受")
