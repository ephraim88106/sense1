#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
관련 글(내부 링크) 자동 삽입 스크립트 (2026-08-08 추가)

카테고리 이름이 시기마다 달라도 키워드 기반으로 주제 그룹핑해서
같은 주제 글을 최신순 3개 링크한다. 재실행 시 중복 없이 교체(마커 방식).

사용: python3 internal_links.py
"""

import os, re, glob

ROOT    = os.path.dirname(os.path.abspath(__file__))
SITE    = "https://coffee.ephseed.com"
KD_PATH = os.path.join(ROOT, "knowledge-data.js")
BEGIN   = "<!-- RELATED:BEGIN -->"
END     = "<!-- RELATED:END -->"

# 주제 그룹 — 카테고리명에 아래 키워드 중 하나라도 포함되면 해당 그룹
TOPIC_GROUPS = [
    ("추출",  ["추출"]),
    ("로스팅", ["로스팅"]),
    ("창업",  ["창업"]),
    ("산지",  ["산지", "농장", "테루아르"]),
    ("품종",  ["품종", "가공"]),
    ("트렌드", ["트렌드", "글로벌", "스페셜티 커피"]),
    ("바리스타", ["바리스타", "라떼아트", "스킬"]),
]

def categorize(cat_str):
    for group_name, keywords in TOPIC_GROUPS:
        if any(kw in cat_str for kw in keywords):
            return group_name
    return "기타"


def parse_knowledge():
    raw = open(KD_PATH, encoding="utf-8").read()
    pattern = re.compile(
        r'\{\s*id:\s*(\d+).*?'
        r'emoji:\s*["\']([^"\']*)["\'].*?'
        r'category:\s*["\']([^"\']*)["\'].*?'
        r'title:\s*"([^"]*)".*?'
        r'date:\s*"([^"]*)".*?'
        r'link:\s*"([^"]*)"',
        re.S
    )
    articles = []
    for m in pattern.finditer(raw):
        link = m.group(6)
        if not link.startswith("coffee-article-"):
            continue
        articles.append({
            "id":       m.group(1),
            "emoji":    m.group(2),
            "category": m.group(3),
            "group":    categorize(m.group(3)),
            "title":    m.group(4),
            "date":     m.group(5),
            "link":     link,
        })
    return articles


CARD_STYLE = """<style>
.related-section{margin:48px 0 0;padding:32px 0 0;border-top:2px solid #e8d8c8}
.related-section h3{font-size:17px;font-weight:900;color:#2c1810;margin-bottom:20px}
.related-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:14px}
.related-card{background:#fff;border:1px solid #e8d8c8;border-radius:10px;padding:16px 18px;
  text-decoration:none;color:inherit;display:block;transition:box-shadow .2s,transform .2s}
.related-card:hover{box-shadow:0 6px 20px rgba(107,58,42,.13);transform:translateY(-2px)}
.related-card .rc-cat{font-size:11px;font-weight:700;color:#c8860a;margin-bottom:6px}
.related-card .rc-title{font-size:13.5px;font-weight:700;color:#2c1810;line-height:1.45;
  display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden}
.related-card .rc-date{font-size:11px;color:#a08070;margin-top:8px}
</style>"""


def build_block(picks):
    cards = ""
    for a in picks:
        url   = f"{SITE}/{a['link'].replace('.html', '')}"
        title = a["title"].replace('"', '&quot;').replace("'", "&#39;")
        date  = a["date"].replace(".", ". ")
        cards += (
            f'<a class="related-card" href="{url}">'
            f'<div class="rc-cat">{a["emoji"]} {a["category"]}</div>'
            f'<div class="rc-title">{title}</div>'
            f'<div class="rc-date">{date}</div></a>'
        )
    return (
        f"\n{BEGIN}\n"
        f"{CARD_STYLE}\n"
        f'<div class="related-section">'
        f'<h3>📚 함께 읽으면 좋은 글</h3>'
        f'<div class="related-grid">{cards}</div>'
        f'</div>\n'
        f"{END}\n"
    )


def inject(path, block):
    with open(path, encoding="utf-8") as f:
        src = f.read()
    # 기존 블록 제거
    src = re.sub(re.escape(BEGIN) + r".*?" + re.escape(END), "", src, flags=re.S)
    # 삽입 위치 우선순위: .tags div → /article-body → </body>
    for anchor in [r'(<div class="tags")', r'(</div><!-- /article-body -->)', r'(</body>)']:
        new = re.sub(anchor, block + r'\1', src, count=1, flags=re.I)
        if new != src:
            with open(path, "w", encoding="utf-8") as f:
                f.write(new)
            return True
    return False


def run():
    articles = parse_knowledge()
    if not articles:
        print("[WARN] knowledge-data.js 파싱 실패")
        return

    # 그룹별 인덱스 (날짜 내림차순)
    by_group = {}
    link_map  = {}
    for a in articles:
        link_map[a["link"]] = a
        by_group.setdefault(a["group"], []).append(a)
    for g in by_group:
        by_group[g].sort(key=lambda x: x["date"], reverse=True)

    html_files = sorted(glob.glob(os.path.join(ROOT, "coffee-article-*.html")))
    ok = skip = err = 0

    for path in html_files:
        fname = os.path.basename(path)
        meta  = link_map.get(fname)
        if not meta:
            skip += 1
            continue

        pool  = [a for a in by_group.get(meta["group"], []) if a["link"] != fname]
        picks = pool[:3]
        if not picks:
            skip += 1
            continue

        if inject(path, build_block(picks)):
            ok += 1
        else:
            err += 1

    print(f"[관련 글] ✅ 삽입 완료: {ok}개 / 건너뜀: {skip}개 / 실패: {err}개")


if __name__ == "__main__":
    run()
