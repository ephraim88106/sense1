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
                
                /* Details-like styling for answer section */
                .answer-details {
                    background: #f8f9fa;
                    border: 1px solid #e9ecef;
                    border-radius: 8px;
                    padding: 15px;
                }
                .answer-summary {
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    cursor: pointer;
                    font-weight: bold;
                    color: #0056b3;
                    user-select: none;
                }
                .answer-content {
                    margin-top: 15px;
                    border-top: 1px dashed #ccc;
                    padding-top: 15px;
                    display: none; /* Initially hidden */
                }
                .answer-content.show {
                    display: block;
                }
                .answer-badge {
                    color: #d9534f;
                    font-weight: bold;
                    font-size: 1.1rem;
                    margin-bottom: 10px;
                }
                .explanation {
                    color: #212529;
                    font-size: 0.95rem;
                    line-height: 1.6;
                }
                .arrow-icon {
                    transition: transform 0.2s;
                }
                .arrow-icon.rotated {
                    transform: rotate(180deg);
                }
            </style>
            
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
                    <div class="answer-badge">정답: ${answerText.split('.')[0]}</div>
                    <div class="explanation"><strong>해설:</strong> ${explanationText}</div>
                </div>
            </div>
        `;

        shadow.appendChild(wrapper);

        // Logic
        const toggleBtn = shadow.getElementById('toggle-btn');
        const answerBox = shadow.getElementById('answer-box');
        const arrowIcon = toggleBtn.querySelector('.arrow-icon');

        toggleBtn.addEventListener('click', () => {
            const isShown = answerBox.classList.contains('show');
            if (isShown) {
                answerBox.classList.remove('show');
                arrowIcon.classList.remove('rotated');
            } else {
                answerBox.classList.add('show');
                arrowIcon.classList.add('rotated');
            }
        });
    }
}

customElements.define('exam-question', ExamQuestion);