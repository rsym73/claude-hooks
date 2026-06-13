"""Claude Code Stop Hook 通知脚本
当 Claude 完成响应、等待用户输入时，弹出桌面提醒窗口，5 秒后自动关闭。

实现方式：ctypes 调用 Windows MessageBoxTimeoutW API，无需任何第三方依赖。
"""

import ctypes
import os
from datetime import datetime

# MessageBox 样式标志
MB_ICONINFORMATION = 0x40      # 信息图标
MB_TOPMOST = 0x40000           # 置顶窗口
MB_SETFOREGROUND = 0x10000     # 抢占前台


def log(msg: str) -> None:
    """写入调试日志（如果启用）"""
    log_path = os.path.join(os.path.expanduser("~"), ".claude", "hook-debug.log")
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(f"{timestamp} - {msg}\n")
    except Exception:
        pass  # 日志写入失败不影响通知


def notify(title: str = "Claude Code", message: str = "Claude 在等你", timeout: int = 5) -> None:
    """弹出桌面通知窗口，超时后自动关闭。

    Args:
        title: 窗口标题
        message: 通知内容
        timeout: 自动关闭秒数
    """
    flags = MB_ICONINFORMATION | MB_TOPMOST | MB_SETFOREGROUND

    # MessageBoxTimeoutW 是 user32.dll 中未正式文档化但稳定存在的 API
    # 签名: int MessageBoxTimeoutW(HWND, LPCWSTR, LPCWSTR, UINT, WORD, DWORD)
    MessageBoxTimeout = ctypes.windll.user32.MessageBoxTimeoutW
    MessageBoxTimeout(0, message, title, flags, 0, timeout * 1000)


if __name__ == "__main__":
    log("Hook 已触发")
    notify()
    log("弹窗已执行")
