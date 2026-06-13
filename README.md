# claude-hooks

Claude Code hooks 配置 —— 当 Claude 停下来等你时，Windows 桌面弹出提醒，5 秒后自动消失。

支持两种安装模式：**全局配置**（所有项目生效）和**项目配置**（仅当前项目生效）。

## 包含内容

- `hooks/notify.py` — Windows 通知脚本（Python）
- `README.md` — 本文件

## 前提条件

- Windows 10 或 Windows 11
- Claude Code 已安装
- Python 3.x 已安装且 `python` 命令在 PATH 中（推荐安装时勾选 "Add to PATH"）

---

## 安装方式一：全局配置

所有 Claude Code 项目生效。

### 1. 放置通知脚本

将 `notify.py` 复制到 Claude Code 全局配置目录：

```
C:\Users\<你的用户名>\.claude\hooks\notify.py
```

### 2. 配置 Hook

编辑 `C:\Users\<你的用户名>\.claude\settings.json`，添加或合并 `hooks` 字段：

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python \"C:\\Users\\<你的用户名>\\.claude\\hooks\\notify.py\"",
            "timeout": 10
          }
        ]
      }
    ]
  }
}
```

> ⚠️ `settings.json` 可能已有其他配置，请将 `hooks` 字段合并进去，不要覆盖已有内容。

### 3. 验证

```powershell
python "C:\Users\<你的用户名>\.claude\hooks\notify.py"
```

---

## 安装方式二：项目配置

仅对当前项目生效，配置跟随项目走，方便团队共享。

### 1. 放置通知脚本

将 `notify.py` 复制到项目的 `.claude` 目录下：

```
<项目根目录>\.claude\hooks\notify.py
```

### 2. 配置 Hook

创建或编辑 `<项目根目录>\.claude\settings.json`，添加：

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python \".claude\\notify.py\"",
            "timeout": 10
          }
        ]
      }
    ]
  }
}
```

> 💡 项目级配置使用相对路径 `.claude\notify.py`，Claude Code 会自动基于项目根目录解析。

### 3. 验证

在项目根目录下运行：

```powershell
python ".claude\notify.py"
```

---

## 效果

- 给 Claude 发完指令后切走做其他事
- Claude 停下来等你时 → 桌面弹出 "Claude 在等你"，5 秒后自动消失
- 切回来继续操作

## Hook 说明

| 项目 | 值 |
|---|---|
| 事件 | `Stop` — Claude 停止等待用户输入时触发 |
| 通知形式 | Windows MessageBox 弹窗，5 秒后自动消失 |
| 通知内容 | "Claude 在等你" |
| 实现方式 | Python ctypes 调用 `MessageBoxTimeoutW` API（标准库，无第三方依赖） |

## 免责声明

本项目仅为个人 Claude Code 配置的备份和分享。使用前请确保理解脚本内容，脚本仅执行本地通知功能，不会：

- 上传或泄露任何数据
- 修改系统关键配置
- 在后台持续运行

因使用本配置造成的任何问题，作者不承担责任。
