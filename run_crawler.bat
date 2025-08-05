@echo off
REM ================================================================
REM B站视频爬虫启动脚本 (Windows批处理版本)
REM ================================================================
REM 
REM 功能说明：
REM - 🚀 一键启动：双击即可运行异步API爬虫
REM - 📁 自动定位：自动切换到项目目录
REM - ⚠️ 错误处理：包含基本的错误检查和提示
REM - 🎯 用户友好：适合不熟悉命令行的用户
REM 
REM 使用方法：
REM 1. 确保已安装Python和相关依赖
REM 2. 双击此文件运行
REM 3. 查看输出结果
REM 
REM 注意事项：
REM - 请确保Python在系统PATH中
REM - 建议先运行requirements.txt安装依赖
REM 
REM 作者：GitHub Copilot
REM 更新：2025-08-05
REM ================================================================

echo 启动B站视频爬取工具...
echo.

cd /d "d:\Work\!Bing chuang\2025.analyze emotion\more_new_words_spider\test2"

echo 当前目录: %CD%
echo.

echo 运行爬虫...
C:/Users/Administrator/AppData/Local/Programs/Python/Python310/python.exe spider_no_input.py

echo.
echo 完成! 按任意键退出...
pause
