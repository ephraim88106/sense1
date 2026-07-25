# sense1 SEO 운영 가이드

## 한 줄 요약

**새 글을 추가한 뒤 `python3 update_knowledge.py ...` 를 실행하면 SEO 정비가 자동으로 따라온다.**
별도로 외울 명령은 없다.

## 왜 이 파일이 생겼나 (2026-07-25)

이전까지 아래 문제가 있었다.

- `canonical` 과 `sitemap.xml` 전체가 **`kca-portal.com`** 을 가리키고 있었다.
  이 도메인은 **DNS에 등록되어 있지 않다**(A/NS 레코드 없음). 검색엔진 입장에서는
  "정본이 존재하지 않는 페이지"라 색인 대상에서 제외된다.
- `sitemap.xml` 이 2026-07-17 이후 갱신되지 않아 **8일치 글이 검색엔진에 노출되지 않았다.**
- 158개 페이지 중 대부분에 `description` · `og:*` · 구조화 데이터가 없었다.
- Google Analytics 가 일부 페이지에만 들어 있었다.

## 구조

```
seo_fix.py           SEO 정비 스크립트 (재실행 안전 · 멱등)
update_knowledge.py  글 추가 시 실행 → 내부에서 seo_fix.py 를 자동 호출
sitemap.xml          seo_fix.py 가 생성 (직접 수정하지 말 것)
robots.txt           seo_fix.py 가 생성 (직접 수정하지 말 것)
assets/og-default.png  공유용 대표 이미지
```

## seo_fix.py 가 하는 일

1. 모든 `*.html` 의 `<head>` 에 아래를 주입
   `canonical` · `robots` · `og:*` · `twitter:*` · Google Analytics · JSON-LD
   (기존 `description` 이 있으면 그대로 존중하고, 없을 때만 본문 첫 문단에서 생성)
2. 실제 파일 목록을 스캔해 `sitemap.xml` 재생성
3. `robots.txt` 재생성 — 네이버 `Yeti`, 다음 `Daumoa` 명시 허용 포함

주입 블록은 `<!-- SEO:BEGIN -->` ~ `<!-- SEO:END -->` 로 감싸여 있어
몇 번을 다시 돌려도 결과가 동일하다(멱등). 빈 줄이 쌓이지 않는다.

## ⚠️ URL 규칙 — 반드시 지킬 것

Cloudflare Pages 는 `.html` 확장자를 자동으로 제거한다.
`/coffee-article-2026-07-25.html` 로 접근하면 **308 리다이렉트**가 걸린다.

그래서 `canonical` 과 `sitemap.xml` 의 URL은 모두 **확장자 없는 절대경로**로 만든다.

```
O  https://sense1.pages.dev/coffee-article-2026-07-25
X  https://sense1.pages.dev/coffee-article-2026-07-25.html
```

한글 파일명은 URL 인코딩된다(`주식보고서` → `%EC%A3%BC...`). 이는 사이트맵 표준 요구사항이다.

## 도메인을 바꿀 때

`seo_fix.py` 의 `SITE` 상수 한 줄만 고치고 다시 실행하면
canonical · 사이트맵 · robots · OG URL 이 전부 따라온다.

```python
SITE = "https://sense1.pages.dev"
```

단, `assets/og-default.png` 안에 주소 텍스트가 그려져 있으므로 이미지도 새로 만들어야 한다.

## 남은 할 일

- [ ] `contact.html` · `privacy.html` 의 이메일이 `help@kca-portal.com` 으로 되어 있다.
      **존재하지 않는 도메인이라 메일이 실제로 도착하지 않는다.** 실제 주소로 교체 필요.
- [ ] Google Search Console 에 사이트맵 제출 (`https://sense1.pages.dev/sitemap.xml`)
- [ ] 네이버 서치어드바이저에 사이트맵 제출 및 웹페이지 수집 요청
