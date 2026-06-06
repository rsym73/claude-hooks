# claude-rsym-hooks

Claude Code hooks 配置 —— 当 Claude 停下来等你时，Windows 右下角弹出提醒通知。

支持两种安装模式：**全局配置**（所有项目生效）和**项目配置**（仅当前项目生效）。

## 包含内容

- `notify.ps1` — Windows 通知脚本
- `README.md` — 本文件

## 前提条件

- Windows 10 或 Windows 11
- Claude Code 已安装

---

## 安装方式一：全局配置

所有 Claude Code 项目生效。

### 1. 放置通知脚本

将 `notify.ps1` 复制到 Claude Code 全局配置目录：

```
C:\Users\<你的用户名>\.claude\notify.ps1
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
            "command": "powershell -ExecutionPolicy Bypass -File \"C:\\Users\\<你的用户名>\\.claude\\notify.ps1\"",
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
powershell -ExecutionPolicy Bypass -File "C:\Users\<你的用户名>\.claude\notify.ps1"
```

---

## 安装方式二：项目配置

仅对当前项目生效，配置跟随项目走，方便团队共享。

### 1. 放置通知脚本

将 `notify.ps1` 复制到项目的 `.claude` 目录下：

```
<项目根目录>\.claude\notify.ps1
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
            "command": "powershell -ExecutionPolicy Bypass -File \".claude\\notify.ps1\"",
            "timeout": 10
          }
        ]
      }
    ]
  }
}
```

> 💡 项目级配置使用相对路径 `.claude\notify.ps1`，Claude Code 会自动基于项目根目录解析。

### 3. 验证

在项目根目录下运行：

```powershell
powershell -ExecutionPolicy Bypass -File ".claude\notify.ps1"
```

---

## 效果

- 给 Claude 发完指令后切走做其他事
- Claude 停下来等你时 → 右下角弹出 "Claude 在等你"
- 切回来继续操作

## Hook 说明

| 项目 | 值 |
|---|---|
| 事件 | `Stop` — Claude 停止等待用户输入时触发 |
| 通知形式 | Windows 系统托盘气泡通知 |
| 通知内容 | "Claude 在等你" |
| 显示时长 | 5 秒 |

## 免责声明

本项目仅为个人 Claude Code 配置的备份和分享。使用前请确保理解脚本内容，脚本仅执行本地通知功能，不会：

- 上传或泄露任何数据
- 修改系统关键配置
- 在后台持续运行

因使用本配置造成的任何问题，作者不承担责任。
