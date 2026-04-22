#!/usr/bin/env python3
"""GitHub Trending Daily — fetch & send to Slack."""

import sys, re, json, subprocess, os
from datetime import date

TODAY = date.today().isoformat()
WEBHOOK_URL = os.environ.get("SLACK_WEBHOOK_URL", "")

if not WEBHOOK_URL:
    print("SLACK_WEBHOOK_URL not set")
    sys.exit(1)

# Fetch HTML
try:
    result = subprocess.run(
        ["curl", "-s", "https://github.com/trending",
         "-H", "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
         "-L"],
        capture_output=True, text=True, timeout=15
    )
    html = result.stdout
except Exception as e:
    print(f"curl failed: {e}")
    sys.exit(1)

rows = re.findall(r"<article class=\"Box-row\">(.*?)</article>", html, re.DOTALL)
if not rows:
    print("No repos found")
    sys.exit(1)

blocks = [
    {
        "type": "header",
        "text": {"type": "plain_text", "text": f"GitHub Trending — {TODAY}", "emoji": True}
    },
    {"type": "divider"}
]

for row in rows:
    paths = re.findall(r"/([a-zA-Z0-9_\-]+/[a-zA-Z0-9_\-\.]+)", row)
    real_paths = [p for p in paths
                  if len(p.split("/")) == 2
                  and p.split("/")[0] not in ("join","login","orgs","sponsors","search",
                                               "features","trending","explore","settings",
                                               "notifications","new","pulls","issues",
                                               "marketplace","packages","discussions")]
    lang_m = re.search(r"programmingLanguage[^>]*>([^<]+)<", row)
    lang = lang_m.group(1).strip() if lang_m else ""
    today_m = re.search(r"([\d,]+) stars today", row)
    today = today_m.group(1) if today_m else "0"
    desc_m = re.search(r"<p[^>]*>([^<]+)</p>", row)
    desc = desc_m.group(1).strip()[:80] if desc_m else ""

    if real_paths:
        url = "https://github.com/" + real_paths[0]
        name = real_paths[0]
        text = f"*{today} stars today*\n<{url}|{name}>"
        if lang:
            text += f" | _{lang}_"
        text += f"\n>{desc}"
        blocks.append({"type": "section", "text": {"type": "mrkdwn", "text": text}})

blocks.append({"type": "divider"})
blocks.append({
    "type": "context",
    "elements": [{"type": "mrkdwn", "text": f"Source: github.com/trending | {TODAY}"}]
})

payload = json.dumps({"blocks": blocks})

# Send to Slack
try:
    r = subprocess.run(
        ["curl", "-s", "-X", "POST", WEBHOOK_URL,
         "-H", "Content-Type: application/json",
         "-d", payload],
        capture_output=True, text=True, timeout=10
    )
    if r.returncode == 0:
        print("OK")
    else:
        print(f"Slack error: {r.stderr}")
except Exception as e:
    print(f"Slack send failed: {e}")
