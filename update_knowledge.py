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
