#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
sense1 SEO 정비 스크립트 (재실행 안전)

하는 일
  1) 모든 *.html 의 <head> 에 SEO 메타를 주입 (canonical / description / og / twitter / GA / JSON-LD)
  2) sitemap.xml 을 실제 파일 목록 기준으로 재생성
  3) robots.txt 의 Sitemap 경로 교정

주의
  - Cloudflare Pages 가 .html 확장자를 자동으로 제거하므로 모든 URL은 **확장자 없는 절대경로**로 만든다.
    (.html 로 두면 308 리다이렉트가 발생해 색인에 불리하다)
  - 주입 블록은 <!-- SEO:BEGIN --> ~ <!-- SEO:END --> 로 감싸므로 재실행하면 깔끔히 교체된다.

사용:  python3 seo_fix.py
"""

import os, re, glob, json, html, datetime
from urllib.parse import quote

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = "https://sense1.pages.dev"
GA_ID = "G-L6H7ZKF5GE"
SITE_NAME = "KCA 바리스타 포털"
OG_IMAGE = SITE + "/assets/og-default.png"
TODAY = datetime.date.today().isoformat()

# robots.txt 에서 차단 중인 문서 + 사이트맵에 넣지 않을 것
EXCLUDE = {"kca.html", "404.html"}
# 검색엔진 소유확인용 파일 — 색인 대상이 아니므로 사이트맵/메타 주입에서 제외
EXCLUDE |= {f for f in os.listdir(ROOT) if re.match(r"^(naver|google)[0-9a-f]{8,}\.html$", f)}

BEGIN, END = "<!-- SEO:BEGIN -->", "<!-- SEO:END -->"


def clean_url(fname):
    """coffee-article-2026-07-25.html -> https://sense1.pages.dev/coffee-article-2026-07-25"""
    if fname == "index.html":
        return SITE + "/"
    # 사이트맵/캐노니컬은 URL 인코딩된 형태여야 한다 (한글 파일명 대응)
    return SITE + "/" + quote(fname[:-len(".html")], safe="-_./~")


def strip_tags(s):
    s = re.sub(r"<script.*?</script>", " ", s, flags=re.S | re.I)
    s = re.sub(r"<style.*?</style>", " ", s, flags=re.S | re.I)
    s = re.sub(r"<[^>]+>", " ", s)
    s = html.unescape(s)
    return re.sub(r"\s+", " ", s).strip()


def head_of(src):
    m = re.search(r"<head[^>]*>(.*?)</head>", src, flags=re.S | re.I)
    return m.group(1) if m else ""


def get_title(src):
    m = re.search(r"<title[^>]*>(.*?)</title>", src, flags=re.S | re.I)
    return strip_tags(m.group(1)) if m else SITE_NAME


def get_description(src):
    """기존 description 이 있으면 존중, 없으면 본문 첫 문단에서 생성"""
    h = head_of(src)
    m = re.search(r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']', h, flags=re.S | re.I)
    if m and m.group(1).strip():
        return strip_tags(m.group(1))[:300]

    body = re.sub(r"<head.*?</head>", " ", src, flags=re.S | re.I)
    for para in re.findall(r"<p[^>]*>(.*?)</p>", body, flags=re.S | re.I):
        t = strip_tags(para)
        if len(t) >= 30:
            return (t[:157] + "…") if len(t) > 158 else t
    # 문단이 없으면 h1/h2 로 대체
    for tag in ("h1", "h2"):
        m = re.search(r"<%s[^>]*>(.*?)</%s>" % (tag, tag), body, flags=re.S | re.I)
        if m:
            t = strip_tags(m.group(1))
            if t:
                return t[:158]
    return get_title(src)[:158]


def lastmod_of(fname):
    m = re.search(r"(\d{4}-\d{2}-\d{2})", fname)
    if m:
        try:
            datetime.date.fromisoformat(m.group(1))
            return m.group(1)
        except ValueError:
            pass
    return TODAY


def is_article(fname):
    return fname.startswith("coffee-article-") or "주식보고서" in fname


def esc(s):
    return html.escape(s, quote=True)


def build_block(fname, src):
    title = get_title(src)
    desc = get_description(src)
    url = clean_url(fname)
    h = head_of(src)

    parts = [BEGIN]

    # description — 기존에 없을 때만 새로 넣는다
    if not re.search(r'<meta\s+name=["\']description["\']', h, flags=re.I):
        parts.append('<meta name="description" content="%s">' % esc(desc))

    parts += [
        '<link rel="canonical" href="%s">' % url,
        '<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">',
        '<meta property="og:type" content="%s">' % ("article" if is_article(fname) else "website"),
        '<meta property="og:site_name" content="%s">' % esc(SITE_NAME),
        '<meta property="og:title" content="%s">' % esc(title),
        '<meta property="og:description" content="%s">' % esc(desc),
        '<meta property="og:url" content="%s">' % url,
        '<meta property="og:locale" content="ko_KR">',
        '<meta property="og:image" content="%s">' % OG_IMAGE,
        '<meta property="og:image:width" content="1200">',
        '<meta property="og:image:height" content="630">',
        '<meta name="twitter:card" content="summary_large_image">',
        '<meta name="twitter:image" content="%s">' % OG_IMAGE,
    ]

    if is_article(fname):
        d = lastmod_of(fname)
        parts += ['<meta property="article:published_time" content="%sT09:00:00+09:00">' % d,
                  '<meta property="article:modified_time" content="%sT09:00:00+09:00">' % d]

    # Google Analytics — 없을 때만
    if GA_ID not in src:
        parts.append(
            '<script async src="https://www.googletagmanager.com/gtag/js?id=%s"></script>'
            '<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}'
            'gtag("js",new Date());gtag("config","%s");</script>' % (GA_ID, GA_ID))

    # 구조화 데이터 — 없을 때만
    if "application/ld+json" not in h:
        org = {"@type": "Organization", "@id": SITE + "/#organization",
               "name": SITE_NAME, "url": SITE + "/"}
        node = {
            "@type": "Article" if is_article(fname) else "WebPage",
            "@id": url + "#page", "url": url,
            "headline" if is_article(fname) else "name": title,
            "description": desc, "inLanguage": "ko-KR",
            "image": OG_IMAGE,
            "isPartOf": {"@id": SITE + "/#website"},
        }
        if is_article(fname):
            d = lastmod_of(fname)
            node.update({"datePublished": d, "dateModified": d,
                         "author": {"@id": SITE + "/#organization"},
                         "publisher": {"@id": SITE + "/#organization"}})
        site = {"@type": "WebSite", "@id": SITE + "/#website", "url": SITE + "/",
                "name": SITE_NAME, "inLanguage": "ko-KR",
                "publisher": {"@id": SITE + "/#organization"}}
        graph = {"@context": "https://schema.org", "@graph": [org, site, node]}
        parts.append('<script type="application/ld+json">%s</script>'
                     % json.dumps(graph, ensure_ascii=False))

    parts.append(END)
    return "\n".join(parts)


def fix_file(path):
    fname = os.path.basename(path)
    with open(path, encoding="utf-8") as f:
        src = f.read()

    if "</head>" not in src.lower():
        return "head없음"

    # 죽은 도메인(kca-portal.com) URL 교정 — 이메일 주소는 건드리지 않는다
    src = src.replace("https://kca-portal.com", SITE).replace("http://kca-portal.com", SITE)

    # 이전 실행 블록 제거 — 앞뒤 공백까지 흡수해야 재실행 시 빈 줄이 쌓이지 않는다
    src = re.sub(r"[ \t]*\n?" + re.escape(BEGIN) + r".*?" + re.escape(END) + r"[ \t]*\n?",
                 "", src, flags=re.S)
    # 우리가 관리하는 태그 중 중복될 수 있는 것 제거 (head 안에서만)
    def clean_head(m):
        h = m.group(0)
        h = re.sub(r'[ \t]*<link[^>]+rel=["\']canonical["\'][^>]*>[ \t]*\n?', "", h, flags=re.I)
        h = re.sub(r'[ \t]*<meta[^>]+property=["\']og:[^"\']*["\'][^>]*>[ \t]*\n?', "", h, flags=re.I)
        h = re.sub(r'[ \t]*<meta[^>]+name=["\']twitter:[^"\']*["\'][^>]*>[ \t]*\n?', "", h, flags=re.I)
        h = re.sub(r"\n{3,}", "\n\n", h)          # 빈 줄 누적 방지
        h = re.sub(r"[ \t\n]*</head>", "\n</head>", h, flags=re.I)
        return h
    src = re.sub(r"<head[^>]*>.*?</head>", clean_head, src, flags=re.S | re.I)

    block = build_block(fname, src)
    src = re.sub(r"[ \t\n]*</head>", "\n" + block + "\n</head>", src, count=1, flags=re.I)

    with open(path, "w", encoding="utf-8") as f:
        f.write(src)
    return "ok"


def write_sitemap(files):
    urls = []
    for fname in files:
        pr = "1.0" if fname == "index.html" else ("0.9" if fname in ("knowledge.html", "board.html") else "0.7")
        urls.append(
            "  <url>\n    <loc>%s</loc>\n    <lastmod>%s</lastmod>\n"
            "    <changefreq>weekly</changefreq>\n    <priority>%s</priority>\n  </url>"
            % (clean_url(fname), lastmod_of(fname), pr))
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
           + "\n".join(urls) + "\n</urlset>\n")
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(xml)
    return len(urls)


def write_robots():
    txt = """User-agent: *
Allow: /

Disallow: /firebase-config.js
Disallow: /questions.js
Disallow: /firebase-debug.log
Disallow: /kca.html
Disallow: /text_kca.txt
Disallow: /.firebase/

# 네이버
User-agent: Yeti
Allow: /

# 다음(카카오)
User-agent: Daum
Allow: /

User-agent: Daumoa
Allow: /

# 구글
User-agent: Googlebot
Allow: /

User-agent: Googlebot-Image
Allow: /

# 빙
User-agent: Bingbot
Allow: /

Sitemap: %s/sitemap.xml
""" % SITE
    with open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(txt)


if __name__ == "__main__":
    files = sorted(os.path.basename(p) for p in glob.glob(os.path.join(ROOT, "*.html")))
    targets = [f for f in files if f not in EXCLUDE]

    stats = {}
    for f in targets:
        r = fix_file(os.path.join(ROOT, f))
        stats[r] = stats.get(r, 0) + 1

    n = write_sitemap(targets)
    write_robots()

    print("메타 주입: %s" % ", ".join("%s %d개" % (k, v) for k, v in stats.items()))
    print("sitemap.xml: %d개 URL (%s 기준)" % (n, SITE))
    print("robots.txt: 갱신 완료")
