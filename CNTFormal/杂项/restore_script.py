#!/usr/bin/env python3
"""恢复被覆盖的联立求解_光速_标度.py"""
import os

target = "d:/WorkSpace/物理/闭合核理论/联立求解_光速_标度.py"

# 直接写入全部内容
# 由于内容太长，用另一种方式：读取会话记录中最后一个成功运行的版本
# 但事实上我们无法直接恢复，需要重写

print("Recovery needed - file was overwritten by Write tool")
print(f"Target: {target}")
print(f"Current size: {os.path.getsize(target)} bytes")
