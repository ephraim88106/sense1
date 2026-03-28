# 바리스타 자격증 종합 가이드 및 기출문제 플랫폼 기획안 (Blueprint)

## 1. 개요 및 목표
- **주제:** 바리스타 및 홈바리스타 자격증 합격을 위한 종합 포털 웹사이트
- **목표:** 한국커피협회(KCA)의 다양한 자격증 라인업 정보 통합 제공, 맞춤형 학습 경로 제시를 통한 사용자 경험 고도화 및 구글 애드센스 승인 조건 충족.

## 2. 사이트맵 및 계층형 메뉴 구조 (Silo Architecture)
* **홈 (Home)**: 자격증 종류별 퀵 메뉴, 실시간 시험 공지, 학습 로드맵
* **자격시험 (Exam Guide)**
  * 시험 일정 (Schedule)
  * 시험 안내/규정 (Guide)
  * 기출문제 풀이 (Practice)
* **정보센터 (Info Center)**
  * **공지사항 (Notice)**: 사이트의 중요 공지 및 업데이트 정보 제공 [IMPLEMENTED]
  * **Q&A 게시판 (Q&A)**: 사용자 질의응답 및 소통 공간 [IMPLEMENTED]
  * **소개 (About)**: 사이트 운영 목적 및 전문성 강조
  * **문의 (Contact)**: 사용자 피드백 및 기술 지원
* **학습센터 (Learning Center)**
  * **지식 백과 (Knowledge Base)**: 커피 품종, 로스팅, 추출 등 전문 지식 아티클
  * **기출문제 풀이 (Practice)**: 등급별 모의고사 및 해설
  * **시험 안내 (Guide)**: KCA 규정 및 전형 방법
  * **시험 일정 (Schedule)**: 최신 시험 일정 테이블
* **법적 공지 (Legal)**
  * 개인정보처리방침 (Privacy Policy)
  * 이용약관 (Terms of Service)
* **시스템 페이지**
  * **404 에러 페이지**: 사용자 친화적 오류 안내 및 홈 연결

## 3. 핵심 페이지별 화면 구성 기획 (UI/UX Layout)

### 3.1. 홈 (Index.html)
- **Hero:** 신뢰감 있는 문구와 함께 명확한 CTA(Call to Action) 버튼.
- **Monetization:** 히어로 섹션 하단에 쿠팡 파트너스 캐러셀 광고 배치.

### 3.2. 정보센터 (Notice.html & Qna.html)
- **Interactive Board:** Firebase Firestore와 연동된 실시간 게시판 시스템.
- **PostBoard Component:** 웹 컴포넌트 기반으로 설계되어 게시글 작성 및 목록 조회를 단일 인터페이스에서 제공.

## 4. 기술 스택 및 수익화 전략
- **Frontend:** Vanilla JS (Web Components), CSS3 (Modern Baseline), HTML5.
- **Backend:** Firebase Hosting, Firestore (Real-time Database).
- **수익화 채널:** Google AdSense, Coupang Partners (자동 연동 및 필수 고지 문구 적용).

---

## 5. 현재 구현 계획 (진행 내역)
- **[Done]** KCA 기준 바리스타 1급/2급 시험 안내 및 일정 페이지 구축.
- **[Done]** 180문항 이상의 기출문제 데이터 및 전문가 해설 구축.
- **[Done]** 애드센스 필수 페이지(Privacy, Terms, About, Contact) 구축.
- **[Done]** 독창적 콘텐츠 강화를 위한 '커피 지식 백과' 아티클 추가.
- **[Done]** 쿠팡 파트너스 광고 위젯 연동 및 필수 고지 문구 적용.
- **[Done]** 공지사항 및 Q&A 게시판 시스템 구축 (Web Components & Firestore 연동).
- **[To-Do]** `firebase-config.js`에 실제 Firebase 프로젝트 API 키 설정 필요.
- **[To-Do]** 지식 백과 아티클 지속 확장 및 학습 로드맵 시각화 보강.