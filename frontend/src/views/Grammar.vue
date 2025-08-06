<template>
  <div class="grammar-app">
    <!-- Header -->
    <!-- Main Content -->
    <main class="main-center">
      <!-- Dashboard View -->
      <div v-if="mode === 'dashboard'">
        <div class="dashboard-title text-center mb-10">
          <h2 class="text-3xl font-bold mb-2">Ứng dụng học 12 thì của EnglishTutor</h2>
          <p class="text-slate-600 max-w-2xl mx-auto">Luyện tập 12 thì tiếng Anh, lý thuyết chi tiết và bài tập AI.</p>
          <p class="text-slate-500 mt-2">Chọn chế độ học hoặc luyện tập bên dưới để bắt đầu!</p>
          <p class="text-slate-500 mt-2">Sửa lại frontend cho đồng bộ + thêm nút trang chủ bên trên nhé, nút quay về trang chính bên trong 2 tính năng, test đi thấy cái gì cần thêm css thì thêm
          </p>
        </div>
        <div class="dashboard-grid">
          <!-- Box học từng thì -->
          <div class="dashboard-box">
            <h3 class="dashboard-heading text-indigo-700">Chế độ học theo từng thì</h3>
            <p class="dashboard-desc">Chọn một trong 12 thì dưới đây để bắt đầu học lý thuyết chuyên sâu và làm bài tập củng cố.</p>
            <select v-model="selectedTense" class="dashboard-select">
              <option v-for="tense in tenses" :key="tense.id" :value="tense.id">{{ tense.name }}</option>
            </select>
            <button @click="startLearning" class="dashboard-btn dashboard-btn-primary">Bắt đầu học</button>
          </div>
          <!-- Box luyện tập nâng cao -->
          <div class="dashboard-box">
            <h3 class="dashboard-heading text-teal-700">Chế độ luyện tập nâng cao</h3>
            <p class="dashboard-desc">Thử thách bản thân với các bài tập ngẫu nhiên, tổng hợp từ tất cả 12 thì để kiểm tra toàn diện kiến thức của bạn.</p>
            <button @click="startAdvanced" class="dashboard-btn dashboard-btn-secondary">Bắt đầu luyện tập tổng hợp</button>
          </div>
        </div>
      </div>

      <!-- Learning/Practice View -->
      <div v-else>
        <button @click="resetToDashboard" class="mb-6 main-btn">Quay lại trang chính</button>
        <div class="flex-row grammar-content">
          <!-- Bài tập bên phải (đưa lên trên) -->
          <div
            class="exercise-panel grammar-box"
            :class="{ 'advanced-mode': mode === 'advanced' }"
          >
            <div class="exercise-header">
              <h3 class="exercise-title">Bài tập thực hành</h3>
              <div class="exercise-progress" v-if="currentQuestion">
                Câu {{ currentQuestionIndex + 1 }}/{{ questionsToPractice.length }}
              </div>
            </div>
            <div v-if="loading" class="flex flex-col items-center justify-center h-full">
              <div class="loader mb-2"></div>
              <p class="loading-text">Đang tải câu hỏi...</p>
            </div>
            <div v-else>
              <div v-if="currentQuestion">
                <div class="practice-box">
                  <div class="practice-question">
                    <!-- Hiển thị câu hỏi, thay [verb] bằng ____ -->
                    {{ currentQuestion.question.replace(/\[[^\]]+\]/g, '____') }}
                  </div>
                  <div class="practice-options">
                    <div
                      v-for="(option, idx) in currentQuestion.options"
                      :key="idx"
                      class="practice-option"
                      :class="{ selected: userAnswers[currentQuestionIndex] === option }"
                      @click="userAnswers[currentQuestionIndex] = option"
                      style="cursor:pointer;"
                    >
                      <label style="width:100%;display:flex;align-items:center;">
                        <input
                          type="radio"
                          :value="option"
                          v-model="userAnswers[currentQuestionIndex]"
                          style="margin-right:8px;pointer-events:none;"
                        />
                        {{ option }}
                      </label>
                    </div>
                  </div>
                  <div class="practice-actions">
                    <button class="practice-btn" @click="prevQuestion" :disabled="currentQuestionIndex === 0">Câu trước</button>
                    <button class="practice-btn main-btn" @click="checkAnswer">Kiểm tra</button>
                    <button class="practice-btn" @click="nextQuestion" :disabled="currentQuestionIndex === questionsToPractice.length - 1">Câu sau</button>
                  </div>
                </div>
                <hr class="practice-divider" />
                <button class="end-btn" @click="resetToDashboard">Kết thúc buổi học</button>
              </div>
              <div v-else>
                <h3 class="exercise-result">Kết quả: {{ score }}/{{ questionsToPractice.length }}</h3>
                <div v-if="wrongAnswers.length > 0" class="review-box">
                  <h4 class="text-red-600 font-bold mt-4">Các lỗi sai cần xem lại:</h4>
                  <ul>
                    <li v-for="(item, idx) in wrongAnswers" :key="idx" style="margin-bottom:12px;">
                      <div><strong>Câu hỏi:</strong> {{ item.question.replace(/\[[^\]]+\]/g, '_____') }}</div>
                      <div>
                        <strong>Bạn chọn:</strong>
                        <span style="color:#ef4444;font-weight:bold;background:#fee2e2;padding:2px 6px;border-radius:4px;">
                          {{ item.userAnswer }}
                        </span>
                        |
                        <strong>Đáp án đúng:</strong>
                        <span style="color:#22c55e;font-weight:bold;background:#dcfce7;padding:2px 6px;border-radius:4px;">
                          {{ item.correctAnswer }}
                        </span>
                      </div>
                    </li>
                  </ul>
                  <div class="text-slate-700 mt-2">Bạn nên xem lại lý thuyết và luyện tập thêm các câu trên!</div>
                </div>
                <div v-else class="text-green-600 font-bold mt-4">🎉 Tuyệt vời! Bạn đã làm đúng tất cả!</div>
                <button @click="resetToDashboard" class="main-btn mt-4">Quay lại</button>
              </div>
            </div>
          </div>
          <!-- Lý thuyết bên trái (đưa xuống dưới) -->
          <div v-if="mode !== 'advanced'" class="theory-panel grammar-box">
            <h2 class="theory-title">{{ currentTenseName }}</h2>
            <div class="prose theory-content" v-html="currentTheoryHtml"></div>
            <hr class="my-6">
          </div>
        </div>
      </div>
    </main>
    <!-- Modal, loader, báo cáo... có thể thêm sau -->
  </div>
</template>

<script>
import theoryData from "@/assets/data/theoryData.js";
import { marked } from "marked";
import data from "@/assets/data/questions.js"; // File dữ liệu mẫu

export default {
  name: "Grammar",
  data() {
    return {
      mode: "dashboard", // 'learning', 'advanced'
      tenses: [
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
      ],
      selectedTense: "present_simple",
      currentTenseName: "",
      currentTheory: "",
      exampleTopic: "",
      exampleOutput: "",
      questions: data,
      questionsToPractice: [],
      currentQuestionIndex: 0,
      currentQuestion: data[0],
      userAnswers: [],
      score: 0,
      wrongAnswers: [], // Thêm dòng này
      loading: false,
    };
  },
  computed: {
    currentTheoryHtml() {
      return marked.parse(this.currentTheory || "");
    }
  },
  methods: {
    goHome() {
      this.$router.push("/home");
    },
    startLearning() {
      this.mode = "learning";
      this.currentTenseName = this.tenses.find(t => t.id === this.selectedTense)?.name || "";
      this.currentTheory = theoryData[this.selectedTense] || "Lý thuyết đang cập nhật...";
      // Lọc 5 câu random theo thì
      const filtered = this.questions.filter(q => q.tenseId === this.selectedTense);
      this.questionsToPractice = this.getRandom(filtered, 5);
      this.currentQuestionIndex = 0;
      this.currentQuestion = this.questionsToPractice[0];
      this.userAnswers = [];
      this.score = 0;
    },
    startAdvanced() {
      this.mode = "advanced";
      this.currentTenseName = "Tổng hợp";
      this.currentTheory = "";
      // Lấy 5 câu random từ toàn bộ bộ câu hỏi
      this.questionsToPractice = this.getRandom(this.questions, 5);
      this.currentQuestionIndex = 0;
      this.currentQuestion = this.questionsToPractice[0];
      this.userAnswers = [];
      this.score = 0;
    },
    getRandom(arr, n) {
      // Trả về mảng n phần tử random từ arr, đồng thời shuffle options
      const shuffled = arr.slice().sort(() => 0.5 - Math.random()).slice(0, n);
      // Shuffle options cho từng câu hỏi
      shuffled.forEach(q => {
        q.options = q.options.slice().sort(() => 0.5 - Math.random());
      });
      return shuffled;
    },
    checkAnswer() {
      const q = this.currentQuestion;
      const userAnswer = this.userAnswers[this.currentQuestionIndex];
      if (!userAnswer) return;

      let isCorrect = false;
      let type = q.type || "mcq";
      if (type === "mcq" || type === "fill") {
        isCorrect = userAnswer.trim().toLowerCase() === q.answer.trim().toLowerCase();
      } else if (q.type === "find_error") {
        isCorrect = userAnswer.replace(/\s+/g, ' ').trim().toLowerCase() === q.answer.replace(/\s+/g, ' ').trim().toLowerCase();
      }

      if (isCorrect) {
        this.score++;
      } else {
        // Lưu lại câu sai
        this.wrongAnswers.push({
          question: q.question,
          userAnswer,
          correctAnswer: q.answer
        });
      }
      this.currentQuestionIndex++;
      if (this.currentQuestionIndex < this.questionsToPractice.length) {
        this.currentQuestion = this.questionsToPractice[this.currentQuestionIndex];
      } else {
        this.currentQuestion = null;
      }
    },
    resetToDashboard() {
      this.mode = "dashboard";
      this.currentQuestionIndex = 0;
      this.currentQuestion = null;
      this.userAnswers = [];
      this.score = 0;
      this.exampleTopic = "";
      this.exampleOutput = "";
      this.wrongAnswers = []; // Thêm dòng này để reset lỗi
      this.questionsToPractice = [];
    },
    async generateExample() {
      if (!this.exampleTopic) return;
      this.exampleOutput = `<ul><li><strong>Câu 1:</strong> He goes to work every day.<br><em>Dịch:</em> Anh ấy đi làm mỗi ngày.</li></ul>`;
    },
    refreshQuestions() {
      // Nếu muốn random lại bộ câu hỏi từ data
      this.currentQuestionIndex = 0;
      this.currentQuestion = null;
      this.userAnswers = [];
      this.score = 0;
      this.wrongAnswers = []; // Thêm dòng này để reset lỗi
      this.questionsToPractice = [];
    },
    nextQuestion() {
      if (this.currentQuestionIndex < this.questionsToPractice.length - 1) {
        this.currentQuestionIndex++;
        this.currentQuestion = this.questionsToPractice[this.currentQuestionIndex];
      } else {
        this.currentQuestion = null;
      }
    },
    prevQuestion() {
      if (this.currentQuestionIndex > 0) {
        this.currentQuestionIndex--;
        this.currentQuestion = this.questionsToPractice[this.currentQuestionIndex];
      }
    },
    reset() {
      this.currentQuestionIndex = 0;
      this.currentQuestion = this.questions[0];
      this.userAnswers = [];
      this.score = 0;
    }
  },
  mounted() {
    this.currentTenseName = this.tenses.find(t => t.id === this.selectedTense)?.name || "";
    this.currentTheory = theoryData[this.selectedTense] || "Lý thuyết đang cập nhật...";
  }
};
</script>

<style scoped>
.grammar-app {
  font-family: 'Inter', sans-serif;
  background-color: #f9fafb;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}
.bg-white {
  background-color: #fff !important;
}
.shadow-md {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1) !important;
}
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
  width: 100%;
}
.main-center {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 2rem 0;
}
.dashboard-title {
  margin-bottom: 32px;
}
.dashboard-grid {
  display: flex;
  flex-direction: row;
  gap: 40px;
  justify-content: center;
  align-items: stretch;
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
}
.dashboard-box {
  background: #fff;
  border-radius: 18px;
  box-shadow: 0 4px 24px rgba(76,195,247,0.12);
  border: 1.5px solid #e0e7ef;
  padding: 38px 32px 32px 32px;
  min-width: 340px;
  max-width: 480px;
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}
.dashboard-heading {
  font-size: 2rem;
  font-weight: bold;
  margin-bottom: 12px;
}
.dashboard-desc {
  font-size: 1.08rem;
  color: #607d8b;
  margin-bottom: 22px;
}
.dashboard-select {
  width: 100%;
  padding: 12px;
  border-radius: 8px;
  border: 1.5px solid #b2bec3;
  margin-bottom: 18px;
  font-size: 1.08rem;
}
.dashboard-btn {
  width: 100%;
  padding: 14px 0;
  border-radius: 8px;
  font-size: 1.15rem;
  font-weight: bold;
  border: none;
  cursor: pointer;
  margin-top: 8px;
  transition: background 0.2s, transform 0.2s;
}
.dashboard-btn-primary {
  background: #4f46e5;
  color: #fff;
}
.dashboard-btn-primary:hover {
  background: #6366f1;
  transform: scale(1.04);
}
.dashboard-btn-secondary {
  background: #06d6a0;
  color: #fff;
}
.dashboard-btn-secondary:hover {
  background: #43e6b5;
  transform: scale(1.04);
}
.grammar-box {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  padding: 24px;
  margin-bottom: 24px;
}
.theory-title {
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 16px;
}
.theory-content {
  font-size: 1rem;
  line-height: 1.6;
  color: #333;
}
.input-ai {
  width: 100%;
  padding: 12px;
  border-radius: 8px;
  border: 1.5px solid #b2bec3;
  margin-bottom: 18px;
  font-size: 1rem;
}
.loader {
  border: 4px solid rgba(76, 195, 247, 0.3);
  border-top: 4px solid #4f46e5;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 0.8s linear infinite;
}
@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
.practice-box {
  background: #f0f4f8;
  border-radius: 12px;
  padding: 16px;
  margin-bottom: 16px;
}
.practice-question {
  font-size: 1.2rem;
  font-weight: 500;
  margin-bottom: 12px;
}
.practice-options {
  margin-bottom: 12px;
}
.practice-option {
  background: #fff;
  border-radius: 8px;
  padding: 10px;
  margin-bottom: 8px;
  border: 1px solid #e0e7ef;
}
.practice-actions {
  display: flex;
  justify-content: space-between;
  margin-top: 12px;
}
.practice-btn {
  flex: 1;
  padding: 12px;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 500;
  border: none;
  cursor: pointer;
  transition: background 0.2s, transform 0.2s;
}
.practice-btn:hover {
  transform: scale(1.02);
}
.practice-divider {
  border: 0;
  height: 1px;
  background: #e0e7ef;
  margin: 16px 0;
}
.end-btn {
  width: 100%;
  padding: 12px;
  border-radius: 8px;
  font-size: 1.15rem;
  font-weight: 600;
  background: #ef4444;
  color: #fff;
  border: none;
  cursor: pointer;
  transition: background 0.2s, transform 0.2s;
}
.end-btn:hover {
  background: #dc2626;
  transform: scale(1.02);
}
.exercise-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}
.exercise-title {
  font-size: 1.5rem;
  font-weight: 600;
}
.exercise-progress {
  font-size: 1rem;
  color: #4f46e5;
}
.exercise-result {
  font-size: 1.5rem;
  font-weight: 500;
  margin-top: 16px;
}
.refresh-btn {
  width: 100%;
  padding: 10px;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 500;
  background: #4fc3f7;
  color: #fff;
  border: none;
  margin-bottom: 12px;
  cursor: pointer;
  transition: background 0.2s, transform 0.2s;
}
.refresh-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
.refresh-btn:hover {
  background: #0288d1;
  transform: scale(1.03);
}
.error-option.selected-error {
  background: #6366f1 !important;
  color: #fff !important;
  box-shadow: 0 0 0 2px #6366f1;
}
.error-option:hover {
  background: #c7d2fe !important;
}
.exercise-panel.grammar-box.advanced-mode {
  width: 800px;      /* Chiều rộng cố định, bạn có thể chỉnh lại số này */
  max-width: 800px;
  min-width: 800px;
  margin: 0 auto;
  flex: none;
}
</style>

