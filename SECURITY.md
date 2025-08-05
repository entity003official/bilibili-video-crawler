# 安全配置指南

## 🔒 爬虫安全最佳实践

### 1. 请求频率控制
- 设置合理的延迟时间（建议2-5秒）
- 避免并发过多请求
- 使用随机延迟避免被检测

### 2. User-Agent 管理
```python
# 轮换使用不同的 User-Agent
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
    # 更多 User-Agent...
]
```

### 3. IP 保护
- 避免频繁请求导致IP被封
- 考虑使用代理服务器
- 监控请求状态码，及时调整策略

### 4. 数据存储安全
- 不要存储敏感信息
- 定期清理临时文件
- 使用安全的文件路径

### 5. 法律合规
- 遵守网站的 robots.txt
- 不要用于商业用途
- 尊重数据版权和隐私

## ⚡ 性能优化建议

### 1. 内存管理
```python
# 及时释放大型对象
del large_data_list
gc.collect()
```

### 2. 异步处理
- 使用 aiohttp 进行异步请求
- 合理设置并发数量
- 使用连接池复用连接

### 3. 缓存策略
- 缓存已爬取的数据
- 避免重复请求相同内容
- 设置合理的缓存过期时间

## 🛡️ 错误处理

### 1. 网络异常
```python
try:
    response = await session.get(url)
except aiohttp.ClientError as e:
    logger.error(f"网络请求失败: {e}")
    # 重试或降级处理
```

### 2. 解析异常
```python
try:
    data = await response.json()
except json.JSONDecodeError:
    # 尝试HTML解析备用方案
    html_content = await response.text()
```

### 3. 限流处理
```python
if response.status == 429:  # Too Many Requests
    retry_after = int(response.headers.get('Retry-After', 60))
    await asyncio.sleep(retry_after)
```
