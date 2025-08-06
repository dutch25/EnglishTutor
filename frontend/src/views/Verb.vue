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
  background-image: url('../assets/images/background.jpg');
  background-size: cover;
  background-position: center;
  background-attachment: fixed;
  color: #ffffff;
  min-height: 100vh;
  padding: 40px 20px;
  font-family: "Poppins", sans-serif;
  display: flex;
  flex-direction: column;
  align-items: center;
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

.back-button {
  position: absolute;
  left: 0;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(6px);
  background:#97b368;
  font-size: 14px;
  padding: 10px 18px;
  border-radius: 10px;
  cursor: pointer;
  font-weight: bold;
  transition: all 0.3s ease;
}
.back-button:hover {
  background: #9bb56e;
  transform: translateY(-2px) scale(1.05);
  color: #ffffff;
}

.title {
  font-size: 2.5rem;
  font-weight: bold;
  background: linear-gradient(90deg, #373737, #555555, #373737);
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  text-shadow: 0 2px 8px rgba(0,0,0,0.4);
}

.search-box {
  margin-bottom: 2rem;
  padding: 12px 16px;
  width: 320px;
  border-radius: 10px;
  border: 1px solid #4fc3f7;
  background: #23234b;
  color: #fff;
  font-size: 16px;
  outline: none;
  box-shadow: 0 0 0 2px rgba(255, 255, 255, 0.05);
  transition: box-shadow 0.3s, border 0.3s;
}
.search-box:focus {
  border: 2px solid #ffd166;
  box-shadow: 0 0 12px rgba(255, 209, 102, 0.5);
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
  width: 100%;
  max-width: 260px;
  background: rgba(0, 0, 0, 0.393);
  border: 1px solid rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(8px);
  border-radius: 16px;
  padding: 20px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.4), 0 0 24px rgba(255, 255, 255, 0.05);
  display: flex;
  flex-direction: column;
  gap: 12px;
  text-align: left;
  transition: all 0.3s ease;
}
.verb-card:hover {
  background: rgba(94, 94, 94, 0.533); /* Sáng lên nhẹ nhàng */
  transform: translateY(-6px) scale(1.03);
  box-shadow: 0 0 20px rgba(79, 195, 247, 0.4), 0 0 32px rgba(255, 209, 102, 0.3);
}

.verb-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.95rem;
}

.verb-label {
  font-weight: 500;
  color: #333232;
}

.verb-word {
  font-weight: bold;
  color: #31b4f6;
  cursor: pointer;
  text-decoration: underline; 
  transition: color 0.2s ease;
  display: flex;
  align-items: center;
  gap: 6px;
}
.verb-word:hover {
  color: #03a9f4;
  filter: drop-shadow(0 0 6px rgba(79, 195, 247, 0.7));
}

.verb-meaning {
  color: #fbc037;
  font-style: italic;
  font-size: 0.9rem;
  text-align: right;
}

.verb-meaning:hover {
  color: #fbc037;
  text-decoration: underline;
  cursor: pointer;
}
</style>