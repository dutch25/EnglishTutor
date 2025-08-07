<template>
  <div class="sentence-listening-page">
    <div class="content-wrapper">
      <!-- Modal luôn nằm trên card -->
      <div v-if="showReadyBox" class="ready-modal">
        <div class="ready-modal-content">
          <button class="close-btn" @click="closeAndgoHome" title="Đóng">
            &times;
          </button>
          <p>Bạn đã sẵn sàng luyện nghe câu chưa?</p>
          <button class="main-btn" @click="startTest">Bắt đầu</button>
        </div>
      </div>
      <!-- Card luôn hiển thị phía dưới -->
      <div>
        <div class="back-btn-row">
          <button @click="goHome" class="back-btn">
            ⬅ Về trang chủ
          </button>
        </div>
        <div class="card">
          <div class="card-header new-btn-row">
            <button @click="getNewSentence" class="main-btn new-btn">
              ↪ Câu mới
            </button>
          </div>
          <h1 class="title">📝 Học theo câu tiếng Anh</h1>
          <div class="volume-row">
            <label for="volumeControl">🔊 Âm lượng:</label>
            <input
              type="range"
              id="volumeControl"
              min="0"
              max="1"
              step="0.01"
              v-model="volume"
              @input="setVolume"
              @mousedown="dragging = true"
              @mouseup="dragging = false"
            />
          </div>
          <div class="input-row">
            <label for="userInput" class="input-label">Bạn nghe được gì?</label>
            <div class="input-with-icon">
              <input
                type="text"
                id="userInput"
                v-model="userInput"
                placeholder="Nhập câu bạn nghe được..."
                @keydown.enter.prevent="checkAnswer"
                class="input-box"
              />
              <button
                class="icon-btn"
                @click="playSentence"
                :disabled="!currentSentence"
                title="Nghe lại"
                type="button"
              >
                <svg width="32" height="32" viewBox="0 0 24 24" fill="none">
                  <circle cx="12" cy="12" r="12" fill="#4fc3f7" />
                  <path
                    d="M16.5 12a4.5 4.5 0 1 1-2.7-4.09"
                    stroke="#fff"
                    stroke-width="2"
                    fill="none"
                  />
                  <polygon points="15,7 15,11 11,9" fill="#fff" />
                </svg>
              </button>
            </div>
          </div>
          <div class="btn-group bottom-group">
            <button @click="checkAnswer" class="main-btn">Kiểm tra</button>
            <button @click="showAnswer" class="main-btn">Hiện đáp án</button>
          </div>
          <div id="result" class="result" v-html="result"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import sentences from "@/assets/data/sentences.json";

// Import âm thanh phản hồi
import correctSound from "@/assets/audios/correct.mp3";
import incorrectSound from "@/assets/audios/incorrect.mp3";

export default {
  data() {
    return {
      sentences,
      currentSentence: "",
      userInput: "",
      result: "",
      volume: 1,
      audio: null,
      showReadyBox: true,
      dragging: false,
      correctAudio: null,
      incorrectAudio: null
    };
  },
  mounted() {
    this.audio = new Audio();
    this.audio.volume = this.volume;

    // Tạo audio phản hồi đúng/sai
    this.correctAudio = new Audio(correctSound);
    this.incorrectAudio = new Audio(incorrectSound);
  },
  methods: {
    setVolume() {
      if (this.audio) {
        this.audio.volume = this.volume;
      }
    },
    goHome() {
      this.$router.push("/home");
    },
    closeAndgoHome() {
      this.showReadyBox = false;
      this.$router.push("/home");
    },
    getNewSentence() {
      const randomIndex = Math.floor(Math.random() * this.sentences.length);
      this.currentSentence = this.sentences[randomIndex];
      this.userInput = "";
      this.result = "<span style='color:#3f3f3f'>Đã tải câu mới, nhấn nút Nghe để phát lại.</span>";
      this.playSentence();
    },
    playSentence() {
      if (!this.currentSentence) {
        this.result = "<span style='color:#ef476f'>Click New Sentence first.</span>";
        return;
      }
      fetch(`http://127.0.0.1:8000/audio/${encodeURIComponent(this.currentSentence)}`)
        .then(response => response.blob())
        .then(blob => {
          this.audio.src = URL.createObjectURL(blob);
          this.audio.volume = this.volume;
          this.audio.play();
        })
        .catch(err => {
          console.error("Error playing sentence:", err);
          this.result = "<span style='color:#ef476f'>Failed to load sentence.</span>";
        });
    },
    checkAnswer() {
      if (!this.currentSentence) {
        this.result = "<span style='color:#ef476f'>Hãy bấm chọn Câu mới trước</span>";
        return;
      }

      const cleanedInput = this.userInput.trim().toLowerCase().replace(/[.,!?]/g, "");
      const cleanedSentence = this.currentSentence.toLowerCase().replace(/[.,!?]/g, "");

      // Reset âm thanh phản hồi
      this.correctAudio.pause();
      this.correctAudio.currentTime = 0;
      this.incorrectAudio.pause();
      this.incorrectAudio.currentTime = 0;

      if (cleanedInput === cleanedSentence) {
        this.result = `<span style='color:#06d6a0'>✅ Correct!</span><br> <span style='color:#ffd166'>Câu chính xác là: <strong>${this.currentSentence}</strong></span>`;
        this.correctAudio.play();
        setTimeout(() => {
          this.getNewSentence();
        }, 3000);
      } else {
        this.result = "<span style='color:#ef476f'>❌ Incorrect. Try again.</span>";
        this.incorrectAudio.play();
      }
    },
    showAnswer() {
      if (!this.currentSentence) {
        this.result = "<span style='color:#ef476f'>Please play a sentence first.</span>";
        return;
      }
      this.result = `<span style='color:#ffd166'>Câu chính xác là:<br><strong>${this.currentSentence}</strong></span>`;
    },
    startTest() {
      this.showReadyBox = false;
      this.getNewSentence();
    }
  },
  watch: {
    dragging(newVal) {
      const slider = this.$el.querySelector('#volumeControl');
      if (newVal) {
        slider.classList.add('active');
      } else {
        slider.classList.remove('active');
      }
    }
  }
};
</script>
<style scoped>
.sentence-listening-page {
  background-image: url("../assets/images/background.jpg");
  background-size: cover;
  background-position: center;
  min-height: 100vh;
  padding: 40px 0;
  font-family: "Poppins", sans-serif;
  display: flex;
  color: #ffffff;
  flex-direction: column;
  align-items: center; /* Đảm bảo căn giữa mọi thứ theo chiều ngang */
}

.content-wrapper {
  width: 100%;
  max-width: 480px;
  margin: 0 auto;
  position: relative; /* Thêm dòng này để modal phủ lên card */
  min-height: 600px; /* Đảm bảo đủ cao cho modal căn giữa */
}

.back-btn-row {
  width: 100%;
  max-width: 480px;
  display: flex;
  justify-content: flex-start;
  margin: 0 auto 32px auto;
}

.back-btn {
  background: rgba(255, 255, 255, 0.1);
  color: #23234b;
  border: none;
  border-radius: 8px;
  padding: 8px 16px;
  font-weight: bold;
  margin-bottom: 24px;
  cursor: pointer;
}

.back-btn:hover {
  background: #97b368;
  color: #fff;
}

.card {
  background: rgba(255, 255, 255, 0.473);
  border-radius: 20px;
  border: 1px solid rgba(255, 255, 255, 0.08);
  backdrop-filter: blur(10px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
  padding: 36px 32px 32px 32px;
  max-width: 480px;
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.card-header {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 12px;
}

.title {
  font-size: 32px;
  font-weight: bold;
  color: #3f3f3f;
  margin: 0 0 32px 0; /* tăng margin-bottom từ 24px lên 32px */
  text-align: center; /* Căn giữa tiêu đề */
}

.new-btn {
  min-width: 120px;
  padding: 8px 18px;
  font-size: 15px;
  border-radius: 10px;
  border: none;
  background: linear-gradient(90deg, #06d6a0 0%, #4fc3f7 100%);
  color: #fff;
  font-weight: bold;
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(76, 195, 247, 0.08);
  transition: background 0.2s, transform 0.2s;
  min-height: 44px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}
.new-btn:hover {
  background: linear-gradient(90deg, #b7a1e8 0%, #c387ee 100%);
  transform: translateY(-2px) scale(1.04);
}

.btn-group {
  display: flex;
  gap: 16px;
  margin: 18px 0 0 0;
  justify-content: center;
  width: 100%;
}
.top-group {
  margin-bottom: 12px;
}
.bottom-group {
  margin-top: 8px;
  display: flex;
  gap: 16px;
  justify-content: space-between;
  width: 100%;
}

.main-btn {
  padding: 10px 24px;
  border-radius: 10px;
  border: none;
  background: linear-gradient(90deg, #97b368 0%, #95b561 100%);
  color: #fff;
  font-size: 17px;
  font-weight: bold;
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(76, 195, 247, 0.08);
  transition: background 0.2s, transform 0.2s;
  min-width: 130px;
  min-height: 44px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}
.main-btn:disabled {
  background: #888;
  cursor: not-allowed;
}
.main-btn:hover:not(:disabled) {
  background: linear-gradient(90deg, #a2b87a 0%, #9bb473 100%);
  transform: translateY(-2px) scale(1.04);
  color: rgb(32, 32, 32);
}

.volume-row {
  width: 100%;
  margin-bottom: 24px; /* Tăng khoảng cách với phần dưới */
  display: flex;
  align-items: center;
  gap: 12px;
}
.volume-row label {
  font-size: 16px;
  color: #2e2e2e;
  font-weight: 500;
  margin-right: 8px;
}

input[type="range"] {
  flex: 1;
  margin-top: 0;
}

.input-row {
  width: 100%;
  margin-bottom: 18px;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}
.input-label {
  font-size: 16px;
  color: #2e2e2e;
  margin-bottom: 8px;
  font-weight: 500;
}
.input-box {
  width: 100%;
  padding: 12px;
  padding-right: 44px; /* chừa chỗ cho icon */
  border-radius: 10px;
  border: 1px solid #4fc3f7;
  background: #23234b;
  color: #fff;
  font-size: 17px;
  outline: none;
  margin-bottom: 4px;
  transition: border 0.2s;
  box-sizing: border-box; /* Thêm dòng này */
}
.input-box:focus {
  border: 2px solid #ffd166;
}
.result {
  margin-top: 18px;
  font-weight: bold;
  font-size: 19px;
  text-align: center;
  min-height: 32px;
}
.input-with-icon {
  width: 100%;
  display: flex;
  align-items: center;
  position: relative;
}

.icon-btn {
  position: absolute;
  right: 9px; /* giảm khoảng cách với viền phải */
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  padding: 0;
  cursor: pointer;
  display: flex;
  align-items: center;
  height: 32px; /* bằng với svg */
  width: 32px;
  transition: transform 0.15s;
  margin-top: -2px; /* Căn giữa với input */
}
.icon-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
.icon-btn:hover:not(:disabled) {
  background: rgba(79, 195, 247, 0.08); /* Thêm hiệu ứng nền nhẹ nếu muốn */
  border-radius: 50%;
}

.new-btn-row {
  width: 100%;
  display: flex;
  justify-content: flex-end;
  margin-bottom: 20px; /* tăng từ 8px lên 20px */
}

.ready-modal {
  position: absolute; /* Đổi từ fixed sang absolute */
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: transparent; /* hoặc bỏ hẳn thuộc tính background */
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 10;
  /* Xoá border-radius ở đây */
  pointer-events: auto;
}

.ready-modal-content {
  position: relative;
  z-index: 2;
  background: rgba(35, 35, 75, 0.55); /* alpha thấp hơn để trong suốt hơn */
  backdrop-filter: blur(8px); /* hiệu ứng mờ nền phía sau */
  padding: 36px 32px 32px 32px;
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.18);
  text-align: center;
  color: rgb(255, 255, 255);
  font-size: 20px;
  min-width: 320px;
  max-width: 90vw;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  align-items: center;
  left: 50%;
  transform: translateX(-50%);
}

.close-btn {
  position: absolute;
  top: 12px;
  right: 16px;
  background: none;
  border: none;
  color: black;
  font-size: 28px;
  font-weight: bold;
  cursor: pointer;
  z-index: 3;
  transition: color 0.2s;
}
.close-btn:hover {
  color: #ef476f;
}

input[type="range"] {
  appearance: none;
  -webkit-appearance: none;
  width: 100%;
  height: 6px;
  border-radius: 3px;
  background: linear-gradient(90deg, #4fc3f7, #06d6a0);
  outline: none;
  transition: background 0.3s;
}

input[type="range"] {
  appearance: none;
  -webkit-appearance: none;
  width: 100%;
  height: 6px;
  border-radius: 3px;
  background: rgb(159, 159, 159); /* Mặc định là màu trắng */
  transition: background 0.3s;
  position: relative;
}

input[type="range"].active {
  background: linear-gradient(90deg, #5b5a5a, #000000);
}

input[type="range"]::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: #ffffff;
  border: 3px solid #4fc3f7;
  cursor: pointer;
  transition: all 0.2s;
  margin-top: -7px; /* Căn tâm */
  box-shadow: 0 0 0 3px #2b2b38; /* Để track đi xuyên qua tâm */
}

input[type="range"]::-webkit-slider-thumb:hover {
  background: #4fc3f7;
  border-color: #06d6a0;
  transform: scale(1.1);
}

/* Firefox Thumb */
input[type="range"]::-moz-range-thumb {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: #ffffff;
  border: 3px solid #4fc3f7;
  cursor: pointer;
  transition: all 0.2s;
  box-shadow: 0 0 0 3px #2b2b38; /* Track đi xuyên tâm */
}

input[type="range"]::-moz-range-thumb:hover {
  background: #4fc3f7;
  border-color: #06d6a0;
  transform: scale(1.1);
}

/* Firefox Track */
input[type="range"]::-moz-range-track {
  height: 6px;
  border-radius: 3px;
  background: white;
}

input[type="range"].active::-moz-range-track {
  background: linear-gradient(90deg, #4fc3f7, #06d6a0);
}
</style>
