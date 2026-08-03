#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ads_fix.py — 카카오 애드핏 광고 스니펫 자동 주입 (재실행 안전 · 멱등)

왜 이 파일이 생겼나 (2026-08-03)
--------------------------------
2026-06-25 ~ 08-02, 39일간 매일 올린 커피 아티클 37개에 애드핏 광고가
단 하나도 들어가지 않았다. 자동 생성 템플릿에서 스니펫이 빠진 채로
배포가 반복된 것이 원인이다. 검색 유입이 가장 많이 몰리는 최신 글들이
그 기간 내내 무수익 상태였다.

사람이 매번 스니펫을 복사해 넣는 방식은 또 빠진다. 그래서 seo_fix.py 와
같은 방식으로 스크립트가 강제 주입하도록 만들었다.

사용법
------
    python3 ads_fix.py            # 커피 아티클 검사 + 누락분 주입 (기본)
    python3 ads_fix.py --check    # 주입 없이 누락 현황만 출력 (CI 용)
    python3 ads_fix.py --all      # 커피 아티클 외 전체 페이지까지 확대

update_knowledge.py 가 글 추가 시 자동으로 호출한다. 따로 외울 필요 없다.

주의
----
- 이미 kakao_ad_area 가 있는 파일은 건드리지 않는다 (멱등).
- <body> 가 정확히 1개가 아닌 파일은 안전을 위해 건너뛴다.
- 기본 범위는 SCOPE 패턴(커피 아티클)이다. 성경 시리즈·주식보고서 등은
  --all 로 명시해야 대상이 된다. 매일 도는 자동 워크플로우가 의도치 않게
  다른 페이지를 건드리지 않게 하려는 안전장치다.
- 광고를 넣지 않을 페이지는 EXCLUDE 에 추가한다.
"""

import os, sys, glob

ROOT = os.path.dirname(os.path.abspath(__file__))

# 기본 대상 — 매일 자동 생성되는 커피 아티클
SCOPE = "coffee-article*.html"

# 애드핏 광고 유닛 ID — 애드핏 콘솔에서 발급받은 값
UNIT_TOP = "DAN-hn8rh47xe9PjfTNC"      # 300x250 상단 배너
UNIT_SIDE = "DAN-q3Gqza2plqVgg8uW"     # 160x600 사이드바

# 새 도메인(*.ephseed.com) 전용 유닛 (2026-08-03 발급)
# 애드핏 매체는 도메인 단위로 등록된다. 위의 옛 유닛은 *.pages.dev 매체에
# 묶여 있어 새 도메인에서는 채워지지 않는다. 그래서 별도로 발급받았다.
UNIT_NEW = "DAN-9S7Ka99jukqetMgb"
UNIT_NEW_W = 300
UNIT_NEW_H = 250

# 광고를 넣지 않을 페이지 (약관·개인정보처리방침·에러·소유확인 파일 등)
EXCLUDE = {
    "404.html",
    "privacy.html",
    "terms.html",
    # 검색엔진 소유확인 파일 — 색인 대상이 아니다
    "naver3d47fe98e4401d5badee383f9e39359d.html",
}

TOP_AD = '''
<!-- ============================================= -->
<!-- 카카오 애드핏: 상단 배너 (300x250)            -->
<!-- 페이지 최상단, 콘텐츠 시작 직전 위치            -->
<!-- ads_fix.py 가 자동 주입 — 직접 지우지 말 것     -->
<!-- ============================================= -->
<div class="kakao-top-ad" style="display:flex;justify-content:center;margin:20px auto 30px;width:fit-content;background:rgba(255,255,255,0.95);border-radius:12px;padding:10px;box-shadow:0 4px 20px rgba(0,0,0,0.08);">
    <ins class="kakao_ad_area" style="display:none;"
    data-ad-unit="__UNIT_TOP__"
    data-ad-width="300"
    data-ad-height="250"></ins>
</div>
'''.replace('__UNIT_TOP__', UNIT_TOP)

BOTTOM_AD = '''
<!-- ============================================= -->
<!-- 카카오 애드핏: 우측 사이드바 고정 광고 (160x600) -->
<!-- 데스크탑: 화면 오른쪽 고정 / 태블릿 이하: 하단   -->
<!-- ads_fix.py 가 자동 주입 — 직접 지우지 말 것     -->
<!-- ============================================= -->
<style>
  .kakao-sidebar-fixed{position:fixed;right:20px;top:50%;transform:translateY(-50%);z-index:900;background:rgba(255,255,255,0.95);border-radius:12px;padding:10px;box-shadow:0 4px 20px rgba(0,0,0,0.08);border:1px solid rgba(0,0,0,0.08);}
  @media (max-width:1400px){.kakao-sidebar-fixed{position:static;transform:none;display:flex;justify-content:center;margin:30px auto;width:fit-content;}}
</style>
<div class="kakao-sidebar-fixed">
    <ins class="kakao_ad_area" style="display:none;"
    data-ad-unit="__UNIT_SIDE__"
    data-ad-width="160"
    data-ad-height="600"></ins>
</div>
<!-- 새 도메인 전용 유닛 -->
<div class="kakao-ad-lead" style="display:flex;justify-content:center;align-items:center;margin:14px auto;max-width:100%;overflow:hidden;">
<ins class="kakao_ad_area" style="display:none;"
data-ad-unit="__UNIT_NEW__"
data-ad-width="__UNIT_NEW_W__"
data-ad-height="__UNIT_NEW_H__"></ins>
</div>
<style>
/* 728x90 은 모바일 화면에 들어가지 않는다. 가로 넘침·미노출 방지 */
@media (max-width:767px){
  ins.kakao_ad_area[data-ad-width="728"]{display:none !important;}
  .fixed-top-ad{display:none !important;}
}
</style>
<script type="text/javascript" src="//t1.kakaocdn.net/kas/static/ba.min.js" async></script>
'''.replace('__UNIT_SIDE__', UNIT_SIDE).replace('__UNIT_NEW__', UNIT_NEW).replace('__UNIT_NEW_W__', str(UNIT_NEW_W)).replace('__UNIT_NEW_H__', str(UNIT_NEW_H))


def inject(path, dry=False):
    """반환값: 'ok' | 'already' | 'skip:<사유>'"""
    fname = os.path.basename(path)
    with open(path, encoding="utf-8") as f:
        src = f.read()

    if "kakao_ad_area" in src:
        return "already"
    if src.count("<body>") != 1 or src.count("</body>") != 1:
        return "skip:body 태그가 1개가 아님"

    new = src.replace("<body>", "<body>\n" + TOP_AD, 1)
    new = new.replace("</body>", BOTTOM_AD + "\n</body>", 1)

    # 삽입 검증 — 실패하면 파일을 건드리지 않는다
    # CSS 선택자에도 kakao_ad_area 문자열이 들어가므로 <ins 태그만 센다
    if new.count('<ins class="kakao_ad_area"') != 3 or new.count("ba.min.js") != 1:
        return "skip:삽입 검증 실패"

    if not dry:
        with open(path, "w", encoding="utf-8") as f:
            f.write(new)
    return "ok"


def main():
    dry = "--check" in sys.argv
    pattern = "*.html" if "--all" in sys.argv else SCOPE
    files = sorted(os.path.basename(p) for p in glob.glob(os.path.join(ROOT, pattern)))
    targets = [f for f in files if f not in EXCLUDE]

    stats, injected, skipped = {}, [], []
    for f in targets:
        r = inject(os.path.join(ROOT, f), dry=dry)
        key = r.split(":")[0]
        stats[key] = stats.get(key, 0) + 1
        if r == "ok":
            injected.append(f)
        elif r.startswith("skip"):
            skipped.append((f, r.split(":", 1)[1]))

    mode = "검사만" if dry else "주입"
    scope = "전체 페이지" if "--all" in sys.argv else "커피 아티클"
    print("애드핏 %s (%s): 대상 %d개 / 이미 있음 %d개 / 신규 %d개 / 건너뜀 %d개"
          % (mode, scope, len(targets), stats.get("already", 0),
             stats.get("ok", 0), stats.get("skip", 0)))

    if injected:
        print("  신규 주입:")
        for f in injected[:20]:
            print("    -", f)
        if len(injected) > 20:
            print("    ... 외 %d개" % (len(injected) - 20))

    if skipped:
        print("  ⚠️ 건너뜀 (수동 확인 필요):")
        for f, why in skipped:
            print("    -", f, "—", why)

    # --check 모드에서 누락이 있으면 종료코드 1 (CI 에서 실패 처리 가능)
    if dry and stats.get("ok", 0) > 0:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
