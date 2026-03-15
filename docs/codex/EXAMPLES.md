# 代码示例

## Python 示例

### 1. 数据结构与算法

#### 快速排序

**Prompt**: "用 Python 实现快速排序，包含注释"

```python
def quick_sort(arr):
    """
    快速排序实现
    时间复杂度：平均 O(n log n)，最坏 O(n²)
    空间复杂度：O(log n)
    """
    if len(arr) <= 1:
        return arr
    
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    
    return quick_sort(left) + middle + quick_sort(right)

# 使用示例
arr = [3, 6, 8, 10, 1, 2, 1]
sorted_arr = quick_sort(arr)
print(sorted_arr)  # [1, 1, 2, 3, 6, 8, 10]
```

#### 二分查找

**Prompt**: "Python 二分查找，返回索引，找不到返回 -1"

```python
def binary_search(arr, target):
    """二分查找，返回目标值的索引"""
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1

# 使用示例
arr = [1, 3, 5, 7, 9, 11]
print(binary_search(arr, 7))   # 3
print(binary_search(arr, 4))   # -1
```

### 2. Web 开发

#### Flask REST API

**Prompt**: "用 Flask 创建一个简单的 REST API，包含 GET 和 POST 端点"

```python
from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# 内存存储
items = []

@app.route('/api/items', methods=['GET'])
def get_items():
    """获取所有项目"""
    return jsonify({
        'success': True,
        'data': items,
        'count': len(items)
    })

@app.route('/api/items', methods=['POST'])
def create_item():
    """创建新项目"""
    data = request.get_json()
    
    if not data or 'name' not in data:
        return jsonify({
            'success': False,
            'error': 'Name is required'
        }), 400
    
    item = {
        'id': len(items) + 1,
        'name': data['name'],
        'description': data.get('description', ''),
        'created_at': datetime.now().isoformat()
    }
    
    items.append(item)
    
    return jsonify({
        'success': True,
        'data': item
    }), 201

@app.route('/api/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    """获取单个项目"""
    item = next((i for i in items if i['id'] == item_id), None)
    
    if not item:
        return jsonify({
            'success': False,
            'error': 'Item not found'
        }), 404
    
    return jsonify({
        'success': True,
        'data': item
    })

if __name__ == '__main__':
    app.run(debug=True)
```

#### 异步 HTTP 客户端

**Prompt**: "使用 aiohttp 创建异步 HTTP 客户端，支持重试"

```python
import aiohttp
import asyncio
from typing import Optional, Dict, Any

class AsyncHTTPClient:
    def __init__(self, max_retries: int = 3, timeout: int = 30):
        self.max_retries = max_retries
        self.timeout = timeout
    
    async def get(self, url: str, headers: Optional[Dict] = None) -> Optional[Dict[str, Any]]:
        """发送 GET 请求"""
        for attempt in range(self.max_retries):
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(
                        url,
                        headers=headers,
                        timeout=aiohttp.ClientTimeout(total=self.timeout)
                    ) as response:
                        if response.status == 200:
                            return await response.json()
                        elif response.status >= 500:
                            await asyncio.sleep(2 ** attempt)  # 指数退避
                            continue
                        else:
                            response.raise_for_status()
            except Exception as e:
                if attempt == self.max_retries - 1:
                    print(f"请求失败 after {self.max_retries} attempts: {e}")
                    return None
                await asyncio.sleep(2 ** attempt)
        
        return None
    
    async def post(self, url: str, data: Dict, headers: Optional[Dict] = None) -> Optional[Dict[str, Any]]:
        """发送 POST 请求"""
        for attempt in range(self.max_retries):
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.post(
                        url,
                        json=data,
                        headers=headers,
                        timeout=aiohttp.ClientTimeout(total=self.timeout)
                    ) as response:
                        if response.status in [200, 201]:
                            return await response.json()
                        elif response.status >= 500:
                            await asyncio.sleep(2 ** attempt)
                            continue
                        else:
                            response.raise_for_status()
            except Exception as e:
                if attempt == self.max_retries - 1:
                    print(f"请求失败：{e}")
                    return None
                await asyncio.sleep(2 ** attempt)
        
        return None

# 使用示例
async def main():
    client = AsyncHTTPClient()
    data = await client.get('https://api.example.com/data')
    print(data)

asyncio.run(main())
```

### 3. 数据处理

#### Pandas 数据清洗

**Prompt**: "用 pandas 清洗数据：处理缺失值、删除重复、标准化列名"

```python
import pandas as pd
import numpy as np

def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    数据清洗函数
    - 标准化列名
    - 删除完全重复行
    - 处理缺失值
    """
    # 标准化列名：小写，空格变下划线
    df.columns = (
        df.columns
        .str.lower()
        .str.replace(' ', '_')
        .str.replace('[^a-z0-9_]', '', regex=True)
    )
    
    # 删除完全重复的行
    df = df.drop_duplicates()
    
    # 处理缺失值
    for col in df.columns:
        if df[col].dtype == 'object':
            # 字符串列：用众数填充
            df[col] = df[col].fillna(df[col].mode()[0] if not df[col].mode().empty else 'Unknown')
        elif df[col].dtype in ['int64', 'float64']:
            # 数值列：用中位数填充
            df[col] = df[col].fillna(df[col].median())
        elif df[col].dtype == 'datetime64[ns]':
            # 日期列：用众数填充
            df[col] = df[col].fillna(df[col].mode()[0] if not df[col].mode().empty else pd.NaT)
    
    # 重置索引
    df = df.reset_index(drop=True)
    
    return df

# 使用示例
df = pd.read_csv('data.csv')
clean_df = clean_dataframe(df)
print(clean_df.info())
```

### 4. 装饰器与高级特性

**Prompt**: "Python 装饰器：缓存、重试、计时"

```python
import functools
import time
import hashlib
from typing import Callable, Any

# 缓存装饰器
def cache_result(ttl: int = 300):
    """结果缓存装饰器，ttl 为过期时间（秒）"""
    cache = {}
    
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            # 创建缓存键
            key = hashlib.md5(
                f"{func.__name__}:{args}:{kwargs}".encode()
            ).hexdigest()
            
            # 检查缓存
            if key in cache:
                result, timestamp = cache[key]
                if time.time() - timestamp < ttl:
                    return result
            
            # 执行函数并缓存
            result = func(*args, **kwargs)
            cache[key] = (result, time.time())
            return result
        
        wrapper.cache_clear = lambda: cache.clear()
        return wrapper
    return decorator

# 重试装饰器
def retry(max_attempts: int = 3, delay: float = 1.0, exceptions: tuple = (Exception,)):
    """重试装饰器"""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            last_exception = None
            
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        time.sleep(delay * (2 ** attempt))  # 指数退避
            
            raise last_exception
        
        return wrapper
    return decorator

# 计时装饰器
def timing(func: Callable) -> Callable:
    """函数执行时间统计"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} 执行时间：{end - start:.4f}秒")
        return result
    return wrapper

# 使用示例
@cache_result(ttl=60)
@timing
def expensive_operation(n: int) -> int:
    time.sleep(2)
    return sum(range(n))

@retry(max_attempts=3, delay=0.5)
def flaky_request():
    import random
    if random.random() < 0.7:
        raise ConnectionError("网络错误")
    return "成功"
```

## JavaScript/TypeScript 示例

### 1. React 自定义 Hook

**Prompt**: "TypeScript React 自定义 Hook：useFetch 带缓存和重试"

```typescript
import { useState, useEffect, useCallback } from 'react';

interface UseFetchResult<T> {
  data: T | null;
  loading: boolean;
  error: Error | null;
  refetch: () => void;
}

interface CacheEntry<T> {
  data: T;
  timestamp: number;
}

const cache = new Map<string, CacheEntry<any>>();
const CACHE_TTL = 5 * 60 * 1000; // 5 分钟

export function useFetch<T>(
  url: string,
  options: RequestInit = {},
  cacheEnabled: boolean = true
): UseFetchResult<T> {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<Error | null>(null);

  const fetchData = useCallback(async () => {
    // 检查缓存
    if (cacheEnabled && cache.has(url)) {
      const entry = cache.get(url)!;
      if (Date.now() - entry.timestamp < CACHE_TTL) {
        setData(entry.data);
        setLoading(false);
        return;
      }
    }

    setLoading(true);
    setError(null);

    try {
      const response = await fetch(url, {
        ...options,
        headers: {
          'Content-Type': 'application/json',
          ...options.headers,
        },
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const result = await response.json();
      setData(result);

      // 缓存结果
      if (cacheEnabled) {
        cache.set(url, {
          data: result,
          timestamp: Date.now(),
        });
      }
    } catch (err) {
      setError(err instanceof Error ? err : new Error('Unknown error'));
    } finally {
      setLoading(false);
    }
  }, [url, options, cacheEnabled]);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  return { data, loading, error, refetch: fetchData };
}

// 使用示例
function UserProfile({ userId }: { userId: string }) {
  const { data, loading, error, refetch } = useFetch<User>(
    `https://api.example.com/users/${userId}`
  );

  if (loading) return <div>加载中...</div>;
  if (error) return <div>错误：{error.message}</div>;
  if (!data) return null;

  return (
    <div>
      <h1>{data.name}</h1>
      <button onClick={refetch}>刷新</button>
    </div>
  );
}
```

### 2. Node.js 中间件

**Prompt**: "Express 中间件：日志、认证、限流"

```typescript
import { Request, Response, NextFunction } from 'express';
import rateLimit from 'express-rate-limit';
import jwt from 'jsonwebtoken';

// 日志中间件
export function logger(req: Request, res: Response, next: NextFunction) {
  const start = Date.now();
  
  res.on('finish', () => {
    const duration = Date.now() - start;
    console.log(
      `[${new Date().toISOString()}] ${req.method} ${req.originalUrl} ` +
      `${res.statusCode} ${duration}ms`
    );
  });
  
  next();
}

// 认证中间件
export function authenticate(
  req: Request,
  res: Response,
  next: NextFunction
) {
  const authHeader = req.headers.authorization;
  
  if (!authHeader || !authHeader.startsWith('Bearer ')) {
    res.status(401).json({ error: '缺少认证令牌' });
    return;
  }
  
  const token = authHeader.substring(7);
  
  try {
    const payload = jwt.verify(token, process.env.JWT_SECRET!);
    (req as any).user = payload;
    next();
  } catch (error) {
    res.status(401).json({ error: '无效的认证令牌' });
  }
}

// 限流中间件
export const rateLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 分钟
  max: 100, // 最多 100 请求
  message: { error: '请求过于频繁，请稍后重试' },
  standardHeaders: true,
  legacyHeaders: false,
});

// 使用示例
import express from 'express';
const app = express();

app.use(logger);
app.use('/api/', rateLimiter);
app.use('/api/protected/', authenticate);
```

## SQL 示例

### 复杂查询

**Prompt**: "SQL 查询：统计每月活跃用户，包含留存率"

```sql
-- 计算每月活跃用户和留存率
WITH monthly_active_users AS (
    SELECT 
        DATE_TRUNC('month', login_date) AS month,
        COUNT(DISTINCT user_id) AS active_users
    FROM user_logins
    WHERE login_date >= DATE_SUB(CURRENT_DATE, INTERVAL 12 MONTH)
    GROUP BY DATE_TRUNC('month', login_date)
),
user_cohorts AS (
    SELECT 
        u1.user_id,
        DATE_TRUNC('month', u1.login_date) AS cohort_month,
        DATE_TRUNC('month', u2.login_date) AS active_month
    FROM (
        SELECT user_id, MIN(login_date) AS login_date
        FROM user_logins
        GROUP BY user_id
    ) u1
    JOIN user_logins u2 ON u1.user_id = u2.user_id
)
SELECT 
    mau.month,
    mau.active_users,
    LAG(mau.active_users) OVER (ORDER BY mau.month) AS prev_month_users,
    ROUND(
        (mau.active_users * 100.0 / 
        LAG(mau.active_users) OVER (ORDER BY mau.month)), 2
    ) AS retention_rate
FROM monthly_active_users mau
ORDER BY mau.month;
```

## Shell 脚本示例

### 自动化部署

**Prompt**: "Bash 脚本：自动化部署，包含回滚功能"

```bash
#!/bin/bash

set -e

# 配置
APP_NAME="myapp"
DEPLOY_DIR="/var/www/$APP_NAME"
BACKUP_DIR="/var/backups/$APP_NAME"
GIT_REPO="git@github.com:user/repo.git"
BRANCH="main"

# 颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 创建备份
backup() {
    log "创建备份..."
    mkdir -p "$BACKUP_DIR"
    timestamp=$(date +%Y%m%d_%H%M%S)
    tar -czf "$BACKUP_DIR/backup_$timestamp.tar.gz" "$DEPLOY_DIR"
    log "备份完成：backup_$timestamp.tar.gz"
}

# 拉取代码
pull_code() {
    log "拉取最新代码..."
    cd "$DEPLOY_DIR"
    git fetch origin
    git checkout "$BRANCH"
    git pull origin "$BRANCH"
}

# 安装依赖
install_deps() {
    log "安装依赖..."
    if [ -f "package.json" ]; then
        npm ci --production
    elif [ -f "requirements.txt" ]; then
        pip install -r requirements.txt
    fi
}

# 重启服务
restart_service() {
    log "重启服务..."
    if [ -f "systemd.service" ]; then
        sudo systemctl restart "$APP_NAME"
    elif [ -f "Procfile" ]; then
        sudo supervisorctl restart all
    fi
}

# 回滚
rollback() {
    log "执行回滚..."
    latest_backup=$(ls -t "$BACKUP_DIR" | head -1)
    if [ -z "$latest_backup" ]; then
        error "未找到备份文件"
        exit 1
    fi
    
    tar -xzf "$BACKUP_DIR/$latest_backup" -C /
    log "回滚完成：$latest_backup"
    restart_service
}

# 主流程
main() {
    if [ "$1" == "rollback" ]; then
        rollback
        exit 0
    fi
    
    log "开始部署 $APP_NAME"
    
    backup
    pull_code
    install_deps
    restart_service
    
    log "部署完成！"
}

main "$@"
```

---

*最后更新：2026-03-15*
