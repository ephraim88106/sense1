// KCA Portal Multi-Page Logic & Components

// Shared Header Component
class MainHeader extends HTMLElement {
    constructor() {
        super();
        this.attachShadow({ mode: 'open' });
    }
    connectedCallback() {
        this.render();
    }
    render() {
        const activePage = this.getAttribute('active') || 'home';
        this.shadowRoot.innerHTML = `
            <style>
                :host { display: block; font-family: 'Noto Sans KR', sans-serif; position: sticky; top: 0; z-index: 1000; }
                header { background: rgba(255, 255, 255, 0.95); backdrop-filter: blur(15px); border-bottom: 1px solid #e9edc9; box-shadow: 0 2px 10px rgba(0,0,0,0.05); }
                .container { max-width: 1200px; margin: 0 auto; padding: 0 20px; display: flex; justify-content: space-between; align-items: center; height: 80px; }
                .logo { font-size: 1.6rem; font-weight: 900; color: #3b2f2f; text-decoration: none; letter-spacing: -1px; }
                nav ul { list-style: none; display: flex; gap: 30px; margin: 0; padding: 0; }
                nav li { position: relative; }
                nav a { text-decoration: none; color: #2b2d42; font-weight: 700; font-size: 1rem; transition: 0.3s; }
                nav a:hover, nav a.active { color: #d4a373; }
                .btn-login { background: #3b2f2f; color: white; padding: 10px 24px; border-radius: 25px; text-decoration: none; font-size: 0.9rem; font-weight: 700; }
                .has-dropdown:hover .dropdown { opacity: 1; visibility: visible; transform: translateY(0); }
                .dropdown { position: absolute; top: 100%; left: 0; background: white; min-width: 180px; padding: 10px 0; border-radius: 12px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); opacity: 0; visibility: hidden; transform: translateY(10px); transition: 0.3s; border: 1px solid #eee; }
                .dropdown a { padding: 10px 20px; display: block; font-size: 0.9rem; color: #8d99ae; font-weight: 500; }
                .dropdown a:hover { background: #f8f9fa; color: #3b2f2f; }
            </style>
            <header>
                <div class="container">
                    <a href="index.html" class="logo">☕ KCA PORTAL</a>
                    <nav>
                        <ul>
                            <li class="has-dropdown">
                                <a href="exam-guide.html" class="${activePage === 'exam' ? 'active' : ''}">자격시험</a>
                                <ul class="dropdown">
                                    <li><a href="schedule.html">자격시험일정</a></li>
                                    <li><a href="exam-guide.html">시험안내/규정</a></li>
                                    <li><a href="practice.html">기출문제</a></li>
                                </ul>
                            </li>
                            <li><a href="cert-library.html" class="${activePage === 'cert' ? 'active' : ''}">심사평가</a></li>
                            <li><a href="#" class="${activePage === 'info' ? 'active' : ''}">정보센터</a></li>
                            <li><a href="#">마이페이지</a></li>
                        </ul>
                    </nav>
                    <a href="#" class="btn-login">로그인</a>
                </div>
            </header>
        `;
    }
}
customElements.define('main-header', MainHeader);

// Shared Footer Component
class MainFooter extends HTMLElement {
    constructor() { super(); this.attachShadow({ mode: 'open' }); }
    connectedCallback() {
        this.shadowRoot.innerHTML = `
            <style>
                :host { display: block; font-family: 'Noto Sans KR', sans-serif; background: #f1f3f5; color: #8d99ae; padding: 60px 0; margin-top: 80px; }
                .container { max-width: 1200px; margin: 0 auto; padding: 0 20px; display: flex; justify-content: space-between; align-items: center; }
                .info p { margin-bottom: 5px; font-size: 0.9rem; }
                .links a { color: #8d99ae; text-decoration: none; margin-left: 15px; font-size: 0.9rem; }
            </style>
            <footer>
                <div class="container">
                    <div class="info">
                        <p><strong>(사)한국커피협회 포털</strong> | 대표: 최주호</p>
                        <p>서울시 마포구 마포대로1길 26-1 | 02-702-4080</p>
                        <p>© 2024 KCA Korea Coffee Association.</p>
                    </div>
                    <div class="links">
                        <a href="#">이용약관</a>
                        <a href="#">개인정보처리방침</a>
                    </div>
                </div>
            </footer>
        `;
    }
}
customElements.define('main-footer', MainFooter);

// Exam Card Component (Detailed info)
class ExamCard extends HTMLElement {
    constructor() { super(); this.attachShadow({ mode: 'open' }); }
    connectedCallback() { this.render(); }
    render() {
        const level = this.getAttribute('level') || '급수';
        const eligWritten = this.getAttribute('eligibility-written') || '-';
        const eligPractical = this.getAttribute('eligibility-practical') || '-';
        const formatWritten = this.getAttribute('format-written') || '-';
        const formatPractical = this.getAttribute('format-practical') || '-';
        const subjectsWritten = this.getAttribute('subjects-written') || '-';
        const subjectsPractical = this.getAttribute('subjects-practical') || '-';
        const critWritten = this.getAttribute('criteria-written') || '-';
        const critPractical = this.getAttribute('criteria-practical') || '-';
        const theme = this.getAttribute('theme') || 'primary';

        const themeColors = {
            primary: { bg: '#eff6ff', text: '#1d4ed8', border: '#bfdbfe' },
            danger: { bg: '#fef2f2', text: '#b91c1c', border: '#fecaca' }
        };
        const colors = themeColors[theme] || themeColors.primary;

        this.shadowRoot.innerHTML = `
            <style>
                :host { display: block; font-family: 'Noto Sans KR', sans-serif; height: 100%; }
                .card { background: white; border-radius: 20px; border: 1px solid #e2e8f0; box-shadow: 0 10px 30px rgba(0,0,0,0.05); overflow: hidden; height: 100%; display: flex; flex-direction: column; }
                .card-header { background-color: ${colors.bg}; color: ${colors.text}; padding: 20px 25px; font-size: 1.5rem; font-weight: 800; border-bottom: 1px solid ${colors.border}; }
                .card-body { padding: 25px; flex-grow: 1; }
                .info-group { margin-bottom: 24px; }
                .info-label { font-size: 0.9rem; color: #6b7280; font-weight: 700; margin-bottom: 12px; display: flex; align-items: center; gap: 8px; }
                .info-item { display: flex; gap: 10px; margin-bottom: 8px; background: #f8fafc; padding: 12px; border-radius: 12px; border: 1px solid #f1f5f9; }
                .type-tag { font-weight: 700; color: #475569; min-width: 45px; text-align: center; background: #e2e8f0; padding: 2px 6px; border-radius: 6px; font-size: 0.85rem; height: fit-content; }
                .detail { color: #334155; font-size: 0.95rem; line-height: 1.4; }
                .subjects-box { margin-top: 10px; padding: 10px; background: #fff; border: 1px dashed #cbd5e1; border-radius: 8px; font-size: 0.85rem; color: #64748b; }
            </style>
            <div class="card">
                <div class="card-header">바리스타 ${level}</div>
                <div class="card-body">
                    <div class="info-group">
                        <div class="info-label">응시자격</div>
                        <div class="info-item"><span class="type-tag">필기</span><span class="detail">${eligWritten}</span></div>
                        <div class="info-item"><span class="type-tag">실기</span><span class="detail">${eligPractical}</span></div>
                    </div>
                    <div class="info-group">
                        <div class="info-label">전형 및 범위</div>
                        <div class="info-item"><span class="type-tag">필기</span><div class="detail"><span>${formatWritten}</span><div class="subjects-box">${subjectsWritten}</div></div></div>
                        <div class="info-item"><span class="type-tag">실기</span><div class="detail"><span>${formatPractical}</span><div class="subjects-box">${subjectsPractical}</div></div></div>
                    </div>
                    <div class="info-group">
                        <div class="info-label">합격기준</div>
                        <div class="info-item"><span class="type-tag">필기</span><span class="detail">${critWritten}</span></div>
                        <div class="info-item"><span class="type-tag">실기</span><span class="detail">${critPractical}</span></div>
                    </div>
                </div>
            </div>
        `;
    }
}
customElements.define('exam-card', ExamCard);

// Exam Table Component
class ExamTable extends HTMLElement {
    constructor() { super(); this.attachShadow({ mode: 'open' }); }
    connectedCallback() {
        this.shadowRoot.innerHTML = `
            <style>
                :host { display: block; margin-top: 30px; font-family: 'Noto Sans KR', sans-serif; }
                .rules-box { background: #fff; border-radius: 16px; padding: 25px; border: 1px solid #e2e8f0; }
                .rules-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 15px; }
                .rule-card { background: #f8fafc; padding: 20px; border-radius: 12px; border-left: 4px solid #94a3b8; }
                .rule-card.warning { border-left-color: #ef4444; background: #fef2f2; }
                h4 { margin: 0 0 8px 0; font-size: 1rem; color: #334155; }
                p { margin: 0; font-size: 0.9rem; color: #64748b; line-height: 1.5; }
            </style>
            <div class="rules-box">
                <div class="rules-grid">
                    <div class="rule-card"><h4>유효기간</h4><p>바리스타 자격증의 유효기간은 없으며, 비갱신 자격입니다.</p></div>
                    <div class="rule-card warning"><h4>실격사유 (실기)</h4><p>감각평가에서 총 8잔의 음료가 제공되지 않은 경우 실격 처리됩니다.</p></div>
                </div>
            </div>
        `;
    }
}
customElements.define('exam-table', ExamTable);

// Quiz Logic (Only runs on practice.html)
import { baristaQuestions } from './questions.js';

class ExamQuestion extends HTMLElement {
    constructor() {
        super();
        this.attachShadow({ mode: 'open' });
    }
    connectedCallback() { this.render(); }
    static get observedAttributes() { return ['question', 'options', 'answer', 'explanation']; }
    attributeChangedCallback() { this.render(); }
    render() {
        const questionText = this.getAttribute('question') || '문제가 없습니다.';
        const options = JSON.parse(this.getAttribute('options') || '[]');
        const answerText = this.getAttribute('answer') || '정답이 없습니다.';
        const explanationText = this.getAttribute('explanation') || '해설이 없습니다.';

        let optionsHtml = '';
        options.forEach((opt, idx) => {
            optionsHtml += `
                <label class="option-label">
                    <input type="radio" name="q-option" value="${idx}">
                    <span class="custom-radio">${idx + 1}</span>
                    <span class="option-text">${opt}</span>
                </label>
            `;
        });

        this.shadowRoot.innerHTML = `
            <style>
                :host { display: block; margin-bottom: 30px; font-family: 'Noto Sans KR', sans-serif; }
                .question-title { font-size: 1.2rem; font-weight: 700; color: #1f2937; margin-bottom: 25px; }
                .options-container { display: flex; flex-direction: column; gap: 12px; }
                .option-label { display: flex; align-items: center; padding: 16px; background: #f9fafb; border: 1px solid #e5e7eb; border-radius: 12px; cursor: pointer; transition: 0.2s; }
                .option-label:hover { background: #f3f4f6; }
                .option-label input { display: none; }
                .custom-radio { width: 28px; height: 28px; border-radius: 50%; border: 2px solid #d1d5db; display: flex; align-items: center; justify-content: center; margin-right: 15px; font-weight: bold; }
                .option-label input:checked + .custom-radio { background: #d4a373; color: white; border-color: #d4a373; }
                .answer-box { margin-top: 25px; padding: 20px; background: #f8fafc; border-radius: 12px; display: none; }
                .answer-box.show { display: block; }
                .btn-check { margin-top: 20px; padding: 12px 25px; background: #3b2f2f; color: white; border-radius: 8px; border: none; cursor: pointer; }
            </style>
            <div class="question-wrapper">
                <div class="question-title">${questionText}</div>
                <div class="options-container">${optionsHtml}</div>
                <button class="btn-check" id="check-btn">정답 확인</button>
                <div class="answer-box" id="answer-box">
                    <p><strong>정답:</strong> ${answerText}</p>
                    <p><strong>해설:</strong> ${explanationText}</p>
                </div>
            </div>
        `;
        const btn = this.shadowRoot.getElementById('check-btn');
        const box = this.shadowRoot.getElementById('answer-box');
        btn.onclick = () => box.classList.toggle('show');
    }
}
customElements.define('exam-question', ExamQuestion);

// Global Initial Load
document.addEventListener('DOMContentLoaded', () => {
    // Schedule Tab Logic
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');
    if (tabBtns.length > 0) {
        tabBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                const target = btn.getAttribute('data-target');
                tabBtns.forEach(b => b.classList.remove('active'));
                tabContents.forEach(c => c.classList.remove('active'));
                btn.classList.add('active');
                document.getElementById(target).classList.add('active');
            });
        });
    }

    // Quiz Navigation Logic
    const qContainer = document.querySelector('.questions-container');
    if (qContainer && baristaQuestions) {
        let curIdx = 0;
        const renderQuiz = () => {
            const q = baristaQuestions[curIdx];
            qContainer.innerHTML = `<exam-question question="${q.question}" options='${JSON.stringify(q.options)}' answer="${q.answer}" explanation="${q.explanation}"></exam-question>`;
            const curQ = document.querySelector('.current-q');
            const totalQ = document.querySelector('.total-q');
            const progress = document.querySelector('.progress');
            if(curQ) curQ.textContent = curIdx + 1;
            if(totalQ) totalQ.textContent = baristaQuestions.length;
            if(progress) progress.style.width = `${((curIdx + 1) / baristaQuestions.length) * 100}%`;
        };
        const prev = document.querySelector('.btn-nav.outline');
        const next = document.querySelector('.btn-nav.fill');
        if(prev) prev.onclick = () => { if(curIdx > 0) { curIdx--; renderQuiz(); } };
        if(next) next.onclick = () => { if(curIdx < baristaQuestions.length - 1) { curIdx++; renderQuiz(); } else { alert('마지막 문제입니다.'); } };
        renderQuiz();
    }
});
