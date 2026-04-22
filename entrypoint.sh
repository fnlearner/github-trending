#!/bin/sh
# Entrypoint: start cron daemon + run script on schedule

echo "30 9 * * *  python3 /app/github-trending-daily.py >> /var/log/trending.log 2>&1" > /etc/crontabs/root

chmod 0644 /etc/crontabs/root

# Run cron in background
crond -f -l 2 &
