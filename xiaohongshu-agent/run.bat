@echo off
chcp 65001 >nul
echo ========================================
echo 小红书文案自动生成
echo ========================================
echo.

python "%~dp0generate_copy.py"

echo.
echo 按任意键退出...
pause >nul
