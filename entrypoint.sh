#!/bin/sh
# Entrypoint: set up cron + keep container alive

CRON_SCHEDULE="${SCHEDULE:-30 21 * * *}"  # 21:30 EDT = 09:30 next day Beijing (UTC+8)
WEBHOOK_URL="${SLACK_WEBHOOK_URL:-}"

echo "[$(date)] Starting github-trending cron container"
echo "[$(date)] Schedule: $CRON_SCHEDULE (US East, UTC-4)"
echo "[$(date)] 09:30 EDT = 21:30 previous day EDT = Beijing 09:30"
echo "[$(date)] Webhook configured: $([ -n "$WEBHOOK_URL" ] && echo yes || echo NO)"

# Set up cron — TODAY_VAR evaluated at job execution time by Python
echo "$CRON_SCHEDULE  python3 /app/github-trending-daily.py >> /var/log/trending.log 2>&1" > /etc/crontabs/root
chmod 0600 /etc/crontabs/root

echo "[$(date)] Cron entries:"
cat /etc/crontabs/root

# Start cron daemon in background
crond -f -l 2 &

echo "[$(date)] Cron daemon started, keeping container alive..."

# Keep container running (tail -f instead of sleep to avoid signals)
tail -f /dev/null
