<template>
  <div class="listening-page">
    <button v-if="selectedTheme" @click="goHome" class="back-btn">⬅️ Back to Homepage</button>
    <h1>🎧 Listening Practice</h1>
    <template v-if="!selectedTheme">
      <p class="theme-title">Select a theme to begin the Word Listening Test:</p>
      <div class="theme-grid">
        <div
          v-for="(words, theme) in themes"
          :key="theme"
          class="theme-card"
          @click="chooseTheme(theme)"
        >
          <div class="theme-icon">{{ themeIcon(theme) }}</div>
          <div class="theme-name">{{ themeTitle(theme) }}</div>
        </div>
      </div>
    </template>
    <template v-else>
      <div class="test-card">
        <p class="theme-title">Theme: {{ themeTitle(selectedTheme) }}</p>
        <button @click="playAudio" class="main-btn">▶️ Play Word</button>
        <input v-model="userInput" placeholder="Type what you hear" class="input-box" />
        <div class="btn-group">
          <button @click="checkAnswer" class="main-btn">Check</button>
          <button @click="resetTheme" class="main-btn">🔄 Choose another theme</button>
        </div>
        <p class="result" v-html="result"></p>
      </div>
    </template>
  </div>
</template>

<script>
import themes from "@/assets/data/themes.json";

export default {
  data() {
    return {
      themes,
      selectedTheme: "",
      currentWord: "",
      currentAudioUrl: "",
      userInput: "",
      result: ""
    };
  },
  methods: {
    themeTitle(theme) {
      const titles = {
        animals: "Animals",
        fruits: "Fruits",
        colors: "Colors",
        numbers: "Numbers",
        vehicles: "Vehicles",
        weather: "Weather",
        professions: "Professions",
        sports: "Sports",
        body: "Body Parts",
        clothing: "Clothing",
        food: "Food",
        drinks: "Drinks",
        emotions: "Emotions",
        school: "School",
        nature: "Nature",
        family: "Family",
        jobs: "Jobs",
        tools: "Tools",
        countries: "Countries",
        cities: "Cities",
        technology: "Technology",
        space: "Space",
        holidays: "Holidays",
        furniture: "Furniture"
      };
      return titles[theme] || theme;
    },
    themeIcon(theme) {
      const icons = {
        animals: "🦁",
        fruits: "🍎",
        colors: "🎨",
        numbers: "🔢",
        vehicles: "🚗",
        weather: "⛅",
        professions: "👨‍🏫",
        sports: "⚽",
        body: "💪",
        clothing: "👕",
        food: "🍔",
        drinks: "🥤",
        emotions: "😊",
        school: "🏫",
        nature: "🌲",
        family: "👨‍👩‍👧",
        jobs: "💼",
        tools: "🔧",
        countries: "🌍",
        cities: "🏙️",
        technology: "💻",
        space: "🚀",
        holidays: "🎉",
        furniture: "🛋️"
      };
      return icons[theme] || "";
    },
    chooseTheme(theme) {
      this.selectedTheme = theme;
      this.setWord();
      this.result = "";
      this.userInput = "";
    },
    setWord() {
      const words = this.themes[this.selectedTheme];
      const randomIndex = Math.floor(Math.random() * words.length);
      this.currentWord = words[randomIndex];
      this.currentAudioUrl = `http://127.0.0.1:8000/audio/${this.currentWord}?speed=0.7`;
      this.userInput = "";
    },
    playAudio() {
      if (!this.currentAudioUrl) {
        alert("No word selected.");
        return;
      }
      const audio = new Audio(this.currentAudioUrl);
      audio.play().catch(err => {
        console.error("Audio Error:", err);
      });
    },
    checkAnswer() {
      if (this.userInput.trim().toLowerCase() === this.currentWord) {
        this.result = `<span style='color:#06d6a0'>✅ Correct!</span>`;
      } else {
        this.result = `<span style='color:#ef476f'>❌ Incorrect. The correct word was "<strong>${this.currentWord}</strong>".</span>`;
      }
      this.userInput = "";
      setTimeout(() => {
        this.setWord();
        this.result += "<br><span style='color:#ffd166'>🔁 New word loaded. Click Play again.</span>";
      }, 1000);
    },
    resetTheme() {
      this.selectedTheme = "";
      this.result = "";
      this.userInput = "";
    },
    goHome() {
      this.$router.push("/home");
    }
  }
};
</script>

<style scoped>
.listening-page {
  background-color: #1a1a2e;
  color: #fff;
  min-height: 100vh;
  padding: 40px 20px;
  box-sizing: border-box;
  font-family: "Segoe UI", sans-serif;
  display: flex;
  flex-direction: column;
  align-items: center;
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
}
.back-btn:hover {
  background-color: #ef476f;
  color: #fff;
}
.theme-title {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 32px;
  color: #fff;
}
.theme-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 24px;
  width: 100%;
  max-width: 900px;
  margin-bottom: 40px;
}
.theme-card {
  background-color: #23234b;
  border-radius: 16px;
  padding: 32px 0 24px 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  cursor: pointer;
  transition: box-shadow 0.2s, transform 0.2s;
  box-shadow: 0 4px 12px rgba(255,255,255,0.05);
}
.theme-card:hover {
  box-shadow: 0 8px 24px rgba(255,255,255,0.12);
  transform: translateY(-6px) scale(1.03);
  background-color: #2a2a3d;
}
.theme-icon {
  font-size: 48px;
  margin-bottom: 16px;
}
.theme-name {
  font-size: 22px;
  font-weight: bold;
  color: #4fc3f7;
}
.test-card {
  background: #23234b;
  border-radius: 18px;
  box-shadow: 0 8px 32px rgba(0,0,0,0.18);
  padding: 36px 32px 32px 32px;
  max-width: 420px;
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
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
  margin: 10px 8px;
}
.main-btn:hover {
  background: linear-gradient(90deg, #4fc3f7 0%, #06d6a0 100%);
  transform: translateY(-2px) scale(1.04);
}
.btn-group {
  display: flex;
  gap: 12px;
  margin: 10px 0 0 0;
  justify-content: center;
}
.input-box {
  padding: 12px;
  font-size: 17px;
  margin: 18px 0 0 0;
  width: 100%;
  border-radius: 10px;
  border: 1.5px solid #4fc3f7;
  background: #23234b;
  color: #fff;
  outline: none;
  transition: border 0.2s;
}
.input-box:focus {
  border: 2px solid #ffd166;
}
.result {
  font-weight: bold;
  font-size: 18px;
  margin-top: 18px;
  min-height: 32px;
  text-align: center;
}
</style>