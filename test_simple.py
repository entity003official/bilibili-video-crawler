"""
简单测试脚本 - 检查环境和直接爬取
"""
print("🔧 环境检查开始...")

# 检查selenium
try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    print("✅ Selenium导入成功")
except ImportError as e:
    print(f"❌ Selenium导入失败: {e}")
    exit(1)

# 检查webdriver-manager
try:
    from webdriver_manager.chrome import ChromeDriverManager
    print("✅ WebDriver Manager导入成功")
except ImportError as e:
    print(f"⚠️ WebDriver Manager导入失败: {e}")

print("\n🚀 开始简单爬取测试...")

try:
    # 最简单的Chrome配置
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    print("正在启动Chrome...")
    driver = webdriver.Chrome(options=options)
    
    url = "https://space.bilibili.com/93796936/upload/video"
    print(f"访问页面: {url}")
    
    driver.get(url)
    
    import time
    time.sleep(5)
    
    title = driver.title
    print(f"页面标题: {title}")
    
    # 简单查找视频链接
    from selenium.webdriver.common.by import By
    links = driver.find_elements(By.CSS_SELECTOR, "a[href*='/video/BV']")
    print(f"找到 {len(links)} 个视频链接")
    
    # 显示前5个
    for i, link in enumerate(links[:5], 1):
        href = link.get_attribute('href')
        title = link.get_attribute('title') or "无标题"
        print(f"{i}. {title[:30]}... - {href}")
    
    driver.quit()
    print("\n✅ 测试完成！Chrome和Selenium工作正常")
    
except Exception as e:
    print(f"❌ 测试失败: {e}")
    import traceback
    traceback.print_exc()
