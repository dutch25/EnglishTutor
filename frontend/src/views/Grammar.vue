```vue
<template>
  <div class="grammar-app">
    <main class="main-container">
      <!-- DASHBOARD VIEW -->
      <div v-if="mode === 'dashboard'" class="dashboard-section">
        <div class="dashboard-header">
          <button class="back-btn" @click="goHome">← Quay lại Trang Chủ</button>
          <h2 class="dashboard-title">Ứng dụng học 12 thì của EnglishTutor</h2>
        </div>
        <p class="dashboard-subtitle">Luyện tập 12 thì tiếng Anh, lý thuyết chi tiết và bài tập AI.</p>
        <div class="dashboard-grid">
          <div class="dashboard-card">
            <h3 class="card-title">Chế độ học theo từng thì</h3>
            <p class="card-desc">Chọn một trong 12 thì dưới đây để bắt đầu học lý thuyết chuyên sâu và làm bài tập củng cố.</p>
            <select v-model="selectedTense" class="custom-select">
              <option v-for="tense in tenses" :key="tense.id" :value="tense.id">{{ tense.name }}</option>
            </select>
            <button @click="startLearning" :class="['main-btn', 'primary', { clicked: isStartLearningClicked }]">Bắt đầu học</button>
          </div>
          <div class="dashboard-card">
            <h3 class="card-title">Chế độ luyện tập nâng cao</h3>
            <p class="card-desc">Thử thách bản thân với các bài tập ngẫu nhiên, tổng hợp từ tất cả 12 thì để kiểm tra toàn diện kiến thức của bạn.</p>
            <button @click="startAdvanced" class="main-btn secondary">Bắt đầu luyện tập</button>
          </div>
        </div>
      </div>

      <!-- Chế độ Học Lý Thuyết -->
      <div v-if="mode === 'learning'" class="content-grid">
        <div class="theory-panel">
          <h3 class="panel-title">{{ currentTenseName }}</h3>
          <div class="theory-content" v-html="currentTheoryHtml"></div>
        </div>
        <div class="exercise-panel">
          <div v-if="currentQuestion">
            <div class="question-header">
              <div class="question-title">Câu hỏi</div>
              <div class="question-progress">{{ currentQuestionIndex + 1 }}/{{ questionsToPractice.length }}</div>
            </div>
            <div class="question-text" v-html="formattedQuestionText"></div>
            <div class="options-list">
              <div 
                v-for="(option, idx) in currentQuestion.options" 
                :key="idx" 
                :class="['option-item', { selected: userAnswers[currentQuestionIndex] === option }]"
                @click="userAnswers[currentQuestionIndex] = option"
              >
                {{ option }}
              </div>
            </div>
            <div class="action-buttons">
              <button class="action-btn" @click="prevQuestion">← Trước</button>
              <button class="action-btn" @click="checkAnswer">Trả lời</button>
            </div>
            <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
          </div>
          <div v-else class="result-box">
            <div class="result-score">Bạn đã trả lời đúng {{ score }}/{{ questionsToPractice.length }}</div>
            <div v-if="wrongAnswers.length > 0" class="wrong-list">
              <h4>Các câu trả lời sai:</h4>
              <ul>
                <li v-for="(item, idx) in wrongAnswers" :key="idx">
                  {{ item.question }}<br>
                  <span class="wrong">Sai: {{ item.userAnswer }}</span> | 
                  <span class="correct">Đúng: {{ item.correctAnswer }}</span>
                </li>
              </ul>
            </div>
            <div v-else class="perfect-score">Tuyệt vời! Bạn đã trả lời chính xác tất cả!</div>
          </div>
          <div class="panel-footer">
            <button @click="resetToDashboard" class="main-btn secondary back-dashboard-btn">Quay lại Dashboard</button>
          </div>
        </div>
      </div>

      <!-- Chế độ Luyện Tập Nâng Cao -->
      <div v-if="mode === 'advanced'" class="content-grid advanced-mode">
        <div class="theory-panel advanced-theory">
          <h3 class="panel-title">Luyện tập tổng hợp các thì</h3>
          <p class="advanced-desc">Thử thách kiến thức của bạn với các câu hỏi ngẫu nhiên từ tất cả 12 thì tiếng Anh.</p>
          <button @click="resetToDashboard" class="main-btn secondary back-dashboard-btn">Quay lại Dashboard</button>
        </div>
        <div class="exercise-panel advanced-exercise">
          <div v-if="currentQuestion">
            <div class="question-header">
              <div class="question-title">{{ formattedQuestionText }}</div>
              <div class="question-progress">{{ currentQuestionIndex + 1 }}/{{ questionsToPractice.length }}</div>
            </div>
            <div class="options-list">
              <div 
                v-for="(option, idx) in currentQuestion.options" 
                :key="idx" 
                :class="['option-item', { selected: userAnswers[currentQuestionIndex] === option }]"
                @click="userAnswers[currentQuestionIndex] = option"
              >
                {{ option }}
              </div>
            </div>
            <div class="action-buttons">
              <button class="action-btn" @click="prevQuestion" :disabled="currentQuestionIndex === 0">← Trước</button>
              <button class="action-btn" @click="checkAnswer">Trả lời</button>
              <button class="action-btn" @click="nextQuestion" :disabled="currentQuestionIndex === questionsToPractice.length - 1">Tiếp →</button>
            </div>
            <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
          </div>
          <div v-else class="result-box">
            <div class="result-score">Bạn đã trả lời đúng {{ score }}/{{ questionsToPractice.length }}</div>
            <div v-if="wrongAnswers.length > 0" class="wrong-list">
              <h4>Các câu trả lời sai:</h4>
              <ul>
                <li v-for="(item, idx) in wrongAnswers" :key="idx">
                  {{ item.question.replace(/\[.*?\]/g, '__________') }}<br>
                  <span class="wrong">Sai: {{ item.userAnswer }}</span> | 
                  <span class="correct">Đúng: {{ item.correctAnswer }}</span>
                </li>
              </ul>
            </div>
            <div v-else class="perfect-score">Tuyệt vời! Bạn đã trả lời chính xác tất cả!</div>
            <button class="main-btn primary" @click="refreshQuestions">Làm lại</button>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import { marked } from 'marked';
import theoryData from '@/assets/data/theoryData.js';
import questionsData from '@/assets/data/questions.js';

// Reactive state
const errorMessage = ref("");
const previousMode = ref("dashboard");
const isStartLearningClicked = ref(false);
const mode = ref("dashboard");
const tenses = ref([
  { id: "present_simple", name: "Hiện tại đơn" },
  { id: "present_continuous", name: "Hiện tại tiếp diễn" },
  { id: "present_perfect", name: "Hiện tại hoàn thành" },
  { id: "present_perfect_continuous", name: "Hiện tại hoàn thành tiếp diễn" },
  { id: "past_simple", name: "Quá khứ đơn" },
  { id: "past_continuous", name: "Quá khứ tiếp diễn" },
  { id: "past_perfect", name: "Quá khứ hoàn thành" },
  { id: "past_perfect_continuous", name: "Quá khứ hoàn thành tiếp diễn" },
  { id: "future_simple", name: "Tương lai đơn" },
  { id: "future_continuous", name: "Tương lai tiếp diễn" },
  { id: "future_perfect", name: "Tương lai hoàn thành" },
  { id: "future_perfect_continuous", name: "Tương lai hoàn thành tiếp diễn" }
]);
const selectedTense = ref("present_simple");
const currentTenseName = ref("");
const currentTheory = ref("");
const exampleTopic = ref("");
const exampleOutput = ref("");
const questions = ref(questionsData);
const questionsToPractice = ref([]);
const currentQuestionIndex = ref(0);
const currentQuestion = ref(questionsData[0]);
const userAnswers = ref([]);
const score = ref(0);
const wrongAnswers = ref([]);
const loading = ref(false);

// Computed properties
const currentTheoryHtml = computed(() => {
  return marked.parse(currentTheory.value || "");
});

const formattedQuestionText = computed(() => {
  if (!currentQuestion.value) return '';
  return currentQuestion.value.question.replace(/\[.*?\]/g, '__________');
});

// Methods
const router = useRouter();

const goBack = () => {
  mode.value = 'dashboard';
  currentQuestionIndex.value = 0;
  currentQuestion.value = null;
  userAnswers.value = [];
  score.value = 0;
  exampleTopic.value = "";
  exampleOutput.value = "";
  wrongAnswers.value = [];
  questionsToPractice.value = [];
  errorMessage.value = "";
};

const goHome = () => {
  router.push("/home");
};

const startLearning = () => {
  previousMode.value = mode.value;
  isStartLearningClicked.value = true;
  mode.value = "learning";
  currentTenseName.value = tenses.value.find(t => t.id === selectedTense.value)?.name || "";
  currentTheory.value = theoryData[selectedTense.value] || "Lý thuyết đang cập nhật...";
  const filtered = questions.value.filter(q => q.tenseId === selectedTense.value);
  questionsToPractice.value = getRandom(filtered, 5);
  currentQuestionIndex.value = 0;
  currentQuestion.value = questionsToPractice.value[0] || null;
  userAnswers.value = [];
  score.value = 0;
  wrongAnswers.value = [];
  errorMessage.value = "";
};

const startAdvanced = () => {
  mode.value = "advanced";
  currentTenseName.value = "Tổng hợp";
  currentTheory.value = "";
  questionsToPractice.value = getRandom(questions.value, 10); // Set to 10 questions
  currentQuestionIndex.value = 0;
  currentQuestion.value = questionsToPractice.value[0] || null;
  userAnswers.value = [];
  score.value = 0;
  wrongAnswers.value = [];
  errorMessage.value = "";
};

const getRandom = (arr, n) => {
  if (arr.length < n) {
    console.warn(`Not enough questions available. Requested: ${n}, Available: ${arr.length}`);
    n = arr.length; // Adjust to available questions
  }
  const shuffled = arr.slice().sort(() => 0.5 - Math.random()).slice(0, n);
  shuffled.forEach(q => {
    q.options = q.options.slice().sort(() => 0.5 - Math.random());
  });
  return shuffled;
};

const checkAnswer = () => {
  if (!currentQuestion.value) {
    errorMessage.value = "Không có câu hỏi hiện tại để kiểm tra!";
    return;
  }

  const q = currentQuestion.value;
  const userAnswer = userAnswers.value[currentQuestionIndex.value];

  if (!userAnswer) {
    errorMessage.value = "Vui lòng chọn một đáp án trước khi trả lời!";
    return;
  } else {
    errorMessage.value = "";
  }

  let isCorrect = false;
  const type = q.type || "mcq";

  try {
    if (type === "mcq" || type === "fill") {
      isCorrect = userAnswer.trim().toLowerCase() === q.answer.trim().toLowerCase();
    } else if (type === "find_error") {
      isCorrect = userAnswer.replace(/\s+/g, ' ').trim().toLowerCase() === q.answer.replace(/\s+/g, ' ').trim().toLowerCase();
    } else {
      errorMessage.value = "Loại câu hỏi không hợp lệ!";
      return;
    }

    if (isCorrect) {
      score.value++;
    } else {
      wrongAnswers.value.push({
        question: q.question,
        userAnswer,
        correctAnswer: q.answer
      });
    }

    currentQuestionIndex.value++;
    if (currentQuestionIndex.value < questionsToPractice.value.length) {
      currentQuestion.value = questionsToPractice.value[currentQuestionIndex.value];
    } else {
      currentQuestion.value = null;
    }
  } catch (error) {
    console.error("Error in checkAnswer:", error);
    errorMessage.value = "Đã xảy ra lỗi khi kiểm tra đáp án. Vui lòng thử lại!";
  }
};

const resetToDashboard = () => {
  mode.value = "dashboard";
  currentQuestionIndex.value = 0;
  currentQuestion.value = null;
  userAnswers.value = [];
  score.value = 0;
  exampleTopic.value = "";
  exampleOutput.value = "";
  wrongAnswers.value = [];
  questionsToPractice.value = [];
  errorMessage.value = "";
};

const refreshQuestions = () => {
  questionsToPractice.value = getRandom(questions.value, 10); // Set to 10 questions
  currentQuestionIndex.value = 0;
  currentQuestion.value = questionsToPractice.value[0] || null;
  userAnswers.value = [];
  score.value = 0;
  wrongAnswers.value = [];
  errorMessage.value = "";
};

const nextQuestion = () => {
  if (currentQuestionIndex.value < questionsToPractice.value.length - 1) {
    currentQuestionIndex.value++;
    currentQuestion.value = questionsToPractice.value[currentQuestionIndex.value];
    errorMessage.value = "";
  } else {
    currentQuestion.value = null;
  }
};

const prevQuestion = () => {
  if (currentQuestionIndex.value > 0) {
    currentQuestionIndex.value--;
    currentQuestion.value = questionsToPractice.value[currentQuestionIndex.value];
    errorMessage.value = "";
  }
};

const reset = () => {
  currentQuestionIndex.value = 0;
  currentQuestion.value = questions.value[0];
  userAnswers.value = [];
  score.value = 0;
};

const generateExample = async () => {
  if (!exampleTopic.value) return;
  exampleOutput.value = `<ul><li><strong>Câu 1:</strong> He goes to work every day.<br><em>Dịch:</em> Anh ấy đi làm mỗi ngày.</li></ul>`;
};

// Initialize on mount
currentTenseName.value = tenses.value.find(t => t.id === selectedTense.value)?.name || "";
currentTheory.value = theoryData[selectedTense.value] || "Lý thuyết đang cập nhật...";
</script>

<style scoped>
  .grammar-app {
    background-image: url('../assets/images/background.jpg');
    background-size: cover;
    background-position: center;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
  }
  .overlay {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-image: url('../assets/images/background.jpg');
    background-size: cover;
    background-position: center;
    filter: brightness(0.6);
    z-index: 0;
  }
  .main-container {
    width: 100%;
    max-width: 1400px;
    margin: 0 auto;
    padding: 40px 20px;
    display: flex;
    flex-direction: column;
    align-items: center;
    color: #fff;
  }

  /* Dashboard */
  .dashboard-section {
    text-align: center;
  }
  .dashboard-header {
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 16px;
    position: relative;
  }
  .dashboard-header .back-btn {
    position: absolute;
    left: 0;
    top: 50%;
    transform: translateY(-50%);
    background: rgba(255, 255, 255, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.2);
    padding: 10px 18px;
    border-radius: 10px;
    font-weight: bold;
    cursor: pointer;
    transition: all 0.2s ease;
  }
  .dashboard-title {
    font-size: 3rem;
    font-weight: bold;
    color: #434343;
    text-align: center;
    margin: 0;
  }
  .dashboard-subtitle {
    font-size: 1.3rem;
    color: #434343;
    margin-bottom: 48px;
    text-align: center;
  }
  .dashboard-grid {
    display: flex;
    flex-wrap: wrap;
    gap: 40px;
    justify-content: center;
  }
  .dashboard-card {
    background: rgba(255, 255, 255, 0.2);
    backdrop-filter: blur(14px);
    border-radius: 24px;
    padding: 48px 36px;
    width: 600px;
    min-height: 280px;
    box-shadow: 0 12px 36px rgba(0,0,0,0.25);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }
  .dashboard-card:hover {
    transform: translateY(-10px) scale(1.05);
    box-shadow: 0 16px 48px rgba(0,0,0,0.35);
  }
  .card-title {
    font-size: 2.2rem;
    font-weight: bold;
    margin-bottom: 20px;
    color: #1e1e1e;
  }
  .card-desc {
    font-size: 1.2rem;
    color: #333;
    margin-bottom: 32px;
  }
  .custom-select {
    width: 100%;
    padding: 16px;
    border-radius: 14px;
    background: rgba(255,255,255,0.6);
    border: 2px solid rgba(0,0,0,0.2);
    color: #333;
    margin-bottom: 28px;
    font-size: 1.1rem;
  }

  /* Buttons */
  .main-btn {
    padding: 14px 28px;
    border-radius: 12px;
    font-weight: bold;
    cursor: pointer;
    transition: background 0.3s, transform 0.2s;
    display: inline-block;
    font-size: 1.1rem;
  }
  .primary {
    background: linear-gradient(90deg, #06d6a0, #4fc3f7);
    color: #fff;
  }
  .primary:hover {
    background: linear-gradient(90deg, #06d69e72, #4fc2f78b);
    transform: scale(1.05);
    color: #252525;
  }
  .secondary {
    background: linear-gradient(90deg, #ff6b6b, #f06595);
    color: #fff;
  }
  .secondary:hover {
    transform: scale(1.05);
  }
  .back-btn {
    background: #97b368;
    margin-top: 30px;
    margin-right: 30px;
    color: #23234b;
    border: none;
    border-radius: 8px;
    padding: 10px 20px;
    font-weight: bold;
    cursor: pointer;
    transition: background 0.3s;
  }
  .back-btn:hover {
    background-color: #b6cf75;
    color: #fff;
  }

  /* Practice Layout */
  .content-grid {
    display: grid;
    grid-template-columns: 1fr auto;
    gap: 32px;
    width: 100%;
    max-width: 1200px;
    align-items: start;
  }
  .content-grid.advanced-mode {
    grid-template-columns: 1fr 600px;
    justify-content: center;
    margin: 0 auto;
  }
  @media (max-width: 768px) {
    .content-grid, .content-grid.advanced-mode {
      grid-template-columns: 1fr;
    }
    .exercise-panel, .theory-panel, .advanced-exercise, .advanced-theory {
      width: 100%;
      max-width: 100%;
    }
  }
  .theory-panel {
    background: rgba(78, 78, 78, 0.3);
    backdrop-filter: blur(6px);
    border-radius: 16px;
    padding: 24px;
    color: #000000;
    grid-column: 1 / 2;
  }
  .theory-panel.advanced-theory {
    background: linear-gradient(135deg, rgba(255, 107, 107, 0.2), rgba(240, 101, 149, 0.2));
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.3);
    padding: 32px;
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
  }
  .panel-title {
    font-size: 1.8rem;
    font-weight: bold;
    margin-bottom: 16px;
    color: #1e1e1e;
  }
  .advanced-desc {
    font-size: 1.1rem;
    color: #333;
    margin-bottom: 24px;
  }
  .theory-content {
    font-size: 1rem;
    line-height: 1.6;
    color: #000000;
  }
  .exercise-panel {
    background: rgba(72, 72, 72, 0.3);
    backdrop-filter: blur(6px);
    border-radius: 16px;
    padding: 24px;
    color: #000000;
    width: 500px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }
  .exercise-panel.advanced-exercise {
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.3), rgba(200, 200, 200, 0.2));
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.3);
    width: 600px;
    padding: 32px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.2);
  }
  .panel-footer {
    display: flex;
    justify-content: flex-end;
    margin-top: auto;
  }
  .question-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16px;
  }
  .question-title {
    font-size: 1.25rem;
    font-weight: bold;
    color: #1e1e1e;
  }
  .question-progress {
    font-size: 1rem;
    color: #000000;
    font-weight: 500;
  }
  .question-text {
    font-size: 1.2rem;
    margin-bottom: 16px;
    color: #333;
  }
  .options-list {
    display: flex;
    flex-direction: column;
    gap: 10px;
  }
  .option-item {
    padding: 12px;
    background: rgba(255,255,255,0.08);
    border-radius: 10px;
    cursor: pointer;
    transition: all 0.2s;
    border: 1px solid rgba(0,0,0,0.1);
  }
  .option-item:hover {
    background: rgba(255,255,255,0.18);
    border-color: #4fc3f7;
  }
  .option-item.selected {
    background: #4fc3f7;
    color: #000;
    font-weight: bold;
    border-color: #06d6a0;
  }
  .action-buttons {
    display: flex;
    justify-content: space-between;
    margin-top: 16px;
    gap: 12px;
  }
  .action-btn {
    flex: 1;
    padding: 12px;
    border-radius: 8px;
    font-weight: bold;
    cursor: pointer;
    border: none;
    background: linear-gradient(90deg, #06d6a0, #4fc3f7);
    color: #fff;
    transition: all 0.2s;
  }
  .action-btn:hover {
    background: linear-gradient(90deg, #06d69e72, #4fc2f78b);
    transform: scale(1.05);
  }
  .action-btn:disabled {
    background: #ccc;
    cursor: not-allowed;
    transform: none;
  }
  .result-box {
    text-align: center;
    padding: 20px;
    background: rgba(255,255,255,0.1);
    border-radius: 12px;
  }
  .result-score {
    font-size: 1.5rem;
    font-weight: bold;
    margin-bottom: 20px;
    color: #1e1e1e;
  }
  .wrong-list ul {
    text-align: left;
    margin-top: 12px;
  }
  .wrong {
    background: #fee2e2;
    color: #ef4444;
    padding: 2px 6px;
    border-radius: 4px;
  }
  .correct {
    background: #dcfce7;
    color: #22c55e;
    padding: 2px 6px;
    border-radius: 4px;
  }
  .perfect-score {
    color: #06d6a0;
    font-weight: bold;
    font-size: 1.2rem;
    margin-bottom: 20px;
  }
  .error-message {
    color: red;
    background: rgba(255, 77, 79, 0.1);
    padding: 10px 14px;
    border-radius: 8px;
    margin-top: 12px;
    font-weight: bold;
  }
  .refresh-btn {
    margin-top: 20px;
    background: linear-gradient(90deg, #4fc3f7, #06d6a0);
    color: #fff;
  }
  .refresh-btn:hover {
    background: linear-gradient(90deg, #4fc2f78b, #06d69e72);
    transform: scale(1.05);
  }
  .back-dashboard-btn {
    margin-top: 12px;
  }
</style>
```