@echo off
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
