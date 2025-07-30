@echo off
chcp 65001 >nul
echo ========================================
echo    B站爬虫 - 安全退出版本
echo ========================================
echo.
echo 💡 使用说明:
echo    - 运行过程中按 Ctrl+C 可安全退出
echo    - 程序会自动保存已爬取的数据
echo.
pause

python spider_safe_exit.py

echo.
echo ========================================
echo    程序执行完毕
echo ========================================
pause
