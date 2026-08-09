#!/usr/bin/env python3
"""
sense1 레포 자동 실행 스크립트
새 커피 아티클이 추가될 때 knowledge-data.js를 자동으로 갱신합니다.
사용법: python3 update_knowledge.py --date 2026-07-23 --html coffee-article-2026-07-23.html
"""
import re, sys, os, argparse

# 주제 순환 (day % 7)
TOPIC_MAP = {
    0: {"emoji": "📈", "category": "스페셜티 커피 트렌드",      "categoryColor": '{ bg: "#e0f2fe", text: "#0369a1" }'},
    1: {"emoji": "☕", "category": "추출 기법 심층 가이드",      "categoryColor": '{ bg: "#dcfce7", text: "#166534" }'},
    2: {"emoji": "🔥", "category": "로스팅 & 원두 과학",         "categoryColor": '{ bg: "#fef3c7", text: "#92400e" }'},
    3: {"emoji": "🎨", "category": "바리스타 스킬 & 라떼아트",   "categoryColor": '{ bg: "#fce7f3", text: "#9d174d" }'},
    4: {"emoji": "🏪", "category": "카페 창업 & 운영 실전",      "categoryColor": '{ bg: "#fee2e2", text: "#991b1b" }'},
    5: {"emoji": "🌋", "category": "원두 산지 & 테루아르",       "categoryColor": '{ bg: "#ecfccb", text: "#3f6212" }'},
    6: {"emoji": "☕", "category": "커피 품종 & 가공법",          "categoryColor": '{ bg: "#fef3c7", text: "#92400e" }'},
}

def extract_info(html_path):
    """HTML 파일에서 title, summary 추출"""
    html = open(html_path, encoding='utf-8').read()
    # title
    t = re.search(r'<title>(.*?)</title>', html, re.DOTALL)
    title = re.sub(r'<[^>]+>', '', t.group(1)).strip() if t else ''
    # | 구분자 제거 (사이트명 제거)
    title = title.split('|')[0].strip()
    # hook or summary
    h = re.search(r'class="hook[^"]*"[^>]*>(.*?)</p>', html, re.DOTALL)
    if h:
        summary = re.sub(r'<[^>]+>', '', h.group(1)).replace('\n', ' ').strip()
    else:
        summary = title
    # 쌍따옴표 이스케이프
    title = title.replace('"', '\\"')
    summary = summary.replace('"', '\\"')[:350]
    return title, summary

def get_max_id(kd_content):
    ids = [int(x) for x in re.findall(r'id:\s*(\d+)', kd_content)]
    return max(ids) if ids else 0

def already_has_link(kd_content, link):
    return link in kd_content

def add_entry(kd_path, date_str, html_filename, html_path=None):
    """knowledge-data.js에 새 엔트리 추가"""
    content = open(kd_path, encoding='utf-8').read()

    if already_has_link(content, html_filename):
        print(f"[SKIP] {html_filename} 이미 존재")
        return False

    # 날짜에서 day 추출
    day = int(date_str.split('-')[2])
    topic = TOPIC_MAP[day % 7]
    new_id = get_max_id(content) + 1

    # HTML에서 title/summary 추출
    if html_path and os.path.exists(html_path):
        title, summary = extract_info(html_path)
    else:
        title = html_filename.replace('.html', '').replace('-', ' ')
        summary = title

    date_display = date_str.replace('-', '.')  # 2026.07.23

    entry = f"""  {{
    id: {new_id}, emoji: "{topic['emoji']}", category: "{topic['category']}",
    categoryColor: {topic['categoryColor']},
    title: "{title}",
    date: "{date_display}",
    summary: "{summary}",
    link: "{html_filename}"
  }},"""

    updated = content.replace(
        "export const knowledgeArticles = [",
        "export const knowledgeArticles = [\n" + entry
    )
    open(kd_path, 'w', encoding='utf-8').write(updated)
    print(f"[OK] 추가 완료: id={new_id}, date={date_display}, title={title[:60]}...")
    return True

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--date', required=True, help='YYYY-MM-DD')
    parser.add_argument('--html', required=True, help='coffee-article-YYYY-MM-DD.html')
    parser.add_argument('--html-path', default=None, help='HTML 파일 전체 경로 (없으면 현재 디렉토리)')
    parser.add_argument('--kd', default='knowledge-data.js', help='knowledge-data.js 경로')
    args = parser.parse_args()

    html_full = args.html_path or os.path.join(os.path.dirname(args.kd), args.html)
    add_entry(args.kd, args.date, args.html, html_full)

    # ------------------------------------------------------------------
    # SEO 자동 정비 (2026-07-25 추가)
    # 새 글에 canonical·og·GA·구조화 데이터를 주입하고 sitemap.xml 을 갱신한다.
    # 이 단계를 건너뛰면 새 글이 검색엔진에 색인되지 않는다.
    # 별도 명령을 외우지 않아도 되도록 여기에 연결해 두었다.
    # ------------------------------------------------------------------
    try:
        import subprocess
        repo_dir = os.path.dirname(os.path.abspath(__file__))
        seo = os.path.join(repo_dir, 'seo_fix.py')
        if os.path.exists(seo):
            r = subprocess.run([sys.executable, seo], capture_output=True, text=True, cwd=repo_dir)
            print((r.stdout or '').strip() or (r.stderr or '').strip())
            if r.returncode != 0:
                print('[WARN] seo_fix.py 실패 — 커밋 전에 `python3 seo_fix.py` 를 수동 실행하세요.')
        else:
            print('[WARN] seo_fix.py 를 찾지 못했습니다. sitemap.xml 이 갱신되지 않았습니다.')
    except Exception as e:
        print('[WARN] SEO 정비 중 오류: %s' % e)

    # ------------------------------------------------------------------
    # 애드핏 광고 자동 주입 (2026-08-03 추가)
    # 2026-06-25 ~ 08-02 사이 커피 아티클 37개에 광고가 통째로 빠진 채
    # 39일간 배포된 사고가 있었다. 사람이 매번 스니펫을 넣는 방식으로는
    # 또 빠지므로 스크립트가 강제 주입하도록 여기에 연결한다.
    # 이 단계를 건너뛰면 새 글이 무수익 상태로 배포된다.
    # ------------------------------------------------------------------
    try:
        import subprocess
        repo_dir = os.path.dirname(os.path.abspath(__file__))
        ads = os.path.join(repo_dir, 'ads_fix.py')
        if os.path.exists(ads):
            r = subprocess.run([sys.executable, ads], capture_output=True, text=True, cwd=repo_dir)
            print((r.stdout or '').strip() or (r.stderr or '').strip())
            if r.returncode != 0:
                print('[WARN] ads_fix.py 실패 — 커밋 전에 `python3 ads_fix.py` 를 수동 실행하세요.')
        else:
            print('[WARN] ads_fix.py 를 찾지 못했습니다. 새 글에 광고가 없을 수 있습니다.')
    except Exception as e:
        print('[WARN] 광고 주입 중 오류: %s' % e)

    # ------------------------------------------------------------------
    # 관련 글 내부 링크 자동 삽입 (2026-08-08 추가)
    # 새 글뿐 아니라 기존 글의 관련 글 목록도 갱신한다
    # (새 글이 추가되면 같은 주제 기존 글에 새 글이 관련 글로 뜨도록)
    # ------------------------------------------------------------------
    try:
        repo_dir = os.path.dirname(os.path.abspath(__file__))
        il = os.path.join(repo_dir, 'internal_links.py')
        if os.path.exists(il):
            r = subprocess.run([sys.executable, il], capture_output=True, text=True, cwd=repo_dir)
            print((r.stdout or '').strip() or (r.stderr or '').strip())
        else:
            print('[WARN] internal_links.py 없음 — 관련 글 미삽입')
    except Exception as e:
        print('[WARN] 관련 글 삽입 중 오류: %s' % e)

    # ------------------------------------------------------------------
    # IndexNow 즉시 색인 신청 (2026-08-08 추가)
    # 새 글 URL을 Bing·Yandex·IndexNow 네트워크에 즉시 통보한다
    # ------------------------------------------------------------------
    try:
        from importlib.util import spec_from_file_location, module_from_spec
        repo_dir = os.path.dirname(os.path.abspath(__file__))
        ix_path  = os.path.join(repo_dir, 'indexnow_notify.py')
        if os.path.exists(ix_path):
            spec = spec_from_file_location("indexnow_notify", ix_path)
            ix   = module_from_spec(spec)
            spec.loader.exec_module(ix)
            # URL은 .html 확장자 없는 형태 (Cloudflare Pages canonical)
            article_slug = args.html.replace('.html', '')
            ix.notify(f"https://coffee.ephseed.com/{article_slug}")
        else:
            print('[WARN] indexnow_notify.py 없음 — IndexNow 미신청')
    except Exception as e:
        print('[WARN] IndexNow 신청 중 오류: %s' % e)
