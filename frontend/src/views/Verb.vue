<template>
  <div class="verb-page">
    <div class="header">
      <button class="back-button" @click="goHome">
        ← Quay về trang chủ
      </button>
      <h1 class="title">Động từ bất quy tắc</h1>
    </div>
    <input v-model="search" placeholder="Tìm động từ..." class="search-box" />
    <div class="verb-grid">
      <div v-for="verb in filteredVerbs" :key="verb.base" class="verb-card">
        <div class="verb-row">
          <span class="verb-label">Nguyên mẫu:</span>
          <span class="verb-word clickable" @click="playAudio(verb.base)"
            >{{ verb.base }}</span
          >
        </div>
        <div class="verb-row">
          <span class="verb-label">Quá khứ đơn:</span>
          <span class="verb-word clickable" @click="playAudio(verb.past)"
            >{{ verb.past }}</span
          >
        </div>
        <div class="verb-row">
          <span class="verb-label">Quá khứ phân từ:</span>
          <span class="verb-word clickable" @click="playAudio(verb.pastParticiple)"
            >{{ verb.pastParticiple }}</span
          >
        </div>
        <div class="verb-row">
          <span class="verb-label">Nghĩa:</span>
          <span class="verb-meaning">{{ verb.meaning }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import verbs from "@/assets/data/irregular-verbs.json";
export default {
  data() {
    return {
      search: "",
      verbs,
    };
  },
  computed: {
    filteredVerbs() {
      const s = this.search.trim().toLowerCase();
      if (!s) return this.verbs;
      const filtered = this.verbs.filter(v => {
        // Tìm chính xác từng từ trong nghĩa
        const meaningWords = v.meaning.toLowerCase().split(/[\s,.;/]+/);
        return (
          v.base.toLowerCase() === s ||
          v.past.toLowerCase() === s ||
          v.pastParticiple.toLowerCase() === s ||
          meaningWords.includes(s)
        );
      });
      // Loại bỏ trùng lặp theo base
      const unique = [];
      const seen = new Set();
      for (const verb of filtered) {
        if (!seen.has(verb.base)) {
          unique.push(verb);
          seen.add(verb.base);
        }
      }
      return unique;
    },
  },
  methods: {
    playAudio(word) {
      const audio = new Audio(`http://localhost:8000/audio/${word}`);
      audio.play();
    },
    goHome() {
      this.$router.push("/home");
    },
  },
};
</script>

<style scoped>
.verb-page {
  background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
  color: #ffffff;
  min-height: 100vh;
  padding: 40px 20px;
  font-family: "Segoe UI", sans-serif;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.title {
  font-size: 2.5rem;
  font-weight: bold;
  margin-bottom: 2rem;
  background-clip: text;
  background: linear-gradient(to right, #a7e8fa, #ffffff, #a7e8fa);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  text-shadow: 1px 1px 6px rgba(0, 0, 0, 0.4);
}

.search-box {
  margin-bottom: 2rem;
  padding: 12px 16px;
  width: 320px;
  border-radius: 10px;
  border: none;
  font-size: 16px;
  background: rgba(30, 30, 45, 0.95);
  color: #fff;
  outline: none;
  box-shadow: 0 0 0 2px #3a3a4d inset;
  transition: box-shadow 0.3s;
}
.search-box:focus {
  box-shadow: 0 0 0 2px #00c6ff inset;
}

.verb-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 24px;
  width: 100%;
  max-width: 1100px;
  justify-items: center;
}

.verb-card {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(6px);
  border-radius: 16px;
  padding: 20px;
  width: 100%;
  max-width: 260px;
  box-shadow: 0 6px 18px rgba(0, 0, 0, 0.4);
  display: flex;
  flex-direction: column;
  gap: 10px;
  text-align: left;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.verb-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 0 20px rgba(0, 198, 255, 0.5);
}

.verb-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.95rem;
}

.verb-label {
  font-weight: 500;
  color: #b0b0c3;
}

.verb-word {
  font-weight: bold;
  color: #4fc3f7;
  cursor: pointer;
  text-decoration: underline;
  transition: color 0.2s ease;
  display: flex;
  align-items: center;
  gap: 6px;
}
.verb-word:hover {
  color: #03a9f4;
}

.verb-meaning {
  color: #ffd166;
  font-style: italic;
  font-size: 0.9rem;
  text-align: right;
}

.back-button {
  align-self: flex-start;
  background-color: #ffd166;
  color: #23234b;
  font-size: 14px;
  padding: 8px 16px;
  margin-bottom: 24px;
  position: absolute;
  left: 0;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: bold;
  transition: background 0.2s;
}
.back-button:hover {
  background-color: #ef476f;
  color: #fff;
}

.header {
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  width: 100%;
  max-width: 1100px;
  margin-bottom: 32px;
}

</style>