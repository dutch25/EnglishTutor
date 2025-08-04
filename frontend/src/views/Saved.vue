<template>
  <div class="saved-page">
    <button @click="$router.push('/')" class="back-btn">⬅️ Trang chủ</button>
    <h1>📚 Từ đã lưu</h1>
    <div v-if="loading" class="loading">Đang tải...</div>
    <div v-if="error" class="error">{{ error }}</div>
    <div v-if="!loading && savedWords.length === 0" class="empty">Chưa có từ nào được lưu.</div>
    <div v-for="item in savedWords" :key="item.id" class="saved-card">
      <div class="saved-row">
        <div class="cell word">
          <b>{{ item.word }}</b>
          <button class="speak-btn" @click="speak(item.word)" title="Nghe phát âm">
            🔊
          </button>
        </div>
        <div class="cell phonetic" v-if="item.phonetic">/ {{ item.phonetic }} /</div>
        <div class="cell meaning">{{ item.meaning }}</div>
        <div class="cell date">{{ item.created_at }}</div>
        <div class="cell action">
          <button class="delete-btn" @click="deleteWord(item.id)">Xoá</button>
        </div>
      </div>
      <div v-if="item.note" class="note">Ghi chú: {{ item.note }}</div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      savedWords: [],
      loading: false,
      error: "",
    };
  },
  mounted() {
    this.fetchSaved();
  },
  methods: {
    async fetchSaved() {
      this.loading = true;
      this.error = "";
      try {
        const userId = localStorage.getItem("user_id");
        if (!userId) {
          alert("Bạn cần đăng nhập lại!");
          return;
        }
        const res = await fetch(`http://localhost:8000/api/saved_words?user_id=${userId}`);
        if (!res.ok) throw new Error("Không tải được danh sách.");
        this.savedWords = await res.json();
      } catch (e) {
        this.error = e.message;
      } finally {
        this.loading = false;
      }
    },
    async deleteWord(id) {
      if (!confirm("Bạn chắc chắn muốn xoá?")) return;
      try {
        const res = await fetch(`http://localhost:8000/api/saved_word/${id}`, { method: "DELETE" });
        if (!res.ok) throw new Error("Xoá thất bại.");
        this.fetchSaved();
      } catch (e) {
        this.error = e.message;
      }
    },
    speak(text) {
      if (!text) return;
      const utter = new window.SpeechSynthesisUtterance(text);
      utter.lang = "en-US";
      window.speechSynthesis.speak(utter);
    },
  }
};
</script>

<style scoped>
.saved-page {
  background: linear-gradient(135deg, #393953 0%, #293453 100%);
  min-height: 100vh;
  color: #fff;
  padding: 40px 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
}
.back-btn {
  background: #ffd166;
  color: #23234b;
  border: none;
  border-radius: 8px;
  padding: 8px 16px;
  font-weight: bold;
  margin-bottom: 24px;
  cursor: pointer;
}
h1 {
  color: #ffd166;
  margin-bottom: 24px;
}
.saved-card {
  background: #23234b;
  border-radius: 16px;
  padding: 18px 24px;
  margin-bottom: 18px;
  width: 100%;
  max-width: 700px;
  box-shadow: 0 4px 16px rgba(0,0,0,0.12);
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}
.saved-row {
  display: flex;
  width: 100%;
  align-items: center;
  margin-bottom: 6px;
}
.cell {
  padding: 0 8px;
  font-size: 16px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.word { flex: 1.2; color: #4fc3f7; font-weight: bold; font-size: 20px; }
.phonetic { flex: 1; color: #ffd166; font-size: 16px; }
.meaning { flex: 2; color: #fff; }
.date { flex: 1.2; color: #aaa; font-size: 13px; }
.action { flex: 0.7; }
.note {
  color: #ffd166;
  margin: 8px 0 0 0;
  font-size: 15px;
}
.delete-btn {
  background: #ef476f;
  color: #fff;
  border: none;
  border-radius: 8px;
  padding: 6px 14px;
  font-weight: bold;
  cursor: pointer;
  margin-top: 8px;
}
.loading, .error, .empty {
  margin: 18px 0;
  font-size: 17px;
}
.error { color: #ef476f; }
.empty { color: #ffd166; }
.speak-btn {
  background: none;
  border: none;
  color: #ffd166;
  font-size: 20px;
  margin-left: 8px;
  cursor: pointer;
  vertical-align: middle;
  transition: color 0.2s;
}
.speak-btn:hover {
  color: #4fc3f7;
}
</style>