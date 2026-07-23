#!/bin/bash
# sense1 커피 아티클 자동 푸시 스크립트
# 사용법: bash push_article.sh <날짜 YYYY-MM-DD> <HTML파일 경로>
# 예시:   bash push_article.sh 2026-07-23 /path/to/coffee-article-2026-07-23.html
#
# 토큰 설정: 환경변수 GITHUB_TOKEN 또는 ~/.sense1_token 파일에 토큰을 저장하세요.

set -e

DATE="$1"
HTML_SRC="$2"

if [ -z "$DATE" ] || [ -z "$HTML_SRC" ]; then
  echo "사용법: bash push_article.sh <YYYY-MM-DD> <HTML_파일_경로>"
  exit 1
fi

# 토큰 로드 (환경변수 우선, 없으면 파일에서 읽기)
if [ -n "$GITHUB_TOKEN" ]; then
  TOKEN="$GITHUB_TOKEN"
elif [ -f "$HOME/.sense1_token" ]; then
  TOKEN=$(cat "$HOME/.sense1_token" | tr -d '\n')
else
  echo "오류: GITHUB_TOKEN 환경변수 또는 ~/.sense1_token 파일이 필요합니다."
  exit 1
fi

HTML_FILENAME="coffee-article-${DATE}.html"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "[1/4] HTML 파일 복사..."
cp "$HTML_SRC" "$SCRIPT_DIR/$HTML_FILENAME"

echo "[2/4] knowledge-data.js 업데이트..."
python3 "$SCRIPT_DIR/update_knowledge.py" \
  --date "$DATE" \
  --html "$HTML_FILENAME" \
  --html-path "$SCRIPT_DIR/$HTML_FILENAME" \
  --kd "$SCRIPT_DIR/knowledge-data.js"

echo "[3/4] Git 커밋..."
cd "$SCRIPT_DIR"
git config user.email "namho1123@gmail.com"
git config user.name "ephraim88106"
git add "$HTML_FILENAME" knowledge-data.js

SUBJECT=$(python3 -c "
import re
html = open('$HTML_FILENAME', encoding='utf-8').read()
t = re.search(r'<title>(.*?)</title>', html, re.DOTALL)
title = re.sub(r'<[^>]+>', '', t.group(1)).split('|')[0].strip() if t else '$HTML_FILENAME'
print(title[:50])
" 2>/dev/null || echo "$HTML_FILENAME")

git commit -m "스페셜티 커피 아티클 추가 ($DATE): $SUBJECT"

echo "[4/4] GitHub 푸시..."
git push "https://ephraim88106:${TOKEN}@github.com/ephraim88106/sense1.git" main

echo ""
echo "완료: $DATE 아티클 + knowledge-data.js 동시 반영됨"
