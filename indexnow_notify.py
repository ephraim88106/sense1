#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IndexNow 즉시 색인 신청 모듈 (2026-08-08 추가)

새 아티클을 발행할 때마다 Bing·Yandex·IndexNow 네트워크에
URL을 즉시 통보한다. 구글은 직접 지원하지 않지만
Bing이 색인하면 빠르게 따라오는 경향이 있다.

단독 실행: python3 indexnow_notify.py <url>
모듈 호출: from indexnow_notify import notify
"""

import sys
import json
import urllib.request
import urllib.error

INDEXNOW_KEY = "a3f8c2e1b4d795603e827a4f1c8b5d09"
SITE         = "https://coffee.ephseed.com"
KEY_LOCATION = f"{SITE}/{INDEXNOW_KEY}.txt"

# IndexNow 지원 엔드포인트 목록 (Bing이 다른 엔진에도 전파함)
ENDPOINTS = [
    "https://api.indexnow.org/indexnow",
    "https://www.bing.com/indexnow",
]


def notify(url: str) -> None:
    """단일 URL을 모든 IndexNow 엔드포인트에 신청한다."""
    payload = json.dumps({
        "host":        "coffee.ephseed.com",
        "key":         INDEXNOW_KEY,
        "keyLocation": KEY_LOCATION,
        "urlList":     [url],
    }, ensure_ascii=False).encode("utf-8")

    for endpoint in ENDPOINTS:
        req = urllib.request.Request(
            endpoint,
            data=payload,
            headers={"Content-Type": "application/json; charset=utf-8"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                status = resp.status
            if status in (200, 202):
                print(f"[IndexNow] ✅ {endpoint.split('/')[2]} → {status} OK")
            else:
                print(f"[IndexNow] ⚠️  {endpoint.split('/')[2]} → {status}")
        except urllib.error.HTTPError as e:
            print(f"[IndexNow] ❌ {endpoint.split('/')[2]} HTTP {e.code}: {e.reason}")
        except Exception as e:
            print(f"[IndexNow] ❌ {endpoint.split('/')[2]}: {e}")


def notify_batch(urls: list) -> None:
    """여러 URL을 한 번에 신청한다 (최대 10,000건)."""
    if not urls:
        return
    payload = json.dumps({
        "host":        "coffee.ephseed.com",
        "key":         INDEXNOW_KEY,
        "keyLocation": KEY_LOCATION,
        "urlList":     urls[:10000],
    }, ensure_ascii=False).encode("utf-8")

    for endpoint in ENDPOINTS:
        req = urllib.request.Request(
            endpoint,
            data=payload,
            headers={"Content-Type": "application/json; charset=utf-8"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                status = resp.status
            if status in (200, 202):
                print(f"[IndexNow 배치] ✅ {endpoint.split('/')[2]} → {status} ({len(urls)}건)")
            else:
                print(f"[IndexNow 배치] ⚠️  {endpoint.split('/')[2]} → {status}")
        except Exception as e:
            print(f"[IndexNow 배치] ❌ {endpoint.split('/')[2]}: {e}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("사용법: python3 indexnow_notify.py <url>")
        print(f"예시 : python3 indexnow_notify.py {SITE}/coffee-article-2026-08-08")
        sys.exit(1)
    notify(sys.argv[1])
