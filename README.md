# GitHub Trending Daily

每天自动抓取 GitHub Trending，发送到 Slack 频道。

## 功能

- 抓取 github.com/trending 当天热门项目
- 格式化输出：项目名、描述、语言、今日 ★ 数、链接
- 通过 Slack Incoming Webhook 推送消息

## 部署（Docker）

### 1. 镜像

```
docker.io/kidding123/github-trending:latest
```

### 2. 环境变量

| 变量 | 必填 | 说明 |
|------|------|------|
| `SLACK_WEBHOOK_URL` | ✅ | Slack Incoming Webhook URL |
| `SCHEDULE` | ❌ | Cron 表达式，默认 `30 1 * * *`（UTC 01:30 = 北京时间 09:30）|

### 3. 时区对照

| 北京时间 | UTC |
|---------|-----|
| 09:30 | 01:30 |
| 10:00 | 02:00 |
| 20:00 | 12:00 |

### 4. 本地测试

```bash
docker run --rm \
  -e SLACK_WEBHOOK_URL="https://hooks.slack.com/services/..." \
  -e SCHEDULE="* * * * *" \
  docker.io/kidding123/github-trending:latest
```

## 本地开发

```bash
# 依赖：python3, curl

# 直接运行
SLACK_WEBHOOK_URL="https://hooks.slack.com/services/..." \
  python3 github-trending-daily.py
```

## Slack Webhook 创建

1. https://api.slack.com/apps > Create New App > Incoming Webhooks
2. 选择目标频道
3. 复制 Webhook URL

## CI/CD

每次 push 到 `main` 自动构建 Docker 镜像并推送到 Docker Hub。
