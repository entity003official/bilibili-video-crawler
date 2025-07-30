# Bilibili Video Crawler Upload Script
# 快速上传到GitHub的脚本

echo "🚀 准备上传 Bilibili 视频爬虫项目到 GitHub"
echo "============================================"

# 检查Git是否安装
git --version
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Git 未安装，请先安装 Git" -ForegroundColor Red
    exit 1
}

# 进入项目目录
$projectPath = "d:\Work\!Bing chuang\2025.analyze emotion\more_new_words_spider\test2"
Set-Location $projectPath

Write-Host "📁 当前目录: $((Get-Location).Path)" -ForegroundColor Green

# 初始化Git仓库
Write-Host "`n🔧 初始化 Git 仓库..."
git init

# 添加所有文件
Write-Host "`n📦 添加文件到Git..."
git add .

# 创建初次提交
Write-Host "`n💾 创建初次提交..."
git commit -m "Initial commit: Bilibili video crawler with multiple features

Features:
- Batch crawling of Bilibili UP主 videos
- Selenium-based web scraping
- Auto-login support using Chrome user data
- Multiple output formats (CSV, JSON)
- Safe exit mechanism with Ctrl+C
- Comprehensive error handling
- Multiple crawler versions for different use cases"

Write-Host "`n✅ 本地Git仓库准备完成！" -ForegroundColor Green
Write-Host "`n📋 接下来的步骤："
Write-Host "1. 在GitHub上创建新仓库（推荐名称：bilibili-video-crawler）"
Write-Host "2. 复制仓库的HTTPS链接"
Write-Host "3. 运行以下命令连接远程仓库："
Write-Host "   git remote add origin https://github.com/你的用户名/bilibili-video-crawler.git"
Write-Host "   git branch -M main"
Write-Host "   git push -u origin main"

pause
