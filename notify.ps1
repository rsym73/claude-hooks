# 记录脚本被调用（调试用）
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
"$timestamp - Hook 已触发" | Out-File -Append "$env:USERPROFILE\.claude\hook-debug.log"

# 生成临时 VBScript 并弹窗（Windows 后台进程唯一可靠的弹窗方式）
$vbs = @"
Set WshShell = CreateObject("WScript.Shell")
WshShell.Popup "Claude 在等你", 5, "Claude Code", 64
"@
$vbsPath = "$env:TEMP\claude-notify.vbs"
$vbs | Out-File -FilePath $vbsPath -Encoding Unicode
wscript.exe $vbsPath
"$timestamp - 弹窗已执行" | Out-File -Append "$env:USERPROFILE\.claude\hook-debug.log"
