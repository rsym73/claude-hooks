// DeepSeek Harness 插件：移植 Claude Code 的 Stop hook。
// 当 Agent 结束当前回合、停下来等待用户输入时，弹出 Windows 桌面提醒。
//
// 通知本体用 Python（notify.py，ctypes 调 MessageBoxTimeoutW），
// 本文件只是一个极薄的 Cordis 插件壳：监听 agent/status → idle → 拉起 python notify.py。

import { spawn } from "node:child_process";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

export const name = "stop-notify";

// 定位 notify.py（与包根目录同级）
const SCRIPT = join(dirname(fileURLToPath(import.meta.url)), "..", "notify.py");

/**
 * @param {object} [config]
 * @param {string} [config.title]      窗口标题
 * @param {string} [config.message]    提醒内容
 * @param {number} [config.timeout]    自动关闭秒数（默认 5）
 * @param {string} [config.python]     Python 解释器（默认 python；可用 pythonw 免控制台闪烁）
 * @param {boolean} [config.rootsOnly] 只对根 Agent 提醒、跳过子代理（默认 true）
 */
export function apply(ctx, config = {}) {
  // 仅 Windows 生效（MessageBoxTimeoutW 是 Win32 API）
  if (process.platform !== "win32") return;

  const title = typeof config.title === "string" ? config.title : "DeepSeek Harness";
  const message = typeof config.message === "string" ? config.message : "DeepSeek 在等你";
  const timeout = Number.isFinite(config.timeout) ? Math.floor(config.timeout) : 5;
  const python = typeof config.python === "string" ? config.python : "python";
  const rootsOnly = config.rootsOnly !== false;

  const notify = () => {
    try {
      const child = spawn(python, [SCRIPT, title, message, String(timeout)], {
        detached: true,
        stdio: "ignore",
        windowsHide: true,
      });
      child.on("error", (e) => ctx.logger?.warn?.(`stop-notify: 通知失败: ${e.message}`));
      child.unref(); // 不阻塞 DSH 宿主进程
    } catch (error) {
      ctx.logger?.warn?.(`stop-notify: 通知失败: ${String(error)}`);
    }
  };

  ctx.on("agent/status", ({ agent, status }) => {
    if (status !== "idle") return;
    // 子代理（fork/spawn）也有自己的 idle 事件，默认只对根 Agent 提醒
    if (rootsOnly && agent?.session?.header?.delegationDepth) return;
    notify();
  });
}
