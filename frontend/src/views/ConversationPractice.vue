<template>
  <div class="conversation-page">
    <button @click="goHome" class="back-btn">⬅️ Back to Homepage</button>
    
    <template v-if="!selectedTopic">
      <h1>💬 1000+ Câu Giao Tiếp</h1>
      <div class="topic-grid">
        <div
          v-for="(topic, key) in conversations"
          :key="key"
          class="topic-card"
          @click="selectTopic(key)"
        >
          <div class="topic-icon">{{ topic.icon }}</div>
          <div class="topic-title">{{ topic.title }}</div>
          <div class="topic-count">{{ topic.sentences.length }} câu</div>
        </div>
      </div>
    </template>

    <template v-else>
      <div class="practice-card">
        <h2>{{ conversations[selectedTopic].title }}</h2>
        <div class="sentence-card">
          <div class="english-text">{{ currentSentence.english }}</div>
          <div class="vietnamese-text" v-if="showVietnamese">
            {{ currentSentence.vietnamese }}
          </div>
          <div class="pronunciation" v-if="showPronunciation">
            {{ currentSentence.pronunciation }}
          </div>
        </div>
        
        <div class="controls">
          <button @click="playAudio" class="main-btn">🔊 Nghe</button>
          <button @click="toggleVietnamese" class="main-btn">
            {{ showVietnamese ? 'Ẩn' : 'Hiện' }} Tiếng Việt
          </button>
          <button @click="togglePronunciation" class="main-btn">
            {{ showPronunciation ? 'Ẩn' : 'Hiện' }} Phiên Âm
          </button>
        </div>

        <div class="navigation">
          <button @click="previousSentence" :disabled="currentIndex === 0">⬅️ Trước</button>
          <span>{{ currentIndex + 1 }} / {{ totalSentences }}</span>
          <button @click="nextSentence" :disabled="currentIndex === totalSentences - 1">Sau ➡️</button>
        </div>

        <button @click="resetTopic" class="main-btn">🔄 Chọn chủ đề khác</button>
      </div>
    </template>
  </div>
</template>

<script>
import conversations from "@/assets/data/conversations.json";

export default {
  data() {
    return {
      conversations,
      selectedTopic: "",
      currentIndex: 0,
      showVietnamese: false,
      showPronunciation: false
    };
  },
  computed: {
    currentSentence() {
      if (!this.selectedTopic) return {};
      return this.conversations[this.selectedTopic].sentences[this.currentIndex];
    },
    totalSentences() {
      if (!this.selectedTopic) return 0;
      return this.conversations[this.selectedTopic].sentences.length;
    }
  },
  methods: {
    goHome() {
      this.$router.push("/home");
    },
    selectTopic(topic) {
      this.selectedTopic = topic;
      this.currentIndex = 0;
      this.showVietnamese = false;
      this.showPronunciation = false;
    },
    resetTopic() {
      this.selectedTopic = "";
    },
    nextSentence() {
      if (this.currentIndex < this.totalSentences - 1) {
        this.currentIndex++;
      }
    },
    previousSentence() {
      if (this.currentIndex > 0) {
        this.currentIndex--;
      }
    },
    toggleVietnamese() {
      this.showVietnamese = !this.showVietnamese;
    },
    togglePronunciation() {
      this.showPronunciation = !this.showPronunciation;
    },
    playAudio() {
      const audio = new Audio(`http://127.0.0.1:8000/audio/${encodeURIComponent(this.currentSentence.english)}`);
      audio.play();
    }
  }
};
</script>

<style scoped>
.conversation-page {
  background: linear-gradient(135deg, #393953 0%, #293453 100%);
  color: #fff;
  min-height: 100vh;
  padding: 40px 20px;
  font-family: "Segoe UI", sans-serif;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.topic-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  width: 100%;
  max-width: 1200px;
}

.topic-card {
  background-color: #23234b;
  border-radius: 16px;
  padding: 20px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(255,255,255,0.05);
}

.topic-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 20px rgba(255,255,255,0.12);
}

.topic-icon {
  font-size: 36px;
  margin-bottom: 12px;
}

.topic-title {
  font-size: 18px;
  font-weight: bold;
  color: #4fc3f7;
  margin-bottom: 8px;
}

.topic-count {
  font-size: 14px;
  color: #ffd166;
}

.practice-card {
  background: #23234b;
  border-radius: 20px;
  padding: 32px;
  width: 100%;
  max-width: 600px;
  text-align: center;
  box-shadow: 0 8px 32px rgba(0,0,0,0.18);
}

.practice-card h2 {
  font-size: 24px;
  color: #ffd166;
  margin-bottom: 24px;
}

.sentence-card {
  background: #1a1a2e;
  border-radius: 16px;
  padding: 24px;
  margin: 20px 0;
  text-align: center;
  border: 1px solid #4fc3f7;
}

.english-text {
  font-size: 22px;
  font-weight: bold;
  color: #4fc3f7;
  margin-bottom: 16px;
  line-height: 1.4;
}

.vietnamese-text {
  font-size: 18px;
  color: #ffd166;
  margin-bottom: 12px;
  line-height: 1.3;
}

.pronunciation {
  font-size: 16px;
  color: #06d6a0;
  font-style: italic;
}

.controls {
  display: flex;
  gap: 12px;
  margin: 20px 0;
  justify-content: center;
  flex-wrap: wrap;
}

.navigation {
  display: flex;
  gap: 16px;
  margin: 20px 0;
  justify-content: center;
  align-items: center;
}

.navigation button {
  padding: 8px 16px;
  border-radius: 10px;
  border: none;
  background: linear-gradient(90deg, #06d6a0 0%, #4fc3f7 100%);
  color: #fff;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.2s;
  font-size: 14px;
}

.navigation button:hover:not(:disabled) {
  transform: translateY(-2px);
  background: linear-gradient(90deg, #4fc3f7 0%, #06d6a0 100%);
}

.navigation button:disabled {
  background: #555;
  cursor: not-allowed;
  transform: none;
}

.navigation span {
  font-size: 16px;
  font-weight: bold;
  color: #ffd166;
  padding: 0 12px;
  min-width: 60px;
}

.main-btn {
  padding: 10px 20px;
  border-radius: 10px;
  border: none;
  background: linear-gradient(90deg, #06d6a0 0%, #4fc3f7 100%);
  color: #fff;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.2s;
  font-size: 14px;
}

.main-btn:hover {
  transform: translateY(-2px);
  background: linear-gradient(90deg, #4fc3f7 0%, #06d6a0 100%);
}

.back-btn {
  background-color: #ffd166;
  color: #23234b;
  font-size: 14px;
  padding: 8px 16px;
  margin-bottom: 20px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: bold;
  transition: background 0.2s;
  position: fixed;
  top: 20px;
  left: 20px;
  z-index: 100;
}

.back-btn:hover {
  background-color: #ef476f;
  color: #fff;
}

h1 {
  font-size: 28px;
  margin-bottom: 32px;
  color: #fff;
  text-align: center;
}
</style>