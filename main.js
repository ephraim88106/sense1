import { baristaQuestions } from './questions.js';

// Web Component for Exam Question
class ExamQuestion extends HTMLElement {
    constructor() {
        super();
        const shadow = this.attachShadow({ mode: 'open' });
        this.render();
    }

    static get observedAttributes() {
        return ['question', 'options', 'answer', 'explanation'];
    }

    attributeChangedCallback() {
        this.render();
    }

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
                :host { display: block; margin-bottom: 30px; }
                .question-wrapper { font-family: 'Noto Sans KR', sans-serif; }
                .question-title { font-size: 1.15rem; font-weight: 700; color: #1f2937; margin-bottom: 20px; line-height: 1.5; }
                .options-container { display: flex; flex-direction: column; gap: 12px; margin-bottom: 24px; }
                .option-label { display: flex; align-items: center; padding: 16px; background: #f9fafb; border: 1px solid #e5e7eb; border-radius: 10px; cursor: pointer; transition: all 0.2s; }
                .option-label:hover { background: #f3f4f6; border-color: #d1d5db; }
                .option-label input { display: none; }
                .option-label input:checked + .custom-radio { background: #3b82f6; color: white; border-color: #3b82f6; }
                .option-label input:checked ~ .option-text { font-weight: 700; color: #1f2937; }
                .custom-radio { width: 28px; height: 28px; border-radius: 50%; border: 2px solid #d1d5db; display: flex; align-items: center; justify-content: center; font-size: 0.9rem; font-weight: bold; color: #6b7280; margin-right: 15px; flex-shrink: 0; }
                .option-text { color: #4b5563; font-size: 1rem; line-height: 1.4; }
                .answer-details { background: #f8f9fa; border: 1px solid #e9ecef; border-radius: 8px; padding: 15px; }
                .answer-summary { display: flex; justify-content: space-between; align-items: center; cursor: pointer; font-weight: bold; color: #0056b3; user-select: none; }
                .answer-content { margin-top: 15px; border-top: 1px dashed #ccc; padding-top: 15px; display: none; }
                .answer-content.show { display: block; }
                .answer-badge { color: #d9534f; font-weight: bold; font-size: 1.1rem; margin-bottom: 10px; }
                .explanation { color: #212529; font-size: 0.95rem; line-height: 1.6; }
                .arrow-icon { transition: transform 0.2s; }
                .arrow-icon.rotated { transform: rotate(180deg); }
            </style>
            
            <div class="question-wrapper">
                <div class="question-title">${questionText}</div>
                <div class="options-container">
                    ${optionsHtml}
                </div>
                
                <div class="answer-details">
                    <div class="answer-summary" id="toggle-btn">
                        <span>👉 정답 및 해설 확인하기</span>
                        <svg class="arrow-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"></polyline></svg>
                    </div>
                    <div class="answer-content" id="answer-box">
                        <div class="answer-badge">정답: ${answerText}</div>
                        <div class="explanation"><strong>해설:</strong> ${explanationText}</div>
                    </div>
                </div>
            </div>
        `;

        const toggleBtn = this.shadowRoot.getElementById('toggle-btn');
        const answerBox = this.shadowRoot.getElementById('answer-box');
        const arrowIcon = toggleBtn.querySelector('.arrow-icon');

        toggleBtn.onclick = () => {
            const isShown = answerBox.classList.contains('show');
            if (isShown) {
                answerBox.classList.remove('show');
                arrowIcon.classList.remove('rotated');
            } else {
                answerBox.classList.add('show');
                arrowIcon.classList.add('rotated');
            }
        };
    }
}

customElements.define('exam-question', ExamQuestion);

// Quiz Logic
let currentQuestionIndex = 0;
const questionsContainer = document.querySelector('.questions-container');
const prevBtn = document.querySelector('.btn-nav.outline');
const nextBtn = document.querySelector('.btn-nav.fill');
const currentQSpan = document.querySelector('.current-q');
const totalQSpan = document.querySelector('.total-q');
const progressBar = document.querySelector('.progress');

function updateQuiz() {
    const q = baristaQuestions[currentQuestionIndex];
    questionsContainer.innerHTML = `
        <exam-question 
            question="${q.question}"
            options='${JSON.stringify(q.options)}'
            answer="${q.answer}"
            explanation="${q.explanation}"
        ></exam-question>
    `;

    // Update progress
    currentQSpan.textContent = currentQuestionIndex + 1;
    totalQSpan.textContent = baristaQuestions.length;
    const progressPercent = ((currentQuestionIndex + 1) / baristaQuestions.length) * 100;
    progressBar.style.width = `${progressPercent}%`;

    // Button states
    prevBtn.disabled = currentQuestionIndex === 0;
    nextBtn.textContent = currentQuestionIndex === baristaQuestions.length - 1 ? '마지막 문제' : '다음 문제';
}

prevBtn.onclick = () => {
    if (currentQuestionIndex > 0) {
        currentQuestionIndex--;
        updateQuiz();
        window.scrollTo({ top: questionsContainer.offsetTop - 100, behavior: 'smooth' });
    }
};

nextBtn.onclick = () => {
    if (currentQuestionIndex < baristaQuestions.length - 1) {
        currentQuestionIndex++;
        updateQuiz();
        window.scrollTo({ top: questionsContainer.offsetTop - 100, behavior: 'smooth' });
    } else {
        alert('모든 문제를 다 풀었습니다! 고생하셨습니다.');
    }
};

// Initial Load
document.addEventListener('DOMContentLoaded', updateQuiz);

// Exam Card Component
class ExamCard extends HTMLElement {
    constructor() {
        super();
        this.attachShadow({ mode: 'open' });
    }

    connectedCallback() {
        this.render();
    }

    render() {
        const level = this.getAttribute('level') || '급수';
        const eligWritten = this.getAttribute('eligibility-written') || '-';
        const eligPractical = this.getAttribute('eligibility-practical') || '-';
        const formatWritten = this.getAttribute('format-written') || '-';
        const formatPractical = this.getAttribute('format-practical') || '-';
        const critWritten = this.getAttribute('criteria-written') || '-';
        const critPractical = this.getAttribute('criteria-practical') || '-';
        const subjectsWritten = this.getAttribute('subjects-written') || '-';
        const subjectsPractical = this.getAttribute('subjects-practical') || '-';
        const theme = this.getAttribute('theme') || 'primary';

        const themeColors = {
            primary: { bg: '#eff6ff', text: '#1d4ed8', border: '#bfdbfe' },
            danger: { bg: '#fef2f2', text: '#b91c1c', border: '#fecaca' }
        };

        const colors = themeColors[theme] || themeColors.primary;

        this.shadowRoot.innerHTML = `
            <style>
                :host {
                    display: block;
                    font-family: 'Noto Sans KR', sans-serif;
                }
                .card {
                    background: rgba(255, 255, 255, 0.8);
                    backdrop-filter: blur(12px);
                    border-radius: 20px;
                    border: 1px solid var(--border-color, #e2e8f0);
                    box-shadow: 0 10px 30px -10px rgba(0,0,0,0.1);
                    overflow: hidden;
                    transition: transform 0.3s ease;
                    height: 100%;
                    display: flex;
                    flex-direction: column;
                }
                .card:hover {
                    transform: translateY(-5px);
                }
                .card-header {
                    background-color: ${colors.bg};
                    color: ${colors.text};
                    padding: 20px 25px;
                    font-size: 1.5rem;
                    font-weight: 800;
                    display: flex;
                    align-items: center;
                    justify-content: space-between;
                    border-bottom: 1px solid ${colors.border};
                }
                .badge {
                    font-size: 0.8rem;
                    background: white;
                    padding: 4px 10px;
                    border-radius: 12px;
                    font-weight: 700;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
                }
                .card-body {
                    padding: 25px;
                    flex-grow: 1;
                }
                .info-group {
                    margin-bottom: 24px;
                }
                .info-group:last-child {
                    margin-bottom: 0;
                }
                .info-label {
                    font-size: 0.9rem;
                    color: #6b7280;
                    font-weight: 700;
                    margin-bottom: 12px;
                    display: flex;
                    align-items: center;
                    gap: 6px;
                }
                .info-label svg { width: 16px; height: 16px; }
                .info-item {
                    display: flex;
                    gap: 10px;
                    margin-bottom: 8px;
                    background: #f8fafc;
                    padding: 12px 15px;
                    border-radius: 12px;
                    border: 1px solid #f1f5f9;
                }
                .type-tag {
                    font-weight: 700;
                    color: #475569;
                    min-width: 45px;
                    text-align: center;
                    background: #e2e8f0;
                    padding: 2px 6px;
                    border-radius: 6px;
                    font-size: 0.85rem;
                    height: fit-content;
                }
                .detail {
                    color: #334155;
                    font-size: 0.95rem;
                    line-height: 1.4;
                }
                .subjects-box {
                    margin-top: 15px;
                    padding: 12px;
                    background: #fff;
                    border: 1px dashed #cbd5e1;
                    border-radius: 10px;
                    font-size: 0.85rem;
                    color: #64748b;
                }
                .subjects-box strong { color: #475569; }
            </style>
            <div class="card">
                <div class="card-header">
                    <span>바리스타 ${level}</span>
                    <span class="badge">KCA 인증</span>
                </div>
                <div class="card-body">
                    <div class="info-group">
                        <div class="info-label">
                            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path><circle cx="8.5" cy="7" r="4"></circle><polyline points="17 11 19 13 23 9"></polyline></svg>
                            응시자격
                        </div>
                        <div class="info-item">
                            <span class="type-tag">필기</span>
                            <span class="detail">${eligWritten}</span>
                        </div>
                        <div class="info-item">
                            <span class="type-tag">실기</span>
                            <span class="detail">${eligPractical}</span>
                        </div>
                    </div>
                    
                    <div class="info-group">
                        <div class="info-label">
                            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect><line x1="16" y1="2" x2="16" y2="6"></line><line x1="8" y1="2" x2="8" y2="6"></line><line x1="3" y1="10" x2="21" y2="10"></line></svg>
                            전형방법 및 범위
                        </div>
                        <div class="info-item">
                            <span class="type-tag">필기</span>
                            <div style="display:flex; flex-direction:column; gap:5px;">
                                <span class="detail">${formatWritten}</span>
                                <div class="subjects-box"><strong>범위:</strong> ${subjectsWritten}</div>
                            </div>
                        </div>
                        <div class="info-item">
                            <span class="type-tag">실기</span>
                            <div style="display:flex; flex-direction:column; gap:5px;">
                                <span class="detail">${formatPractical}</span>
                                <div class="subjects-box"><strong>범위:</strong> ${subjectsPractical}</div>
                            </div>
                        </div>
                    </div>

                    <div class="info-group">
                        <div class="info-label">
                            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
                            합격기준
                        </div>
                        <div class="info-item">
                            <span class="type-tag">필기</span>
                            <span class="detail">${critWritten}</span>
                        </div>
                        <div class="info-item">
                            <span class="type-tag">실기</span>
                            <span class="detail">${critPractical}</span>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }
}
customElements.define('exam-card', ExamCard);

// Exam Table Component for Common Rules
class ExamTable extends HTMLElement {
    constructor() {
        super();
        this.attachShadow({ mode: 'open' });
    }

    connectedCallback() {
        this.render();
    }

    render() {
        this.shadowRoot.innerHTML = `
            <style>
                :host {
                    display: block;
                    margin-top: 30px;
                    font-family: 'Noto Sans KR', sans-serif;
                }
                .common-rules-box {
                    background: #fff;
                    border-radius: 16px;
                    padding: 25px;
                    border: 1px solid #e2e8f0;
                    box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
                }
                .rule-title {
                    font-size: 1.2rem;
                    font-weight: 800;
                    color: #1e293b;
                    margin-bottom: 20px;
                    display: flex;
                    align-items: center;
                    gap: 8px;
                }
                .rules-grid {
                    display: grid;
                    grid-template-columns: 1fr;
                    gap: 15px;
                }
                @container (min-width: 600px) {
                    .rules-grid {
                        grid-template-columns: 1fr 1fr;
                    }
                }
                .rule-card {
                    background: #f8fafc;
                    padding: 20px;
                    border-radius: 12px;
                    border-left: 4px solid #94a3b8;
                }
                .rule-card.warning {
                    border-left-color: #ef4444;
                    background: #fef2f2;
                }
                .rule-card h4 {
                    margin: 0 0 8px 0;
                    font-size: 1rem;
                    color: #334155;
                }
                .rule-card p {
                    margin: 0;
                    font-size: 0.95rem;
                    color: #475569;
                    line-height: 1.5;
                }
            </style>
            <div class="common-rules-box">
                <div class="rule-title">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="16" x2="12" y2="12"></line><line x1="12" y1="8" x2="12.01" y2="8"></line></svg>
                    공통 안내사항
                </div>
                <div class="rules-grid">
                    <div class="rule-card">
                        <h4>유효기간</h4>
                        <p>바리스타 자격증의 유효기간은 없으며, <strong>비갱신 자격</strong>입니다.</p>
                    </div>
                    <div class="rule-card warning">
                        <h4>실격사유 (실기)</h4>
                        <p>감각평가에서 총 8잔의 음료(에스프레소 4잔, 카푸치노 4잔)가 제공되지 않은 경우 실격 처리됩니다.</p>
                    </div>
                </div>
            </div>
        `;
    }
}
customElements.define('exam-table', ExamTable);