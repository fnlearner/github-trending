#!/bin/sh
# Entrypoint: set up cron + keep container alive

CRON_SCHEDULE="${SCHEDULE:-30 9 * * *}"
WEBHOOK_URL="${SLACK_WEBHOOK_URL:-}"
TODAY_VAR="$(date +%Y-%m-%d)"

echo "[$(date)] Starting github-trending cron container"
echo "[$(date)] Schedule: $CRON_SCHEDULE"
echo "[$(date)] Webhook configured: $([ -n "$WEBHOOK_URL" ] && echo yes || echo NO)"

# Set up cron
echo "$CRON_SCHEDULE  TODAY_VAR=\"$(date +%Y-%m-%d)\" python3 /app/github-trending-daily.py >> /var/log/trending.log 2>&1" > /etc/crontabs/root
chmod 0600 /etc/crontabs/root

echo "[$(date)] Cron entries:"
cat /etc/crontabs/root

# Start cron daemon in background
crond -f -l 2 &

echo "[$(date)] Cron daemon started, keeping container alive..."

# Keep container running (tail -f instead of sleep to avoid signals)
tail -f /dev/null
