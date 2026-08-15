# claude-hooks

Claude Code hooks 配置 —— 当 Claude 停下来等你时，Windows 桌面弹出提醒，5 秒后自动消失。另提供 **DeepSeek Harness（DSH）移植版**（见下文）。

支持两种 Claude Code 安装模式：**全局配置**（所有项目生效）和**项目配置**（仅当前项目生效）。

## 包含内容

- `hooks/notify.py` — Windows 通知脚本（Python，Claude Code 版）
- `dsh-stop-notify/` — DeepSeek Harness 版（Cordis 插件 + Python 通知脚本）
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

---

## DeepSeek Harness（DSH）版本

本项目同时提供 **DeepSeek Harness** 的移植版：当 DSH 的 Agent 停下来等你时，同样弹出 Windows 桌面提醒，5 秒后自动消失。

### 与 Claude Code 的对应关系

| Claude Code | DeepSeek Harness |
|---|---|
| `Stop` 事件（Agent 停止等待输入） | `agent/status` 事件，`status === 'idle'` |
| `hooks/notify.py`（ctypes `MessageBoxTimeoutW`） | `dsh-stop-notify/notify.py`（相同实现，增加命令行参数） |
| `settings.json` 的 `hooks` 字段 | `cordis.patch.yml` 的 `insert` 插件行 |
| `~/.claude/settings.json`（全局） | `<DSH_HOME>\cordis.patch.yml` |
| `<项目>/.claude/settings.json`（单项目） | `<DSH_HOME>\profiles\<profile>\cordis.patch.yml` |

> DSH 的插件入口必须是 JavaScript（Cordis 插件），所以本版本采用「极薄 JS 壳 + Python 通知脚本」：JS 只负责监听 `agent/status → idle` 事件并拉起 `python notify.py`，通知本体仍是 Python + ctypes，零第三方依赖。

### 前提条件

- Windows 10 / 11
- DeepSeek Harness（`dsh` 命令）已安装
- Python 3.x 且 `python` 在 PATH 中

### 目录结构

```
dsh-stop-notify/
├── package.json   # 插件包描述（无第三方依赖）
├── notify.py      # Python 通知脚本（ctypes 调 MessageBoxTimeoutW）
└── lib/
    └── index.js   # Cordis 插件壳：agent/status → idle → spawn python notify.py
```

### 安装（全局配置，所有 profile 生效）

`<DSH_HOME>` 默认是 `C:\Users\<你的用户名>\.dsh`。

1. 把整个 `dsh-stop-notify/` 目录复制到共享插件目录：

```
<DSH_HOME>\profiles\node_modules\dsh-stop-notify\
```

2. 创建或编辑全局 patch 文件 `<DSH_HOME>\cordis.patch.yml`，添加：

```yaml
- insert:
    - id: stop-notify
      name: 'dsh-stop-notify'
      config:
        title: DeepSeek Harness
        message: DeepSeek 在等你
        timeout: 5
```

> 💡 若只想对单个 profile 生效，把同样的 `insert` 写到 `<DSH_HOME>\profiles\<profile>\cordis.patch.yml` 即可。

3. 重启 DSH（首次新增全局 patch 后需要重启才会被读到）。

### 验证

```powershell
python "<DSH_HOME>\profiles\node_modules\dsh-stop-notify\notify.py"
```

### 可选配置

| 字段 | 默认值 | 说明 |
|---|---|---|
| `title` | `DeepSeek Harness` | 窗口标题 |
| `message` | `DeepSeek 在等你` | 提醒内容 |
| `timeout` | `5` | 自动关闭秒数 |
| `python` | `python` | Python 解释器（可用 `pythonw` 免控制台闪烁） |
| `rootsOnly` | `true` | 只对根 Agent 提醒，跳过子代理（fork/spawn） |

---

## 免责声明

本项目仅为个人 Claude Code 配置的备份和分享。使用前请确保理解脚本内容，脚本仅执行本地通知功能，不会：

- 上传或泄露任何数据
- 修改系统关键配置
- 在后台持续运行

因使用本配置造成的任何问题，作者不承担责任。
