// Web Component for Exam Question
class ExamQuestion extends HTMLElement {
    constructor() {
        super();
        const shadow = this.attachShadow({ mode: 'open' });
        
        // Attributes
        const questionText = this.getAttribute('question') || '문제가 없습니다.';
        const options = JSON.parse(this.getAttribute('options') || '[]');
        const answerText = this.getAttribute('answer') || '정답이 없습니다.';
        const explanationText = this.getAttribute('explanation') || '해설이 없습니다.';

        // Create elements
        const wrapper = document.createElement('div');
        wrapper.setAttribute('class', 'question-wrapper');

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

        wrapper.innerHTML = `
            <style>
                :host {
                    display: block;
                    margin-bottom: 30px;
                }
                .question-wrapper {
                    font-family: 'Noto Sans KR', sans-serif;
                }
                .question-title {
                    font-size: 1.15rem;
                    font-weight: 700;
                    color: #1f2937;
                    margin-bottom: 20px;
                    line-height: 1.5;
                }
                .options-container {
                    display: flex;
                    flex-direction: column;
                    gap: 12px;
                    margin-bottom: 24px;
                }
                .option-label {
                    display: flex;
                    align-items: center;
                    padding: 16px;
                    background: #f9fafb;
                    border: 1px solid #e5e7eb;
                    border-radius: 10px;
                    cursor: pointer;
                    transition: all 0.2s;
                }
                .option-label:hover {
                    background: #f3f4f6;
                    border-color: #d1d5db;
                }
                .option-label input {
                    display: none;
                }
                .option-label input:checked + .custom-radio {
                    background: #3b82f6;
                    color: white;
                    border-color: #3b82f6;
                }
                .option-label input:checked ~ .option-text {
                    font-weight: 700;
                    color: #1f2937;
                }
                .custom-radio {
                    width: 28px;
                    height: 28px;
                    border-radius: 50%;
                    border: 2px solid #d1d5db;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 0.9rem;
                    font-weight: bold;
                    color: #6b7280;
                    margin-right: 15px;
                    flex-shrink: 0;
                    transition: all 0.2s;
                }
                .option-text {
                    color: #4b5563;
                    font-size: 1rem;
                    line-height: 1.4;
                }
                .toggle-answer-btn {
                    width: 100%;
                    background: #1f2937;
                    color: white;
                    border: none;
                    padding: 16px;
                    border-radius: 10px;
                    font-size: 1rem;
                    font-weight: 700;
                    cursor: pointer;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    gap: 8px;
                    transition: background 0.2s;
                }
                .toggle-answer-btn:hover {
                    background: #111827;
                }
                .answer-section {
                    margin-top: 16px;
                    background: #f0fdf4;
                    border: 1px solid #bbf7d0;
                    border-radius: 10px;
                    padding: 20px;
                    display: none;
                    opacity: 0;
                    transform: translateY(-10px);
                    transition: all 0.3s ease;
                }
                .answer-section.open {
                    display: block;
                    opacity: 1;
                    transform: translateY(0);
                }
                .answer-badge {
                    display: inline-block;
                    background: #22c55e;
                    color: white;
                    padding: 4px 10px;
                    border-radius: 6px;
                    font-size: 0.85rem;
                    font-weight: bold;
                    margin-bottom: 12px;
                }
                .answer-text {
                    font-weight: 700;
                    color: #166534;
                    margin-bottom: 10px;
                    font-size: 1.05rem;
                }
                .explanation-title {
                    font-size: 0.9rem;
                    color: #15803d;
                    font-weight: bold;
                    margin-bottom: 4px;
                    margin-top: 16px;
                }
                .explanation {
                    color: #374151;
                    font-size: 0.95rem;
                    line-height: 1.6;
                }
                .adsense-placeholder-inner {
                    margin-top: 20px;
                    padding: 15px;
                    background: #fff;
                    border: 1px dashed #cbd5e1;
                    text-align: center;
                    color: #94a3b8;
                    font-size: 0.85rem;
                    border-radius: 8px;
                }
            </style>
            
            <div class="question-title">${questionText}</div>
            <div class="options-container">
                ${optionsHtml}
            </div>
            
            <button class="toggle-answer-btn">
                <span>정답 및 해설 보기</span>
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"></polyline></svg>
            </button>
            
            <div class="answer-section">
                <div class="answer-badge">정답</div>
                <div class="answer-text">${answerText}</div>
                <div class="explanation-title">해설</div>
                <div class="explanation">${explanationText}</div>
                
                <div class="adsense-placeholder-inner">
                    [애드센스 광고] 해설 하단 배너 (가장 클릭률이 높은 영역)
                </div>
            </div>
        `;

        shadow.appendChild(wrapper);

        // Logic
        const toggleBtn = wrapper.querySelector('.toggle-answer-btn');
        const answerSection = wrapper.querySelector('.answer-section');
        const btnText = toggleBtn.querySelector('span');
        const btnIcon = toggleBtn.querySelector('svg');

        toggleBtn.addEventListener('click', () => {
            const isOpen = answerSection.classList.contains('open');
            if (isOpen) {
                answerSection.classList.remove('open');
                btnText.textContent = '정답 및 해설 보기';
                toggleBtn.style.background = '#1f2937';
                btnIcon.innerHTML = '<polyline points="6 9 12 15 18 9"></polyline>'; // down arrow
            } else {
                answerSection.classList.add('open');
                btnText.textContent = '정답 및 해설 숨기기';
                toggleBtn.style.background = '#6b7280';
                btnIcon.innerHTML = '<polyline points="18 15 12 9 6 15"></polyline>'; // up arrow
            }
        });
    }
}

customElements.define('exam-question', ExamQuestion);