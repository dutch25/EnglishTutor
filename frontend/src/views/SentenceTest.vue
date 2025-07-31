<template>
  <div class="sentence-listening-page">
    <button @click="goHome" class="back-btn">⬅️ Back to Homepage</button>
    <div class="card">
      <h1 class="title">📝 Sentence Listening Test</h1>
      <div class="btn-group">
        <button @click="playSentence" :disabled="!currentSentence" class="main-btn">▶️ Play Again</button>
        <button @click="getNewSentence" class="main-btn">🔄 New Sentence</button>
      </div>
      <div class="volume-row">
        <label for="volumeControl">🔊 Volume:</label>
        <input type="range" id="volumeControl" min="0" max="1" step="0.01" v-model="volume" @input="setVolume" />
      </div>
      <div class="input-row">
        <label for="userInput" class="input-label">What did you hear?</label>
        <input
          type="text"
          id="userInput"
          v-model="userInput"
          placeholder="Type the sentence here..."
          @keydown.enter.prevent="checkAnswer"
          class="input-box"
        />
      </div>
      <div class="btn-group">
        <button @click="checkAnswer" class="main-btn">Check</button>
        <button @click="showAnswer" class="main-btn">Show Answer</button>
      </div>
      <div id="result" class="result" v-html="result"></div>
    </div>
  </div>
</template>

<script>
import sentences from "@/assets/data/sentences.json";

export default {
  data() {
    return {
      sentences,
      currentSentence: "",
      userInput: "",
      result: "",
      volume: 1,
      audio: null
    };
  },
  mounted() {
    this.audio = new Audio();
    this.audio.volume = this.volume;
  },
  methods: {
    goHome() {
      this.$router.push("/home");
    },
    getNewSentence() {
      const randomIndex = Math.floor(Math.random() * this.sentences.length);
      this.currentSentence = this.sentences[randomIndex];
      this.userInput = "";
      this.result = "<span style='color:#ffd166'>Sentence loaded. Click Play to play again.</span>";
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
    setVolume() {
      if (this.audio) {
        this.audio.volume = this.volume;
      }
    },
    checkAnswer() {
      if (!this.currentSentence) {
        this.result = "<span style='color:#ef476f'>Please play a sentence first.</span>";
        return;
      }
      const cleanedInput = this.userInput.trim().toLowerCase().replace(/[.,!?]/g, "");
      const cleanedSentence = this.currentSentence.toLowerCase().replace(/[.,!?]/g, "");
      if (cleanedInput === cleanedSentence) {
        this.result = `<span style='color:#06d6a0'>✅ Correct!</span><br> <span style='color:#ffd166'>The sentence was: <strong>${this.currentSentence}</strong></span>`;
        this.currentSentence = "";
      } else {
        this.result = "<span style='color:#ef476f'>❌ Incorrect. Try again.</span>";
      }
    },
    showAnswer() {
      if (!this.currentSentence) {
        this.result = "<span style='color:#ef476f'>Please play a sentence first.</span>";
        return;
      }
      this.result = `<span style='color:#ffd166'>The correct sentence was:<br><strong>${this.currentSentence}</strong></span>`;
    }
  }
};
</script>

<style scoped>
.sentence-listening-page {
  background-color: #1a1a2e;
  min-height: 100vh;
  padding: 40px 0;
  box-sizing: border-box;
  font-family: "Segoe UI", sans-serif;
  display: flex;
  flex-direction: column;
  align-items: center;
}
.card {
  background: #23234b;
  border-radius: 18px;
  box-shadow: 0 8px 32px rgba(0,0,0,0.18);
  padding: 36px 32px 32px 32px;
  max-width: 480px;
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
}
.title {
  font-size: 32px;
  font-weight: bold;
  color: #ffd166;
  margin-bottom: 24px;
  text-align: center;
}
.back-btn {
  background-color: #ffd166;
  color: #23234b;
  font-size: 14px;
  padding: 8px 16px;
  margin-bottom: 24px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: bold;
  transition: background 0.2s;
}
.back-btn:hover {
  background-color: #ef476f;
  color: #fff;
}
.btn-group {
  display: flex;
  gap: 16px;
  margin: 18px 0;
  justify-content: center;
}
.main-btn {
  padding: 10px 24px;
  border-radius: 10px;
  border: none;
  background: linear-gradient(90deg, #06d6a0 0%, #4fc3f7 100%);
  color: #fff;
  font-size: 17px;
  font-weight: bold;
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(76,195,247,0.08);
  transition: background 0.2s, transform 0.2s;
}
.main-btn:disabled {
  background: #888;
  cursor: not-allowed;
}
.main-btn:hover:not(:disabled) {
  background: linear-gradient(90deg, #4fc3f7 0%, #06d6a0 100%);
  transform: translateY(-2px) scale(1.04);
}
.volume-row {
  width: 100%;
  margin-bottom: 18px;
  display: flex;
  align-items: center;
  gap: 12px;
}
.volume-row label {
  font-size: 16px;
  color: #4fc3f7;
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
  color: #4fc3f7;
  margin-bottom: 8px;
  font-weight: 500;
}
.input-box {
  width: 100%;
  padding: 12px;
  border-radius: 10px;
  border: 1px solid #4fc3f7;
  background: #23234b;
  color: #fff;
  font-size: 17px;
  outline: none;
  margin-bottom: 4px;
  transition: border 0.2s;
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
</style>