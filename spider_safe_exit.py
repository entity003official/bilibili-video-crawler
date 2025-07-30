"""
B站爬虫 - 可控制退出版本
支持Ctrl+C安全退出
"""
import time
import csv
import re
from datetime import datetime
import os
import signal
import sys

# 全局变量用于控制程序退出
should_stop = False
driver = None

def signal_handler(sig, frame):
    """处理Ctrl+C信号"""
    global should_stop, driver
    print('\n\n🛑 检测到退出信号...')
    should_stop = True
    
    if driver:
        print('正在关闭浏览器...')
        try:
            driver.quit()
        except:
            pass
    
    print('✅ 程序已安全退出')
    sys.exit(0)

# 注册信号处理器
signal.signal(signal.SIGINT, signal_handler)

def safe_crawl_bilibili():
    """可安全退出的爬虫"""
    global should_stop, driver
    
    try:
        from selenium import webdriver
        from selenium.webdriver.common.by import By
        from selenium.webdriver.chrome.options import Options
        from webdriver_manager.chrome import ChromeDriverManager
        from selenium.webdriver.chrome.service import Service
        
        url = "https://space.bilibili.com/93796936/upload/video"
        
        print("🚀 B站视频爬取工具 (可安全退出)")
        print("💡 按 Ctrl+C 可随时安全退出")
        print("=" * 60)
        print(f"目标UP主: {url}")
        print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        
        # Chrome配置
        options = Options()
        
        # 使用用户数据目录
        user_data_dir = f"C:/Users/{os.getenv('USERNAME', 'Administrator')}/AppData/Local/Google/Chrome/User Data"
        if os.path.exists(user_data_dir):
            print(f"✓ 使用Chrome用户数据保持登录状态")
            options.add_argument(f'--user-data-dir={user_data_dir}')
            options.add_argument('--profile-directory=Default')
        
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--window-size=1366,768')
        
        print("正在启动Chrome浏览器...")
        
        try:
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)
        except Exception as e:
            print(f"使用默认方式启动Chrome: {e}")
            driver = webdriver.Chrome(options=options)
        
        print("✓ 浏览器启动成功")
        
        if should_stop:
            return []
        
        print("正在访问UP主页面...")
        driver.get(url)
        time.sleep(3)
        
        if should_stop:
            return []
        
        # 检查登录状态
        page_title = driver.title
        print(f"页面标题: {page_title}")
        
        if any(keyword in page_title.lower() for keyword in ['登录', 'login']):
            print("⚠️  检测到登录页面")
            print("请在浏览器中手动登录，程序将等待30秒...")
            
            for i in range(30, 0, -1):
                if should_stop:
                    return []
                print(f"等待登录... {i}秒", end='\r')
                time.sleep(1)
            
            print("\n继续爬取...")
            driver.get(url)
            time.sleep(3)
        
        if should_stop:
            return []
        
        print("🎬 开始爬取视频数据...")
        
        all_videos = []
        max_pages = 20
        
        for page in range(1, max_pages + 1):
            if should_stop:
                print(f"\n用户中断，已爬取 {len(all_videos)} 个视频")
                break
            
            print(f"\n📄 正在爬取第{page}页...")
            
            # 构建分页URL
            if page > 1:
                page_url = f"{url}?pn={page}"
                driver.get(page_url)
                time.sleep(2)
                
                if should_stop:
                    break
            
            # 滚动页面
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
            
            if should_stop:
                break
            
            # 查找视频链接
            video_selectors = [
                "a[href*='/video/BV']",
                "a.bili-cover-card"
            ]
            
            video_links = []
            for selector in video_selectors:
                try:
                    elements = driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements:
                        video_links = elements
                        print(f"  ✓ 找到 {len(elements)} 个视频")
                        break
                except:
                    continue
            
            if not video_links:
                print(f"  ❌ 第{page}页未找到视频")
                break
            
            # 解析视频信息
            page_videos = []
            for i, link in enumerate(video_links):
                if should_stop:
                    break
                
                try:
                    href = link.get_attribute('href')
                    if not href or '/video/BV' not in href:
                        continue
                    
                    bv_match = re.search(r'/video/(BV[\w]+)', href)
                    if not bv_match:
                        continue
                    
                    bv_id = bv_match.group(1)
                    title = link.get_attribute('title') or f"视频_{bv_id}"
                    
                    # 避免重复
                    if not any(v['bv'] == bv_id for v in all_videos):
                        page_videos.append({
                            'bv': bv_id,
                            'title': title.strip(),
                            'url': href,
                            'page': page
                        })
                
                except Exception:
                    continue
                
                # 每处理10个视频检查一次退出信号
                if i % 10 == 0 and should_stop:
                    break
            
            if page_videos and not should_stop:
                all_videos.extend(page_videos)
                print(f"  ✓ 第{page}页获取 {len(page_videos)} 个视频，总计: {len(all_videos)}")
            elif not page_videos:
                print(f"  ❌ 第{page}页无新视频")
                break
            
            # 短暂延迟
            if not should_stop:
                time.sleep(1)
        
        return all_videos
        
    except KeyboardInterrupt:
        print("\n\n🛑 用户中断程序")
        return []
    except Exception as e:
        print(f"\n❌ 爬取过程出错: {e}")
        return []
    finally:
        if driver:
            try:
                driver.quit()
                print("✅ 浏览器已关闭")
            except:
                pass

def save_results(videos):
    """保存结果"""
    if not videos:
        print("❌ 没有数据可保存")
        return None
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"bilibili_videos_safe_{timestamp}.csv"
    
    with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=['序号', 'BV号', '视频标题', '视频链接', '页码'])
        writer.writeheader()
        
        for i, video in enumerate(videos, 1):
            writer.writerow({
                '序号': i,
                'BV号': video['bv'],
                '视频标题': video['title'],
                '视频链接': video['url'],
                '页码': video['page']
            })
    
    print(f"✅ 数据已保存到: {filename}")
    return filename

def main():
    global should_stop, driver
    
    print("=" * 70)
    print("🎯 B站UP主视频爬取工具 - 可控制版本")
    print("💡 使用说明:")
    print("   - 程序运行过程中可随时按 Ctrl+C 安全退出")
    print("   - 退出时会自动保存已爬取的数据")
    print("   - 浏览器会自动关闭")
    print("=" * 70)
    
    start_time = datetime.now()
    
    try:
        # 开始爬取
        videos = safe_crawl_bilibili()
        
        if videos:
            # 保存结果
            filename = save_results(videos)
            
            if filename and not should_stop:
                end_time = datetime.now()
                duration = end_time - start_time
                
                print("\n" + "=" * 70)
                print("🎉 爬取完成!")
                print("=" * 70)
                print(f"✅ 成功爬取: {len(videos)} 个视频")
                print(f"✅ 保存文件: {filename}")
                print(f"✅ 总耗时: {duration}")
                
                # 显示前5个视频
                print(f"\n📺 视频预览:")
                for i, video in enumerate(videos[:5], 1):
                    title = video['title'][:40] + "..." if len(video['title']) > 40 else video['title']
                    print(f"{i}. {title}")
                
                if len(videos) > 5:
                    print(f"... 还有 {len(videos) - 5} 个视频")
        else:
            print("\n📝 没有获取到视频数据")
            
    except KeyboardInterrupt:
        print("\n\n🛑 程序被用户中断")
    except Exception as e:
        print(f"\n❌ 程序异常: {e}")
    finally:
        if driver:
            try:
                driver.quit()
            except:
                pass
        print("\n👋 程序结束")

if __name__ == "__main__":
    main()
