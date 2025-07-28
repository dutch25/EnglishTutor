<template>
  <div class="verb-page">
    <h1 class="title">Động từ bất quy tắc</h1>
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
      return this.verbs.filter(
        v =>
          v.base.toLowerCase() === s ||
          v.past.toLowerCase() === s ||
          v.pastParticiple.toLowerCase() === s ||
          v.meaning.toLowerCase() === s
      );
    },
  },
  methods: {
    playAudio(word) {
      const audio = new Audio(`http://localhost:8000/audio/${word}`);
      audio.play();
    },
  },
};
</script>

<style scoped>
.verb-page {
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
.title {
  font-size: 32px;
  font-weight: bold;
  margin-bottom: 32px;
  color: #fff;
}
.search-box {
  margin-bottom: 32px;
  padding: 10px 16px;
  width: 320px;
  border-radius: 8px;
  border: none;
  font-size: 16px;
  background: #23234b;
  color: #fff;
  outline: none;
}
.verb-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 24px;
  width: 100%;
  max-width: 1100px;
}
.verb-card {
  background-color: #2a2a3d;
  border-radius: 16px;
  padding: 24px;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(255, 255, 255, 0.05);
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.verb-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 8px 20px rgba(255, 255, 255, 0.1);
}
.verb-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
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
  transition: color 0.2s;
}
.verb-word:hover {
  color: #1976d2;
}
.verb-meaning {
  color: #ffd166;
  font-style: italic;
}
</style>