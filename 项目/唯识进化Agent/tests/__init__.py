# -*- coding: utf-8 -*-
"""
测试包初始化

作者：觉心
"""

import sys
import os

# 确保src目录在Python路径中
src_path = os.path.join(os.path.dirname(__file__), '..', 'src')
if src_path not in sys.path:
    sys.path.insert(0, src_path)
