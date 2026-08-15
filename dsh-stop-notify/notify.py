"""DeepSeek Harness Stop hook 通知脚本（Python 版）。

当 Agent 完成响应、等待用户输入时，弹出桌面提醒窗口，超时后自动关闭。

实现方式：ctypes 调用 Windows 的 MessageBoxTimeoutW API（未正式文档化但稳定），
仅使用 Python 标准库，无任何第三方依赖。

用法（由 Node 插件以子进程方式调用）：
    python notify.py [title] [message] [timeout]
"""

import ctypes
import sys

# MessageBox 样式标志（与原 claude-hooks 保持一致）
MB_ICONINFORMATION = 0x40      # 信息图标
MB_TOPMOST = 0x40000           # 置顶窗口
MB_SETFOREGROUND = 0x10000     # 抢占前台

DEFAULT_TITLE = "DeepSeek Harness"
DEFAULT_MESSAGE = "DeepSeek 在等你"
DEFAULT_TIMEOUT = 5


def notify(title=DEFAULT_TITLE, message=DEFAULT_MESSAGE, timeout=DEFAULT_TIMEOUT):
    """弹出桌面通知窗口，超时后自动关闭。

    Args:
        title: 窗口标题
        message: 通知内容
        timeout: 自动关闭秒数
    """
    flags = MB_ICONINFORMATION | MB_TOPMOST | MB_SETFOREGROUND

    # MessageBoxTimeoutW(HWND, LPCWSTR, LPCWSTR, UINT, WORD, DWORD)
    # 参数：窗口句柄(0)、内容、标题、样式标志、语言 ID(0)、超时毫秒数
    MessageBoxTimeout = ctypes.windll.user32.MessageBoxTimeoutW
    MessageBoxTimeout(0, message, title, flags, 0, int(timeout) * 1000)


if __name__ == "__main__":
    args = sys.argv[1:]
    notify(
        title=args[0] if len(args) > 0 else DEFAULT_TITLE,
        message=args[1] if len(args) > 1 else DEFAULT_MESSAGE,
        timeout=int(args[2]) if len(args) > 2 else DEFAULT_TIMEOUT,
    )
